#!/usr/bin/env python
from clima import c, Schema


class C(Schema):
    name: str = 'Klimenko'  # Your first name
    surname: str = 'Ma'  # Surname
    age: int = '132'  # Age is just a number


c: C = c


@c
class Something:
    def print_name(self):
        """This command prints name"""
        print(f'{c.name} {c.surname}')

    def print_age(self):
        """This here, prints my age"""
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
