# Project Management System - as  a file..

So fresh and so lean, lean...

## TODO:

- way to define required parameters in subcommand context
    - nested schema classes
* generate man page in a reasonable fashion
  * though fire v0.2.1 help looks like a man page
* maybe a logging setup (--dryrun)
  * default debug logging wrapper that would log every function called
* way to define schema within the cli class
* clean the implementation
- cwd argument is not respected (special parameter)
- NamedTuple could simplify things, but it's tricky to get past the annotations etc.
    - Could look into how it's implemented..
    - NamedTuple doesn't respect the type hints
- Validation of undefined parameters (should advice that they're not defined in the config)
- configfile helper to advice fixes in parameters etc.
- better error reporting by dynamically handling error objects
- maybe also look into tox testing to verify actual cli running
- fork 0.1.3 - prefer the output
    - Need to parse the parameters
    - implicitly map `cmd` -h -> <cmd> -- -h
    * fire doesn't handle well strings as arguments, when there's spaces
    * better output for subcommands
      * fire v0.2.1 has this, but hides the parameter parsing and looks awful on windows
- better name - again
- script named .conf preferation - multiple conf file selection logic

## Won't fix
* fix doc string and args/parameter help for fire v0.2.1
    * 0.3.0 now. diverged a lot from what I wanted initially (0.1.3 type formatting)
    
## DONE:

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
* base level help (`script` -- -h) doesn't printout the subcommands
  * fixed in fire v0.2.1
* look into autocompletion options (iirc, fire might have sth out-of-the-box)
  * documented
* better name
* readme's pipenv section doesn't make much sense..
* some sane tests
* clean code from `__init__`
* fix args parsing for help description. Something broke it in v0.2.1

## In Review

* tooling and installation helpers 
  * flit is not working on windows at least.. (works with git bash)
  * dephell or alternative to allow dev with whatever setup
* post schema init stuff 
  * validation (fields are what they're supposed to be, optional helper msg what it was and what it should be)
  * post init hook for reassigning variables (...)
  * type assurance as in if the attribute is of type Path, then c.attr is Path when using it
  * optional configurations e.g. mac/win in build scripts 
- config loading doesn't look into current dir or --cwd
- rewriting tests to match current state
