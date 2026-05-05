import inspect
import sys
import tomllib
import typing
# Until poetry fixes this https://github.com/python-poetry/poetry/issues/144
# This hack is necessary to report correct __version__
# inside the project
# Version printing part 0
from pathlib import Path

from clima import utils


def asdict(obj):
    """Helper to create a dictionary out of the class attributes (fields/variables)"""
    obj_dict = obj.__class__.__dict__
    return {k: getattr(obj, k) for k, v in obj_dict.items()
            if not k.startswith('_')
            and not inspect.isfunction(v)
            and not inspect.ismethod(v)}


def schema_decorator(decorators_state, cls):
    """Adds cls to decorator_state"""
    decorators_state['schema'] = cls()
    return cls

# def deduce_importer_version():
#     """Experimental way of deducing the version from the package that
#     imports clima
#     """
#     package = deduce_package()
#     return get_package_version(package)


# def deduce_importer_version():
#     """experimental way of deducing the version from the package that
#     imports clima
#     """
#     from importlib import util
#     version = None
#     try:
#         frame = get_importing_frame()
#         p = Path(frame.filename)
#         parent = str(p.parent.name)
#         importer_package = None
#         while importer_package is None:
#             spec = util.find_spec(parent)
#             if hasattr(spec, 'name'):
#                 importer_package = spec.name
#                 break;
#             if str(p.parent) == str(p.parent.parent):
#                 break
#             p = p.parent
#             parent = str(p.name)
#             if importer_package:
#                 version = metadata.version(importer_package)
#         version = metadata.version(importer_package)
#     except:
#         pass

#     return version



def parse_version_from_pyproject_toml(start: Path = None):
    """Walk up from `start` (default: cwd) looking for a `pyproject.toml`
    with a `[tool.poetry]` section and return its `version`, or None.

    Walking up ensures an installed script invoked as `myscript version`
    from an unrelated cwd can still locate its own `pyproject.toml` sitting
    alongside the importing script.
    """
    if start is None:
        start = Path.cwd()
    start = Path(start)
    if start.is_file():
        start = start.parent

    for directory in [start, *start.parents]:
        toml = directory / 'pyproject.toml'
        if toml.exists():
            try:
                with toml.open('rb') as f:
                    data = tomllib.load(f)
            except (tomllib.TOMLDecodeError, OSError):
                # Unparsable or unreadable pyproject.toml — skip and keep
                # walking upward. This is different from a successfully read
                # file that simply has no [tool.poetry] section.
                continue
            poetry = data.get('tool', {}).get('poetry', {})
            version = poetry.get('version')
            if version is not None:
                return version
            return None
    return None


def _importer_dir():
    frame = utils.get_importing_frame()
    if frame is None:
        return None
    return Path(frame.filename).parent


def get_pkg_version():
    # Version printing part 1
    # Enables version printing out of the box
    # Idea is, that when poetry is used, this will look up the version
    # in its configuration.

    if (version := utils.get_package_version(utils.deduce_package()) ) is not None:
        pass
    elif (version := parse_version_from_pyproject_toml(start=_importer_dir())) is not None:
        pass
    else:
        version = '0.0.1'

    return version


def is_iterable(value):
    iterables = [tuple, list, set]

    if type(value) in iterables or value in iterables:
        return True
    # Recognize parameterized generics like list[str], tuple[int, ...], set[bytes].
    origin = typing.get_origin(value)
    return origin in {tuple, list, set}


def should_wrap_as_list(value, target_type):
    """Helper for casting. Casting a str in list will split it..."""
    res = False
    if not is_iterable(value) and is_iterable(target_type):
        res = True
    elif isinstance(value, str) and (target_type is not str and is_iterable(target_type)):
        res = True

    return res


class MetaSchema(type):
    """
    Validate, cast types, wrap configuration and invoke 'post_hook' method for
    the Schema class
    """

    def __new__(mcs, name, bases, namespace, **kwds):
        cls = type.__new__(mcs, name, bases, namespace)
        cls._schema_ready = False

        # post init hook
        cls.post_init(cls)

        # Parsing type descriptors
        if '__annotations__' in namespace:
            for attr, t in namespace['__annotations__'].items():
                # Validation
                try:
                    value = namespace[attr]
                    schema_value = getattr(cls, attr)

                    # TODO: Nested types. This only wraps a single iterable

                    if should_wrap_as_list(value, t):
                        value = [value]

                    if should_wrap_as_list(schema_value, t):
                        schema_value = [schema_value]

                    # Type casting
                    if t(value) == t(schema_value):
                        if getattr(cls, attr) is not None:
                            setattr(cls, attr, t(value))
                    else:
                        setattr(cls, attr, t(schema_value))
                except TypeError as ex:
                    print('given parameters or defined defaults were of incorrect type:')
                    # print(f'{cls.__qualname__}.{ann} -> {ex.args}')  # f-strings require >=3.6
                    print('{}.{} -> {}'.format(cls.__qualname__, attr, ex.args))
                    sys.exit(1)

        setattr(cls, 'version', get_pkg_version())

        # TODO: Maybe check that given parameters matched the schema?
        # Even a fuzzy search to suggest close matches

        # Wrap schema with c (configuration decorator
        cls._wrap(cls)

        cls._schema_ready = True
        return cls

    def __init__(cls, name, bases, namespace, **kwds):
        super().__init__(name, bases, namespace)

    def __getattribute__(cls, name):
        value = super().__getattribute__(name)
        # Guard: raise for annotated fields that are None (required parameters)
        # Only active after class construction is complete (_schema_ready flag)
        if value is None and not name.startswith('_'):
            try:
                ready = super().__getattribute__('_schema_ready')
            except AttributeError:
                ready = False
            if ready:
                annotations = {}
                try:
                    annotations = super().__getattribute__('__annotations__')
                except AttributeError:
                    pass
                if name in annotations:
                    from clima.core import RequiredParameterException
                    raise RequiredParameterException(f'Missing argument for "{name}"')
        return value

    def cli(cls, cli_cls):
        """Decorator to define the CLI class, equivalent to @c.

        Usage::

            @C.cli
            class MyCli:
                def greet(self):
                    print(C.name)
        """
        # Delegate to Configurable.__call__ to keep both entry points in sync
        from clima import core
        return core.c(cli_cls)
