#: Total number of tiles. Tile IDs go from 1 to NUM_TILES
NUM_TILES = 36

#: Width of the board (including jungle and beach)
BOARD_WIDTH = 8

#: Height of the board (including jungle and beach)
BOARD_HEIGHT = 7

#: Number of possible positions for the temples
NUM_TEMPLES_POSITIONS = BOARD_WIDTH + BOARD_HEIGHT - 4

#: Number of possible positions for the adventurers
NUM_ADVENTURERS_POSITIONS = BOARD_WIDTH + BOARD_HEIGHT - 4

#: Minimum Manhattan distance between a adventurer and temple initial positions
MIN_DISTANCE_ADVENTURER_TEMPLE = 3
