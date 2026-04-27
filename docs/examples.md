# Examples

All examples live in the `examples/` directory and can be run directly.
Legacy versions using the `@c` API are preserved as `*_legacy.py` for comparison.

## Simplest example

A minimal CLI with no schema — just a class with methods. Uses `@c` since there is no Schema to bind to.

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
from clima import Schema

class Configuration(Schema):
    a: str = 'A'  # a description
    x: int = 1  # x description

@Configuration.cli
class Cli:
    def foo(self):
        print(Configuration.a)
```

## Script example

Multiple subcommands, positional arguments, and piping.

```python
from clima import Schema

class C(Schema):
    name: str = 'Klimenko'  # Your first name
    surname: str = 'Ma'  # Surname
    age: int = '132'  # Age is just a number

@C.cli
class Something:
    """This gets printed with -h"""

    def print_name(self):
        """This command prints name"""
        print(f'{C.name} {C.surname}')

    def print_age(self):
        """This here, prints my age"""
        print(C.age)
```

```
$ ./script_example.py print-name --name YoYo
YoYo Ma

$ echo "YoYo" | ./script_example.py print-name
YoYo Ma
```

## Required parameters

Use `None` as the default to mark a parameter as required. Accessing it without providing a value raises `RequiredParameterException`.

```python
from clima import Schema

class C(Schema):
    name: str = None  # (Required) Your first name
    surname: str = 'Ma'  # Surname
    age: int = '132'  # Age is just a number

@C.cli
class Something:
    def print_name(self):
        """If 'name' is not provided, it will raise an error on usage."""
        print(f'{C.name} {C.surname}')

    def print_age(self):
        """This works even without 'name' since C.name is not used here."""
        print(C.age)
```

## Type casting

Schema annotations are used to cast values to the correct type.

```python
from clima import Schema
import pathlib

class Conf(Schema):
    p: pathlib.PurePosixPath = ''  # This path should be cast to path
    s: str = 1  # This int should be cast to str
    i: int = '2'  # This str should be cast to int

@Conf.cli
class Cli:
    def run(self):
        """run this to verify the casting"""
        assert type(Conf.p) is pathlib.PurePosixPath
        assert type(Conf.s) is str
        assert type(Conf.i) is int
        print('Types were cast correctly!')
```

## Traceback example

Demonstrates clima's truncated error display. Uses `@c` since there is no Schema.

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
