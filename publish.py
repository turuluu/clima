#!/usr/bin/env python
from clima import c, Schema
from pathlib import Path
from subprocess import run as R
import functools
import os


class C(Schema):
    convert_cmd = ['dephell', 'deps', 'convert', '--env']
    version = 'fix'  # bump version one of {major, minor, fix}


c: C = c


@c
class Cli:
    def convert(self):
        for e in ['pip', 'setuppy', 'pipenv']:
            print(f'generating {e}')
            R(c.convert_cmd + [e], cwd=Path.cwd())

    def bump(self):
        R(['dephell', 'project', 'bump', '--tag=v.', c.version])

    def build(self):
        R(['poetry', 'build'], cwd=Path.cwd())

    def all(self):
        """foobar"""
        self.convert()
        self.bump()
        self.build()
        R(['poetry', 'publish'], cwd=Path.cwd())
