import pygame
from typing import Optional
from .core import Position, GridPosition, ScreenPosition, Rect
from .ActiveSprite import ActiveSprite
from .SpriteManager import load_asset
from .Settings import BOARD_WIDTH, BOARD_HEIGHT
from . import GameEngine


#: Screen surface for the game
screen = pygame.display.set_mode((1440, 850))

#: Table background. Full screen size
background_rect = Rect(x=0, y=0, width=1440, height=850)

#: Board position
board_rect = Rect(x=50, y=50, width=1024, height=741)

#: Score board
score_rect = Rect(
    x=board_rect.x + board_rect.width + 30, y=board_rect.y, width=280, height=170
)

#: Position for next tile to move
next_tile_rect = Rect(x=1183, y=292, width=117, height=117)

#: Position where to drop the tile to choose to move an adventurer instead
drop_rect = Rect(x=board_rect.x + board_rect.width + 30, y=520, width=280, height=280)

#: The sprite for the background
background_sprite = ActiveSprite(image=load_asset("background"), rect=background_rect)

#: The sprite for the board
board_sprite = ActiveSprite(image=load_asset("board"), rect=board_rect)

#: The sprite for the drop area
drop_sprite = ActiveSprite(
    image=load_asset("drop_tile", keycolor=None, use_alpha=True), rect=drop_rect
)

#: The sprite for the score area
score_sprite = ActiveSprite(
    image=load_asset("score", keycolor=None, use_alpha=True), rect=score_rect
)

#: Position on the board image
top_left_tiles = Position(x=220, y=52)
bottom_left_tiles = Position(x=220, y=676)
top_right_tiles = Position(x=967, y=52)

#: Average size for a Cell on screen
tile_cell_rect = Rect(
    x=0,
    y=0,
    width=(top_right_tiles.x - top_left_tiles.x + 1) / (BOARD_WIDTH - 2),
    height=(bottom_left_tiles.y - top_left_tiles.y + 1) / (BOARD_HEIGHT - 2),
)


def iround(x: float) -> int:
    return int(round(x))


def grid_to_screen(grid_position: GridPosition) -> Rect:
    """
    Return the cell rect on the screen from the grid position.
    Takes into account the different size of top and bottom rows, left and right columns
    """
    _, _, width, height = tile_cell_rect
    # Leftmost column
    if grid_position.x == 0:
        x = top_left_tiles.x - 57
        width = 57
    # Rightmost column
    elif grid_position.x == BOARD_WIDTH - 1:
        x = top_left_tiles.x + width * (grid_position.x - 1)
        width = 57
    # Other columns
    else:
        x = top_left_tiles.x + width * (grid_position.x - 1)

    # Top row
    if grid_position.y == 0:
        y = top_left_tiles.y - 52
        height = 52
    # Bottom row
    elif grid_position.y == BOARD_HEIGHT - 1:
        y = top_left_tiles.y + height * (grid_position.y - 1)
        height = 52
    # Other row
    else:
        y = top_left_tiles.y + height * (grid_position.y - 1)
    return Rect(x=x + board_rect.x, y=y + board_rect.y, width=width, height=height)


def screen_to_grid(screen_position: ScreenPosition) -> Optional[GridPosition]:
    """
    Convert a screen position to the grid position
    """
    _, _, cell_width, cell_height = tile_cell_rect
    board_x = screen_position.x - board_rect.x
    board_y = screen_position.y - board_rect.y

    # x inside the tiles area
    if top_left_tiles.x <= board_x <= top_right_tiles.x:
        x = board_x - top_left_tiles.x
        x = x // int(cell_width) + 1
    # x in left column
    elif top_left_tiles.x - 57 <= board_x < top_left_tiles.x:
        x = 0
    # x in right column
    elif top_right_tiles.x < board_x:
        x = BOARD_WIDTH - 1
    else:
        x = None

    # y in tiles area
    if top_left_tiles.y <= board_y <= bottom_left_tiles.y:
        y = board_y - top_left_tiles.y
        y = y // int(cell_height) + 1
    # y in bottom row
    elif bottom_left_tiles.y <= board_y <= bottom_left_tiles.y + 52:
        y = BOARD_HEIGHT - 1
    # y in top row
    elif 0 <= board_y < top_left_tiles.y:
        y = 0
    else:
        y = None

    if x is None or y is None:
        return None
    return Position(x=x, y=y)


def render() -> None:
    """
    Render the current state of the engine.
    To simplify, we redraw the full screen each time
    """
    for obj in GameEngine.engine.objects:
        obj.draw(screen)
    pygame.display.flip()
