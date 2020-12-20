from unittest import TestCase
from functools import partial
import sys

# Using Pure versions of paths allows testing cross platform code
# Can't use just Path, because that will get rendered to a platform specific
# subclass when validating (e.g. on windows Path('...') -> WindowsPath('...') )
from pathlib import PureWindowsPath as WindowsPath
from pathlib import PurePosixPath as PosixPath
from pathlib import Path

# from clima import Schema

from tests import SysArgvRestore, TmpC

# TODO: sane exception for this scenario
# def test_schema_without_default():
#     class C(Schema):
#         a: int

from functools import wraps


def wrap_cc(func):
    wraps(func)

    from clima import c, Schema

    def wrapped(*args, c=c, Schema=Schema, **kwargs):
        result = func(*args, c=c, Schema=Schema, **kwargs)
        c._clear()
        return result

    return wrapped


def wrap_methods_with_c(cls):
    orig = cls.__getattribute__

    def new_getattr(self, name):
        # print(f'wrapped with {c}')
        if name.startswith('test_'):
            method = getattr(cls, name)
            new_method = wrap_cc(method)
            setattr(cls, name, new_method)
        return orig(self, name)

    cls.__getattribute__ = new_getattr
    return cls


class TestSchemaNoType(TestCase, SysArgvRestore, TmpC):
    default = 42

    def setUp(self) -> None:
        from clima import c, Schema
        self.c = c
        self.save_sysargv()

        class C(Schema):
            a = self.default

    def test_default(self):
        c = self.c
        sys.argv = ['test', 'x']
        assert (c.a == self.default)

    def test_override(self):
        c = self.c
        sys.argv = ['test', 'x', '--a', '1']

        @c
        class Cli:
            def x(self):
                """docstring"""
                pass

        assert (c.a == 1)


class TestSchemaX(TestCase, SysArgvRestore):
    def test_schema_without_type(self):
        from clima import c, Schema
        self.c = c
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

        from clima import c, Schema
        self.c = c
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
        from clima import c, Schema
        self.c = c
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


class TestSchemaArgs(TestCase, SysArgvRestore):
    defaults = {
        'str': 'foobar',
        'bool': False,
    }
    changed = {
        'str': 'changed',
        'bool': True,
    }

    def setUp(self) -> None:
        from clima import c, Schema
        self.c = c
        self.save_sysargv()

        class C(Schema):
            a: str = self.defaults['str']
            b: bool = self.defaults['bool']

    def test_defaults(self):
        c = self.c
        sys.argv = ['test', 'x']

        @c
        class Cli:
            def x(self):
                """docstring"""
                pass

        assert c.a == self.defaults['str'], 'Schema definition should stick if not overridden'
        assert c.b == self.defaults['bool'], 'Schema definition should stick if not overridden'

    def test_schema_order_args(self):
        c = self.c
        sys.argv = ['test', 'x', '--a', self.changed['str'], '--b']

        @c
        class Cli:
            def x(self):
                """docstring"""
                pass

        assert c.a == self.changed['str'], 'Args given in same order as schema def should override values'
        assert c.b == self.changed['bool'], 'Args given in same order as schema def should override values'

    def test_non_schema_order_args(self):
        c = self.c
        sys.argv = ['test', 'x', '--b', '--a', self.changed['str']]

        @c
        class Cli:
            def x(self):
                """docstring"""
                pass

        print(sys.argv)
        assert c.a == self.changed['str'], 'Args given in a different order as schema def should override values'
        assert c.b == self.changed['bool'], 'Args given in a different order as schema def should override values'


