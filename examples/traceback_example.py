from clima import c


@c
class Cli:
    def lumberjack(self):
        self.bright_side_of_death()

    def bright_side_of_death(self):
        print('An expected error: we intentionally raise an exception')
        print('to display the truncated error printing format')
        return tuple()[0]
