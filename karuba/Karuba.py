import pygame
from . import GameEngine
from . import Renderer


def run():
    pygame.init()
    while GameEngine.engine.running:
        GameEngine.engine.process_events()
        Renderer.render()
