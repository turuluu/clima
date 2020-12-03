from unittest import TestCase
from functools import partial
import sys

# Using Pure versions of paths allows testing cross platform code
# Can't use just Path, because that will get rendered to a platform specific
# subclass when validating (e.g. on windows Path('...') -> WindowsPath('...') )
from pathlib import PureWindowsPath as WindowsPath
from pathlib import PurePosixPath as PosixPath
from pathlib import Path

from clima import c, Schema

from tests import SysArgvRestore


# TODO: sane exception for this scenario
# def test_schema_without_default():
#     class C(Schema):
#         a: int


class TestSchemaX(TestCase, SysArgvRestore):
    def test_schema_without_type(self):
        sys.argv = ['test', 'x']

        class C(Schema):
            a = 1
            L = [1, 2, 3]

        @c
        class D:
            def x(self):
                assert c.a == 1
                assert c.L == [1, 2, 3]

        assert c.a == 1


class TestSchemaY(TestCase, SysArgvRestore):
    def test_schema_post_init(self):
        sys.argv = ['test', 'x']

        class C(Schema):
            a = 1

            def post_init(self, *args):
                self.a = 2

        @c
        class D:
            def x(self):
                assert c.a == 2

        assert c.a == 2

    def test_schema_post_init_adding_attr(self):
        sys.argv = ['test', 'x']

        class C(Schema):
            a = 1

            def post_init(self, *args):
                self.b = 2

        @c
        class D:
            def x(self):
                assert c.a == 1
                assert c.b == 2

        assert c.a == 1
        assert c.b == 2


class TestSchemaNoType(TestCase, SysArgvRestore):
    default = 42

    def setUp(self) -> None:
        self.save_sysargv()

        class C(Schema):
            a = self.default

    def test_default(self):
        sys.argv = ['test', 'x']
        assert (c.a == self.default)

    def test_override(self):
        sys.argv = ['test', 'x', '--a', '1']

        @c
        class Cli:
            def x(self):
                """docstring"""
                pass

        assert (c.a == 1)


class TestSchema(TestCase, SysArgvRestore):
    defaults = {
        'test_int': [42, int],
        'test_str': ['oh hi', str],
        'test_posix_path': [PosixPath('/tmp'), PosixPath],
        'test_win_path': [WindowsPath('/tmp'), WindowsPath],
    }

    def setUp(self) -> None:
        super().save_sysargv()

        class C(Schema):
            test_int: int = self.defaults['test_int'][0]
            test_str: str = self.defaults['test_str'][0]
            test_posix_path: PosixPath = self.defaults['test_posix_path'][0]
            test_win_path: WindowsPath = self.defaults['test_win_path'][0]

    def test_default(self):
        sys.argv = ['test', 'x']
        for k, v in self.defaults.items():
            assert (getattr(c, k) == v[0])
            assert (type(getattr(c, k)) == v[1])

    def test_override(self):
        sys.argv = ['test', 'x', '--test_int', '1']

        @c
        class Cli:
            def x(self):
                """docstring"""
                pass

        assert (c.test_int == 1)
        assert (type(c.test_int) == int)

    def test_no_docstring(self):
        """Not defining a docstring in Configuration(Schema) should not crash the script"""
        sys.argv = ['test', 'x', '--test_str', 'no moi']

        @c
        class Cli:
            def x(self):
                pass

        assert (c.test_int == 42)
        assert (c.test_str == 'no moi')

    def test_positional(self):
        """Positional arguments should be parsed from Configuration(Schema) layout order"""
        _int = 96
        _str = 'numberwang'
        sys.argv = ['test', 'x', _int, _str]

        @c
        class Cli:
            def x(self):
                """docstring"""
                pass

        assert (c.test_int == _int)
        assert (c.test_str == _str)