class TestSchema(TestCase, SysArgvRestore):
    defaults = {
        'test_int': [42, int],
        'test_str': ['oh hi', str],
        'test_posix_path': [PosixPath('/tmp'), PosixPath],
        'test_win_path': [WindowsPath('/tmp'), WindowsPath],
    }

    def setUp(self) -> None:
        from clima import c, Schema
        self.c = c
        super().save_sysargv()

        class C(Schema):
            test_int: int = self.defaults['test_int'][0]
            test_str: str = self.defaults['test_str'][0]
            test_posix_path: PosixPath = self.defaults['test_posix_path'][0]
            test_win_path: WindowsPath = self.defaults['test_win_path'][0]

    def test_default(self):
        c = self.c
        sys.argv = ['test', 'x']
        for k, v in self.defaults.items():
            assert (getattr(c, k) == v[0])
            assert (type(getattr(c, k)) == v[1])

    def test_override(self):
        c = self.c
        sys.argv = ['test', 'x', '--test_int', '1']

        @c
        class Cli:
            def x(self):
                """docstring"""
                pass

        assert (c.test_int == 1)
        assert (type(c.test_int) == int)

    def test_no_docstring(self):
        c = self.c
        """Not defining a docstring in Configuration(Schema) should not crash the script"""
        sys.argv = ['test', 'x', '--test_str', 'no moi']

        @c
        class Cli:
            def x(self):
                pass

        assert c.test_int == 42, 'Schema should enable default value as int'
        assert c.test_str == 'no moi', 'cli args not read'

    def test_positional(self):
        c = self.c
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
        from clima import c, Schema
        self.c = c
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
        c = self.c

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
        from clima import c, Schema

        class TestTypes(Schema):
            p: WindowsPath = '.'

        @c
        class Cli:
            def x(self):
                """docstring"""
                pass

        assert (type(c.p) == WindowsPath)

    def test_posix_path(self):
        from clima import c, Schema

        class TestTypes(Schema):
            p: PosixPath = '.'

        @c
        class Cli:
            def x(self):
                """docstring"""
                pass

        assert (type(c.p) == PosixPath)

    def test_builtins_post_init(self):
        from clima import c, Schema
        values = {
            'a': True,
            'f': 1.0,
            'i': ['bbb'],
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
            field = getattr(c, k)
            value = values[k]
            assert type(getattr(c, k)) is valid, 'Fields not cast correctly after schema.post_init'
            assert field == value, f'After casting and schema.post_init, values are incorrect ("{field}"!="{value}")'


class TestTypeCastingWithArgs(TestCase, SysArgvRestore):
    def setUp(self) -> None:
        sys.argv = ['test', 'x', '--a', '0', '--path', 'foobar']

    def test_casting_cli_args(self):
        from clima import c, Schema

        class TestTypes(Schema):
            a: bool = True
            path: PosixPath = ''

        @c
        class Cli:
            @staticmethod
            def post_init(s):
                pass

            def x(self):
                """docstring"""
                pass

        # for attr, cls in TestTypes.__annotations__.items():
        #     if hasattr(c, attr):
        #         setattr(c, attr, cls(getattr(c, attr)))

        assert (type(c.a) == bool), f'Casting of cli args should follow schema {type(c.a)} != bool'
        assert (type(c.path) == PosixPath), f'Casting of cli args should follow schema {type(c.path)} != Path'

    # TODO: TBD
    def test_postinit_after_cli_args(self):
        from clima import c, Schema

        class TestTypes(Schema):
            a: bool = True
            path: PosixPath = ''

        @c
        class Cli:
            @staticmethod
            def post_init(s):
                assert type(s.a) == bool, 'post_init args should have been cast correctly'
                assert not s.a, f'post_init should have access to cli args ({s.a} != False)'

                assert type(
                    s.path) == PosixPath, f'Casting of cli args should follow schema {type(s.path)} != Path'
                assert s.path.name == 'foobar'

                s.path = Path('baz')

            def x(self):
                """docstring"""
                pass

        assert c.path.name == 'baz', 'post_init should override values'


class TestConfigurable(TestCase, SysArgvRestore):

    def setUp(self) -> None:
        from clima import c, Schema
        self.c = c
        self.save_sysargv()

        class C(Schema):
            a: int = 1  # description

    def test_cli(self):
        c = self.c
        """Basic Cli definition"""

        sys.argv = ['test', '--a', 13]

        @partial(c, noprepare=True)
        class Cli:
            def x(self):
                """docstring"""
                pass

    def test_cli_without_ds(self):
        c = self.c
        """Cli definition without a docstring"""

        @partial(c, noprepare=True)
        class Cli:
            def x(self):
                pass


class TestIterables(TestCase, SysArgvRestore):
    _int = 123
    _str = 'abc'

    def setUp(self) -> None:
        from clima import c, Schema
        self.c = c
        self.save_sysargv()

        class C(Schema):
            a: tuple = self._int  # description
            b: tuple = self._str  # description
            c: list = self._int  # description
            d: list = self._str  # description
            e: set = self._int  # description
            f: set = self._str  # description

    def test_cli_with_args(self):
        c = self.c
        """Basic Cli definition with iterables and cli args parsing"""

        sys.argv = ['test', 'x',
                    '--a', '13',
                    '--b', 'cd',
                    '--c', '13',
                    '--d', 'cd',
                    '--e', '13',
                    '--f', 'cd',
                    ]

        @c
        class Cli:
            def x(self):
                """docstring"""
                pass

        assert c.a == tuple([13]), 'Should wrap in iterable when parsing cli args'
        assert c.b == tuple(['cd']), 'Should wrap in iterable when parsing cli args'
        assert c.c == list([13]), 'Should wrap in iterable when parsing cli args'
        assert c.d == list(['cd']), 'Should wrap in iterable when parsing cli args'
        assert c.e == set([13]), 'Should wrap in iterable when parsing cli args'
        assert c.f == set(['cd']), 'Should wrap in iterable when parsing cli args'

    def test_cli(self):
        c = self.c
        """Basic Cli with iterables"""

        sys.argv = ['test', 'x']

        @c
        class Cli:
            def x(self):
                """docstring"""
                pass

        assert c.a == tuple([self._int]), 'Should wrap in iterable when configured in schema'
        assert c.b == tuple([self._str]), 'Should wrap in iterable when configured in schema'
        assert c.c == list([self._int]), 'Should wrap in iterable when configured in schema'
        assert c.d == list([self._str]), 'Should wrap in iterable when configured in schema'
        assert c.e == set([self._int]), 'Should wrap in iterable when configured in schema'
        assert c.f == set([self._str]), 'Should wrap in iterable when configured in schema'
