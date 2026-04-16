"""Tests for warning-on-unknown CLI parameters.

Covers the pure helper `unknown_cli_flags` and the stderr warning wired
through `prepare()`.
"""
import sys
from unittest import TestCase

from clima import c, Schema
from clima.core import unknown_cli_flags

from tests import SysArgvRestore


class TestUnknownCliFlags(TestCase):
    def test_all_known_returns_empty(self):
        self.assertEqual(
            unknown_cli_flags(['--foo', '1', '--bar', '2'], {'foo', 'bar'}),
            [],
        )

    def test_returns_single_unknown(self):
        self.assertEqual(
            unknown_cli_flags(['--foo', '1', '--nope', 'x'], {'foo'}),
            ['nope'],
        )

    def test_handles_equals_form(self):
        self.assertEqual(
            unknown_cli_flags(['--nope=x', '--foo=1'], {'foo'}),
            ['nope'],
        )

    def test_ignores_help_and_short_flags(self):
        self.assertEqual(
            unknown_cli_flags(['--help', '-h', '-v'], set()),
            [],
        )

    def test_stops_at_double_dash_sentinel(self):
        self.assertEqual(
            unknown_cli_flags(['--foo', '1', '--', '--nope'], {'foo'}),
            [],
        )

    def test_returns_sorted_unique(self):
        self.assertEqual(
            unknown_cli_flags(['--zeta', '--alpha', '--zeta'], set()),
            ['alpha', 'zeta'],
        )


class TestPrepareWarnsOnUnknown(TestCase, SysArgvRestore):
    def setUp(self):
        self.save_sysargv()

    def tearDown(self):
        self.restore_sysargv()
        c._clear()

    def test_warns_when_unknown_flag_present(self):
        from io import StringIO
        buf = StringIO()
        real_stderr = sys.stderr
        sys.stderr = buf
        try:
            sys.argv = ['prog', 'run', '--nope', 'x', 'version']

            class S(Schema):
                foo: str = 'default'

            @c
            class Cli:
                def run(self):
                    pass
        finally:
            sys.stderr = real_stderr

        self.assertIn('nope', buf.getvalue())
        self.assertIn('unknown parameter', buf.getvalue())

    def test_silent_when_all_known(self):
        from io import StringIO
        buf = StringIO()
        real_stderr = sys.stderr
        sys.stderr = buf
        try:
            sys.argv = ['prog', 'run', '--foo', 'x', 'version']

            class S(Schema):
                foo: str = 'default'

            @c
            class Cli:
                def run(self):
                    pass
        finally:
            sys.stderr = real_stderr

        self.assertEqual(buf.getvalue(), '')

    def test_help_excludes_unknown_parameters(self):
        from io import StringIO
        from clima.fire.core import FireExit

        stdout_buf = StringIO()
        stderr_buf = StringIO()
        real_stdout = sys.stdout
        real_stderr = sys.stderr
        sys.stdout = stdout_buf
        sys.stderr = stderr_buf
        try:
            sys.argv = ['prog', 'foo', '--undefined-param', 'test', '--help']

            class S(Schema):
                a: str = 'default'

            @c
            class Cli:
                def foo(self):
                    pass
        except FireExit:
            pass  # Expected when --help is used
        finally:
            sys.stdout = real_stdout
            sys.stderr = real_stderr

        help_output = stderr_buf.getvalue()
        # The usage line should NOT contain the undefined parameter
        usage_line = help_output.split('\n')[0]
        self.assertNotIn('--undefined-param', usage_line)
        # The warning should still be present
        self.assertIn('unknown parameter', stderr_buf.getvalue())
