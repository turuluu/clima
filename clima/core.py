from collections import ChainMap
import inspect
import sys
import os
from functools import partial

from clima.fire import Fire

from clima import schema, utils, password_store
from clima import docstring, configfile

from typing import Dict


class RequiredParameterException(Exception):
    pass


DECORATORS_STATE = {
    'schema': None,
    'generated': None,
}

schema_decorator = partial(schema.schema_decorator, DECORATORS_STATE)


class Configurable:
    """Configuration management"""
    # TODO: idiomatic handling for use cases that apply to NamedTuple
    __configured = None

    def _setup(self, params: dict, configuration_tuple):
        """Chains all configuration options together"""
        self.__configured = dict(
            ChainMap(
                params,
                config_dict(configuration_tuple),
                utils.filter_fields(os.environ, configuration_tuple),
                get_secrets(configuration_tuple),
                configuration_tuple._asdict()
            )
        )

        return self.__configured

    def _init(self, cls: schema.MetaSchema):
        is_schema = isinstance(cls, schema.MetaSchema)
        if not is_schema:
            raise TypeError('The configuration should inherit Schema')

        # Allows using Schema as a subclass only
        c.__configured = cls
        # Allows deoorator usage with @c.init
        return schema_decorator(cls)

    def __call__(self, cls, *, noprepare=False):
        """
        Decorator to define the Cli object
        """
        _cli = cli(cls)
        if not noprepare:
            global DECORATORS_STATE
            prepare(DECORATORS_STATE['generated'], DECORATORS_STATE['schema'])

        return _cli

    def __repr__(self):
        return repr(self.__configured)

    def __getattr__(self, item):
        res = None
        if self.__configured is not None:
            try:
                res = self.__configured[item]
            except Exception:
                res = getattr(self.__configured, item)

        if res is None:
            raise RequiredParameterException(f'Missing argument for "{item}"')
        return res

    def __getitem__(self, item):
        c_item = self.__configured[item]
        if c_item is None:
            print('none')
        return c_item


c = Configurable()


def get_secrets(configuration_tuple):
    params = [t for t in configuration_tuple._asdict()]
    secrets = {}
    try:
        for p in params:
            secret = password_store.decrypt(p)
            if len(secret) > 0:
                secrets.update({p: secret})
    except:
        # TODO: Wanted to keep this lean, as one might not have gpg installed and what not..
        # Need to provide for example a configuration key 'use gpg' that the user can use to
        # enable this feature. This way it won't get in the way of other use cases.
        pass

    return secrets


def add_to_decorators(key, value):
    DECORATORS_STATE[key] = value


def cli(cls):
    """Decorator that wraps the command line interface
     specific class with fire
    """
    state = DECORATORS_STATE

    def init(self, **cli_args):
        """Generated init"""
        initialize_cli(cli_args, state['schema'])

    cls_attrs = dict(
        __init__=init,
        __repr__=cls.__repr__,
        **{k: v for k, v in cls.__dict__.items() if not k.startswith('_')}
    )

    _Cli = type('Cli', (cls,), cls_attrs)
    state['generated'] = _Cli

    return _Cli


# TODO: config dict and parameter parsing have diverged type casting processes
def config_dict(configuration_tuple):
    result: Dict = {}

    _config_file = configuration_tuple._asdict().get('CFG')
    if _config_file is None:
        _config_file = configfile.get_config_path(configuration_tuple)

    if _config_file is not None:
        result = utils.filter_fields(configfile.read_config(_config_file), configuration_tuple)
        result = utils.type_correct_with(result, configuration_tuple)

    return result


def initialize_cli(a, b):
    global c
    c._setup(a, b)


class Schema(object, metaclass=schema.MetaSchema):
    """Base class for the user's configuration class"""

    def _asdict(self):
        return schema.asdict(self)

    def _wrap(self):
        # TODO: Figure this out so Schema could live inside schema.py file
        c._init(self)

    @staticmethod
    def post_init(self, *args):
        pass

    @property
    def _fields(self):
        fields = [
            k for k in self.__dir__()
            if not k.startswith('_') and not inspect.ismethod(getattr(self, k))
        ]
        return fields

    def __call__(self, *args, **kwargs):
        pass


def prepare_signatures(cls, schema):
    """Adds possible parameters gathered from Schema to all methods
    defined in the 'Cli' class (decorated with @c). This way the parameters
    are the same for all methods, but at the same time they don't need to
    be duplicated in every method signature.
    """

    methods = {
        k: v for k, v in cls.__dict__.items()
        if not k.startswith('_') and inspect.isfunction(v)
    }

    params_with_post_init = [
        inspect.Parameter(name=field, kind=inspect._VAR_KEYWORD)
        for field in schema._fields
    ]

    # pop the post_init from the end of parameters
    params = [prm for prm in params_with_post_init if prm.name != 'post_init']

    # Hacking sys.argv to include positional keywords with assumed keyword names
    # as I couldn't find another workaround to tell python-fire how to parse these
    # The alternative had been to integrate python-fire with tighter coupling into this
    if len(sys.argv) > 2 and not any(['-h' in sys.argv, '--help' in sys.argv]):
        new_args = sys.argv[0:2]
        i = 2
        while i < len(sys.argv):
            arg = sys.argv[i]
            prm = params[i - 2]

            if isinstance(arg, str) and arg.startswith('--') and not arg.endswith('--'):
                new_args += sys.argv[i:i + 2]
                i += 2
            else:
                new_args.append(f'--{prm.name}')
                new_args.append(f'{arg}')
                i += 1
        sys.argv = new_args

    for m_name, method in methods.items():
        sig = inspect.signature(method)
        new_parameters = [v for v in sig.parameters.values()]
        new_parameters += params

        method.__signature__ = sig.replace(parameters=new_parameters)


def prepare(cls, schema: Schema):
    """Beef: prepares signatures, docstrings and initiates fire for the cli-magic"""
    prepare_signatures(cls, schema)
    docstring.wrap_method_docstring(cls, schema)
    with utils.suppress_traceback():
        if len(sys.argv) > 1 and sys.argv[-1] == 'version':
            # Version printing part 2
            print(schema.version)
        else:
            Fire(cls)
