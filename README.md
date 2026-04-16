<img src="https://raw.githubusercontent.com/turuluu/clima/master/docs/assets/clima.png" align="left" /> Create a command line interface with minimal setup.

[![PyPI](https://img.shields.io/pypi/v/clima)](https://pypi.org/project/clima/)
[![Python versions](https://img.shields.io/pypi/pyversions/clima)]()
[![PyPI license](https://img.shields.io/pypi/l/clima)]() 

# clima - command line interface with a schema

## Installation

```
pip install clima
```

Requires Python 3.9+.

## Why clima?

clima eliminates CLI boilerplate: define a `Schema` dataclass and a `Cli` class — that's it. Unlike click, typer, or argparse, clima gives you a built-in config cascade (CLI args → env vars → `.env` file → config file → defaults) with zero extra code. Schema fields double as CLI flags, environment variables, and config file keys automatically.

## Features

- **Config cascade** — CLI args → env vars → `.env` file → config file → defaults, resolved automatically
- **Type casting** — Schema field annotations are used to cast string CLI/env values to the right type
- **Help from field comments** — docstrings on Schema fields appear in `--help` output
- **`--verbose` / `--quiet` logging** — add `verbose: bool` or `quiet: bool` to Schema and get preconfigured logging
- **Undefined param warnings** — unknown `--flags` on the command line produce a clear warning
- **`version` subcommand** — `myscript version` prints the package version automatically
- **Config file support** — declare defaults in an INI-style `.conf` file keyed to your package name
- **`.env` file and env var support** — Schema fields are also read from environment variables and `.env` files
- **Optional gpg secrets** — decrypt secrets via `pass` / gnupg if installed

Create a command-line interface:

    from clima import c
    
    @c
    class Cli:
        def say_hi(self):
            print('oh hi - whatever this is..')

![example ascii](https://raw.githubusercontent.com/turuluu/clima/master/example.svg)

Create a cli program with arguments:

    from clima import c, Schema
    
    # Defining the settings (configuration object)
    class S(Schema):
        place = 'Finland'
        
    @c
    class Cli:
        def say_hi(self):
            print(f'Hi from {c.place}')
            
            
Usage example:
  
     cli.py say_hi
     > Hi from Finland
     cli.py say_hi --place 'Sweden'
     > Hi from Sweden
 
[Read the docs](https://python-clima.readthedocs.io/)

See and run the `examples`...
