from clima import c, Schema

class S(Schema):
    foobar = 'default'
    verbose = True

@c
class C:
    def run(self):
        print(c.foobar)
