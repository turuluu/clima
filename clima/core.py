import fileinput
import inspect
import os
import sys
from collections import ChainMap
from functools import partial
from pathlib import Path
from typing import Dict

from clima import docstring, configfile
from clima import schema, utils, password_store, env
from clima.fire import Fire


class RequiredParameterException(Exception):
    pass


DECORATORS_STATE = {
    'schema': None,
    'generated': None,
}

schema_decorator = partial(schema.schema_decorator, DECORATORS_STATE)


class Configurable:
    """Configuration management"""
    __configured = None

    def _get_configured(self):
        return self.__configured

    def _set_configured(self, dct: dict):
        self.__configured = dct

    def _chain_configurations(self, params: dict, _schema):
        """Chains all configuration options together"""
        cm = ChainMap(
            params,
            utils.filter_fields(os.environ, _schema),
            env.get_env(_schema),
            _schema._get_configfile_asdict(),
            password_store.get_secrets(_schema),
            _schema._asdict()
        )

        return dict(cm)

    def _init(self, _schema: schema.MetaSchema):
        is_schema = isinstance(_schema, schema.MetaSchema)
        if not is_schema:
            raise TypeError('The configuration should inherit Schema')

        # Allows using Schema as a subclass only
        c.__configured = _schema

        # Allows deoorator usage with @c.init
        return schema_decorator(_schema)

    def __call__(self, cls, *, noprepare=False):
        """
        Decorator to define the Cli object
        """
        _cli = _build_cli(cls)
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
        return c_item

    def _clear(self):
        """Testing requires clearing global state"""

        self.__configured = None
        Schema._package_name = None

        DECORATORS_STATE['schema'] = None
        DECORATORS_STATE['generated'] = None


c = Configurable()


def add_to_decorators(key, value):
    DECORATORS_STATE[key] = value


def cast_as_annotated(_schema, attr, container=None, value=None):
    """Schema is annotated with types. These types are used to
    recast the value (value == container[attr] if not specified in kwargs)
    in container (container == _schema if not specified in kwargs)
    """
    if container is None:
        container = _schema

    if value is None:
        try:
            value = getattr(container, attr)
        except RequiredParameterException:
            return None
    result = value

    if hasattr(type(_schema), '__annotations__'):
        annotated_type = type(_schema).__annotations__.get(attr)
        if annotated_type is not None:

            if schema.should_wrap_as_list(value, annotated_type):
                result = annotated_type([value])
            elif annotated_type is bool and isinstance(value, str):
                # Special handling for boolean strings from config files
                result = value.lower() in ('true', '1', 'yes', 'on')
            else:
                result = annotated_type(value)
    return result


def _auto_setup_logging(schema, configured):
    """Set up logging if Schema has verbose or quiet fields."""
    fields = schema._fields
    if 'verbose' not in fields and 'quiet' not in fields:
        return
    from clima.logging import setup_logging
    verbose = getattr(configured, 'verbose', False)
    quiet = getattr(configured, 'quiet', False)
    log_file = f'{Path(sys.argv[0]).stem}.debug.log'
    setup_logging(verbose=verbose, quiet=quiet, log_file=log_file)


def _build_cli(cls):
    """Decorator that wraps the command line interface specific class with fire"""
    state = DECORATORS_STATE

    CliClass = cls

    def init(self, **cli_args):
        """Generated init"""
        s = state['schema']

        # Extract and set cwd FIRST if provided via CLI, before config file discovery.
        # This ensures _chain_configurations uses the correct directory for config lookup.
        if hasattr(s, 'cwd') and 'cwd' in cli_args:
            cwd_value = cli_args.pop('cwd')  # Remove from cli_args to prevent override
            cwd_path = cast_as_annotated(s, 'cwd', value=cwd_value)
            if isinstance(cwd_path, str):
                cwd_path = Path(cwd_path)
            if not cwd_path.is_absolute():
                cwd_path = Path.cwd() / cwd_path
            setattr(s, 'cwd', cwd_path)

        # Cast everything according to schema before Cli.post_init
        for attr, cli_arg_value in cli_args.items():
            if hasattr(s, attr) and attr != 'cwd':  # Skip cwd, already handled above
                setattr(s, attr, cast_as_annotated(s, attr, value=cli_arg_value))
            s: type(s) = s

        # Handle cwd if not already set from CLI (apply relative path logic)
        if hasattr(s, 'cwd'):
            p: Path = getattr(s, 'cwd')
            if p and not p.is_absolute():
                setattr(s, 'cwd', Path.cwd() / p)

        global c
        cm = c._chain_configurations(cli_args, s)

        tmp_c = Configurable()
        tmp_c._set_configured(cm)
        for attr in s._asdict():
            if attr in cm:
                setattr(tmp_c, attr, cast_as_annotated(s, attr, container=tmp_c))

        if hasattr(CliClass, 'post_init'):
            CliClass.post_init(tmp_c)

            for attr in s._asdict():
                if hasattr(tmp_c, attr):
                    setattr(tmp_c, attr, cast_as_annotated(s, attr, container=tmp_c))

        for attr in tmp_c._get_configured():
            val = tmp_c._get_configured()[attr]
            if val is not None:
                setattr(c, attr, getattr(tmp_c, attr))

        # Write resolved values back onto Schema class attributes
        # so C.field works in the new @C.cli API
        schema_cls = type(s)
        for attr in s._asdict():
            try:
                val = getattr(c, attr)
                setattr(schema_cls, attr, val)
            except (RequiredParameterException, AttributeError):
                pass

        _auto_setup_logging(s, c)

    cls_attrs = dict(
        __init__=init,
        __repr__=cls.__repr__,
        __doc__=cls.__doc__,
        **{m_name: m for m_name, m in cls.__dict__.items() if not m_name.startswith('_')}
    )

    _Cli = type('Cli', (cls,), cls_attrs)
    state['generated'] = _Cli

    return _Cli


