"""Configuration file (sth.cfg / sth.toml) handling"""
import configparser
import sys

from pathlib import Path

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # pragma: no cover - 3.9/3.10 fallback
    import tomli as tomllib  # type: ignore[no-redef]

from clima import utils


def is_in_module(f):
    return len(list(Path(f).parent.glob('__init__.py')))


def cfgs_gen(p):
    yield from Path(p).glob('*.toml')
    yield from Path(p).glob('*.conf')
    yield from Path(p).glob('*.cfg')


def _read_toml(path):
    with open(path, 'rb') as f:
        return tomllib.load(f)


def _has_relevant_section(path, package_name):
    """Return True if `path` parses as a config file containing either
    [<package_name>] or [Clima]."""
    suffix = Path(path).suffix.lower()
    if suffix == '.toml':
        try:
            data = _read_toml(path)
        except (tomllib.TOMLDecodeError, OSError):
            return False
        if package_name is not None and package_name in data:
            return True
        return 'Clima' in data
    try:
        parser = configparser.ConfigParser()
        parser.read(path)
    except configparser.Error:
        return False
    if package_name is not None and package_name in parser:
        return True
    return 'Clima' in parser


def find_cfg(p, level=2, package_name=None):
    """Find a `.toml`, `.conf`, or `.cfg` file starting at `p`, optionally walking up.

    Discovery rules:
    - Glob `p` for `*.toml` then `*.conf` then `*.cfg`; returns the first
      match (first `.toml` preferred, then `.conf`, then `.cfg`). Ordering
      within each extension is whatever `Path.glob` yields (typically
      filesystem order).
    - If `package_name` is provided, candidates are filtered to files that
      parse as INI and contain either a `[<package_name>]` or `[Clima]`
      section. Files that cannot be parsed as INI are skipped.
    - If no candidate is found at `p`, recursion walks up to `level` parent
      directories, but only while `is_in_module(p)` holds — which, note,
      checks whether **`p`'s parent** (not `p` itself) contains an
      `__init__.py`. In practice this means the hop happens when the next
      directory up still looks like part of a Python package tree, so
      unrelated configs outside the user's package are not picked up.
    - Default `level` is 2, so at most two parent hops are attempted.
    - Returns the matching `Path`, or `None` if nothing is found.
    """
    p = Path(p)
    cfgs = list(cfgs_gen(p))
    if package_name is not None:
        cfgs = [c for c in cfgs if _has_relevant_section(c, package_name)]
    if len(cfgs) == 0:
        if is_in_module(p) and level > 0:
            return find_cfg(p.parent, level - 1, package_name=package_name)
        else:
            return None
    else:
        return cfgs[0]



def read_config(_filepath='test.cfg', package_name=None) -> dict:
    """Read and parse a config file.
    
    Args:
        _filepath: Path to the config file
        package_name: Package name to look for in config sections. Only used in tests,
                     normally deduced automatically.

    Returns:
        Dictionary containing the parsed config values
    """
    filepath = Path(_filepath)
    parsed_conf = {}
    if not filepath.exists():
        return parsed_conf

    if package_name is None:
        package_name = utils.deduce_package()

    if filepath.suffix.lower() == '.toml':
        try:
            data = _read_toml(filepath)
        except (tomllib.TOMLDecodeError, OSError):
            print(f'warning: inferred {_filepath} to be a valid config file, but could not read it.', file=sys.stderr)
            return parsed_conf
        if package_name is not None and package_name in data:
            parsed_conf = dict(data[package_name])
        elif 'Clima' in data:
            parsed_conf = dict(data['Clima'])
        return parsed_conf

    try:
        file_config = configparser.ConfigParser()
        file_config.read(filepath)

        if package_name is not None and package_name in file_config:
            parsed_conf = dict(file_config[package_name])
        elif 'Clima' in file_config:
            parsed_conf = dict(file_config['Clima'])
    except (configparser.Error, OSError):
        print(f'warning: inferred {_filepath} to be a valid config file, but could not read it.', file=sys.stderr)

    return parsed_conf

def get_config_path(_schema):
    """
    Resolve filepath for a config file, if one can be found.

    Args:
        _schema:

    Returns:
        Path of config file or None

    Examples of parsing patterns:
        {}                                  -> glob for any .cfg file at pwd
        {cwd: '../foo'}                     -> glob for any .cfg file using cwd
        {cwd: '/root/foo'}                  -> glob for any .cfg file using cwd
        {cwd: '../foo', CFG: 'my.cfg'}      -> select my.cfg at dir cwd
        {cwd: '/root/foo', CFG: 'my.cfg'}   -> select my.cfg at dir cwd
        {CFG: 'my.cfg'}                     -> select my.cfg at pwd
        {CFG: '/root/foo/my.cfg'}           -> select cfg using absolute path

    """
    # if hasattr cfg and absolute, use cfg
    cfg_filepath = Path(getattr(_schema, 'CFG', ''))
    if not cfg_filepath.is_absolute():
        # concate getattr cwd/'' getattr cfg/''
        cfg_filepath = Path(getattr(_schema, 'cwd', '')) / cfg_filepath
        if not cfg_filepath.is_file():
            package_name = utils.deduce_package()
            cfg_filepath = find_cfg(cfg_filepath, package_name=package_name)

    return cfg_filepath
