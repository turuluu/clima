from clima import c, Schema
from pathlib import Path

@c
class Configuration(Schema):
    a: str = 'A'  # a description
    x: int = 1  # x description
    p: Path = Path.cwd()  # target home directory

    def post_init(cls):
        i: Schema = cls()
        print('post init')

        d = i._asdict().update({'p': Path(i.p)})
        print(repr(d))
        return cls(d)



# Hack to enable autocompletion in IDEs
c: Configuration = c

