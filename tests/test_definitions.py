from unittest import TestCase
from functools import partial
import sys

# Using Pure versions of paths allows testing cross platform code
# Can't use just Path, because that will get rendered to a platform specific
# subclass when validating (e.g. on windows Path('...') -> WindowsPath('...') )
from pathlib import PureWindowsPath as WindowsPath
from pathlib import PurePosixPath as PosixPath

from clima import c, Schema

from tests import SysArgvRestore


# TODO: sane exception for this scenario
# def test_schema_without_default():
#     @c
#     class C(Schema):
#         a: int


class TestSchemaX(TestCase, SysArgvRestore):
    def test_schema_without_type(self):
        sys.argv = ['test', 'x']

        @c
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
        '_int': [42, int],
        '_str': ['oh hi', str],
        '_posix_path': [PosixPath('/tmp'), PosixPath],
        '_win_path': [WindowsPath('/tmp'), WindowsPath],
    }

    def setUp(self) -> None:
        self.save_sysargv()

        class C(Schema):
            _int: int = self.defaults['_int'][0]
            _str: str = self.defaults['_str'][0]
            _posix_path: PosixPath = self.defaults['_posix_path'][0]
            _win_path: WindowsPath = self.defaults['_win_path'][0]

    def test_default(self):
        sys.argv = ['test', 'x']
        for k, v in self.defaults.items():
            assert (getattr(c, k) == v[0])
            assert (type(getattr(c, k)) == v[1])

    def test_override(self):
        sys.argv = ['test', 'x', '--a', '1']

        @c
        class Cli:
            def x(self):
                """docstring"""
                pass

        assert (c.a == 1)
        assert (type(c.a) == int)


class TestTypeCasting(TestCase, SysArgvRestore):
    def test_builtins(self):
        sys.argv = ['test', 'x']

        @c
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

        @c
        class Cli:
            def x(self):
                """docstring"""
                pass

        for k, valid in zip('abcdefghilmn', [
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
        ]):
            assert type(getattr(c, k)) == valid


class TestConfigurable(TestCase, SysArgvRestore):

    def setUp(self) -> None:
        self.save_sysargv()

        @c
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


