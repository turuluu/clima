# API Reference

## `c`

```python
from clima import c
```

The global configuration object. Used as both a decorator and an attribute accessor.

**As a decorator:** wraps a `Cli` class to register its methods as subcommands.

```python
@c
class Cli:
    def my_command(self):
        pass
```

**As an accessor:** provides access to all resolved configuration values.

```python
print(c.name)   # attribute access
print(c['name'])  # dict-style access
```

## `Schema`

```python
from clima import Schema
```

Base class for defining CLI arguments. Subclass it with class-level attributes:

```python
class S(Schema):
    name: str = 'world'  # description for --help
    count: int = 1  # another description
```

### Field format

```
attribute[: type] = default  [# description]
```

- **attribute**: becomes a `--attribute` CLI flag and `c.attribute` accessor
- **type** (optional): used for casting values from all sources
- **default**: the fallback value
- **description** (optional): shown in `--help` output

### Special fields

| Field | Purpose |
|-------|---------|
| `cwd` | Directory for config file discovery |
| `CFG` | Explicit config file path (bypasses discovery) |
| `verbose` | Enables debug logging on stderr when `True` |
| `quiet` | Suppresses logging below WARNING when `True` |

### `Schema.post_init(self, *args)`

Override to compute derived defaults. Runs after Schema init but before CLI init. Can introduce new fields.

```python
class S(Schema):
    platform: str = 'linux'
    bin_path: str = ''

    def post_init(self, *args):
        if self.platform == 'win':
            self.bin_path = 'C:/tools/bin'
```

## `Cli.post_init`

A `@staticmethod` on the `Cli` class. Runs after configuration resolution. Has access to CLI args but cannot introduce new fields.

```python
@c
class Cli:
    @staticmethod
    def post_init(s):
        if s.platform == 'win':
            s.bin_path = 'C:/tools/bin'

    def run(self):
        print(c.bin_path)
```

## `setup_logging`

```python
from clima import setup_logging
```

```python
setup_logging(verbose=False, quiet=False, log_file=None)
```

Configures Python's root logger:

- **Default**: `INFO` on stderr
- **verbose=True**: `DEBUG` on stderr
- **quiet=True**: `WARNING` on stderr
- **log_file**: if set, writes `DEBUG` to the given file

Called automatically when Schema has `verbose` or `quiet` fields. Can also be called manually.

## Truncated tracebacks

Clima wraps subcommand execution in a traceback handler that shows a condensed error summary and writes the full traceback to `exception.log`.

For table-formatted output, install the optional extra:

```
pip install clima[tabulate]
```

## Fire flags

Clima wraps a vendored copy of [python-fire](https://github.com/google/python-fire). These Fire flags are available after a `--` separator:

```
my_tool -- --trace       # show Fire's call trace
my_tool -- --interactive  # drop into IPython after execution
my_tool -- --completion   # print bash completion script
```
