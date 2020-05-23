from clima import c, Schema
from pathlib import Path


class Configuration(Schema):
    a: str = 'A'  # a description
    x: int = 1  # x description
    p: Path = Path.cwd()  # target home directory

    def post_init(cls):
        # i: Schema = cls()
        print('post init')
        if cls.a == 'A':
            print('default "A" is set for c.a. Setting c.a to "123"')
            print('This should be cast as a string even if assigned as an integer')
            cls.a = 123


# Hack to enable autocompletion in IDEs
c: Configuration = c
