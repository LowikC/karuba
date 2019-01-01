import logging
from typing import Optional, List, Dict
from .core import GridPosition, TileID, Position
from .Tile import Tile, tiles, Direction
from .Color import Color
from .Settings import BOARD_WIDTH, BOARD_HEIGHT
from .Graph import Graph, shortest_path, connect


def grid_to_index(grid_position: GridPosition) -> int:
    """
    Convert grid position to array index
    """
    return grid_position.x + grid_position.y * BOARD_WIDTH


def index_to_grid(index: int) -> GridPosition:
    return GridPosition(x=index % BOARD_WIDTH, y=index // BOARD_WIDTH)


def is_border(index: int):
    position = index_to_grid(index)
    return (
        position.x == 0
        or position.x == BOARD_WIDTH - 1
        or position.y == 0
        or position.y == BOARD_HEIGHT - 1
    )


dx = {Direction.LEFT: -1, Direction.BOTTOM: 0, Direction.RIGHT: 1, Direction.TOP: 0}


dy = {Direction.LEFT: 0, Direction.BOTTOM: 1, Direction.RIGHT: 0, Direction.TOP: -1}


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
        #: Graph representing board
        self.graph: Graph = {i: set() for i in range(BOARD_HEIGHT * BOARD_WIDTH)}

    def get_tile(self, grid_position: GridPosition) -> Optional[Tile]:
        index = grid_to_index(grid_position)
        if 0 <= index < len(self.tiles_ids):
            return self.tiles_ids[index]
        return None

    def add_tile(self, tile_id: TileID, grid_position: GridPosition):
        index = grid_to_index(grid_position)
        assert 0 <= index < len(self.tiles_ids)
        self.tiles_ids[index] = tile_id

        # Update the graph
        tile = tiles[tile_id]
        logging.debug(f"Add tile at index: {index}")
        for d in Direction:
            if tile.ways[d.value]:
                next_index = grid_to_index(
                    Position(grid_position.x + dx[d], grid_position.y + dy[d])
                )
                if is_border(next_index):
                    connect(self.graph, next_index, index)
                    logging.debug(f"Connect with index: {next_index} (border)")
                elif self.tiles_ids[next_index] is not None:
                    next_tile = tiles[self.tiles_ids[next_index]]
                    if next_tile.ways[d.opposite().value]:
                        connect(self.graph, next_index, index)
                        logging.debug(f"Connect with index: {next_index}")
        logging.debug(f"Updated graph: {self.graph}")

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

    def get_path(
        self, start: GridPosition, end: GridPosition
    ) -> Optional[List[GridPosition]]:
        index_start = grid_to_index(start)
        index_end = grid_to_index(end)
        path = shortest_path(self.graph, index_start, index_end)
        logging.debug(f"Path from {index_start} to {index_end}: {path}")
        if path is not None:
            path = [index_to_grid(p) for p in path]
        return path

    def connected(self, start: GridPosition, end: GridPosition, num_moves: int):
        path = self.get_path(start, end)
        if path is None:
            return False
        num_moves_required = len(self.get_path(start, end)) - 1
        return num_moves_required <= num_moves
