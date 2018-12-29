from .DragAndDropSprite import DragAndDropSprite
from .core import TileID, Position, Rect
from .Tile import Tile, tiles
from .SpriteManager import load_asset
from .Phase import Phase
from .Coordinates import center_rect
from . import GameEngine  # avoid circular imports
from . import Renderer


class TileSprite(DragAndDropSprite):
    def __init__(self, tile_id: TileID, rect: Rect, draggable: bool = False):
        """
        A renderable tile, that can be dragged and dropped.
        It contains all logic related to tiles.

        :param tile_id: Tile unique ID
        :param rect: Inital position of the tile
        :param draggable: Can be dragged and dropped
        """
        self.tile_id: Tile = tiles[tile_id]
        self.grid_position = None
        image = load_asset(f"tile_{tile_id:02d}")
        super().__init__(image, rect)
        self.draggable = draggable

    def on_mouse_down(self, mouse_pos: Position):
        # When in MOVE_NEXT_TILE
        # Start drag
        if GameEngine.engine.phase == Phase.MOVE_NEXT_TILE:
            super().on_mouse_down(mouse_pos)
            return
        # When in SELECT_ADVENTURER_DESTINATION
        # Check if click on this tile, then set the adventurer destination.
        if GameEngine.engine.phase == Phase.SELECT_ADVENTURER_DESTINATION:
            if self.rect.collidepoint(x=mouse_pos.x, y=mouse_pos.y):
                GameEngine.engine.set_adventurer_destination(self.grid_position)

    def on_mouse_move(self, mouse_pos: Position):
        # When in MOVE_NEXT_TILE
        # Move is dragged
        if GameEngine.engine.phase == Phase.MOVE_NEXT_TILE:
            super().on_mouse_move(mouse_pos)

    def on_mouse_up(self, mouse_pos: Position):
        # When in MOVE_NEXT_TILE
        # Release the tile if dragged
        if GameEngine.engine.phase == Phase.MOVE_NEXT_TILE and self.drag:
            # Case 1: in drop zone
            if Renderer.drop_rect.collidepoint(x=mouse_pos.x, y=mouse_pos.y):
                GameEngine.engine.drop_tile(self.tile_id)
                self.rect = center_rect(Renderer.drop_rect, self.image)
                self.drag = False
                self.draggable = False
                return
            # Case 2: in tile area
            grid_position = Renderer.screen_to_grid(mouse_pos)
            if grid_position is not None and GameEngine.engine.valid_tile_move(
                grid_position
            ):
                self.grid_position = grid_position
                # Get the exact position for the tile (center of the cell)
                cell_rect = Renderer.grid_to_screen(self.grid_position)
                self.rect = center_rect(cell_rect, self.image)
                # Add the tile to game state
                GameEngine.engine.add_tile(self.tile_id, grid_position)
                self.drag = False
                self.draggable = False
                return
            # Case 3: released elsewhere, reset position
            self.rect = Renderer.next_tile_rect
