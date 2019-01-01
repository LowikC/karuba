import pygame
from .core import Position, GridPosition
from .ActiveSprite import ActiveSprite
from .Color import Color
from .Coordinates import center_rect
from .SpriteManager import load_asset
from .Renderer import grid_to_screen
from .Phase import Phase
from .Settings import BOARD_HEIGHT
from . import GameEngine


class AdventurerSprite(ActiveSprite):
    """
    Adventurer sprite.
    Use cases:
    - Selection when in phase SELECT_ADVENTURER_TO_MOVE
    """

    def __init__(self, color: Color, grid_position: GridPosition):
        self.image = load_asset(
            f"adventurer_{color.name}", keycolor=None, use_alpha=True
        )
        self.image_selected = load_asset(
            f"adventurer_{color.name}_selected", keycolor=None, use_alpha=True
        )
        self.set_grid_position(grid_position)
        self.color = color
        self.selected = False
        super().__init__(self.image, self.rect)

    def set_grid_position(self, grid_position: GridPosition):
        cell_rect = grid_to_screen(grid_position)
        rect = center_rect(cell_rect, self.image)
        if grid_position.y == BOARD_HEIGHT - 1:
            bottom = cell_rect.y + cell_rect.height
            bottom -= 5
            top = bottom - rect.height
            rect = rect._replace(y=top)
        self.rect = rect

    def on_mouse_down(self, mouse_pos: Position):
        if self.rect.collidepoint(x=mouse_pos.x, y=mouse_pos.y):
            if GameEngine.engine.phase == Phase.MOVE_ADVENTURER:
                if self.selected:
                    # already selected, no need to change anything
                    return
                GameEngine.engine.reset_selected_adventurer()
                self.selected = True
                GameEngine.engine.set_selected_adventurer(self.color)

    def draw(self, on_surface: pygame.Surface):
        if self.selected:
            on_surface.blit(self.image_selected, self.rect)
        else:
            on_surface.blit(self.image, self.rect)
