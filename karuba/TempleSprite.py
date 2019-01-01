from .core import Latitude, ScreenPosition
from .ActiveSprite import ActiveSprite
from .Color import Color
from .Phase import Phase
from .SpriteManager import load_asset
from .Coordinates import temple_latitude_to_grid_position, center_rect
from .Renderer import grid_to_screen
from . import GameEngine


class TempleSprite(ActiveSprite):
    """
    Can be clicked to select the adventurer move.
    """

    def __init__(self, color: Color, latitude: Latitude) -> None:
        if latitude <= 60:
            image = load_asset(
                f"temple_horizontal_{color.name}", keycolor=None, use_alpha=True
            )
        else:
            image = load_asset(
                f"temple_vertical_{color.name}", keycolor=None, use_alpha=True
            )
        self.grid_position = temple_latitude_to_grid_position(latitude)
        cell_rect = grid_to_screen(self.grid_position)
        rect = center_rect(cell_rect, image)
        super().__init__(image, rect)

    def on_mouse_down(self, mouse_pos: ScreenPosition):
        if GameEngine.engine.phase == Phase.MOVE_ADVENTURER:
            if self.rect.collidepoint(x=mouse_pos.x, y=mouse_pos.y):
                GameEngine.engine.set_adventurer_destination(self.grid_position)
