"""Simple boilerplate for cli scripts

Preferred API (new)::

    from clima import Schema

    class C(Schema):
        name: str = 'World'

    @C.cli
    class Cli:
        def greet(self):
            print(C.name)

Legacy API (deprecated — will be removed in a future major version)::

    from clima import c, Schema

    class C(Schema):
        name: str = 'World'

    @c
    class Cli:
        def greet(self):
            print(c.name)
"""
import importlib.metadata
try:
    __version__ = importlib.metadata.version('clima')
except importlib.metadata.PackageNotFoundError:
    __version__ = '0.0.0+local'

from clima import fire
from clima.core import Schema, Configurable
from clima.core import c  # Deprecated: use @YourSchema.cli instead of @c
from clima.helputils import print_help, HelpString
from clima.utils import suppress_traceback
from clima.logging import setup_logging

__all__ = [
    'c', 'Schema', 'Configurable',
    'fire',
    'print_help', 'HelpString',
    'suppress_traceback',
    'setup_logging',
]
