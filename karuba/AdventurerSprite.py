from .core import Position
from .ActiveSprite import ActiveSprite
from .Coordinates import center_rect
from .SpriteManager import load_asset
from .Renderer import grid_to_screen
from .Phase import Phase
from . import GameEngine


class AdventurerSprite(ActiveSprite):
    """
    Adventurer sprite.
    Use cases:
    - Selection when in phase SELECT_ADVENTURER_TO_MOVE
    """

    def __init__(self, color, grid_position):
        image = load_asset(f"adventurer_{color.name}")
        cell_rect = grid_to_screen(grid_position)
        rect = center_rect(cell_rect, image)
        self.color = color
        self.selected = False
        super().__init__(image, rect)

    def on_mouse_down(self, mouse_pos: Position):
        if self.rect.collidepoint(x=mouse_pos.x, y=mouse_pos.y):
            if GameEngine.engine.phase == Phase.SELECT_ADVENTURER_TO_MOVE:
                if self.selected:
                    # already selected, no need to change anything
                    return
                # Unselect other adventurers
                for adv in GameEngine.engine.adventurers:
                    adv.selected = False
                GameEngine.engine.reset_selected_adventurer()
                self.selected = True
                GameEngine.engine.set_selected_adventurer(self.color)
