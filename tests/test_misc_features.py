from unittest import TestCase
import sys

from clima import c, Schema

from tests import SysArgvRestore


class TestSimple(TestCase, SysArgvRestore):
    def test_version_print(self):
        sys.argv = ['--version']

        class C(Schema):
            pass

        @c
        class D:
            def x(self):
                pass
