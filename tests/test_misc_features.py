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

    def test_start_is_file_normalized_to_parent(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / 'pyproject.toml').write_text(
                '[tool.poetry]\nname = "foo"\nversion = "4.5.6"\n'
            )
            script = root / 'some_script.py'
            script.write_text('# marker\n')
            version = parse_version_from_pyproject_toml(start=script)
            self.assertEqual(version, '4.5.6')

    def test_returns_none_when_pyproject_has_no_poetry_section(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / 'pyproject.toml').write_text(
                '[build-system]\nrequires = ["setuptools"]\n'
            )
            self.assertIsNone(parse_version_from_pyproject_toml(start=root))

    def test_walk_skips_malformed_pyproject(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / 'pyproject.toml').write_text(
                '[tool.poetry]\nname = "outer"\nversion = "9.9.9"\n'
            )
            nested = root / 'pkg' / 'sub'
            nested.mkdir(parents=True)
            # Malformed TOML in nested dir — should be skipped during walk.
            (nested.parent / 'pyproject.toml').write_text(
                'this is = not valid [ toml at all ]]]\n'
            )
            version = parse_version_from_pyproject_toml(start=nested)
            self.assertEqual(version, '9.9.9')
