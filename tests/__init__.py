import sys

from clima.core import Configurable


class SysArgvRestore:

    def setUp(self) -> None:
        self.save_sysargv()

    def save_sysargv(self):
        self.sys_argv = sys.argv

    def restore_sysargv(self):
        sys.argv = self.sys_argv

    def tearDown(self) -> None:
        self.restore_sysargv()
