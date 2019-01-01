import random
import pygame
from collections import OrderedDict
from typing import List, Dict, Optional
from .core import Latitude, TileID, GridPosition, Position, Rect
from .Color import Color
from .Phase import Phase
from .GameState import GameState
from .ActiveSprite import ActiveSprite
from .AdventurerSprite import AdventurerSprite
from .TempleSprite import TempleSprite
from .TileSprite import TileSprite
from .TileEffect import TileValidEffect, TileEffectMode
from .Tile import tiles
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
        #: Layers of renderable and active sprites
        self.layers: Dict[str, List[ActiveSprite]] = OrderedDict()
        #: Current phase
        self.phase: Phase = Phase.START

        self.selected_adventurer: Optional[Color] = None

        self.initialize()

    @property
    def objects(self):
        all_objects = []
        for layer, objs in self.layers.items():
            all_objects.extend(objs)
        return all_objects

    def initialize(self) -> None:
        self.layers = OrderedDict(
            static=[],
            tiles=[],
            tiles_effects=[],
            temples=[],
            adventurers=[],
            drop_tile=[],
            next_tile=[],
        )
        # Add static objects
        self.layers["static"] = [
            Renderer.background_sprite,
            Renderer.board_sprite,
            Renderer.score_sprite,
            Renderer.drop_sprite,
        ]

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
        self.layers["next_tile"] = [tile_sprite]
        self.phase = Phase.MOVE_NEXT_TILE

    def valid_tile_move(self, grid_position):
        if (
            1 <= grid_position.x <= BOARD_WIDTH - 2
            and 1 <= grid_position.y <= BOARD_HEIGHT - 2
        ):
            if self.state.player.board.get_tile(grid_position) is None:
                return True
        return False

    def set_temple_latitude(self, color: Color, latitude: Latitude) -> None:
        self.state.temples[latitude] = color
        # Add a sprite
        self.layers["temples"].append(TempleSprite(color=color, latitude=latitude))

    def set_adventurer_latitude(self, color: Color, latitude: Latitude) -> None:
        self.state.adventurers_start[latitude] = color
        # Add a sprite
        pos = Coordinates.adventurer_latitude_to_grid_position(latitude)
        self.layers["adventurers"].append(
            AdventurerSprite(color=color, grid_position=pos)
        )

    def remove_next_tile(self):
        self.layers["next_tile"] = []

    def add_tile(self, tile: TileSprite):
        self.state.player.board.add_tile(tile.tile_id, tile.grid_position)
        self.phase = Phase.SAMPLE_NEXT_TILE
        self.layers["tiles"].append(tile)
        self.layers["tiles_effects"].append(
            TileValidEffect(grid_position=tile.grid_position)
        )

    def drop_tile(self, tile: TileSprite):
        self.layers["drop_tile"] = [tile]
        self.remove_next_tile()
        self.phase = Phase.MOVE_ADVENTURER
        pass

    def reset_selected_adventurer(self):
        for adventurer in self.layers["adventurers"]:
            adventurer.selected = False
        for tile_effect in self.layers["tiles_effects"]:
            tile_effect.set_mode(TileEffectMode.NEUTRAL)
        self.selected_adventurer = None

    def set_selected_adventurer(self, color: Color):
        self.selected_adventurer = color
        self.update_tile_effects()

    def update_tile_effects(self):
        for tile_effect in self.layers["tiles_effects"]:
            if self.reachable(tile_effect.grid_position):
                tile_effect.set_mode(TileEffectMode.VALID)
            else:
                tile_effect.set_mode(TileEffectMode.INVALID)

    def reachable(self, grid_position: GridPosition):
        dropped_tile_id = self.layers["drop_tile"][0].tile_id
        num_moves = tiles[dropped_tile_id].num_ways()
        adv_position = self.state.player.board.adventurers[self.selected_adventurer]
        return self.state.player.board.connected(adv_position, grid_position, num_moves)

    def set_adventurer_destination(self, grid_position):
        pass

    def process_events(self):
        # Delegate mouse events to each object
        mouse_pos = Position(*pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for obj in self.objects:
                    obj.on_mouse_down(mouse_pos)

            if event.type == pygame.MOUSEBUTTONUP:
                for obj in self.objects:
                    obj.on_mouse_up(mouse_pos)

            if event.type == pygame.MOUSEMOTION:
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
