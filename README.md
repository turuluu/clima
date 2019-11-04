# clima - command line interface with a schema

[![PyPI](https://img.shields.io/pypi/v/clima)](https://pypi.org/project/clima/)
[![Python versions](https://img.shields.io/pypi/pyversions/clima)]()

[![Build status](https://travis-ci.com/d3rp/clima.svg?branch=master)](https://travis-ci.com/d3rp/clima)
[![Dependencies](https://img.shields.io/librariesio/github/d3rp/clima)]() 

[![PyPI license](https://img.shields.io/pypi/l/clima)]()


Create a command line interface and a configuration object with minimal setup and less maintenance.
It handles loading and parsing configuration files and overriding it with env variables by defining 
a simple schema of the configuration and a class with your "business logic".

Example: to setup a configuration and a command line interface ready to go:

    from clima import c, Schema
    
    class C(Schema):
       a = 1
     
    @c
    class Cli:
        def foo(self):
            # using configuration
            print(c.a)
 
Command line usage in a terminal would then be e.g.:

    ./script.py foo
    ./script.py foo --a 42

See the example scripts and other sections for more examples.

## Long description

In other words, you can use this to wrap your scripts as command line commands without resorting to bash or maintaining argument parsing in python. This removes the need of duplicating comments in order `--help` to remember what the arguments were and what they did. Sprinkling some decorator magic offers a typical use experience of a cli program (e.g. argument parsing and validation, --help, subcommands, ...).

The implementation is focused on a premise that for a simple script there's usually a script wide global configuration which would be used through out the user code i.e. a context for the program that is refered to in different parts of the code. That configuration is populated with given arguments falling back on defaults in the code and some further complimentary options. Those are then made accessible via a global `c` variable that can be tossed around the code base with very little additional effort. With a small adjustment this can made to autocomplete in IDEs (as attributes). This helps when the schema of the configuration grows larger as the autocomplete kicks in after typing `c.` offering those fields in your "schema" as attributes.

## Installing

    pip install --user clima
    
or with [pipx](https://pipxproject.github.io/pipx/) to use dedicated virtualenv:
    
    pipx install --user clima
    
### Installing from source

Choose your favourite flavour of build system. Check their documentation if puzzled ([poetry](https://poetry.eustace.io), [flit](https://flit.readthedocs.io/en/latest), [pipx](https://pipxproject.github.io/pipx/), [pipx](https://pipxproject.github.io/pipx/), [pipenv](https://docs.pipenv.org/en/latest)..)

The tooling here has been exported with [DepHell](https://github.com/dephell/dephell) from the poetry declarations. In case your favourite build tool flavour files are not up to date, see the `publish.py` for its `convert` subcommand, which should convert to all the possible alternatives once dephell is installed.

## Usage

See the example file in [`examples/script_example.py`](examples/script_example.py). Here's a run down of the individual
parts in such a script (adapted from another example at [module example](examples/module_example)).

First import the required components:

    from clima import c, Schema
    
In your code define the `Schema` subclass by decorating the class with `c`:

    class Configuration(Schema):
        a: str = 'A'  # a description
        x: int = 1  # x description

"Configuration" is an arbitrary name, no magic there. The inherited `Schema` class
simplifies the schema's templating to defining just the attributes (i.e. `a` and `x` in this
example). Those have a set way:

        # attribute[: type] = default value  [# Description for the --help]
        a: str = 'A'  # a description
       
`a` is the attribute which can be called in the code later with `c.a`. It has a type of 'str', default
value of 'A'. The comment after it is parsed for the command line so it's not redundant. The values in square brackets `[]` are
optional. All of these parts will be parsed for the '--help' for the subcommands of the cli, which should be defined as follows:

    @c
    class Cli:
        def subcommand_foo(self):
            """This will be shown in --help for subcommand-foo"""
            print('foo')
            print(c.a)
            print(c.x)

        def subcommand_bar(self):
            """This will be shown in --help for subcommand-bar"""
            print('bar')

The methods are parsed as subcommands and their respective doc strings will show in the 
subcommands' help printout. Note the usage of the parsed configuration `c` inside the method:

    ...
        ...
        print(c.a)
        print(c.x)
   
Also, to enable autocompletion in IDEs, this hack suffices:

    c: Configuration = c

Put it in the "global space" e.g. just after defining the template. See the [`examples/script_example.py`](examples/script_example.py) for a specific example.

When all is complete, the imported `c` variable should have all the bits and pieces for the configuration. It can be
used inside the Cli class as well as imported around the codebase thus encapsulating all the configurations into one
container with quick access with attributes `c.a`, `c.x`, etc...

## Examples and platforms

Should work for linux, macos and windows.

More examples in the [examples directory](examples) with printouts of the defined subcommands and helps.

### Post init hook

In some occasions it's useful to deduce specific defaults from the given parameters e.g. in a cross platform build allowing
only minimal cli arguments. For those cases there's an `post_init` hook in which the fields can be refered to as in a
typical class, but that still allows validation and type casting etc.:

    class SoAdvanced(Schema):
        platform: str = 'win'  # a description
        bin_path: pathlib.Path = ''  # x description
        
        def post_init(self, *args):
            if self.platform = 'win':
                self.bin_path = 'c:/Users/foo/bar'
            else:
                self.bin_path = '/Users/mac/sth'

### Testing the examples

The [examples](examples) can be tried out by cloning the repo and running from repo directory root (on linux and the like):

    PYTHONPATH=$PWD python ./examples/module_example/__main__.py -- -h
    PYTHONPATH=$PWD python ./examples/module_example/__main__.py subcommand-foo -- -h
    PYTHONPATH=$PWD python ./examples/module_example/__main__.py subcommand-bar
    ...

Output should resemble this (fire v0.1.3 prints out Args, fire v0.2.1 doesn't (though looks much nicer))

```
$ tester subcommand-foo -- -h

Type:        method
String form: <bound method Cli.subcommand_foo of <__main__.Cli object at 0x000002995AD74BE0>>
File:        C:\Users\foobar\code\py\clima\tester\__main__.py
Line:        18
Docstring:   This will be shown in --help for subcommand-foo
Args:
    --a (str): a description (Default is 'A')
    --x (int): x description (Default is 1)

Usage:       __main__.py subcommand-foo [--X ...]
```

## Configuration file and environment variables

The `c` decorator/configuration chains multiple configuration options together in order of priority (lower number overrides higher number):

1. command line arguments
1. Environment variables
1. configuration file definitions
1. defaults in the schema/template/namedtuple class

The configuration file should be named with postfix `.cfg` e.g. `foo.cfg` and have an ini type formatting with
a 'Default' section:

    # foo.cfg
    [Default]
    x = 2

The keys are the same as what you define in the schema. You can define all, some or none of the attributes.
Same applies for the env variables.
    
    # linux example
    X=2 tester subcommand-foo
    
## Additional features via Fire

See the [Python Fire's Flags](https://github.com/google/python-fire/blob/master/docs/using-cli.md#python-fires-flags)
documentation for nice additional features such as:

    # e.g. tester.py is our cli program
    tester.py subcommand-foo -- --trace
    tester.py -- --interactive
    tester.py -- --completion
    
## Why another cli framework?

This is just a tool to slap together a cli program in python instead that grew out of the need of having a build automation system and an entrypoint script to build various flavours of C++ projects. The intention is to get something reasonably configurable and generic up and running as fast as possible while still having the "power" of python. I can't bother to memorize argparses syntax, even though it's a very good package. Also click works nice for more elaborate things though fire is my personal favourite for the time being. Often times when I kick off a bash script for this it ends up too elaborate very quick and then I miss python.

Also docopt looks very nice, but it doesn't provide autocompletion and all the configuration chaining magic I was after.

Other options for full cli experience:

* [docopt](https://docopt.org)
* [fire](https://github.com/google/python-fire)
* [click](https://click.palletsprojects.com)


### Dependencies

* fire - [python-fire](https://github.com/google/python-fire) from google does the cli wrapping

