import os
from typing import Tuple
from .Tile import Tile, Quadrant
from PIL import Image, ImageDraw, ImageFont


CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
FONTS_DIR = os.path.join(os.path.dirname(CURRENT_DIR), "assets", "fonts")
FONT_FILENAME = os.path.join(FONTS_DIR, "StardosStencil-Regular.ttf")


def make_tile_asset(tile: Tile, size: Tuple[int, int]) -> Image:
    color = (255, 255, 255)
    thick = 11
    width, height = size
    im = Image.new(mode="RGB", size=size)
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(FONT_FILENAME, height // 4)

    middle = (width // 2, height // 2)
    if tile.ways.left:
        draw.line([(0, height // 2), middle], fill=color, width=thick)
    if tile.ways.right:
        draw.line([(width, height // 2), middle], fill=color, width=thick)
    if tile.ways.top:
        draw.line([(width // 2, 0), middle], fill=color, width=thick)
    if tile.ways.bottom:
        draw.line([(width // 2, height), middle], fill=color, width=thick)

    draw.text((5, 5), f"{tile.uid:02d}", fill=color, font=font)
    tw, th = draw.textsize(text=f"C.", font=font)
    position = {
        Quadrant.BOTTOM: (width // 2 - tw // 2, height // 2 + height // 4 - th // 2),
        Quadrant.RIGHT: (width // 2 + width // 4 - tw // 2, height // 2 - th // 2),
        Quadrant.BOTTOM_RIGHT: (
            width // 2 + width // 4 - tw // 2,
            height // 2 + height // 4 - th // 2,
        ),
        Quadrant.TOP_RIGHT: (width // 2 + width // 4 - tw // 2, height // 4 - th // 2),
        Quadrant.BOTTOM_LEFT: (
            width // 4 - tw // 2,
            height // 2 + height // 4 - th // 2,
        ),
    }
    if tile.cristal is not None:
        pos = position[tile.cristal]
        draw.text(pos, f"C.", fill=color, font=font)
    if tile.gold is not None:
        pos = position[tile.gold]
        draw.text(pos, f"G.", fill=color, font=font)
    return im
