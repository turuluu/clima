import traceback
from contextlib import contextmanager
import sys
from tabulate import tabulate
from pathlib import Path


def filter_fields(d: dict, nt):
    """Excludes fields not found in the schema/namedtuple"""
    res = {}
    for k, v in d.items():
        if k in nt._fields:
            res.update({k: v})

    return res


def type_correct_with(cdict, cfg_tuple):
    """Use type hints of the cfg tuple to cast parameters i.e. attributes into their intended types"""
    # TODO: This would be cleaner, if the config would use Schema or derivative in the
    # first place and use its validation process
    res = {}
    for k, v in cdict.items():
        typename = getattr(cfg_tuple, k)
        res.update({k: type(typename)(v)})
    return res


@contextmanager
def suppress_traceback():
    """Better exception printout

    This is just awful formatting - after years of trying to read this, I still squint
    my eyes to find the real issue. Let's reformat the traceback

          ...
          File "/Users/.../src/py/python-fire/fire/core.py", line 127, in Fire
            component_trace = _Fire(component, args, context, name)
          ...
          File "/Users/.../src/py/clima/clima/core.py", line 114, in __getattr__
            raise RequiredParameterException(f'Missing argument for "{item}"')_

    To something like:

        core.py:114 ::  __getattr__ - ...
        Missing argument for "name"
    """

    try:
        yield
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()

        traceback_file = 'exception_traceback.log'
        with open(traceback_file, 'w') as wf:
            traceback.print_exception(exc_type, exc_value, exc_traceback, file=wf)

        print(f'Truncated error traceback (full trace in {traceback_file}):\n')

        exc_type, exc_value, exc_traceback = sys.exc_info()

        formatted_lines = traceback.format_exc().splitlines()
        exception_desc = formatted_lines[-1]

        truncated_error_table = []
        tbs = traceback.extract_tb(exc_traceback, limit=-3)
        sep = ['::', ':', '=>']
        for tb in tbs[:-1]:
            if str(tb.name).startswith('_'):
                continue
            tb_filename = Path(tb.filename).name
            truncated_error_table.append(
                ['', f'{tb_filename}:{tb.lineno}', sep[0], f'{tb.name}()', sep[1], tb.line, sep[2]])

        error_name = exception_desc.split(':')[0]
        tb = tbs[-1]
        tb_filename = Path(tb.filename).name
        truncated_error_table.append(
            ['', f'{tb_filename}:{tb.lineno}', sep[0], f'{tb.name}()', sep[1], tb.line, sep[2], f'{error_name}'])

        print(tabulate(truncated_error_table, tablefmt='plain'))
        print()
        print(exception_desc)

        sys.exit()
