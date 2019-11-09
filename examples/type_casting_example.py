from clima import c, Schema
import pathlib

class Conf(Schema):
    p: pathlib.Path = ''  # This path should be cast to path


@c
class Cli:
    def run(self):
        """run this to verify the casting"""
        print(repr(c.p))
        assert(type(c.p) is type(pathlib.Path()))
        print('Type was cast correctly!')

