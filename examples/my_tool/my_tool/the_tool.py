from my_tool import c


@c
class Cli:
    def foo(self):
        print(f'Here is the value of bing: {c.bing}')


def main():
    pass
