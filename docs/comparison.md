# Comparison

How clima compares to other Python CLI frameworks.

| Feature | clima | click | typer | argparse | fire |
|---|---|---|---|---|---|
| Define CLI from class | Yes | No | No | No | Yes |
| Schema-driven config | Yes | No | No | No | No |
| Config cascade (CLI + env + file) | Built-in | Manual | Manual | Manual | No |
| Type casting from annotations | Yes | Decorators | Yes | Manual | Partial |
| `.env` file support | Built-in | Via plugin | Via plugin | No | No |
| Config file support | Built-in | No | No | No | No |
| `--help` from docstrings | Yes | Decorators | Docstrings | Manual | Yes |
| `--verbose`/`--quiet` logging | Built-in | Manual | Manual | Manual | No |
| Subcommands | Yes | Yes | Yes | Yes | Yes |
| Positional arg promotion | Yes | No | No | No | Partial |
| Piping support | Yes | Yes | No | No | No |
| Shell completions | No | Yes | Yes | No | No |
| Dependencies | Minimal | Self-contained | click | stdlib | Self-contained |
| Lines of code to get started | ~10 | ~15 | ~10 | ~20 | ~5 |

## When to use clima

- You want a **schema-driven** CLI where one dataclass defines all configuration
- You need a **config cascade** (CLI args, env vars, `.env` files, config files) without extra plumbing
- You prefer **class-based** CLI definitions over decorated functions

## When to use something else

- **click** or **typer**: when you need shell completions, complex parameter types, or a large plugin ecosystem
- **argparse**: when you want zero dependencies and full control over parsing
- **fire**: when you want to expose any Python object as a CLI with zero setup (no schema needed)
