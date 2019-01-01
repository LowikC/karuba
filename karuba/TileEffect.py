import pygame
from .core import GridPosition
from .Drawable import Drawable
from .SpriteManager import load_asset
from . import Renderer
from enum import Enum


class TileMove(Enum):
    VALID = 1
    INVALID = 2


class TileMoveEffect(Drawable):
    def __init__(self, grid_position: GridPosition):
        rect = Renderer.grid_to_screen(grid_position)
        self.image_valid: pygame.Surface = load_asset(
            "tile_valid", keycolor=None, use_alpha=True
        )
        self.image_invalid: pygame.Surface = load_asset(
            "tile_invalid", keycolor=None, use_alpha=True
        )
        self.grid_position: GridPosition = grid_position
        self.mode = None
        super().__init__(self.image_valid, rect)

    def set_valid_move(self):
        self.mode = TileMove.VALID

    def set_invalid_move(self):
        self.mode = TileMove.INVALID

    def reset_effect(self):
        self.mode = None

    def draw(self, on_surface: pygame.Surface):
        if self.mode == TileMove.VALID:
            on_surface.blit(self.image_valid, self.rect)
        elif self.mode == TileMove.INVALID:
            on_surface.blit(self.image_invalid, self.rect)
