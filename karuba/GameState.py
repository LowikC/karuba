from typing import Dict, Set
from .core import TileID, Latitude
from .Color import Color
from .Player import Player
from .Settings import NUM_TILES


class GameState:
    def __init__(self):
        #: Position of the temples (by latitude)
        self.temples: Dict[Latitude, Color] = {}
        #: Start latitude of the adventurers
        self.adventurers_start: Dict[Latitude, Color] = {}
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
