import random
import pygame
from typing import List, Optional
from .core import Latitude, GridPosition, Position, TileID
from .Color import Color
from .Phase import Phase
from .GameState import GameState
from .Drawable import Drawable
from .ActiveSprite import ActiveSprite
from .AdventurerSprite import AdventurerSprite
from .TempleSprite import TempleSprite
from .TileSprite import TileSprite, BoardTileSprite
from .MovableTileSprite import MovableTileSprite
from .TileEffect import TileMoveEffect
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


class Layers:
    def __init__(self):
        self.static: List[ActiveSprite] = []
        self.tiles: List[BoardTileSprite] = []
        self.tiles_effects: List[TileMoveEffect] = []
        self.temples: List[TempleSprite] = []
        self.adventurers: List[AdventurerSprite] = []
        self.dropped_tile: Optional[TileSprite] = None
        self.next_tile: Optional[MovableTileSprite] = None

    @property
    def drawables(self) -> List[Drawable]:
        all_drawables = (
            self.static
            + self.tiles
            + self.tiles_effects
            + self.temples
            + self.adventurers
        )
        if self.dropped_tile is not None:
            all_drawables.append(self.dropped_tile)
        if self.next_tile is not None:
            all_drawables.append(self.next_tile)
        return all_drawables

    @property
    def dynamics(self) -> List[ActiveSprite]:
        all_dynamics = self.tiles + self.temples + self.adventurers
        if self.next_tile is not None:
            all_dynamics.append(self.next_tile)
        return all_dynamics


class GameEngine:
    def __init__(self):
        #: To know when to quit
        self.running: bool = True
        #: Full game state
        self.state: GameState = GameState()
        #: Layers of renderable and active sprites
        self.layers: Layers = Layers()
        #: Current phase
        self.phase: Phase = Phase.START

        self.selected_adventurer: Optional[Color] = None

        self.initialize()

    @property
    def drawables(self) -> List[Drawable]:
        return self.layers.drawables

    @property
    def dynamics(self) -> List[ActiveSprite]:
        return self.layers.dynamics

    def initialize(self) -> None:
        # Add static objects
        self.layers.static = [
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
        self.phase = Phase.SAMPLE_NEXT_TILE

    def choose_next_tile(self):
        assert self.phase == Phase.SAMPLE_NEXT_TILE
        tile_id = random.choice(list(self.state.remaining_tiles_ids))
        self.state.next_tile_id = tile_id
        self.state.remaining_tiles_ids.remove(tile_id)
        tile_sprite = MovableTileSprite(tile_id, Renderer.next_tile_rect)
        self.layers.next_tile = tile_sprite
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
        self.state.set_temple_latitude(color, latitude)
        # Add a sprite
        self.layers.temples.append(TempleSprite(color=color, latitude=latitude))

    def set_adventurer_latitude(self, color: Color, latitude: Latitude) -> None:
        # Modify game state
        self.state.set_adventurer_latitude(color, latitude)
        # Add a sprite
        pos = Coordinates.adventurer_latitude_to_grid_position(latitude)
        self.layers.adventurers.append(AdventurerSprite(color=color, grid_position=pos))

    def remove_next_tile(self):
        self.layers.next_tile = None

    def add_tile(self, tile_id: TileID, grid_position: GridPosition):
        if not self.valid_tile_move(grid_position):
            return
        self.state.player.board.add_tile(tile_id, grid_position)
        self.phase = Phase.SAMPLE_NEXT_TILE
        self.layers.tiles.append(BoardTileSprite(tile_id, grid_position))
        self.layers.tiles_effects.append(TileMoveEffect(grid_position=grid_position))
        self.remove_next_tile()

    def drop_tile(self, tile_id: TileID):
        self.layers.dropped_tile = TileSprite(
            tile_id=tile_id, rect=Renderer.dropped_tile_rect
        )
        self.remove_next_tile()
        self.phase = Phase.MOVE_ADVENTURER
        pass

    def reset_selected_adventurer(self):
        for adventurer in self.layers.adventurers:
            adventurer.selected = False
        for tile_effect in self.layers.tiles_effects:
            tile_effect.reset_effect()
        self.selected_adventurer = None

    def set_selected_adventurer(self, color: Color):
        self.selected_adventurer = color
        self.update_tile_effects()

    def update_tile_effects(self):
        for tile_effect in self.layers.tiles_effects:
            if self.is_valid_adventurer_move(tile_effect.grid_position):
                tile_effect.set_valid_move()
            else:
                tile_effect.set_invalid_move()

    def is_valid_adventurer_move(self, grid_position: GridPosition):
        dropped_tile_id = self.layers.dropped_tile.tile_id
        num_moves = tiles[dropped_tile_id].num_ways()
        return self.state.player.board.is_valid_adventurer_move(
            self.selected_adventurer, grid_position, num_moves
        )

    def set_adventurer_destination(self, grid_position):
        if self.selected_adventurer is None:
            return
        if not self.is_valid_adventurer_move(grid_position):
            return
        self.state.player.board.move_adventurer(self.selected_adventurer, grid_position)
        for adv in self.layers.adventurers:
            if adv.color == self.selected_adventurer:
                adv.move(grid_position)

        self.reset_selected_adventurer()
        self.phase = Phase.SAMPLE_NEXT_TILE

    def process_events(self):
        # Delegate mouse events to each object
        mouse_pos = Position(*pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for obj in self.dynamics:
                    obj.on_mouse_down(mouse_pos)

            if event.type == pygame.MOUSEBUTTONUP:
                for obj in self.dynamics:
                    obj.on_mouse_up(mouse_pos)

            if event.type == pygame.MOUSEMOTION:
                for obj in self.dynamics:
                    obj.on_mouse_move(mouse_pos)

            if event.type == pygame.QUIT:
                for obj in self.dynamics:
                    obj.on_quit()
                self.running = False

        # Manage the phases
        if self.phase == Phase.SAMPLE_NEXT_TILE:
            self.choose_next_tile()


#: Singleton engine
engine = GameEngine()
