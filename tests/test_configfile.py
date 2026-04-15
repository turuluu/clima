import tempfile
from textwrap import dedent
from unittest.mock import patch
from io import StringIO

import pytest

from pathlib import Path
import os
import sys

from clima.configfile import find_cfg


class TestFindCfgSectionFilter:
    """find_cfg should skip .cfg/.conf files that don't contain the package's section."""

    def test_skips_files_without_relevant_section(self, tmp_path):
        # alphabetically first .cfg has no relevant section
        (tmp_path / 'a_unrelated.cfg').write_text('[OtherTool]\nfoo = bar\n')
        # second .cfg has the package section
        (tmp_path / 'b_app.cfg').write_text('[mypkg]\nfoo = bar\n')

        result = find_cfg(tmp_path, package_name='mypkg')

        assert result is not None
        assert result.name == 'b_app.cfg'

    def test_clima_section_also_accepted(self, tmp_path):
        (tmp_path / 'a_unrelated.cfg').write_text('[OtherTool]\nfoo = bar\n')
        (tmp_path / 'b_clima.cfg').write_text('[Clima]\nfoo = bar\n')

        result = find_cfg(tmp_path, package_name='mypkg')

        assert result is not None
        assert result.name == 'b_clima.cfg'

    def test_returns_none_when_no_relevant_file(self, tmp_path):
        (tmp_path / 'unrelated.cfg').write_text('[OtherTool]\nfoo = bar\n')

        result = find_cfg(tmp_path, package_name='mypkg')

        assert result is None

    def test_backwards_compatible_without_package_name(self, tmp_path):
        # When called without package_name (legacy callers), do not filter
        (tmp_path / 'a.cfg').write_text('[OtherTool]\nfoo = bar\n')

        result = find_cfg(tmp_path)

        assert result is not None
        assert result.name == 'a.cfg'


class TestFindCfgRecursion:
    """find_cfg should walk up parents, but only while inside a Python module,
    and at most `level` hops."""

    def test_walks_up_when_start_dir_is_module(self, tmp_path):
        # parent has the config. `is_in_module(child)` checks whether
        # child.parent (== tmp_path) has __init__.py — so the package root
        # must also look like a module for the hop to happen.
        (tmp_path / '__init__.py').write_text('')
        (tmp_path / 'app.cfg').write_text('[Clima]\nfoo = bar\n')
        child = tmp_path / 'pkg'
        child.mkdir()
        (child / '__init__.py').write_text('')

        result = find_cfg(child)

        assert result is not None
        assert result.name == 'app.cfg'

    def test_does_not_walk_up_when_start_dir_not_module(self, tmp_path):
        # parent has config, child is NOT a module (no __init__.py)
        (tmp_path / 'app.cfg').write_text('[Clima]\nfoo = bar\n')
        child = tmp_path / 'plain'
        child.mkdir()

        result = find_cfg(child)

        assert result is None

    def test_respects_level_limit(self, tmp_path):
        # Grandparent has the config; every ancestor is itself a module so
        # the `is_in_module` gate keeps letting us hop.
        (tmp_path / '__init__.py').write_text('')
        (tmp_path / 'app.cfg').write_text('[Clima]\nfoo = bar\n')
        mid = tmp_path / 'mid'
        mid.mkdir()
        (mid / '__init__.py').write_text('')
        leaf = mid / 'leaf'
        leaf.mkdir()
        (leaf / '__init__.py').write_text('')

        # level=1: leaf -> mid (no config there) -> level now 0, stop.
        assert find_cfg(leaf, level=1) is None
        # level=2 (default): leaf -> mid -> tmp_path. Found.
        assert find_cfg(leaf).name == 'app.cfg'

# Using Pure versions of platform explicit paths allows testing cross platform code
# Can't use just Path, because that will get rendered to a platform specific
# subclass when validating (e.g. on windows Path('...') -> WindowsPath('...') )
from pathlib import PureWindowsPath as WindowsPath


# from tests import SysArgvRestore


class ConfigFileTestBase:
    pkg_name = 'test_package'

    @pytest.fixture
    def base_setup(self, monkeypatch):
        from clima import c, Schema

        Schema._package_name = self.pkg_name
        self.c = c
        self.Schema = Schema
        # self.save_sysargv()

        # Create temp file and directory
        self.tmp_dir = tempfile.mkdtemp()
        self.tmp_cfg = Path(self.tmp_dir) / 'foo.cfg'
        # self.tmp_cfg = Path.cwd() / 'foo.cfg'

        # Each subclass will define its own config content and Schema
        self._setup_schema()
        self._write_config()
        # self._setup_argv()

        # def tearDown(self) -> None:
        # self.stdin_patcher.stop()

        yield

        # Clean up temp files
        self.c._clear()
        self.tmp_cfg.unlink()
        os.rmdir(self.tmp_dir)
        # self.restore_sysargv()

    def _write_config(self):
        """Override this in subclasses to write specific config content"""
        raise NotImplementedError

    def _setup_schema(self):
        """Override this in subclasses to define specific Schema"""
        raise NotImplementedError

    def _setup_cli(self):
        """Override this in subclasses to define specific Schema"""
        raise NotImplementedError

    def _setup_argv(self):
        """Override this in subclasses to define specific argv"""
        raise NotImplementedError


