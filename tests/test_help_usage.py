"""Tests for help/usage output when CLI has subcommands."""
import sys
from io import StringIO
from unittest import TestCase

from clima import c, Schema
from clima.fire.core import FireExit

from tests import SysArgvRestore


class TestUsageWithSubcommands(TestCase, SysArgvRestore):
    def setUp(self):
        self.save_sysargv()

    def tearDown(self):
        self.restore_sysargv()
        c._clear()

    def _capture_help(self, argv):
        """Run @c decoration with given argv and return captured stderr."""
        stderr_buf = StringIO()
        real_stderr = sys.stderr
        # Also capture stdout to suppress the print(params) debug line
        stdout_buf = StringIO()
        real_stdout = sys.stdout
        sys.stderr = stderr_buf
        sys.stdout = stdout_buf
        try:
            sys.argv = argv

            class S(Schema):
                a: str = 'A'

            @c
            class Cli:
                def foo(self):
                    pass

                def bar(self):
                    pass
        except FireExit:
            pass
        finally:
            sys.stderr = real_stderr
            sys.stdout = real_stdout
        return stderr_buf.getvalue()

    def test_root_help_shows_subcommand_in_usage(self):
        output = self._capture_help(['prog', '--help'])
        lines = output.strip().split('\n')
        usage_line = next(
            (l for l in lines if l.strip().startswith('Usage:')),
            '',
        )
        self.assertIn('<subcommand>', usage_line)
        self.assertNotIn('[ARGS]', usage_line)

    def test_subcommand_help_unchanged(self):
        output = self._capture_help(['prog', 'foo', '--help'])
        lines = output.strip().split('\n')
        usage_line = next(
            (l for l in lines if l.strip().startswith('Usage:')),
            '',
        )
        self.assertNotIn('<subcommand>', usage_line)
        self.assertIn('foo', usage_line)

    def test_root_help_shows_class_docstring(self):
        stderr_buf = StringIO()
        stdout_buf = StringIO()
        real_stderr = sys.stderr
        real_stdout = sys.stdout
        sys.stderr = stderr_buf
        sys.stdout = stdout_buf
        try:
            sys.argv = ['prog', '--help']

            class S(Schema):
                a: str = 'A'

            @c
            class Cli:
                """My awesome tool for doing things."""
                def foo(self):
                    pass

                def bar(self):
                    pass
        except FireExit:
            pass
        finally:
            sys.stderr = real_stderr
            sys.stdout = real_stdout

        output = stderr_buf.getvalue()
        self.assertIn('My awesome tool for doing things', output)

    def test_single_method_help_shows_class_docstring(self):
        stderr_buf = StringIO()
        stdout_buf = StringIO()
        real_stderr = sys.stderr
        real_stdout = sys.stdout
        sys.stderr = stderr_buf
        sys.stdout = stdout_buf
        try:
            sys.argv = ['prog', '--help']

            class S(Schema):
                a: str = 'A'

            @c
            class Cli:
                """Single method tool description."""
                def run(self):
                    pass
        except FireExit:
            pass
        finally:
            sys.stderr = real_stderr
            sys.stdout = real_stdout

        output = stderr_buf.getvalue()
        self.assertIn('Single method tool description', output)

    def test_error_usage_has_no_dash_separator(self):
        output = self._capture_help(['prog', 'badcmd'])
        usage_lines = [
            l for l in output.split('\n')
            if 'Usage:' in l or 'prog' in l
        ]
        for line in usage_lines:
            self.assertNotRegex(line, r'\bprog\b\s+-\s')
