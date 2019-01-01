from .DragAndDropSprite import DragAndDropSprite
from .core import TileID, Position, Rect
from .SpriteManager import load_asset
from .Phase import Phase
from . import GameEngine  # avoid circular imports
from . import Renderer


class MovableTileSprite(DragAndDropSprite):
    def __init__(self, tile_id: TileID, rect: Rect):
        """
        A renderable tile, that can be dragged and dropped.
        :param tile_id: Tile unique ID
        :param rect: Initial position of the tile
        """
        self.tile_id: TileID = tile_id
        image = load_asset(f"tile_{tile_id:02d}")
        super().__init__(image, rect)

    def on_mouse_down(self, mouse_pos: Position):
        if GameEngine.engine.phase == Phase.MOVE_NEXT_TILE:
            super().on_mouse_down(mouse_pos)

    def on_mouse_move(self, mouse_pos: Position):
        if GameEngine.engine.phase == Phase.MOVE_NEXT_TILE:
            super().on_mouse_move(mouse_pos)

    def on_mouse_up(self, mouse_pos: Position):
        # Release the tile if dragged
        if GameEngine.engine.phase == Phase.MOVE_NEXT_TILE and self.drag:
            # Case 1: in drop zone
            if Renderer.drop_area_rect.collidepoint(x=mouse_pos.x, y=mouse_pos.y):
                GameEngine.engine.drop_tile(self.tile_id)
                return
            # Case 2: in tile area
            grid_position = Renderer.screen_to_grid(mouse_pos)
            if grid_position is not None:
                GameEngine.engine.add_tile(self.tile_id, grid_position)
                return
            # Case 3: released elsewhere, reset position
            self.rect = Renderer.next_tile_rect
            self.drag = False
