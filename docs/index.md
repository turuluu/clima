# clima

Create a command line interface with minimal setup.

[![PyPI](https://img.shields.io/pypi/v/clima)](https://pypi.org/project/clima/)
[![Python versions](https://img.shields.io/pypi/pyversions/clima)]()
[![PyPI license](https://img.shields.io/pypi/l/clima)]()

## Quick example

```python
from clima import Schema

class S(Schema):
    name: str = 'world'

@S.cli
class Cli:
    def greet(self):
        print(f'Hello, {S.name}!')
```

```
pip install clima
python app.py greet --name Ada
# Hello, Ada!
```

## Install

```
pip install clima
```

Python 3.9+.

## Features

- Subcommands from class methods
- Configuration cascade, in order of priority: CLI args > env > .env > config file > Schema defaults
- Parses `--help` from docstrings and field comments
- Define CLI parameters as a Schema class with defaults and types
- Type casting from annotations
- IDE completions work out-of-the-box
- Optional logging with `--verbose` / `--quiet`
- Version subcommand for poetry-packaged tools

## Documentation

- [Getting started](getting-started.md) -- install and first CLI in 5 minutes
- [Configuration](configuration.md) -- config files, env, type casting, logging
- [Examples](examples.md) -- runnable examples
- [Reference](reference.md) -- full API reference


