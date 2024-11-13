import tempfile
from textwrap import dedent
from unittest import TestCase
from pathlib import Path
import os
import sys

# Using Pure versions of platform explicit paths allows testing cross platform code
# Can't use just Path, because that will get rendered to a platform specific
# subclass when validating (e.g. on windows Path('...') -> WindowsPath('...') )
from pathlib import PureWindowsPath as WindowsPath

from tests import SysArgvRestore


class TestConfigFromWorkingDir(TestCase, SysArgvRestore):
    test_cfg = Path.cwd() / 'foo.cfg'

    def setUp(self) -> None:
        from clima import c, Schema
        self.c = c
        self.save_sysargv()
        with open(self.test_cfg, 'w', encoding='UTF-8') as wf:
            wf.write('[Clima]\nbar = 42')
        sys.argv = ['test', 'x']

        class C(Schema):
            bar: int = 0

    def tearDown(self) -> None:
        self.test_cfg.unlink()
        self.restore_sysargv()

    def test_configfile(self):
        @self.c
        class Cli:
            def x(self):
                pass

        assert self.c.bar == 42, f'Failed loading config file - c.bar == {self.c.bar}'


class TestConfigFromCwd(TestCase, SysArgvRestore):
    test_cfg = Path.cwd() / 'foo.cfg'

    def setUp(self) -> None:
        from clima import c, Schema
        self.c = c
        self.save_sysargv()
        with open(self.test_cfg, 'w', encoding='UTF-8') as wf:
            wf.write('[Clima]\nbar = 42')
        sys.argv = ['test', 'x', '--cwd', os.fspath(self.test_cfg.parent)]

        class C(Schema):
            bar: int = 0
            cwd: Path = ''

    def tearDown(self) -> None:
        self.test_cfg.unlink()
        self.restore_sysargv()

    def test_configfile(self):
        @self.c
        class Cli:
            def x(self):
                pass

        assert self.c.bar == 42, f'Not loading from cfg file - c.bar == {self.c.bar}'


class TestConfigFromCwdPath(TestCase, SysArgvRestore):
    test_cfg = Path.cwd() / 'foo.cfg'

    def setUp(self) -> None:
        from clima import c, Schema
        self.c = c
        self.save_sysargv()
        with open(self.test_cfg, 'w', encoding='UTF-8') as wf:
            wf.write('[Clima]\nbar = .')
        sys.argv = ['test', 'x', '--cwd', os.fspath(self.test_cfg.parent)]

        class C(Schema):
            bar: WindowsPath = ''

    def tearDown(self) -> None:
        self.test_cfg.unlink()
        self.restore_sysargv()

    def test_configfile(self):
        @self.c
        class Cli:
            def x(self):
                pass

        assert str(self.c.bar) == '.'
        assert type(self.c.bar) == WindowsPath


class TestBooleansInConfig(TestCase, SysArgvRestore):
    test_cfg = 'foo.cfg'
    wf = tempfile.NamedTemporaryFile()

    def setUp(self) -> None:
        from clima import c, Schema
        self.c = c
        self.save_sysargv()
        self.wf.close()
        self.wf = tempfile.NamedTemporaryFile(mode='w', encoding='UTF-8')
        conf = """
        [Clima]
        #foo = [1, 2, 3]
        bar = true
        """
        self.wf.write(dedent(conf))
        sys.argv = ['test', 'x', '--cwd', os.fspath(tempfile.gettempdir())]

        class C(Schema):
            bar: bool = False

    def tearDown(self) -> None:
        self.wf.close()
        self.restore_sysargv()

    def test_boolean_in_config(self):
        @self.c
        class Cli:
            def x(self):
                pass

        assert not self.c.bar
        assert type(self.c.bar) == bool

    # def test_list_in_config(self):
    #     @self.c
    #     class Cli:
    #         def x(self): pass
    #
    #     assert self.c.foo[0] == 1
    #     assert self.c.foo[0] == 2
    #     assert self.c.foo[0] == 3
    #     assert type(self.c.foo) == list