class Schema(object, metaclass=schema.MetaSchema):
    """Base class for the user's configuration class"""

    _package_name = None
    def _get_configfile_asdict(self):
        result: Dict = {}

        configfile_path = configfile.get_config_path(self)
        if configfile_path is not None:
            result = utils.filter_fields(configfile.read_config(configfile_path, self._package_name), self)
            result = utils.type_correct_with(result, self)

        return result

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

    # Check for piped input (stdin)
    if len(sys.argv) >= 2 and not sys.stdin.isatty():
        try:
            with fileinput.input(files=False) as stdin:
                stdin_str = next(stdin).strip()
            sys.argv += stdin_str.split()
        except StopIteration as ex:
            pass

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
                # After the first explicit `--param` append the rest of args as is i.e.
                # no need to parse for positional arguments after this point
                new_args += sys.argv[i:]
                break
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


def unknown_cli_flags(argv, schema_fields):
    """Return sorted flag names present in argv but missing from schema_fields.

    Accepts both `--foo` and `--foo=bar` forms. Stops scanning at a bare `--`
    sentinel (Fire's end-of-options marker). Ignores `-h` / `--help` and any
    short-form flags.
    """
    known = set(schema_fields)
    unknown = set()
    for token in argv:
        if token == '--':
            break
        if not isinstance(token, str) or not token.startswith('--'):
            continue
        name = token[2:].split('=', 1)[0]
        if not name or name == 'help':
            continue
        if name not in known:
            unknown.add(name)
    return sorted(unknown)


def filter_argv_of_unknown_flags(argv, unknown_flags):
    """Remove unknown flags and their values from argv.

    Handles both `--flag value` and `--flag=value` forms.
    Stops processing at a bare `--` sentinel (Fire's end-of-options marker).
    """
    if not unknown_flags:
        return argv

    unknown_set = set(unknown_flags)
    result = []
    skip_next = False

    for i, token in enumerate(argv):
        if skip_next:
            skip_next = False
            continue

        if token == '--':
            result.append(token)
            result.extend(argv[i + 1:])
            break

        if isinstance(token, str) and token.startswith('--') and not token.endswith('--'):
            # Extract flag name from both forms: --foo and --foo=bar
            if '=' in token:
                flag_name = token[2:].split('=', 1)[0]
                if flag_name in unknown_set:
                    continue  # Skip this flag entirely (it includes the value)
                result.append(token)
            else:
                flag_name = token[2:]
                if flag_name in unknown_set:
                    skip_next = True  # Skip this flag and its value
                    continue
                result.append(token)
        else:
            result.append(token)

    return result


def prepare(cls, schema: Schema):
    """Beef: prepares signatures, docstrings and initiates fire for the cli-magic
    Also: error handling printout customisation
    """
    prepare_signatures(cls, schema)
    docstring.wrap_method_docstring(cls, schema)

    unknown = unknown_cli_flags(sys.argv[2:], schema._fields)
    if unknown:
        print(
            f'clima: warning: unknown parameter(s) not defined in Schema: '
            f'{", ".join(unknown)}',
            file=sys.stderr,
        )
        # Remove unknown flags from sys.argv to prevent them from appearing
        # in help output or being passed to Fire
        sys.argv = filter_argv_of_unknown_flags(sys.argv, unknown)

    with utils.suppress_traceback():

        if len(sys.argv) > 1 and sys.argv[-1] == 'version':
            print(schema.version)
        else:
            Fire(cls)
