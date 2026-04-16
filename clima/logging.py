"""Preconfigured logging setup for clima CLIs.

Provides INFO on stdout and DEBUG in a log file, adjustable via --verbose/--quiet.
"""
import logging
import sys


def setup_logging(verbose=False, quiet=False, log_file=None):
    """Configure the root logger with stdout and optional file handlers.

    Args:
        verbose: If True, stdout handler shows DEBUG+.
        quiet: If True, stdout handler shows WARNING+ only.
        log_file: Path to debug log file. If None, file logging is skipped.
    """
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    fmt = logging.Formatter('%(levelname)s %(name)s: %(message)s')

    stdout_level = logging.INFO
    if verbose:
        stdout_level = logging.DEBUG
    elif quiet:
        stdout_level = logging.WARNING

    sh = logging.StreamHandler(sys.stderr)
    sh.setLevel(stdout_level)
    sh.setFormatter(fmt)
    root.addHandler(sh)

    if log_file:
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s %(name)s: %(message)s'
        ))
        root.addHandler(fh)
