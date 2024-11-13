"""Simple boilerplate for cli scripts"""
import importlib.metadata
__version__= importlib.metadata.version('clima')

from clima import fire
from clima.core import c, Schema
from clima.helputils import print_help, HelpString
from clima.utils import suppress_traceback
