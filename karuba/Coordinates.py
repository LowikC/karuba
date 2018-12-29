import pygame
from .core import Latitude, Position, GridPosition, Rect


def adventurer_latitude_to_grid_position(latitude: Latitude) -> GridPosition:
    if 10 <= latitude <= 50:
        x = 0
        y = latitude // 10
    elif 60 <= latitude <= 110:
        latitude -= 50
        y = 6
        x = latitude // 10
    else:
        raise ValueError("Latitude must be between 10 and 110")
    return Position(x=x, y=y)


def temple_latitude_to_grid_position(latitude: Latitude) -> GridPosition:
    if 10 <= latitude <= 60:
        y = 0
        x = latitude // 10
    elif 70 <= latitude <= 110:
        latitude -= 60
        x = 7
        y = latitude // 10
    else:
        raise ValueError("Latitude must be between 10 and 110")
    return Position(x=x, y=y)


def manhattan_distance(a: Position, b: Position) -> int:
    """
    Return the Manhattan distance between 2 positions om the grid
    """
    return abs(a.x - b.x) + abs(a.y - b.y)


def center_rect(cell_rect: Rect, target: pygame.Surface):
    target_rect = target.get_rect()
    dx = (cell_rect.width - target_rect.width) // 2
    dy = (cell_rect.height - target_rect.height) // 2
    return Rect(
        x=cell_rect.x + dx,
        y=cell_rect.y + dy,
        width=target_rect.width,
        height=target_rect.height,
    )
