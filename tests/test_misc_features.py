from unittest import TestCase
import sys
from pathlib import Path

from clima import c, Schema
from clima.schema import parse_version_from_pyproject_toml

from tests import SysArgvRestore


class TestSimple(TestCase, SysArgvRestore):
    def test_version_print(self):
        sys.argv = ['version']

        class C(Schema):
            pass

        @c
        class D:
            def x(self):
                pass


class TestPyprojectLookup(TestCase):
    def test_walks_up_from_start(self, tmp_path_factory=None):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / 'pyproject.toml').write_text(
                '[tool.poetry]\nname = "foo"\nversion = "1.2.3"\n'
            )
            nested = root / 'pkg' / 'sub'
            nested.mkdir(parents=True)
            version = parse_version_from_pyproject_toml(start=nested)
            self.assertEqual(version, '1.2.3')

    def test_returns_none_when_no_pyproject(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            self.assertIsNone(parse_version_from_pyproject_toml(start=Path(td)))
