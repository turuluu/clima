from collections import ChainMap
import inspect
import os
from functools import partial

from fire import Fire

from clima import schema, utils
from clima import docstring, configfile

DECORATORS_STATE = {
        'schema': None,
        'generated': None,
        }

schema_decorator = partial(schema.schema_decorator, DECORATORS_STATE)


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
        # c(cli_args, state['schema'])

    cls_attrs = dict(
            __init__=init,
            __repr__=cls.__repr__,
            **{k: v for k, v in cls.__dict__.items() if not k.startswith('_')}
            )

    _Cli = type('Cli', (cls,), cls_attrs)
    state['generated'] = _Cli

    return _Cli

def config_dict(configuration_tuple):
    config_dict = {}

    config_file = configfile.get_config_path(configuration_tuple)
    if config_file is not None:
        config_dict = utils.filter_fields(configfile.read_config(config_file), configuration_tuple)
        config_dict = utils.type_correct_with(config_dict, configuration_tuple)

    return config_dict



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

        return res

    def __getitem__(self, item):
        return self.__configured[item]


c = Configurable()


def initialize_cli(a, b):
    global c
    c._setup(a, b)


class Schema(metaclass=schema.MetaSchema):
    """Base class for the user's configuration class"""

    def _asdict(self):
        return schema.asdict(self)

    def _wrap(self):
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


def prepare_signatures(cls, nt):
    """Adds possible parameters gathered from Schema to all methods
    defined in the 'Cli' class (decorated with @c). This way the parameters
    are the same for all methods, but at the same time they don't need to
    be duplicated in every method signature.
    """

    methods = {
            k: v for k, v in cls.__dict__.items()
            if not k.startswith('_') and inspect.isfunction(v)
            }
    for m_name, method in methods.items():
        params = [
                inspect.Parameter(name=field, kind=inspect._VAR_KEYWORD)
                for field in nt._fields
                ]
        sig = inspect.signature(method)
        method.__signature__ = sig.replace(parameters=[
            inspect.Parameter(name='self', kind=inspect._VAR_KEYWORD),
            *params
            ])


def prepare(cls, nt):
    """Beef: prepares signatures, docstrings and initiates fire for the cli-magic"""
    prepare_signatures(cls, nt)
    docstring.wrap_method_docstring(cls, nt)
    Fire(cls)
