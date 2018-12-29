import pygame
from .core import Rect


class Drawable:
    def __init__(self, image: pygame.Surface, rect: Rect):
        self.image: pygame.Surface = image
        self.rect: Rect = rect

    def draw(self, on_surface: pygame.Surface):
        if self.image is not None:
            on_surface.blit(self.image, self.rect)
