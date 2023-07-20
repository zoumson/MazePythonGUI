from enum import IntEnum, auto


# IntEnum is just plain integer, no need a translation to access the data value
class Role(IntEnum):
    NONE = 0
    ENEMY = auto()
    ENTRANCE = auto()
    EXIT = auto()
    EXTERIOR = auto()
    REWARD = auto()
    WALL = auto()
