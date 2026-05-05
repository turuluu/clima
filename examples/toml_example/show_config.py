#!/usr/bin/env python
"""Demonstrates loading every clima-supported type from a TOML config file.

Run from this directory:

    python show_config.py print --cwd .

Or from anywhere by passing --cwd:

    python show_config.py print --cwd path/to/toml_example
"""
from clima import c, Schema


class C(Schema):
    cwd: str = '.'  # directory to search for example.toml
    name: str = 'unset'
    port: int = 0
    ratio: float = 0.0
    debug: bool = False
    tags: list[str] = []
    matrix: list[list] = [[]]
    pair: tuple = ()
    items: list = []


c: C = c


@c
class Cli:
    def print(self):
        """Print every resolved value with its runtime type."""
        fields = ('name', 'port', 'ratio', 'debug', 'tags', 'matrix', 'pair', 'items')
        for field in fields:
            value = getattr(c, field)
            print(f'{field:>8} = {value!r:<40}  ({type(value).__name__})')
