import traceback
from contextlib import contextmanager
import sys
import re
from tabulate import tabulate

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

        core.py ::  __getattr__:114  - ...
        Missing argument for "name"
    """

    # yield
    # return

    # n_last_msgs = 3
    def get_filepath(line):
        m = re.match(r'([^"]+"(/?([^/"]+))+".*)', line)
        if m is not None:
            filename = list(m.groups())[-1]
            return line.replace(m.group(0), f'{filename}')

        else:
            return line

    def split_traceback(line, index=0):
        splitline = line.strip(' ').split('\n')
        res = splitline[index].strip(' ').split(',')

        return res

    def format_file_desc(line):
        filedesc = split_traceback(line)
        cpp_formatted = f'{filedesc[2]}:{filedesc[1][1:]}'
        filename = f'{get_filepath(filedesc[0])}'
        if len(filedesc) > 3:
            filedesc = [cpp_formatted, *filedesc[2:]]
        else:
            filedesc = [cpp_formatted]
        filedesc = [f'{desc}'.replace('in ', '').replace('line ', '') for desc in filedesc]

        filename = f'{filename:35}'
        return [filename, *filedesc]

    def format_line(line):
        return [*format_file_desc(line), *split_traceback(line, 1)[-1:]]

    try:
        yield
    except Exception:
        from copy import deepcopy
        exc_type, exc_value, exc_traceback = sys.exc_info()

        traceback_file = 'exception_traceback.log'
        with open(traceback_file, 'w') as wf:
            traceback.print_exception(exc_type, exc_value, exc_traceback, file=wf)

        print(f'full stacktrace in {traceback_file}')
        print('\nTruncated traceback:')

        tb = traceback.extract_tb(exc_traceback, limit=-2)
        truncated_error_table = []
        error_cell = []
        for line in tb.format():
            if line.strip(' ').startswith('File'):
                truncated_error_table.append(deepcopy(error_cell))
                error_cell = format_line(line)
            else:
                error_cell.append(line)
        print(tabulate(truncated_error_table, tablefmt='plain'))

        sys.exit(exc_value)
