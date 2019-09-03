from unittest import TestCase
from clima import c, Schema
from functools import partial
import sys
import os
# Using Pure versions of paths allows testing cross platform code
# Can't use just Path, because that will get rendered to a platform specific
# subclass when validating (e.g. on windows Path('...') -> WindowsPath('...') )
from pathlib import PureWindowsPath as WindowsPath
from pathlib import PurePosixPath as PosixPath
from pathlib import Path


def test_schema_definition():
    @c
    class C(Schema):
        a: int = 1  # desctiption


def test_schema_without_doc():
    @c
    class C(Schema):
        a: int = 1


# TODO: sane exception for this scenario
# def test_schema_without_default():
#     @c
#     class C(Schema):
#         a: int

def test_schema_without_type():
    @c
    class C(Schema):
        a = 1

    assert c.a == 1


class TestSchemaNoType(TestCase):
    default = 42

    def setUp(self) -> None:
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


class TestSchema(TestCase):
    defaults = {
        '_int': [42, int],
        '_str': ['oh hi', str],
        '_posix_path': [PosixPath('/tmp'), PosixPath],
        '_win_path': [WindowsPath('/tmp'), WindowsPath],
    }

    def setUp(self) -> None:
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


def test_foo(capfd):
    sys.argv = ['test', 'x']

    class C(Schema):
        a = 1

    @c
    class Cli:
        def x(self):
            """docstring"""
            print(c.a)

    assert (c.a == 1)
    # captured = capfd.readouterr()
    # assert captured.out == 'oh hi\nfoo\nbar'


class TestConfigurable(TestCase):

    def setUp(self) -> None:
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


class TestConfigFromCwd(TestCase):
    test_cfg = Path.cwd() / 'foo.cfg'

    def setUp(self) -> None:
        with open(self.test_cfg, 'w', encoding='UTF-8') as wf:
            wf.write('[Default]\nbar = 42')
        sys.argv = ['test', '--cwd', os.fspath(self.test_cfg.parent)]

        class C(Schema):
            bar: int = 0

    def tearDown(self) -> None:
        self.test_cfg.unlink()

    def test_configfile(self):
        @c
        class Cli:
            def x(self):
                pass

        assert c.bar == 42


class TestConfigFromCwdPath(TestCase):
    test_cfg = Path.cwd() / 'foo.cfg'

    def setUp(self) -> None:
        with open(self.test_cfg, 'w', encoding='UTF-8') as wf:
            wf.write('[Default]\nbar = .')
        sys.argv = ['test', '--cwd', os.fspath(self.test_cfg.parent)]

        class C(Schema):
            bar: WindowsPath = ''

    def tearDown(self) -> None:
        self.test_cfg.unlink()

    def test_configfile(self):
        @c
        class Cli:
            def x(self):
                pass

        assert str(c.bar) == '.'
        assert type(c.bar) == WindowsPath
