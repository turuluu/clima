from clima import c


@c
class Cli:
    def lumberjack(self):
        self.bright_side_of_life()

    def bright_side_of_life(self):
        print('An expected error: we intentionally raise an exception')
        print('to display the truncated error printing format')
        return tuple()[0]
