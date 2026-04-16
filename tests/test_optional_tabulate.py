"""Tests for optional tabulate dependency."""
import sys
from unittest import TestCase, mock


class TestSuppressTracebackWithoutTabulate(TestCase):
    def test_suppress_traceback_works_without_tabulate(self):
        """suppress_traceback should not crash when tabulate is not installed."""
        with mock.patch.dict(sys.modules, {'tabulate': None}):
            # Force re-import of utils to trigger the import path
            import importlib
            import clima.utils
            importlib.reload(clima.utils)

            with self.assertRaises(SystemExit):
                with clima.utils.suppress_traceback():
                    raise ValueError("test error")

        # Reload with tabulate available again
        import importlib
        importlib.reload(clima.utils)

    def test_suppress_traceback_uses_tabulate_when_available(self):
        """suppress_traceback should use tabulate when installed."""
        import clima.utils
        self.assertTrue(clima.utils._HAS_TABULATE)
