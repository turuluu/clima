"""Doc string handling"""
from collections import OrderedDict
import inspect


def wrap_method_docs(cls: object, nt):
    methods = [m.object for m in inspect.classify_class_attrs(cls)
               if m.kind == 'method' and not m.name.startswith('_')]
    for m in methods:
        prepare_doc(nt, m)


def params_with_defs(N):
    """parse the source of the schema for its details"""
    params_with_definitions = tuple(
        tuple(
            str(arg_and_def).strip()
            for arg_and_def in src_line.split(':', 1)
        )
        for src_line in inspect.getsourcelines(N.__class__)[0][1:]
        if src_line.startswith(' ')
    )
    return OrderedDict(params_with_definitions)


def attr_map(N):
    """Mapping for the schema's details"""
    _attr_map = {}
    for param, _def in params_with_defs(N).items():
        _type, def_desc = _def.split('=', 1)
        _type = _type.strip()

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

            ps_doc.append(f'    --{attr_name} ({attr["type"]}): {attr["description"]} (Default is {attr["default"]})')

    ps_doc = '\n'.join(ps_doc)
    doc = f.__doc__
    doc = (doc if doc is not None else '') + '\nArgs:\n' + ps_doc
    f.__doc__ = doc
