from clima import c, Schema
from pathlib import Path
import subprocess
import functools
import os


class C(Schema):
    convert_cmd = ['dephell', 'deps', 'convert', '--env']
    params = ['--from-format', '--from-path', '--to-format', '--to-path']
    win_binary: Path = Path.home()

    def post_init(self, *args):
        pass


c: C = c


@c
class Cli:
    def convert(self):
        print(c.convert_cmd)
        for e in ['pip', 'setuppy', 'pipenv']:
            subprocess.run(c.convert_cmd + [e], cwd=Path.cwd())
