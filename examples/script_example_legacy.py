#!/usr/bin/env python
from clima import c, Schema


class C(Schema):
    name: str = 'Klimenko'  # Your first name
    surname: str = 'Ma'  # Surname
    age: int = '132'  # Age is just a number


c: C = c


@c
class Something:
    """This gets printed with -h"""

    def print_name(self):
        """This command prints name"""
        print(f'{c.name} {c.surname}')

    def print_age(self):
        """This here, prints my age"""
        print(c.age)


############################################################
# Running this script without arguments                    #
############################################################
#
# $ ./script_example.py
#
# Usage:       script_example.py -
#              script_example.py - print-age
#              script_example.py - print-name

############################################################
# Running with --help                                      #
############################################################
#
# $ ./script_example.py -h
#
# Usage:       script_example.py [ARGS]
#              
# Description: This is something

############################################################
# Running subcommand with --help                           #
############################################################
#
# $ ./script_example.py print-age -h
#
# Usage:       script_example.py print-age [ARGS]
#              
# Description: This here, prints my age
# Args:
#     --name (str): Your first name (Default is 'Klimenko')
#     --surname (str): Surname (Default is 'Ma')
#     --age (int): Age is just a number (Default is '132')

############################################################
# Running subcommand (uses default)                        #
############################################################
#
# $ ./script_example.py print-age
#
# 132

############################################################
# Running another subcommand (uses its default)            #
############################################################
#
# $ ./script_example.py print-name
#
# Klimenko Ma

############################################################
# Running subcommand using argument --name                 #
############################################################
#
# $ ./script_example.py print-name --name YoYo
#
# YoYo Ma

############################################################
# Running subcommand using positional argument             #
# (--name is first in class C(Schema) )                    #
############################################################
#
# $ ./script_example.py print-name YoYo
#
# YoYo Ma

############################################################
# Running subcommand with piping                           #
# Uses positional arguments like above (--name is first)   #
############################################################
#
# $ echo "YoYo" | ./script_example.py print-name
#
# YoYo Ma
