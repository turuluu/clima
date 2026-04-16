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

### Features

Clima handles loading and parsing command line arguments without the boilerplate. 

Main features:

- A global configuration object mapping as command line arguments defined as a single dataclass
    - Default values
    - Type casting
    - Function docstrings double as `--help` description on the command line
- Configuration for arguments
    - Declaring defaults in a config file
    - Parsing env variables
    - Parsing .env files
    - Decrypting secrets using gnugpg (if installed)

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
