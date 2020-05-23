from module_example import c       # Configuration defined in __init__.py
from module_example import baz     # Using c module wise


@c
class Cli:
    def subcommand_foo(self):
        """This will be shown in --help for subcommand-foo"""
        print('foo: ')
        baz.print_configuration()

    def subcommand_bar(self):
        """This will be shown in --help for subcommand-bar"""
        print('bar')
        print(repr(c))

############################################################
# $ ./examples/module_example/__main__.py subcommand-foo -- -h
#
# Type:        method
# String form: <bound method Cli.subcommand_foo of <clima.Cli object at 0x000001A6E7C919E8>>
# File:        C:/Users/foobar/code/py/fissle/examples/module_example/__main__.py
# Line:        6
# Docstring:   This will be shown in --help for subcommand-foo
# Args:
#     --a (str): a description (Default is 'A')
#     --x (int): x description (Default is 1)
#
# Usage:       __main__.py subcommand-foo [--X ...]

############################################################
# $ ./examples/module_example/__main__.py subcommand-foo
# foo:
# A
# 1

############################################################
# $ ./examples/module_example/__main__.py subcommand-foo --a 'amazing' --x 42
#
# foo:
# amazing
# 42

