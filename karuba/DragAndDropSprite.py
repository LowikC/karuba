import pygame
from .ActiveSprite import ActiveSprite
from .core import ScreenPosition, Rect, Position


class DragAndDropSprite(ActiveSprite):
    def __init__(self, image: pygame.Surface, rect: Rect):
        super().__init__(image, rect)
        self.draggable = True
        self.drag: bool = False
        self.mouse_offset = Position(x=0, y=0)

    def on_mouse_down(self, mouse_pos: ScreenPosition):
        if not self.draggable:
            return
        if self.rect.collidepoint(x=mouse_pos.x, y=mouse_pos.y):
            top_left = Position(x=self.rect.x, y=self.rect.y)
            self.mouse_offset = top_left - mouse_pos
            self.drag = True

    def on_mouse_up(self, mouse_pos: ScreenPosition):
        if not self.draggable:
            return
        self.drag = False

    def on_mouse_move(self, mouse_pos: ScreenPosition):
        if not self.draggable:
            return
        if self.drag:
            top_left = mouse_pos + self.mouse_offset
            self.rect = self.rect._replace(x=top_left.x, y=top_left.y)
