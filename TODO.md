[vfile:../code/py/clima/TODO.md](vfile:../code/py/clima/TODO.md){.wikilink}

[cmd:pandoc -f vimwiki -t markdown -o \~/code/py/clima/TODO.md \~/vimwiki/clima.wiki](cmd:pandoc -f vimwiki -t markdown -o ~/code/py/clima/TODO.md ~/vimwiki/clima.wiki){.wikilink}

\-\-- copy to git

# Project Management System - as a file.. {#Project Management System - as a file..}

So fresh and so lean, lean\...

## TODO v1.0.0: {#TODO v1.0.0:}

### v0.9.0

- \[▣\] Split readme into readme and docs
- \[▣\] .conf file checks
  - \[▣\] Skip .conf files that don\'t include \[Clima\] section
- \[◤\] running linux, macos and windows tests on github/travis
- \[◤\] maybe also look into tox testing to verify actual cli running
- []{.done0}Fix tests and verify state is at least on par with last
  release (0.8.x)
- []{.done0}Fix boolean values loaded from config
- []{.done0}some refactoring (naming, dead code, seams for better tests,
  etc)

### v0.9.1

- []{.done0}.conf file checks
  - []{.done0}Skip .conf files that don\'t include \[\<package\>\]
    section
  - []{.done0}Where the .conf files are loaded (recursive levels etc)?

### v0.9.2

