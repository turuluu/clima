# Configuration

Clima resolves argument values through a chain of sources, highest priority first:

1. **CLI arguments** (`--name Ada`)
2. **Environment variables** (`NAME=Ada my_tool greet`)
3. **`.env` file** (via [python-dotenv](https://github.com/theskumar/python-dotenv))
4. **Config file** (`.conf` or `.cfg`, INI format)
5. **Password store** (`~/.password-store` via gnupg, if installed)
6. **Schema defaults** (the values in your `Schema` subclass)

## Config files

Create an INI-style file with a section matching your package name or `[Clima]`:

```ini
# my_tool.conf
[Clima]
name = Ada
count = 3
```

Place it in the working directory. Clima discovers it automatically.

### Discovery rules

- Clima searches the current directory (or `cwd` if your Schema defines it) for `*.conf` then `*.cfg`.
- Files must contain a `[<package_name>]` or `[Clima]` section to be picked up.
- If nothing matches, Clima walks up to 2 parent directories within the Python package tree.
- Set `CFG` on the Schema to bypass discovery:

```python
from pathlib import Path

class S(Schema):
    name: str = 'world'
    CFG = Path.home() / '.my_tool.conf'
```

## Environment variables

Schema field names are matched case-insensitively against environment variables:

```
NAME=Ada python app.py greet
```

## `.env` file

Supports both forms:

```
name = Ada
export count = 3
```

## Type casting

Schema type annotations are used to cast values from all sources:

```python
class S(Schema):
    count: int = 1
    verbose: bool = False
    output: Path = ''
```

- `int`, `float`, `str` -- standard casting
- `bool` -- string values `true`, `1`, `yes`, `on` (case-insensitive) map to `True`
- `Path` -- cast to `pathlib.Path`
- `list` -- scalars and strings are wrapped (not split character-by-character)

## The `cwd` field

If your Schema defines a `cwd` field, Clima uses that directory for config file discovery:

```python
class S(Schema):
    cwd: Path = ''
    value: int = 0
```

```
python app.py cmd --cwd /path/to/project
```

## Password store

If gnupg is installed, Clima matches Schema fields against files in `~/.password-store/`:

```python
class S(Schema):
    sign_id: str = ''
    sign_pw: str = ''
```

If `~/.password-store/work/ci/sign_id.gpg` exists, it will be decrypted and used as the default for `sign_id`.

## Logging

When your Schema includes `verbose` or `quiet` fields, Clima auto-configures Python logging:

```python
class S(Schema):
    verbose: bool = False
    quiet: bool = False
```

- Default: `INFO` on stderr, `DEBUG` in `<script>.debug.log`
- `--verbose`: `DEBUG` on stderr
- `--quiet`: `WARNING` on stderr

Install with `pip install clima` -- no extra dependencies needed.
