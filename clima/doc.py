"""Doc string handling"""
from collections import OrderedDict
import inspect


def wrap_method_docs(cls: object, nt):
    methods = [m.object for m in inspect.classify_class_attrs(cls)
               if m.kind == 'method' and not m.name.startswith('_')]
    for m in methods:
        prepare_doc(nt, m)


def parse_source_for_params(params):
    """
    parse the source of the schema and split its
    fields
    """
    split_parameters = tuple(
        tuple(
            str(argtype_and_defdesc).strip()
            for argtype_and_defdesc in src_line.split('=', 1)
        )
        for src_line in params
        if src_line.startswith(' ')
    )
    return OrderedDict(split_parameters)


def filter_params(N):
    """Filter source lines of the class
    Returns:
        fields as source lines
    """
    filtered_source = []
    for line in inspect.getsourcelines(N.__class__)[0][1:]:
        # When parsing, post_init would bleed into the attributes without this hack
        if line.strip().startswith('def '):
            break
        filtered_source.append(line)
    return filtered_source


def attr_map(N):
    """Mapping for the schema's fields (parameters)"""
    _attr_map = {}
    filtered = filter_params(N)
    for param_type, def_desc in parse_source_for_params(filtered).items():
        if ':' in param_type:
            param, _type = param_type.split(':', 1)
            _type = _type.strip()
        else:
            param = param_type
            _type = None

        # TODO: this won't handle # in strings ...
        if '#' in def_desc:
            default, description = def_desc.split('#', 1)
            default = default.strip()
            description = description.strip()
        else:
            default = def_desc.strip()
            description = ''

        _attr_map.update(
            {
                param: {
                    'type': _type,
                    'default': default,
                    'description': description,
                }
            }
        )
    return _attr_map


def prepare_doc(N, f):
    """Replace docstrings to include the parameters (schema)"""
    # TODO: fix for fire 0.2.1
    ps_doc = []
    if hasattr(N, '__annotations__'):
        for attr_name, cls in N.__annotations__.items():
            attr = attr_map(N).get(attr_name)
            if attr is None:
                continue

            _type = attr['type'] if attr['type'] is not None else ""

            fmt = '    --{} ({}): {} (Default is {})'
            argument_help = fmt.format(attr_name, _type, attr['description'], attr['default'])
            ps_doc.append(argument_help)
            # Wanted to make clima py >= 3.4 compliant, and f-string require 3.6
            # ps_doc.append(f'    --{attr_name} ({_type if _type is not None else ""}): {attr["description"]} (Default is {attr["default"]})')

    ps_doc = '\n'.join(ps_doc)
    doc = f.__doc__
    doc = (doc if doc is not None else '') + '\nArgs:\n' + ps_doc
    f.__doc__ = doc