- []{.done0}Fix version subcommand
- []{.done0}cwd argument is not respected (special parameter)
- []{.done0}fix string handling corner cases (fire doesn\'t handle well
  strings as arguments, when there\'s spaces)
- []{.done0}include (and fix) hypothesis tests

### v0.9.3

- []{.done0}Validation of undefined parameters (should advice that
  they\'re not defined in the config)
- []{.done0}usage and help page improvements
  - []{.done0}Fix help when given an undefined parameter
  - []{.done0}Fix argument print out (instead of printing just \[ARGS\])
  - []{.done0}Remove redundant - from \<cmd\> - \<subcmd\>
  - []{.done0}Parse top level docstring for general help (when not using
    subcommands)
  - []{.done0}Use fire without \@c
  - []{.done0}rtd documentation

### v0.9.4

- []{.done0}opt-in to overriden tracebacks
- []{.done0}Replace deprecated pipes-usage
- []{.done0}consider providing a preconfigured logging setup, with info
  on stdout and debug in file

### v1.0.0

- []{.done0}include (and fix) hypothesis tests
- []{.done0}fix the clima.core issues with tests
- []{.done0}clean the implementation
- []{.done0}Some perf/sanity considerations
  - []{.done0}docstring parsing takes a second or two, because it\'s run
    so inefficiently (viztracer)
- []{.done0}Rewrite docs
  - []{.done0}Getting started
  - []{.done0}Basic defaults
  - []{.done0}Reference
  - []{.done0}background for logo
  - []{.done0}favicon for good measure

## TODO v1.x.x {#TODO v1.x.x}

- []{.done0}piping v2.0
  - []{.done0}consider: use \-- to explicitly map to an argument and
    mixing with common parameters (cmd \| tool \--arg \--)
- []{.done0}completions
- []{.done0}way to define required parameters in subcommand context for
  the subcommands help
  - []{.done0}probably some syntax for starters, that then is compared
    with and parsed for every method
    - []{.done0}nested schema classes
- []{.done0}maybe a logging setup (\--dryrun)
  - []{.done0}default debug logging wrapper that would log every
    function called
- []{.done0}configfile helper to advice fixes in parameters etc.

## Backlog {#Backlog}

- []{.done0}improve exception.log -\> e.g. sudo runs can create a
  non-overwritable log file that breaks the next run
- []{.done0}piping v2.0
  - []{.done0}consider: use \-- to explicitly map to an argument and
    mixing with common parameters (cmd \| tool \--arg \--)
- []{.done0}completions
- []{.done0}way to define required parameters in subcommand context for
  the subcommands help
  - []{.done0}probably some syntax for starters, that then is compared
    with and parsed for every method
    - []{.done0}nested schema classes
- []{.done0}maybe a logging setup (\--dryrun)
  - []{.done0}default debug logging wrapper that would log every
    function called
- []{.done0}configfile helper to advice fixes in parameters etc.
- []{.done0}usage and help page improvements
  - []{.done0}Fix argument print out (instead of printing just \[ARGS\])
  - []{.done0}Remove redundant - from \<cmd\> - \<subcmd\>
  - []{.done0}Parse top level docstring for general help (when not using
    subcommands)
- []{.done0}script named .conf preferation - multiple conf file
  selection logic
- []{.done0}way to define schema within the cli class
- []{.done0}generate man page in a reasonable fashion
  - []{.done0}though fire v0.2.1 help looks like a man page
- []{.done0}rewrite the fire part

## Won\'t fix {#Won't fix}

- fix doc string and args/parameter help for fire v0.2.1
  - 0.3.0 now. diverged a lot from what I wanted initially (0.1.3 type
    formatting)
- better name - again

## In Review {#In Review}

- []{.done0}post schema init stuff
  - []{.done0}validation (fields are what they\'re supposed to be,
    optional helper msg what it was and what it should be)
  - []{.done0}post init hook for reassigning variables (\...)
  - []{.done0}type assurance as in if the attribute is of type Path,
    then c.attr is Path when using it
  - []{.done0}optional configurations e.g. mac/win in build scripts
- \[◤\] rewriting tests to match current state
  - \[◤\] type casting from config files doesn\'t work for lists (at
    leasts)
- []{.done0}Validation of undefined parameters (should advice that
  they\'re not defined in the config) (kinda done)

## DONE {#DONE}

### v0.8.0

- \[■\] version printing (infer package version with `<cmd> version`)
- \[■\] config loading doesn\'t look into current dir or \--cwd
- \[■\] piping
  - \[■\] consider: piping implicitly to the first argument
- \[■\] handling \# in Schema
  - \[■\] Commenting a field in the middle of the definition breaks
    clima

### v0.7.0

- \[■\] fork python-fire 0.1.3 (-\> forked, branch clima)
  - \[■\] include to code
  - \[■\] add license details
- \[■\] tooling and installation helpers
  - \[■\] flit is not working on windows at least.. (works with git
    bash)
    - \[■\] removed. Use poetry to install intermediary dev versions
  - \[■\] dephell or alternative to allow dev with whatever setup
    - \[■\] Too much hassle. Dephell started breaking everything.
      Removed
- \[■\] better error reporting by dynamically handling error objects
- \[■\] fork python-fire 0.1.3 - prefer the output
  - \[■\] Need to parse the parameters
  - \[■\] implicitly map `cmd` -h -\> \<cmd\> \-- -h
  - \[■\] better output for subcommands
    - \[■\] fire v0.2.1 has this, but hides the parameter parsing and
      looks awful on windows
- \[■\] NamedTuple could simplify things, but it\'s tricky to get past
  the annotations etc.
  - \[■\] Could look into how it\'s implemented..
  - \[■\] NamedTuple doesn\'t respect the type hints
- \[■\] Show params in help / How to pass namedtuple\'s signature
  programmatically to the Cli functions?
  - \[■\] Need to do code generation i.e. write the signature into a
    separate python file and eval that?
  - \[■\] Any fire-specific tricks to use for this? Cli(C) definition
    doesn\'t work..
    - \[■\] Maybe overwriting the \'usage\' portion or generating a
      docstring
  - \[■\] Create a companion class which describes the namedtuple
    fields\' functions
  - \[■\] hardcoded defaults mechanism
- \[■\] config parser
- \[■\] decorator or some other wrapper for the cli-class to configure
  with given parameters without boilerplate
- \[■\] c++ template like behaviour in which you can define the named
  tuple with the cli class
  - \[■\] code completion should work in the IDE (DONE: a hack around
    this..)
  - \[■\] configure should know to chain config file with params
- \[■\] Configuration file requires copying clima in the same directory
  with the user code
  - \[■\] location independent now
- \[■\] parsing configuration and help/description require separate
  steps
  - \[■\] would be nice to have a single point of access and import
    requirement
- \[■\] base level help (`script` \-- -h) doesn\'t printout the
  subcommands
  - \[■\] fixed in fire v0.2.1
- \[■\] look into autocompletion options (iirc, fire might have sth
  out-of-the-box)
  - \[■\] documented
- \[■\] better name
- \[■\] readme\'s pipenv section doesn\'t make much sense..
- \[■\] some sane tests
- \[■\] clean code from `__init__`
- \[■\] fix args parsing for help description. Something broke it in
  v0.2.1
