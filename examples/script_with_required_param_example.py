#!/usr/bin/env python
from clima import c, Schema

class C(Schema):
    name: str = None  # (Required) Your first name
    surname: str = 'Ma'  # Surname
    age: int = '132'  # Age is just a number


c: C = c


@c
class Something:
    def print_name(self):
        """This command prints name. If the 'name' parameter is not provided, it will
        throw an error upon usage (in code). In other words, the check for the required parameters
        is defined by using 'None' as the default value in the configuration class i.e. C(Schema).
        """
        try:
            print(f'{c.name} {c.surname}')
        except:
            print('This is showing an expected error as a required parameter has not been provided')
            raise

    def print_age(self):
        """This here, prints my age. This shouldn't trigger an error even if 'name' is not provided
        as c.name is not used in the code. Thus subcommand level required parameters need only be defined
        in the configuration class i.e. C(Schema)
        """
        print(c.age)


############################################################
# $ ./script_example.py
#
# Usage:       script_example.py -
#              script_example.py - print-age
#              script_example.py - print-name
#
# Process finished with exit code 0

############################################################
# $ ./script_example.py print-age -- -h
#
# Type:        method
# String form: <bound method Something.print_age of <clima.Cli object at 0x00000175B85F7470>>
# File:        ./examples/script_example.py
# Line:        21
# Docstring:   This here, prints my age
# Args:
#     --name (str): Your first name (Default is 'Klimenko')
#     --surname (str): Surname (Default is 'Ma')
#     --age (int): Age is just a number (Default is '132')
#
# Usage:       script_example.py print-age [--AGE ...]

############################################################
# $ ./script_example.py print-age
#
# 132

# $ ./script_example.py print-name
#
# Klimenko Ma

############################################################
# $ ./script_example.py print-name --name YoYo
#
# YoYo Ma
