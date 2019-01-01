import attr
from .core import TileID
from typing import NamedTuple, Optional
from enum import Enum


class Direction(Enum):
    LEFT = 0
    BOTTOM = 1
    RIGHT = 2
    TOP = 3

    def opposite(self):
        return Direction((self.value + 2) % 4)


class Ways(NamedTuple):
    left: bool = False
    bottom: bool = False
    right: bool = False
    top: bool = False

    def num_ways(self) -> int:
        return self.left + self.right + self.top + self.bottom


class Quadrant(Enum):
    TOP_RIGHT = 0
    RIGHT = 1
    BOTTOM_RIGHT = 2
    BOTTOM = 3
    BOTTOM_LEFT = 4
    LEFT = 5
    TOP_LEFT = 6
    TOP = 7


@attr.s(auto_attribs=True)
class Tile:
    #: UID of the Tile
    uid: TileID
    #: Opened sides
    ways: Ways
    #: Has a cristal or not
    cristal: Optional[Quadrant] = None
    #: Has a gold or not
    gold: Optional[Quadrant] = None

    def num_ways(self) -> int:
        return self.ways.num_ways()


tiles = {
    1: Tile(uid=1, ways=Ways(left=True, right=True)),
    2: Tile(uid=2, ways=Ways(left=True, right=True)),
    3: Tile(uid=3, ways=Ways(bottom=True, right=True), cristal=Quadrant.TOP_RIGHT),
    4: Tile(uid=4, ways=Ways(bottom=True, left=True), cristal=Quadrant.TOP_RIGHT),
    5: Tile(uid=5, ways=Ways(bottom=True, left=True, right=True)),
    6: Tile(uid=6, ways=Ways(bottom=True, left=True, right=True)),
    7: Tile(uid=7, ways=Ways(bottom=True, left=True, right=True, top=True)),
    8: Tile(uid=8, ways=Ways(bottom=True, left=True, right=True, top=True)),
    9: Tile(uid=9, ways=Ways(right=True, top=True), cristal=Quadrant.BOTTOM_LEFT),
    10: Tile(uid=10, ways=Ways(left=True, top=True), cristal=Quadrant.BOTTOM_RIGHT),
    11: Tile(
        uid=11, ways=Ways(left=True, right=True, top=True), cristal=Quadrant.BOTTOM
    ),
    12: Tile(uid=12, ways=Ways(left=True, right=True, top=True)),
    13: Tile(uid=13, ways=Ways(left=True, right=True), cristal=Quadrant.BOTTOM),
    14: Tile(uid=14, ways=Ways(left=True, right=True), gold=Quadrant.BOTTOM),
    15: Tile(uid=15, ways=Ways(left=True, right=True), cristal=Quadrant.BOTTOM),
    16: Tile(uid=16, ways=Ways(left=True, right=True), gold=Quadrant.BOTTOM),
    17: Tile(uid=17, ways=Ways(top=True, bottom=True)),
    18: Tile(uid=18, ways=Ways(top=True, bottom=True)),
    19: Tile(uid=19, ways=Ways(right=True, left=True)),
    20: Tile(uid=20, ways=Ways(right=True, left=True)),
    21: Tile(uid=21, ways=Ways(right=True, bottom=True)),
    22: Tile(uid=22, ways=Ways(left=True, bottom=True)),
    23: Tile(uid=23, ways=Ways(right=True, top=True, bottom=True)),
    24: Tile(uid=24, ways=Ways(left=True, top=True, bottom=True)),
    25: Tile(uid=25, ways=Ways(left=True, top=True, bottom=True, right=True)),
    26: Tile(uid=26, ways=Ways(left=True, top=True, bottom=True, right=True)),
    27: Tile(uid=27, ways=Ways(top=True, right=True), cristal=Quadrant.BOTTOM),
    28: Tile(uid=28, ways=Ways(top=True, left=True)),
    29: Tile(uid=29, ways=Ways(top=True, bottom=True, right=True)),
    30: Tile(uid=30, ways=Ways(top=True, bottom=True, left=True)),
    31: Tile(uid=31, ways=Ways(top=True, bottom=True), cristal=Quadrant.RIGHT),
    32: Tile(uid=32, ways=Ways(top=True, bottom=True), gold=Quadrant.RIGHT),
    33: Tile(uid=33, ways=Ways(top=True, bottom=True), cristal=Quadrant.RIGHT),
    34: Tile(uid=34, ways=Ways(top=True, bottom=True), gold=Quadrant.RIGHT),
    35: Tile(uid=35, ways=Ways(top=True, bottom=True)),
    36: Tile(uid=36, ways=Ways(top=True, bottom=True)),
}
