# Getting started

## Install

```
pip install clima
```

## Minimal example

```python
from clima import c

@c
class Cli:
    def hello(self):
        print('Hello from clima!')
```

Save as `app.py` and run:

```
python app.py hello
```

This schema-less form is handy for quick scripts that need no arguments.

## Adding arguments

Define a `Schema` to declare CLI arguments with defaults and types. Use `@S.cli` to connect the schema to the CLI class:

```python
from clima import Schema

class S(Schema):
    name: str = 'world'  # who to greet
    count: int = 1  # how many times

@S.cli
class Cli:
    def greet(self):
        for _ in range(S.count):
            print(f'Hello, {S.name}!')
```

```
python app.py greet
# Hello, world!

python app.py greet --name Ada --count 3
# Hello, Ada!
# Hello, Ada!
# Hello, Ada!
```

Access resolved values directly on the Schema class (`S.name`, `S.count`). Type annotations ensure the values are cast correctly — `count` is always an `int`, even when passed as a string from the command line.

## Subcommands

Every public method on the `Cli` class becomes a subcommand:

```python
from clima import Schema

class S(Schema):
    name: str = 'world'

@S.cli
class Cli:
    def greet(self):
        """Say hello."""
        print(f'Hello, {S.name}!')

    def farewell(self):
        """Say goodbye."""
        print(f'Goodbye, {S.name}!')
```

```
python app.py greet --name Ada
# Hello, Ada!

python app.py farewell --name Ada
# Goodbye, Ada!

python app.py --help
# Shows available subcommands: greet, farewell
```

## Version printing

If your package is managed with poetry, clima automatically exposes a `version` subcommand:

```
my_tool version
# 0.1.0
```

## Legacy API

Older code uses `from clima import c` and the `@c` decorator. This still works and will be maintained:

```python
from clima import c, Schema

class S(Schema):
    name: str = 'world'

@c
class Cli:
    def greet(self):
        print(f'Hello, {c.name}!')
```

The `@S.cli` form is preferred because `S.name` gives IDE completions with correct types.

## Next steps

- [Configuration](configuration.md) -- config files, env variables, `.env`, type casting
- [Examples](examples.md) -- runnable examples for common patterns
- [Reference](reference.md) -- full API reference
