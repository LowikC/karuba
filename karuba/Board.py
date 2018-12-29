from typing import Optional, List, Dict
from .core import GridPosition, TileID
from .Tile import Tile
from .Color import Color
from .Settings import BOARD_WIDTH, BOARD_HEIGHT


def grid_to_index(grid_position: GridPosition) -> int:
    """
    Convert grid position to array index
    """
    return grid_position.x + grid_position.y * BOARD_WIDTH


class Board:
    """
    Store the board state of a player.
    """

    def __init__(self):
        #: Ordered list of tiles IDs. Index 0 is the board position (1, 1).
        self.tiles_ids: List[Optional[TileID]] = [
            None for _ in range(BOARD_WIDTH * BOARD_HEIGHT)
        ]
        #: Current grid position of every adventurer (indexed by color)
        self.adventurers: Dict[Color, GridPosition] = {}
        #: Previous grid positions of every adventurer
        self.adventurers_tracks: Dict[Color, List[GridPosition]] = {}

    def get_tile(self, grid_position: GridPosition) -> Optional[Tile]:
        index = grid_to_index(grid_position)
        if 0 <= index < len(self.tiles_ids):
            return self.tiles_ids[index]
        return None

    def add_tile(self, tile_id: TileID, grid_position: GridPosition):
        index = grid_to_index(grid_position)
        assert 0 <= index < len(self.tiles_ids)
        self.tiles_ids[index] = tile_id

    def add_adventurer(self, color: Color, position: GridPosition):
        self.adventurers[color] = position
        self.adventurers_tracks[color] = [position]

    def move_adventurer(self, color: Color, new_position: GridPosition):
        path = self.get_path(self.adventurers[color], new_position)
        assert path
        assert new_position != self.adventurers[color]
        # path[0] contains the current position
        self.adventurers_tracks[color].extend(path[1:])
        self.adventurers[color] = new_position

    def valid_adventurer_move(self, color: Color, n_cells: int) -> bool:
        raise NotImplementedError()

    def take_treasure(self, grid_position) -> int:
        index = grid_to_index(grid_position)
        assert self.tiles_ids[index] is not None
        score = 0
        if self.tiles_ids[index].has_cristal:
            self.tiles_ids.has_cristal = False
            score += 1
        if self.tiles_ids[index].has_gold:
            self.tiles_ids[index].has_gold = False
            score += 2
        return score

    def get_path(self, start: GridPosition, end: GridPosition) -> List[GridPosition]:
        raise NotImplementedError()
