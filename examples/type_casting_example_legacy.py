from clima import c, Schema
import pathlib

class Conf(Schema):
    p: pathlib.PurePosixPath = ''  # This path should be cast to path
    s: str = 1  # This int should be cast to str
    i: int = '2'  # This int should be cast to str


@c
class Cli:
    def run(self):
        """run this to verify the casting"""
        print(f'Checking casting of c.p {repr(c.p)}')
        assert type(c.p) is pathlib.PurePosixPath, f'Should have cast to path instead of {type(c.p)}'
        print(f'Checking casting of c.s {repr(c.s)}')
        assert type(c.s) is str, f'Should have cast to str instead of {type(c.s)}'
        print(f'Checking casting of c.i {repr(c.i)}')
        assert type(c.i) is int, f'Should have cast to int instead of {type(c.i)}'

        print('Types were cast correctly!')

