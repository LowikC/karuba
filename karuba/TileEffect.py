import pygame
from .core import GridPosition
from .ActiveSprite import ActiveSprite
from .SpriteManager import load_asset
from . import Renderer
from enum import Enum


class TileEffectMode(Enum):
    NEUTRAL = 0
    VALID = 1
    INVALID = 2


class TileValidEffect(ActiveSprite):
    def __init__(self, grid_position: GridPosition):
        rect = Renderer.grid_to_screen(grid_position)
        self.image_valid: pygame.Surface = load_asset(
            "tile_valid", keycolor=None, use_alpha=True
        )
        self.image_invalid: pygame.Surface = load_asset(
            "tile_invalid", keycolor=None, use_alpha=True
        )
        self.grid_position: GridPosition = grid_position
        self.mode = TileEffectMode.NEUTRAL
        super().__init__(None, rect)

    def set_mode(self, mode: TileEffectMode):
        self.mode = mode

    def draw(self, on_surface: pygame.Surface):
        if self.mode == TileEffectMode.VALID:
            on_surface.blit(self.image_valid, self.rect)
        elif self.mode == TileEffectMode.INVALID:
            on_surface.blit(self.image_invalid, self.rect)
