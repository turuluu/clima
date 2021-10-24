#!/usr/bin/env python
from clima import c, Schema
import requests
import logging


class C(Schema):
    debug: bool = False  # Enable verbose printout
    url: str = 'https://pypi.org'  # This will be overriden by foo.cfg


# Hack to enable autocompletion in IDEs
c: C = c


@c
class MyCurl:
    def _configure(self):
        if c.debug:
            logging.getLogger('requests').setLevel(logging.DEBUG)

    def headers(self):
        """GET query to the url and print out the headers of the response"""
        self._configure()
        print(f'requesting from {c.url}..')
        res = requests.get(c.url)
        print(res.headers)

############################################################
# $ ./my_curl headers -- -h
#
# Type:        method
# String form: <bound method MyCurl.headers of <clima.Cli object at 0x0000020FA7324A58>>
# File:        ./examples/config_example/my_curl.py
# Line:        22
# Docstring:   GET query to the url and print out the headers of the response
# Args:
#    --debug (bool): Enable verbose printout (Default is False)
#    --url (str): This will be overriden by foo.cfg (Default is 'https://pypi.org')
#
# Usage:       my_curl.py headers [--URL ...]
