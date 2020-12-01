from unittest import TestCase
from pathlib import Path
import os
import sys

# Using Pure versions of paths allows testing cross platform code
# Can't use just Path, because that will get rendered to a platform specific
# subclass when validating (e.g. on windows Path('...') -> WindowsPath('...') )
from pathlib import PureWindowsPath as WindowsPath

from clima import c, Schema

from tests import SysArgvRestore


class TestConfigFromWorkingDir(TestCase, SysArgvRestore):
    test_cfg = Path.cwd() / 'foo.cfg'

    def setUp(self) -> None:
        self.save_sysargv()
        with open(self.test_cfg, 'w', encoding='UTF-8') as wf:
            wf.write('[Default]\nbar = 42')
        sys.argv = ['test', 'x']

        class C(Schema):
            bar: int = 0

    def tearDown(self) -> None:
        self.test_cfg.unlink()
        self.restore_sysargv()

    def test_configfile(self):
        @c
        class Cli:
            def x(self):
                pass

        assert c.bar == 42


class TestConfigFromCwd(TestCase, SysArgvRestore):
    test_cfg = Path.cwd() / 'foo.cfg'

    def setUp(self) -> None:
        self.save_sysargv()
        with open(self.test_cfg, 'w', encoding='UTF-8') as wf:
            wf.write('[Default]\nbar = 42')
        sys.argv = ['test', 'x', '--cwd', os.fspath(self.test_cfg.parent)]

        class C(Schema):
            bar: int = 0

    def tearDown(self) -> None:
        self.test_cfg.unlink()
        self.restore_sysargv()

    def test_configfile(self):
        @c
        class Cli:
            def x(self):
                pass

        assert c.bar == 42


class TestConfigFromCwdPath(TestCase, SysArgvRestore):
    test_cfg = Path.cwd() / 'foo.cfg'

    def setUp(self) -> None:
        self.save_sysargv()
        with open(self.test_cfg, 'w', encoding='UTF-8') as wf:
            wf.write('[Default]\nbar = .')
        sys.argv = ['test', 'x', '--cwd', os.fspath(self.test_cfg.parent)]

        class C(Schema):
            bar: WindowsPath = ''

    def tearDown(self) -> None:
        self.test_cfg.unlink()
        self.restore_sysargv()

    def test_configfile(self):
        @c
        class Cli:
            def x(self):
                pass

        assert str(c.bar) == '.'
        assert type(c.bar) == WindowsPath