class TestTypeCasting(TestCase, SysArgvRestore):
    def setUp(self) -> None:
        sys.argv = ['test', 'x']

        class TypeGalore(Schema):
            a: bool = 0
            b: bytearray = 0
            c: bytes = 0
            d: complex = 0
            e: dict = tuple(zip('aa', 'bb'))
            f: float = 0
            g: frozenset = {}
            h: int = 0.0
            i: list = 'aa'
            # k: property = 0
            l: set = [1, 2]
            m: str = 0
            n: tuple = []
            o: int = '1'

    def test_builtins(self):
        @c
        class Cli:
            def x(self):
                """docstring"""
                pass

        for k, valid in zip('abcdefghilmno', [
            bool,
            bytearray,
            bytes,
            complex,
            dict,
            float,
            frozenset,
            int,
            list,
            # property,
            set,
            str,
            tuple,
            int
        ]):
            assert type(getattr(c, k)) == valid


class TestTypeCastingWith(TestCase, SysArgvRestore):
    def setUp(self) -> None:
        sys.argv = ['test', 'x']

    def test_win_path(self):
        class TestTypes(Schema):
            p: WindowsPath = '.'

        @c
        class Cli:
            def x(self):
                """docstring"""
                pass

        assert (type(c.p) == WindowsPath)

    def test_posix_path(self):
        class TestTypes(Schema):
            p: PosixPath = '.'

        @c
        class Cli:
            def x(self):
                """docstring"""
                pass

        assert (type(c.p) == PosixPath)

    def test_builtins_post_init(self):
        values = {
            'a': True,
            'f': 1.0,
            'i': ['b', 'b', 'b'],
            'm': '1',
        }

        class TypeGalore(Schema):
            a: bool = 0
            b: bytearray = 0
            c: bytes = 0
            d: complex = 0
            e: dict = tuple(zip('aa', 'bb'))
            f: float = 0
            g: frozenset = {}
            h: int = 0.0
            i: list = 'aa'
            # k: property = 0
            l: set = [1, 2]
            m: str = 0
            n: tuple = []

            def post_init(self, *args):
                # overriding
                self.a = 1
                self.f = 1
                self.i = 'bbb'
                self.m = 1

        @c
        class Cli:
            def x(self):
                """docstring"""
                pass

        for k, valid in zip('afim', [
            bool,
            float,
            list,
            str,
        ]):
            assert type(getattr(c, k)) is valid
            assert getattr(c, k) == values[k]


class TestTypeCastingWithArgs(TestCase, SysArgvRestore):
    def setUp(self) -> None:
        sys.argv = ['test', 'x', '--a', '0', '--path', 'foobar']

    def test_casting_cli_args(self):
        class TestTypes(Schema):
            a: bool = True
            path: PosixPath = ''

        @c
        class Cli:
            def x(self):
                """docstring"""
                pass

        # for attr, cls in TestTypes.__annotations__.items():
        #     if hasattr(c, attr):
        #         setattr(c, attr, cls(getattr(c, attr)))

        assert (type(c.a) == bool), f'Casting of cli args should follow schema {type(c.a)} != bool'
        assert (type(c.path) == PosixPath), f'Casting of cli args should follow schema {type(c.path)} != Path'

    # TODO: TBD
    # def test_postinit_after_cli_args(self):
    #     class TestTypes(Schema):
    #         a: bool = True
    #         path: PosixPath = ''
    #
    #         def post_init(self, *args):
    #             assert type(self.a) == bool, 'post_init args should have been cast correctly'
    #             assert not self.a, f'post_init should have access to cli args ({self.a} != False)'
    #
    #             assert type(
    #                 self.path) == PosixPath, f'Casting of cli args should follow schema {type(self.path)} != Path'
    #             assert self.path.name == 'foobar'
    #
    #             self.path = Path('baz')
    #
    #     @c
    #     class Cli:
    #         def x(self):
    #             """docstring"""
    #             pass
    #
    #     assert c.path.name == 'baz', 'post_init should override values'


class TestConfigurable(TestCase, SysArgvRestore):

    def setUp(self) -> None:
        self.save_sysargv()

        class C(Schema):
            a: int = 1  # description

    def test_cli(self):
        """Basic Cli definition"""

        sys.argv = ['test', '--a', 13]

        @partial(c, noprepare=True)
        class Cli:
            def x(self):
                """docstring"""
                pass

    def test_cli_without_ds(self):
        """Cli definition without a docstring"""

        @partial(c, noprepare=True)
        class Cli:
            def x(self):
                pass
