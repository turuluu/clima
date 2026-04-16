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

## Adding arguments

Define a `Schema` to declare CLI arguments with defaults and types:

```python
from clima import c, Schema

class S(Schema):
    name: str = 'world'  # who to greet
    count: int = 1  # how many times

@c
class Cli:
    def greet(self):
        for _ in range(c.count):
            print(f'Hello, {c.name}!')
```

```
python app.py greet
# Hello, world!

python app.py greet --name Ada --count 3
# Hello, Ada!
# Hello, Ada!
# Hello, Ada!
```

## Subcommands

Every public method on the `Cli` class becomes a subcommand:

```python
from clima import c, Schema

class S(Schema):
    name: str = 'world'

@c
class Cli:
    def greet(self):
        """Say hello."""
        print(f'Hello, {c.name}!')

    def farewell(self):
        """Say goodbye."""
        print(f'Goodbye, {c.name}!')
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

## Next steps

- [Configuration](configuration.md) -- config files, env variables, `.env`, type casting
- [Reference](reference.md) -- full API reference
