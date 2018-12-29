import random
import pygame
from typing import List
from .core import Latitude, TileID, GridPosition, Position
from .Color import Color
from .Phase import Phase
from .GameState import GameState
from .ActiveSprite import ActiveSprite
from .TileSprite import TileSprite
from .TileEffect import TileValidEffect
from .Settings import MIN_DISTANCE_ADVENTURER_TEMPLE, BOARD_WIDTH, BOARD_HEIGHT
from . import Coordinates
from . import Renderer


def valid_start(adv_latitude: Latitude, temple_latitude: Latitude) -> bool:
    """
    Check if the temple latitude is valid
    """
    adv_position = Coordinates.adventurer_latitude_to_grid_position(adv_latitude)
    temple_position = Coordinates.adventurer_latitude_to_grid_position(temple_latitude)
    distance = Coordinates.manhattan_distance(adv_position, temple_position)
    return distance >= MIN_DISTANCE_ADVENTURER_TEMPLE + 1


class GameEngine:
    def __init__(self):
        #: To know when to quit
        self.running: bool = True
        #: Full game state
        self.state: GameState = GameState()
        #: Renderable and active objects
        self.objects: List[ActiveSprite] = []
        #: Current phase
        self.phase: Phase = Phase.START

        self.initialize()

    def initialize(self) -> None:
        # Add static objects
        self.objects.append(Renderer.background_sprite)
        self.objects.append(Renderer.board_sprite)
        # Add tile effects (default is neutral)
        for x in range(1, BOARD_WIDTH - 1):
            for y in range(1, BOARD_HEIGHT - 1):
                self.objects.append(TileValidEffect(grid_position=Position(x=x, y=y)))
        # Should add score + drop zone + marker for next tile
        self.choose_random_start()
        self.choose_next_tile()

    def choose_random_start(self) -> None:
        adventurers_latitudes = set(range(10, 120, 10))
        temples_latitudes = set(range(10, 120, 10))
        for color in Color:
            adv_latitude = random.choice(list(adventurers_latitudes))
            temple_latitude = random.choice(list(temples_latitudes))
            while not valid_start(adv_latitude, temple_latitude):
                temple_latitude = random.choice(list(temples_latitudes))
            self.set_adventurer_latitude(color, adv_latitude)
            self.set_temple_latitude(color, temple_latitude)
            adventurers_latitudes.remove(adv_latitude)
            temples_latitudes.remove(temple_latitude)
        for latitude, color in self.state.adventurers_start.items():
            grid_pos = Coordinates.adventurer_latitude_to_grid_position(latitude)
            self.state.player.board.add_adventurer(color, grid_pos)
        self.phase = Phase.SAMPLE_NEXT_TILE

    def choose_next_tile(self):
        assert self.phase == Phase.SAMPLE_NEXT_TILE
        tile_id = random.choice(list(self.state.remaining_tiles_ids))
        self.state.next_tile_id = tile_id
        self.state.remaining_tiles_ids.remove(tile_id)
        tile_sprite = TileSprite(tile_id, Renderer.next_tile_rect, draggable=True)
        self.objects.append(tile_sprite)
        self.phase = Phase.MOVE_NEXT_TILE

    def valid_tile_move(self, grid_position):
        if (
            1 <= grid_position.x <= BOARD_WIDTH - 2
            and 1 <= grid_position.y <= BOARD_HEIGHT - 2
        ):
            if self.state.player.board.get_tile(grid_position) is None:
                return True
        return False

    def set_temple_latitude(self, temple: Color, latitude: Latitude) -> None:
        self.state.temples[latitude] = temple

    def set_adventurer_latitude(self, adventurer: Color, latitude: Latitude) -> None:
        self.state.adventurers_start[latitude] = adventurer

    def add_tile(self, tile_id: TileID, grid_position: GridPosition):
        self.state.player.board.add_tile(tile_id, grid_position)
        self.phase = Phase.SAMPLE_NEXT_TILE

    def drop_tile(self, tile_id: TileID):
        self.phase = Phase.SAMPLE_NEXT_TILE
        pass

    def set_adventurer_destination(self, grid_position):
        pass

    def process_events(self):
        # Delegate mouse events to each object
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = Position(*pygame.mouse.get_pos())
                for obj in self.objects:
                    obj.on_mouse_down(mouse_pos)

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = Position(*pygame.mouse.get_pos())
                for obj in self.objects:
                    obj.on_mouse_up(mouse_pos)

            if event.type == pygame.MOUSEMOTION:
                mouse_pos = Position(*pygame.mouse.get_pos())
                for obj in self.objects:
                    obj.on_mouse_move(mouse_pos)

            if event.type == pygame.QUIT:
                for obj in self.objects:
                    obj.on_quit()
                self.running = False

        # Manage the phases
        if self.phase == Phase.SAMPLE_NEXT_TILE:
            self.choose_next_tile()


#: Singleton engine
engine = GameEngine()
