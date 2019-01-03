import pygame
from .ActiveSprite import ActiveSprite
from .core import TileID, Position, GridPosition, Rect
from .Tile import Quadrant, tiles
from .SpriteManager import load_asset
from .Phase import Phase
from .Coordinates import center_rect
from . import GameEngine  # avoid circular imports
from . import Renderer


treasure_positions = {
    Quadrant.BOTTOM: Position(x=60, y=92),
    Quadrant.TOP_RIGHT: Position(x=80, y=26),
    Quadrant.BOTTOM_LEFT: Position(x=35, y=95),
    Quadrant.BOTTOM_RIGHT: Position(x=80, y=95),
    Quadrant.RIGHT: Position(x=90, y=59),
}


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
        self.gold = load_asset("gold")
        self.cristal = load_asset("cristal")
        self.grid_position: GridPosition = position

    def on_mouse_down(self, mouse_pos: Position):
        # When in SELECT_ADVENTURER_DESTINATION
        # Check if click on this tile, then set the adventurer destination.
        if GameEngine.engine.phase == Phase.MOVE_ADVENTURER:
            if self.rect.collidepoint(x=mouse_pos.x, y=mouse_pos.y):
                GameEngine.engine.set_adventurer_destination(self.grid_position)

    def _draw_treasure(self, on_surface: pygame.Surface):
        gold_quadrant = tiles[self.tile_id].gold
        cristal_quadrant = tiles[self.tile_id].cristal
        if gold_quadrant is None and cristal_quadrant is None:
            return
        else:
            if gold_quadrant is not None:
                center = treasure_positions[tiles[self.tile_id].gold]
                img_treasure = self.gold
            else:
                center = treasure_positions[tiles[self.tile_id].cristal]
                img_treasure = self.cristal

            rect = img_treasure.get_rect()
            _, _, width, height = rect
            xc = width // 2
            yc = height // 2
            rect = Rect(
                x=self.rect.x + center.x - xc,
                y=self.rect.y + center.y - yc,
                width=rect.width,
                height=rect.height,
            )
            on_surface.blit(img_treasure, rect)

    def draw(self, on_surface: pygame.Surface):
        super().draw(on_surface)
        self._draw_treasure(on_surface)
