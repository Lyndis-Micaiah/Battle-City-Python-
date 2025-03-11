"""
Constants used throughout the game
"""
# Screen settings
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60
TILE_SIZE = 32

# Game settings
PLAYER_LIVES = 3
LEVEL_COUNT = 3

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

# Tank settings
PLAYER_SPEED = 2
ENEMY_SPEED = 1
BULLET_SPEED = 4
ENEMY_SPAWN_DELAY = 3000  # milliseconds
MAX_ENEMIES_ON_SCREEN = 4
MAX_ENEMY_COUNT = 20

# Direction constants
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

# Tank types
BASIC_TANK = 0
FAST_TANK = 1
POWER_TANK = 2
ARMOR_TANK = 3

# Tile types
EMPTY = 0
BRICK = 1
STEEL = 2
WATER = 3
GRASS = 4
ICE = 5
BASE = 6

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
VICTORY = 3
PAUSE = 4

# Power-up types
SHIELD = 0
FREEZE = 1
EXTRA_LIFE = 2
GRENADE = 3
HELMET = 4
CLOCK = 5
SHOVEL = 6
STAR = 7

# Sound effects
TANK_MOVE_SOUND = "tank_move"
TANK_FIRE_SOUND = "tank_fire"
EXPLOSION_SOUND = "explosion"
BRICK_HIT_SOUND = "brick_hit"
STEEL_HIT_SOUND = "steel_hit"
POWER_UP_SOUND = "power_up"
GAME_START_SOUND = "game_start"
GAME_OVER_SOUND = "game_over"
