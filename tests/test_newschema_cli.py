"""Tests for the new Schema.cli decorator API (@C.cli instead of @c)."""
import sys
from unittest import TestCase

from tests import SysArgvRestore


class TestNewSchemaCli(TestCase, SysArgvRestore):
    """Test that @C.cli works as a drop-in replacement for @c."""

    def tearDown(self):
        self.c._clear()
        super().tearDown()

    def test_defaults(self):
        from clima import c, Schema
        self.c = c
        sys.argv = ['test', 'x']

        class C(Schema):
            a: str = 'hello'
            b: int = 42

        @C.cli
        class Cli:
            def x(self):
                """docstring"""
                pass

        assert c.a == 'hello', 'Schema defaults should be accessible via c'
        assert c.b == 42, 'Schema defaults should be accessible via c'

    def test_cli_args_override(self):
        from clima import c, Schema
        self.c = c
        sys.argv = ['test', 'x', '--a', 'world', '--b', '99']

        class C(Schema):
            a: str = 'hello'
            b: int = 42

        @C.cli
        class Cli:
            def x(self):
                """docstring"""
                pass

        assert c.a == 'world', 'CLI args should override defaults'
        assert c.b == 99, 'CLI args should override defaults'

    def test_positional_args(self):
        from clima import c, Schema
        self.c = c
        sys.argv = ['test', 'x', 'world', '99']

        class C(Schema):
            a: str = 'hello'
            b: int = 42

        @C.cli
        class Cli:
            def x(self):
                """docstring"""
                pass

        assert c.a == 'world', 'Positional args should work with @C.cli'
        assert c.b == 99, 'Positional args should work with @C.cli'


class TestNewSchemaCliPostInit(TestCase, SysArgvRestore):
    """Test that @C.cli works with post_init hook."""

    def tearDown(self):
        self.c._clear()
        super().tearDown()

    def test_post_init(self):
        from clima import c, Schema
        self.c = c
        sys.argv = ['test', 'x']

        class C(Schema):
            a: int = 1

            def post_init(self, *args):
                self.a = 2

        @C.cli
        class Cli:
            def x(self):
                """docstring"""
                pass

        assert c.a == 2, 'post_init should mutate values when using @C.cli'


class TestSchemaClassAttrsWriteback(TestCase, SysArgvRestore):
    """Test that resolved values are written back onto Schema class attributes."""

    def tearDown(self):
        self.c._clear()
        super().tearDown()

    def test_schema_attrs_reflect_resolved_values(self):
        from clima import c, Schema
        self.c = c
        sys.argv = ['test', 'x', '--name', 'override']

        class C(Schema):
            name: str = 'default'

        @C.cli
        class Cli:
            def x(self):
                """docstring"""
                pass

        assert C.name == 'override', f'Schema class attr should reflect resolved CLI arg, got {C.name!r}'

    def test_schema_attrs_reflect_post_init(self):
        from clima import c, Schema
        self.c = c
        sys.argv = ['test', 'x']

        class C(Schema):
            a: int = 1

            def post_init(self, *args):
                self.a = 2

        @C.cli
        class Cli:
            def x(self):
                """docstring"""
                pass

        assert C.a == 2, f'Schema class attr should reflect post_init mutation, got {C.a!r}'


class TestSchemaRequiredParameterGuard(TestCase, SysArgvRestore):
    """Test that accessing None-defaulting Schema fields raises RequiredParameterException."""

    def tearDown(self):
        self.c._clear()
        super().tearDown()

    def test_none_field_raises(self):
        from clima import c, Schema
        from clima.core import RequiredParameterException
        self.c = c

        class C(Schema):
            name: str = None

        with self.assertRaises(RequiredParameterException):
            _ = C.name

    def test_non_none_field_works(self):
        from clima import c, Schema
        self.c = c

        class C(Schema):
            a: int = 42

        assert C.a == 42, 'Non-None fields should be accessible normally'

    def test_internal_attrs_work(self):
        from clima import c, Schema
        self.c = c

        class C(Schema):
            a: int = 1

        # These should not raise
        assert hasattr(C, 'cli')
        assert hasattr(C, '_fields')
