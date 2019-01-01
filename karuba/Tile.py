import attr
from .core import TileID
from typing import NamedTuple


class Ways(NamedTuple):
    left: bool = False
    bottom: bool = False
    right: bool = False
    top: bool = False


@attr.s(auto_attribs=True)
class Tile:
    #: UID of the Tile
    uid: TileID
    #: Has a cristal or not
    has_cristal: bool
    #: Has a gold or not
    has_gold: bool
    #: Opened sides
    ways: Ways


# Temp
tiles = {
    i: Tile(uid=1, has_cristal=False, has_gold=False, ways=Ways(left=True, right=True))
    for i in range(1, 37)
}

tilesb = {
    1: Tile(uid=1, has_cristal=False, has_gold=False, ways=Ways(left=True, right=True)),
    2: Tile(uid=2, has_cristal=False, has_gold=False, ways=Ways(left=True, right=True)),
    3: Tile(
        uid=3, has_cristal=True, has_gold=False, ways=Ways(bottom=True, right=True)
    ),
    4: Tile(uid=4, has_cristal=True, has_gold=False, ways=Ways(bottom=True, left=True)),
    5: Tile(
        uid=5,
        has_cristal=False,
        has_gold=False,
        ways=Ways(bottom=True, left=True, right=True),
    ),
    6: Tile(
        uid=6,
        has_cristal=False,
        has_gold=False,
        ways=Ways(bottom=True, left=True, right=True),
    ),
    7: Tile(
        uid=7,
        has_cristal=False,
        has_gold=False,
        ways=Ways(bottom=True, left=True, right=True, top=True),
    ),
    8: Tile(
        uid=8,
        has_cristal=False,
        has_gold=False,
        ways=Ways(bottom=True, left=True, right=True, top=True),
    ),
    9: Tile(uid=9, has_cristal=False, has_gold=False, ways=Ways(right=True, top=True)),
    10: Tile(uid=10, has_cristal=True, has_gold=False, ways=Ways(left=True, top=True)),
    11: Tile(
        uid=11,
        has_cristal=True,
        has_gold=False,
        ways=Ways(left=True, right=True, top=True),
    ),
    12: Tile(
        uid=12,
        has_cristal=False,
        has_gold=False,
        ways=Ways(left=True, right=True, top=True),
    ),
    13: Tile(
        uid=13, has_cristal=True, has_gold=False, ways=Ways(left=True, right=True)
    ),
    14: Tile(
        uid=14, has_cristal=False, has_gold=True, ways=Ways(left=True, right=True)
    ),
    15: Tile(
        uid=15, has_cristal=True, has_gold=False, ways=Ways(left=True, right=True)
    ),
    16: Tile(
        uid=16, has_cristal=False, has_gold=True, ways=Ways(left=True, right=True)
    ),
    17: Tile(
        uid=17, has_cristal=False, has_gold=False, ways=Ways(top=True, bottom=True)
    ),
    18: Tile(
        uid=18, has_cristal=False, has_gold=False, ways=Ways(top=True, bottom=True)
    ),
}
