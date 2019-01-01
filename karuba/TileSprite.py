from .ActiveSprite import ActiveSprite
from .core import TileID, Position, GridPosition, Rect
from .SpriteManager import load_asset
from .Phase import Phase
from .Coordinates import center_rect
from . import GameEngine  # avoid circular imports
from . import Renderer


class TileSprite(ActiveSprite):
    def __init__(self, tile_id: TileID, rect: Rect):
        """
        A renderable tile, when on the board
        Can be clicked to select the adventurer move.

        :param tile_id: Tile unique ID
        :param rect: Screen position. Tile will be centered in the rect if the size is
            different from the tile image.
        """
        self.tile_id: TileID = tile_id
        image = load_asset(f"tile_{tile_id:02d}")
        rect = center_rect(rect, image)
        super().__init__(image, rect)


class BoardTileSprite(TileSprite):
    def __init__(self, tile_id: TileID, position: GridPosition):
        """
        A renderable tile, when on the board
        Can be clicked to select the adventurer move.

        :param tile_id: Tile unique ID
        :param position: Position on the grid
        """
        cell_rect = Renderer.grid_to_screen(position)
        super().__init__(tile_id, cell_rect)
        self.grid_position: GridPosition = position

    def on_mouse_down(self, mouse_pos: Position):
        # When in SELECT_ADVENTURER_DESTINATION
        # Check if click on this tile, then set the adventurer destination.
        if GameEngine.engine.phase == Phase.MOVE_ADVENTURER:
            if self.rect.collidepoint(x=mouse_pos.x, y=mouse_pos.y):
                GameEngine.engine.set_adventurer_destination(self.grid_position)
