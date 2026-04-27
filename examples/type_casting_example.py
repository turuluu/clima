from clima import Schema
import pathlib

class Conf(Schema):
    p: pathlib.PurePosixPath = ''  # This path should be cast to path
    s: str = 1  # This int should be cast to str
    i: int = '2'  # This int should be cast to str


@Conf.cli
class Cli:
    def run(self):
        """run this to verify the casting"""
        print(f'Checking casting of Conf.p {repr(Conf.p)}')
        assert type(Conf.p) is pathlib.PurePosixPath, f'Should have cast to path instead of {type(Conf.p)}'
        print(f'Checking casting of Conf.s {repr(Conf.s)}')
        assert type(Conf.s) is str, f'Should have cast to str instead of {type(Conf.s)}'
        print(f'Checking casting of Conf.i {repr(Conf.i)}')
        assert type(Conf.i) is int, f'Should have cast to int instead of {type(Conf.i)}'

        print('Types were cast correctly!')

