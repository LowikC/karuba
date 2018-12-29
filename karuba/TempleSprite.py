from .core import Latitude
from .Drawable import Drawable
from .Color import Color
from .SpriteManager import load_asset
from .Coordinates import temple_latitude_to_grid_position, center_rect
from .Renderer import grid_to_screen


class TempleSprite(Drawable):
    """
    No interactions
    """

    def __init__(self, latitude: Latitude, color: Color) -> None:
        if latitude < 60:
            image = load_asset(f"temple_horizontal_{color.name}")
        else:
            image = load_asset(f"temple_vertical_{color.name}")
        grid_position = temple_latitude_to_grid_position(latitude)
        cell_rect = grid_to_screen(grid_position)
        rect = center_rect(cell_rect, image)
        super().__init__(image, rect)
