from enum import Enum


class Phase(Enum):
    START = 0
    SAMPLE_NEXT_TILE = 1
    MOVE_NEXT_TILE = 2
    MOVE_ADVENTURER = 3
    END = 4
