"""Tests for clima's preconfigured logging setup."""
import logging
import os
import tempfile
from unittest import TestCase

from clima.logging import setup_logging


class TestSetupLogging(TestCase):
    def setUp(self):
        self.root = logging.getLogger()
        self._original_handlers = self.root.handlers[:]
        self._original_level = self.root.level

    def tearDown(self):
        self.root.handlers = self._original_handlers
        self.root.level = self._original_level
        # Clean up any log files
        for f in ['test.debug.log']:
            if os.path.exists(f):
                os.remove(f)

    def test_default_setup_stdout_at_info(self):
        setup_logging(log_file='test.debug.log')
        stream_handlers = [
            h for h in self.root.handlers
            if isinstance(h, logging.StreamHandler)
            and not isinstance(h, logging.FileHandler)
        ]
        self.assertTrue(len(stream_handlers) >= 1)
        self.assertEqual(stream_handlers[-1].level, logging.INFO)

    def test_default_setup_file_at_debug(self):
        setup_logging(log_file='test.debug.log')
        file_handlers = [
            h for h in self.root.handlers
            if isinstance(h, logging.FileHandler)
        ]
        self.assertTrue(len(file_handlers) >= 1)
        self.assertEqual(file_handlers[-1].level, logging.DEBUG)

    def test_verbose_sets_stdout_to_debug(self):
        setup_logging(verbose=True, log_file='test.debug.log')
        stream_handlers = [
            h for h in self.root.handlers
            if isinstance(h, logging.StreamHandler)
            and not isinstance(h, logging.FileHandler)
        ]
        self.assertEqual(stream_handlers[-1].level, logging.DEBUG)

    def test_quiet_sets_stdout_to_warning(self):
        setup_logging(quiet=True, log_file='test.debug.log')
        stream_handlers = [
            h for h in self.root.handlers
            if isinstance(h, logging.StreamHandler)
            and not isinstance(h, logging.FileHandler)
        ]
        self.assertEqual(stream_handlers[-1].level, logging.WARNING)
