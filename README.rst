.. role:: raw-html-m2r(raw)
   :format: html


clima - command line interface with a schema
============================================


.. image:: https://travis-ci.com/d3rp/clima.svg?branch=master
   :target: https://travis-ci.com/d3rp/clima
   :alt: Build status
 
.. image:: https://img.shields.io/pypi/pyversions/clima
   :target: 
   :alt: Python versions
 
.. image:: https://img.shields.io/librariesio/github/d3rp/clima
   :target: 
   :alt: Dependencies
 
.. image:: https://img.shields.io/pypi/l/clima
   :target: 
   :alt: PyPI license


Create a command line interface out of your script with quick default behaviour for configuration, minimal setup and less maintenance. It handles loading and parsing configuration
files and overriding it with env variables by defining a simple schema of the configuration and a class with your "business logic".

Example: this is the required setup for having configurations and a command line interface ready for use:

.. code-block::

   from clima import c, Schema

   @c
   class C(Schema):
      a = 1

   @c
   class Cli:
       def foo(self):
           # using configuration
           print(c.a)


Long description
----------------

In other words, use this to wrap your scripts as command line commands without resorting to bash or maintaining argument parsing in python. There shouldn't be a need of duplicating comments for ``--help`` to remember what the arguments were and did. This decorator magic offers the typical use experience of a cli program (e.g. argument parsing and validation, --help, subcommands, ...).

The implementation is focused on a premise that for a simple script there's usually a script wide global configuration which would be used through out the user code i.e. a context for the program that is refered to in different parts of the code. That configuration is populated with given arguments falling back on defaults in the code and some further complimentary options and then made accessible via a simple global ``c`` variable around the code base with very little additional effort. With a small adjustment this can made to autocomplete in IDEs. This helps when the schema of the configuration grows larger.

Installing
----------

.. code-block::

   pip install --user clima


Installing from source
^^^^^^^^^^^^^^^^^^^^^^

Choose your favourite flavour of build system. Check their documentation if puzzled (poetry, flit, pip, pipx, pipenv..)

The tooling here has been exported with `DepHell <https://github.com/dephell/dephell>`_ from the poetry declarations.

Usage
-----

See the example file in `\ ``examples/script_example.py`` <examples/script_example.py>`_. Here's a run down of the individual
parts in such a script (adapted from another example at `module example <examples/module_example>`_\ ).

First import the required components:

.. code-block::

   from clima import c, Schema


In your code define the ``Schema`` subclass by decorating the class with ``c``\ :

.. code-block::

   @c
   class Configuration(Schema):
       a: str = 'A'  # a description
       x: int = 1  # x description


"Configuration" is an arbitrary name, no magic there. The inherited ``Schema`` class
simplifies the schema's templating to defining just the attributes (i.e. ``a`` and ``x`` in this
example). Those have a set way:

.. code-block::

       # attribute[: type] = default value  [# Description for the --help]
       a: str = 'A'  # a description


``a`` is the attribute which can be called in the code later with ``c.a``. It has a type of 'str', default
value of 'A'. The comment after it is parsed for the command line so it's not redundant. The values in square brackets ``[]`` are
optional. All of these parts will be parsed for the '--help' for the subcommands of the cli, which should be defined as follows:

.. code-block::

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
subcommands' help printout. Note the usage of the parsed configuration ``c`` inside the method:

    ...
        ...
        print(c.a)
        print(c.x)


Also, to enable autocompletion in IDEs, this hack suffices:

.. code-block::

   c: Configuration = c


Put it in the "global space" e.g. just after defining the template. See the `\ ``examples/script_example.py`` <examples/script_example.py>`_ for a specific example.

When all is complete, the imported ``c`` variable should have all the bits and pieces for the configuration. It can be
used inside the Cli class as well as imported around the codebase thus encapsulating all the configurations into one
container with quick access with attributes ``c.a``\ , ``c.x``\ , etc...

Examples and platforms
----------------------

Should work for linux, macos and windows.

More examples in the `examples directory <examples>`_ with printouts of the defined subcommands and helps.

Testing the examples
^^^^^^^^^^^^^^^^^^^^

The `examples <examples>`_ can be tried out by cloning the repo and running from repo directory root (on linux and the like):

