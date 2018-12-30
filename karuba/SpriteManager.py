import os
import pygame


ASSETS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../assets/1440")


_assets_cache = {}


def load_asset(name, keycolor=(255, 0, 195), use_alpha=False):
    if name not in _assets_cache:
        im = pygame.image.load(os.path.join(ASSETS_DIR, name + ".png"))
        if keycolor is not None:
            im = im.convert()
            im.set_colorkey(keycolor)
        elif use_alpha:
            im = im.convert_alpha()
        _assets_cache[name] = im
    return _assets_cache[name]
