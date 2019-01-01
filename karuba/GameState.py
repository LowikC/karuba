from typing import Dict, Set
from .core import TileID, Latitude
from .Color import Color
from .Player import Player
from .Settings import NUM_TILES
from . import Coordinates


class GameState:
    def __init__(self):
        #: Latitude of the temples (by color)
        self.temples: Dict[Color, Latitude] = {}
        #: Start latitude of the adventurers (by color)
        self.adventurers_start: Dict[Color, Latitude] = {}
        #: Tiles IDs not played yet
        self.remaining_tiles_ids: Set[TileID] = set(range(1, NUM_TILES + 1))
        #: Next tile id for the players
        self.next_tile_id: TileID = None
        #: Player state (tiles + adventurers + score)
        self.player: Player = Player()

    def dump(self, filename):
        raise NotImplementedError()

    def load(self, filename):
        raise NotImplementedError()

    def set_adventurer_latitude(self, color: Color, latitude: Latitude) -> None:
        self.adventurers_start[color] = latitude
        position = Coordinates.adventurer_latitude_to_grid_position(latitude)
        self.player.board.add_adventurer(color, position)

    def set_temple_latitude(self, color: Color, latitude: Latitude) -> None:
        self.temples[color] = latitude
        position = Coordinates.temple_latitude_to_grid_position(latitude)
        self.player.board.add_temple(color, position)
