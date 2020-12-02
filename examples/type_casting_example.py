from clima import c, Schema
import pathlib

class Conf(Schema):
    p: pathlib.Path = ''  # This path should be cast to path
    s: str = 1  # This int should be cast to str
    i: int = '2'  # This int should be cast to str


@c
class Cli:
    def run(self):
        """run this to verify the casting"""
        print(f'Checking casting of c.p {repr(c.p)}')
        assert(type(c.p) is type(pathlib.Path()))
        print(f'Checking casting of c.s {repr(c.s)}')
        assert(type(c.s) is type(str))
        print(f'Checking casting of c.i {repr(c.i)}')
        assert(type(c.i) is type(int))
        print('Types were cast correctly!')

