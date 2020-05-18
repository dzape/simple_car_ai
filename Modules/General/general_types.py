from enum import Enum, auto

class Move(Enum):

    LEFT = auto()
    RIGHT = auto()
    NONE = auto()

class Colors:

    LIGHTGREY = (100, 100, 100)
    DARKGREY = (40, 40, 40)
    GOLD = (139, 105, 20)
    YELLOW = (255, 255, 0)
    LIGHTBROWN = (238, 207, 161)
