from .core import ScreenPosition
from .Drawable import Drawable


class ActiveSprite(Drawable):
    """
    Drawable Sprite that reacts to Mouse events.
    """

    def on_mouse_down(self, mouse_pos: ScreenPosition):
        pass

    def on_mouse_up(self, mouse_pos: ScreenPosition):
        pass

    def on_mouse_move(self, mouse_pos: ScreenPosition):
        pass

    def on_quit(self):
        pass
