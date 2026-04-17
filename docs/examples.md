# Examples

All examples live in the `examples/` directory and can be run directly.

## Simplest example

A minimal CLI with no schema — just a class with methods.

```python
from clima import c

@c
class Cli:
    def hello(self):
        """This command prints hello world"""
        print('hello world')
```

## README example

Basic schema with typed fields and inline descriptions.

```python
from clima import c, Schema

class Configuration(Schema):
    a: str = 'A'  # a description
    x: int = 1  # x description

@c
class Cli:
    def foo(self):
        print(c.a)
```

## Script example

Multiple subcommands, positional arguments, and piping.

```python
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
```

```
$ ./script_example.py print-name --name YoYo
YoYo Ma

$ echo "YoYo" | ./script_example.py print-name
YoYo Ma
```

## Required parameters

Use `None` as the default to mark a parameter as required.

```python
from clima import c, Schema

class C(Schema):
    name: str = None  # (Required) Your first name
    surname: str = 'Ma'  # Surname
    age: int = '132'  # Age is just a number

c: C = c

@c
class Something:
    def print_name(self):
        """If 'name' is not provided, it will raise an error on usage."""
        print(f'{c.name} {c.surname}')

    def print_age(self):
        """This works even without 'name' since c.name is not used here."""
        print(c.age)
```

## Type casting

Schema annotations are used to cast values to the correct type.

```python
from clima import c, Schema
import pathlib

class Conf(Schema):
    p: pathlib.PurePosixPath = ''  # This path should be cast to path
    s: str = 1  # This int should be cast to str
    i: int = '2'  # This str should be cast to int

@c
class Cli:
    def run(self):
        """run this to verify the casting"""
        assert type(c.p) is pathlib.PurePosixPath
        assert type(c.s) is str
        assert type(c.i) is int
        print('Types were cast correctly!')
```

## Traceback example

Demonstrates clima's truncated error display.

```python
from clima import c

@c
class Cli:
    def lumberjack(self):
        self.bright_side_of_life()

    def bright_side_of_life(self):
        print('An expected error: we intentionally raise an exception')
        return tuple()[0]
```
