from clima import c, Schema

class Configuration(Schema):
    a: str = 'A'  # a description
    x: int = 1  # x description

@c
class Cli:
    def foo(self):
        # using configuration
        print(c.a)

