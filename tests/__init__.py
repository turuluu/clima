import sys

from clima.core import Configurable


class SysArgvRestore:
    # from clima import c

    # def __init__(self):
        # from clima import c
        # self.c = c

    def setUp(self) -> None:
        self.save_sysargv()

    def save_sysargv(self):
        self.sys_argv = sys.argv

    def restore_sysargv(self):
        sys.argv = self.sys_argv

    def tearDown(self) -> None:
        self.restore_sysargv()
