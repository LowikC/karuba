import attr
from .Board import Board


@attr.s(auto_attribs=True)
class Player:
    #: The state of the player's board
    board: Board = Board()
    #: Current score
    score: int = 0
