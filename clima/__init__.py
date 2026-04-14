"""Simple boilerplate for cli scripts"""
import importlib.metadata
try:
    __version__ = importlib.metadata.version('clima')
except importlib.metadata.PackageNotFoundError:
    __version__ = '0.0.0+local'

from clima import fire
from clima.core import c, Schema, Configurable
from clima.helputils import print_help, HelpString
from clima.utils import suppress_traceback