.. code-block::

   PYTHONPATH=$PWD python ./examples/module_example/__main__.py -- -h
   PYTHONPATH=$PWD python ./examples/module_example/__main__.py subcommand-foo -- -h
   PYTHONPATH=$PWD python ./examples/module_example/__main__.py subcommand-bar
   ...


Output should resemble this (fire v0.1.3 prints out Args, fire v0.2.1 doesn't (though looks much nicer))

.. code-block::

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

Configuration file and environment variables
--------------------------------------------

The ``c`` decorator/configuration chains multiple configuration options together in order of priority (lower number overrides higher number):


#. command line arguments
#. Environment variables
#. configuration file definitions
#. defaults in the schema/template/namedtuple class

The configuration file should be named with postfix ``.cfg`` e.g. ``foo.cfg`` and have an ini type formatting with
a 'Default' section:

.. code-block::

   # foo.cfg
   [Default]
   x = 2


The keys are the same as what you define in the schema. You can define all, some or none of the attributes.
Same applies for the env variables.

.. code-block::

   # linux example
   X=2 tester subcommand-foo


Additional features via Fire
----------------------------

See the `Python Fire's Flags <https://github.com/google/python-fire/blob/master/docs/using-cli.md#python-fires-flags>`_
documentation for nice additional features such as:

.. code-block::

   # e.g. tester.py is our cli program
   tester.py subcommand-foo -- --trace
   tester.py -- --interactive
   tester.py -- --completion


Why another cli framework?
--------------------------

This is just a tool to slap together a cli program in python instead that grew out of the need of having a build automation system and an entrypoint script to build various flavours of C++ projects. The intention is to get something reasonably configurable and generic up and running as fast as possible while still having the "power" of python. I can't bother to memorize argparses syntax, even though it's a very good package. Also click works nice for more elaborate things though fire is my personal favourite for the time being. Often times when I kick off a bash script for this it ends up too elaborate very quick and then I miss python.

Also docopt looks very nice, but it doesn't provide autocompletion and all the configuration chaining magic I was after.

Other options for full cli experience:


* `docopt <https://docopt.org>`_
* `fire <https://github.com/google/python-fire>`_
* `click <https://click.palletsprojects.com>`_

Dependencies
^^^^^^^^^^^^


* fire - `python-fire <https://github.com/google/python-fire>`_ from google does the cli wrapping

DONE:
-----


* Show params in help / How to pass namedtuple's signature programmatically to the Cli functions?    

  * Need to do code generation i.e. write the signature into a separate python file and eval that?
  * Any fire-specific tricks to use for this? Cli(C) definition doesn't work..

    * Maybe overwriting the 'usage' portion or generating a docstring

  * Create a companion class which describes the namedtuple fields' functions
  * hardcoded defaults mechanism

* config parser
* decorator or some other wrapper for the cli-class to configure with given parameters without boilerplate
* c++ template like behaviour in which you can define the named tuple with the cli class

  * code completion should work in the IDE (DONE: a hack around this..)
  * configure should know to chain config file with params 

* Configuration file requires copying clima in the same directory with the user code

  * location independent now

* parsing configuration and help/description require separate steps

  * would be nice to have a single point of access and import requirement

* base level help (\ ``script`` -- -h) doesn't printout the subcommands

  * fixed in fire v0.2.1

* look into autocompletion options (iirc, fire might have sth out-of-the-box)

  * documented

* better name
* readme's pipenv section doesn't make much sense..

TODO:
-----


* generate man page in a reasonable fashion

  * though fire v0.2.1 help looks like a man page

* maybe a logging setup (--dryrun)

  * default debug logging wrapper that would log every function called

* tooling and installation helpers

  * flit is not working on windows at least.. (works with git bash)
  * dephell or alternative to allow dev with whatever setup

* fix doc string and args/parameter help for fire v0.2.1
* some sane tests
* clean code from ``__init__``
* better output for subcommands

  * fire v0.2.1 has this, but hides the parameter parsing and looks awful on windows

* implicitly map ``cmd`` -h -> :raw-html-m2r:`<cmd>` -- -h
* way to define schema within the cli class
* fire doesn't handle well strings as arguments, when there's spaces
* post schema init stuff

  * validation (fields are what they're supposed to be, optional helper msg what it was and what it should be)
  * post init hook for reassigning variables (...)
  * type assurance as in if the attribute is of type Path, then c.attr is Path when using it
  * optional configurations e.g. mac/win in build scripts
