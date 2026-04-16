"""Test handling of string arguments containing spaces."""
import sys
import pytest
from clima import c, Schema


class TestStringWithSpaces:
    """Test that CLI properly handles string arguments with spaces."""

    def test_string_argument_split_by_shell(self, monkeypatch):
        """Test that a string argument split by the shell is handled correctly.

        When a user types: script cmd hello world
        The shell passes it as: ['script', 'cmd', 'hello', 'world']

        This tests what happens in that case.
        """
        monkeypatch.setattr(
            'sys.argv',
            ['test', 'cmd', 'hello', 'world']  # Argv as the shell would split it
        )

        Schema._package_name = 'test_string_spaces'

        class MySchema(Schema):
            msg: str = 'default'
            other: str = 'other_default'

        @c
        class Cli:
            def cmd(self):
                pass

        # Current behavior: the argv rewriting treats 'hello' as first arg, 'world' as second arg
        # So msg='hello' and other='world'
        assert c.msg == 'hello', f"Expected msg='hello', got '{c.msg}'"
        assert c.other == 'world', f"Expected other='world', got '{c.other}'"

        c._clear()

    def test_multiple_string_arguments_with_spaces(self, monkeypatch):
        """Test multiple string arguments with spaces."""
        monkeypatch.setattr(
            'sys.argv',
            ['test', 'cmd', 'hello world', 'foo bar']
        )

        Schema._package_name = 'test_string_spaces'

        class MySchema(Schema):
            arg1: str = 'default1'
            arg2: str = 'default2'

        @c
        class Cli:
            def cmd(self):
                pass

        # Both strings with spaces should be preserved
        assert c.arg1 == 'hello world', f"Expected 'hello world', got '{c.arg1}'"
        assert c.arg2 == 'foo bar', f"Expected 'foo bar', got '{c.arg2}'"

        c._clear()