# class TestConfigFromTmpFile(ConfigFileTestBase):
#     def _setup_schema(self):
#         class C(self.Schema):
#             bar: int = 0  # Default value should be overridden by config file
#             cwd: Path = os.fspath(self.tmp_dir)  # Default value should be overridden by --cwd
#
#     def _write_config(self):
#         self.tmp_cfg.write_text(f'[{self.pkg_name}]\nbar = 42')
#
#     @pytest.fixture
#     def setup_stdin(self, monkeypatch):
#         stdin_text = f'test x --cwd {str(os.fspath(self.tmp_dir))}'
#         monkeypatch.setattr('sys.stdin.isatty', lambda: False)
#         monkeypatch.setattr('sys.stdin', StringIO(stdin_text))
#
#         yield
#
#     def test_configfile(self):
#         @self.c
#         class Cli:
#             def x(self):
#                 pass  #
#
#         assert self.c.bar == 42, f'Failed loading config file - c.bar == {self.c.bar}'

# class TestConfigGivenCwd(ConfigFileTestBase):
#     def _setup_schema(self):
#         class C(self.Schema):
#             bar: int = 0  # Default value should be overridden by config file
#             cwd: Path = self.tmp_dir  # Default value should be used
#
#     def _write_config(self):
#         self.tmp_cfg.write_text(f'[{self.pkg_name}]\nbar = 42')
#
#     def _setup_argv(self):
#         sys.argv = ['test', 'x']
#
#     def test_configfile(self):
#         @self.c
#         class Cli:
#             def x(self):
#                 pass
#
#         assert self.c.bar == 42, f'Not loading from cfg file - c.bar == {self.c.bar}'
#
    # def test_cwd(self):
    #     self.c = Configurable()
    #     class C(self.Schema):
    #         bar: int = 0  # Default value should be overridden by config file
    #         cwd: Path = self.tmp_dir  # Default value should be used

    #     self.tmp_cfg.write_text(f'[{self.pkg_name}]\nbar = 42')

    #     sys.argv = ['test', 'x']

    #     @self.c
    #     class Cli:
    #         def x(self):
    #             pass

    #     assert self.c.bar == 42, f'Not loading from cfg file - c.bar == {self.c.bar}'

# class TestConfigFromCwdPath(TestCase, SysArgvRestore):
#     test_cfg = Path.cwd() / 'foo.cfg'

#     def setUp(self) -> None:
#         from clima import c, Schema
#         self.c = c
#         self.save_sysargv()
#         with open(self.test_cfg, 'w', encoding='UTF-8') as wf:
#             wf.write('[Clima]\nbar = .')
#         sys.argv = ['test', 'x', '--cwd', os.fspath(self.test_cfg.parent)]

#         class C(Schema):
#             bar: WindowsPath = ''

#     def tearDown(self) -> None:
#         self.test_cfg.unlink()
#         self.restore_sysargv()

#     def test_configfile(self):
#         @self.c
#         class Cli:
#             def x(self):
#                 pass

#         assert str(self.c.bar) == '.'
#         assert type(self.c.bar) == WindowsPath


# class TestBooleansInConfig(TestCase, SysArgvRestore):
#     test_cfg = 'foo.cfg'
#     wf = tempfile.NamedTemporaryFile()

#     def setUp(self) -> None:
#         from clima import c, Schema
#         self.c = c
#         self.save_sysargv()
#         self.wf.close()
#         self.wf = tempfile.NamedTemporaryFile(mode='w', encoding='UTF-8')
#         conf = """
#         [Clima]
#         #foo = [1, 2, 3]
#         bar = true
#         """
#         self.wf.write(dedent(conf))
#         sys.argv = ['test', 'x', '--cwd', os.fspath(tempfile.gettempdir())]

#         class C(Schema):
#             bar: bool = False

#     def tearDown(self) -> None:
#         self.wf.close()
#         self.restore_sysargv()

#     def test_boolean_in_config(self):
#         @self.c
#         class Cli:
#             def x(self):
#                 pass

#         assert not self.c.bar
#         assert type(self.c.bar) == bool

#     # def test_list_in_config(self):
#     #     @self.c
#     #     class Cli:
#     #         def x(self): pass
#     #
#     #     assert self.c.foo[0] == 1
#     #     assert self.c.foo[0] == 2
#     #     assert self.c.foo[0] == 3
#     #     assert type(self.c.foo) == list
