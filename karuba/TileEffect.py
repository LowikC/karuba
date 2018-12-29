import pygame
from .core import Position, GridPosition
from .ActiveSprite import ActiveSprite
from .SpriteManager import load_asset
from .Phase import Phase
from . import GameEngine
from . import Renderer


class TileValidEffect(ActiveSprite):
    def __init__(self, grid_position: GridPosition):
        rect = Renderer.grid_to_screen(grid_position)
        self.image_valid: pygame.Surface = load_asset("tile_valid")
        self.image_invalid: pygame.Surface = load_asset("tile_invalid")
        self.grid_position: GridPosition = grid_position
        super().__init__(None, rect)

    def on_mouse_move(self, mouse_pos: Position):
        self.image = None
        if GameEngine.engine.phase == Phase.MOVE_NEXT_TILE:
            if self.rect.collidepoint(x=mouse_pos.x, y=mouse_pos.y):
                grid_position = Renderer.screen_to_grid(mouse_pos)
                if GameEngine.engine.valid_tile_move(grid_position):
                    self.image = self.image_valid
                else:
                    self.image = self.image_invalid
