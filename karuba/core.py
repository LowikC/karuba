from typing import NamedTuple


class Position(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Position") -> "Position":
        return Position(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other):
        return Position(x=self.x - other.x, y=self.y - other.y)

    def __neg__(self):
        return Position(x=-self.x, y=-self.y)


class Rect(NamedTuple):
    x: int
    y: int
    width: int
    height: int

    def collidepoint(self, x: int, y: int) -> bool:
        return (
            self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
        )


#: Position in the grid (in cells).
GridPosition = Position

#: Position on the screen (in pixels)
ScreenPosition = Position

#: Tile Identifier. From 1 to NUM_TILES
TileID = int

#: Latitude for temple or adventurer. From 10 to 110.
Latitude = int
