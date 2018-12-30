from .core import Latitude
from .ActiveSprite import ActiveSprite
from .Color import Color
from .SpriteManager import load_asset
from .Coordinates import temple_latitude_to_grid_position, center_rect
from .Renderer import grid_to_screen


class TempleSprite(ActiveSprite):
    """
    No interactions
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
        grid_position = temple_latitude_to_grid_position(latitude)
        cell_rect = grid_to_screen(grid_position)
        rect = center_rect(cell_rect, image)
        super().__init__(image, rect)
