from pathlib import Path
from clima import c, Schema
from my_tool.the_tool import main as main_tool


class Conf(Schema):
    bing = 'bang'
    CFG = Path.home() / '.my_tool.cfg'


c: Conf = c
