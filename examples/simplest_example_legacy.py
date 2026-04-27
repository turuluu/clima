#!/usr/bin/env python
from clima import c


@c
class Cli:
    def hello(self):
        """This command prints hello world"""
        print('hello world')
