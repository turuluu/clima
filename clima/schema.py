import sys
import inspect
from typing import NamedTuple


def asdict(cls):
    # TODO: Does this even work?
    return {k: v for k, v in cls.__class__.__dict__.items()
            if not k.startswith('_')
            and not inspect.isfunction(v)
            and not inspect.ismethod(v)}


class MetaSchema(type):
    # print('<1>')

    @classmethod
    def __prepare__(*args, **kwargs):
        # print('<2>', end=' ')
        # print(args)
        return {'a': 0}

    # namespace = metaclass.__prepare__(name, bases, **kwds)
    # obj = metaclass(name, bases, namespace, **kwds)

    def __new__(mcs, name, bases, namespace, **kwds):
        # print('<4>')
        cls = type.__new__(mcs, name, bases, namespace)

        # Parsing type descriptors
        if '__annotations__' in namespace:
            for ann, t in namespace['__annotations__'].items():
                # Validation
                try:
                    setattr(cls, ann, t(namespace[ann]))
                except TypeError as ex:
                    print(f'given parameters or defined defaults were of incorrect type:')
                    print(f'{cls.__qualname__}.{ann} -> {ex.args}')
                    sys.exit(1)

        # Could override attribute values here
        # cls.a = 12
        # TODO: Maybe check that given parameters matched the schema?
        # Even a fuzzy search to suggest close matches

        cls._wrap(cls)
        # post init hook
        cls.post_init(cls)
        return cls

    def __init__(cls, name, bases, namespace, **kwds):
        # print('init')
        # cls.post_init(cls, namespace)
        super().__init__(name, bases, namespace)
        # cls.post_init(cls)


# class Foo:
#     def __get__(self, instance, owner):
#         print(instance)
#         print(owner)
#         return instance.bar


# class Schema(metaclass=MetaSchema):
#     print('<7>')
#
#     def post_init(self, *args):
#         pass
#
#     @property
#     def _fields(self):
#         fields = [
#             k for k in self.__dir__()
#             if not k.startswith('_')
#                and not inspect.ismethod(getattr(self, k))
#         ]
#         return fields

# class X(Schema):
#     print('<3>')
#     field = Foo()
#     bar: int = 1
#     p: Path = '/Users/foobar'
#     # p: Path = 0o755
#     platform: str = 'win'
#     mac_greet = 'oh hi Steve'
#     win_greet = 'oh hi Bill'
#     greet = None
#
#     def post_init(self, *args):
#         print('<5>')
#         print(f'post_init: {args}')
#         if self.platform == 'win':
#             self.greet = self.win_greet
#         else:
#             self.greet = self.mac_greet
#
# print('<0> ( Every thing is top-level/import time code before this )')
# m = X()
# print('<6>')
# # print(type(m.p))
# print(m.greet)
