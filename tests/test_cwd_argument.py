"""Test that cwd argument is respected during config file discovery."""
import tempfile
import shutil
from pathlib import Path
import sys
import os

import pytest

from clima import c, Schema


def setup_test_dirs():
    """Helper to create test directories with config files."""
    wrong_dir = tempfile.mkdtemp()
    correct_dir = tempfile.mkdtemp()

    # Write a config file in the WRONG directory (should not be loaded)
    wrong_cfg = Path(wrong_dir) / 'test.cfg'
    wrong_cfg.write_text('[test_cwd_arg]\nvalue = 99\n')

    # Write a config file in the CORRECT directory (should be loaded)
    correct_cfg = Path(correct_dir) / 'test.cfg'
    correct_cfg.write_text('[test_cwd_arg]\nvalue = 42\n')

    return wrong_dir, correct_dir


def cleanup_test_dirs(wrong_dir, correct_dir):
    """Helper to clean up test directories."""
    shutil.rmtree(wrong_dir, ignore_errors=True)
    shutil.rmtree(correct_dir, ignore_errors=True)


class TestCwdArgumentRespected:
    """Test that --cwd argument is respected during config file discovery."""

    def test_cwd_cli_argument_respected(self, monkeypatch):
        """Test that config file from --cwd directory is loaded, not current dir."""
        wrong_dir, correct_dir = setup_test_dirs()
        old_cwd = os.getcwd()

        try:
            # Change to wrong directory to ensure --cwd is needed
            os.chdir(wrong_dir)

            # Set up argv to pass --cwd with the correct directory
            monkeypatch.setattr(
                'sys.argv',
                ['test', 'cmd', '--cwd', correct_dir]
            )

            Schema._package_name = 'test_cwd_arg'

            class MySchema(Schema):
                value: int = 0
                cwd: Path = ''

            @c
            class Cli:
                def cmd(self):
                    pass

            # The config should be loaded from correct_dir (value = 42)
            # not from wrong_dir (value = 99)
            assert c.value == 42, f"Expected value=42 from correct dir, got {c.value}"
        finally:
            os.chdir(old_cwd)
            cleanup_test_dirs(wrong_dir, correct_dir)
            c._clear()

    def test_cwd_with_relative_path(self, monkeypatch):
        """Test that relative --cwd paths are resolved correctly."""
        wrong_dir, correct_dir = setup_test_dirs()
        old_cwd = os.getcwd()

        try:
            # Create a subdirectory and put a config there
            subdir = Path(correct_dir) / 'subdir'
            subdir.mkdir()
            cfg = subdir / 'test.cfg'
            cfg.write_text('[test_cwd_arg]\nvalue = 77\n')

            # Change to correct_dir, then use relative path to subdir
            os.chdir(correct_dir)

            monkeypatch.setattr(
                'sys.argv',
                ['test', 'cmd', '--cwd', './subdir']
            )

            Schema._package_name = 'test_cwd_arg'

            class MySchema(Schema):
                value: int = 0
                cwd: Path = ''

            @c
            class Cli:
                def cmd(self):
                    pass

            # Should load from subdir (value = 77)
            assert c.value == 77, f"Expected value=77 from subdir, got {c.value}"
        finally:
            os.chdir(old_cwd)
            cleanup_test_dirs(wrong_dir, correct_dir)
            c._clear()
