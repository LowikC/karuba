import attr
from .core import TileID


@attr.s(auto_attribs=True)
class Ways:
    left: bool
    top: bool
    right: bool
    bottom: bool


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
    i: Tile(
        uid=1,
        has_cristal=False,
        has_gold=False,
        ways=Ways(left=True, top=False, right=True, bottom=False),
    )
    for i in range(1, 37)
}
