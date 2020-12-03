#!/usr/bin/env python
from clima import c
from pathlib import Path
from subprocess import run as R


@c
class Cli:
    def bump(self):
        R(['poetry', 'version', 'patch'])

    def build(self):
        R(['poetry', 'build'], cwd=Path.cwd())

    def upload(self):
        R(['poetry', 'publish'], cwd=Path.cwd())

    def all(self):
        """foobar"""
        self.bump()
        self.build()
        self.upload()
