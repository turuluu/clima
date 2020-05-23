from clima import c, Schema


class Configuration(Schema):
    a: str = 'A'  # a description
    x: int = 1  # x description


# Hack to enable autocompletion in IDEs
c: Configuration = c
