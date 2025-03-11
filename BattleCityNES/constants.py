# Battle City Game - Constants Module
# Game constants and configuration

# Screen dimensions
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480
TILE_SIZE = 16  # Size of one tile/cell in the game grid

# Game settings
TITLE = "Battle City NES Recreation"
FPS = 60
MAX_PLAYER_LIVES = 3

# Direction constants
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Tank types
BASIC_TANK = 1

# Tank settings
PLAYER_SPEED = 2
ENEMY_SPEED = 1
SHOOT_COOLDOWN = 30  # Frames between shots
BULLET_SPEED = 4
RESPAWN_INVULNERABLE_TIME = 180  # 3 seconds at 60 FPS

# Power-up settings
POWERUP_DURATION = 600  # 10 seconds at 60 FPS
POWERUP_SPAWN_CHANCE = 0.2  # 20% chance to spawn a powerup when a brick is destroyed
FREEZE_DURATION = 300  # 5 seconds at 60 FPS

# Effect settings
EXPLOSION_DURATION = 30  # 0.5 seconds at 60 FPS

# Tank types and their properties
TANK_TYPES = {
    0: {  # Player tank
        "speed": 2,
        "health": 1,
        "max_bullets": 2,
        "points": 0
    },
    1: {  # Basic enemy tank
        "speed": 1,
        "health": 1,
        "max_bullets": 1,
        "points": 100
    },
    2: {  # Fast enemy tank
        "speed": 2,
        "health": 1,
        "max_bullets": 1,
        "points": 200
    },
    3: {  # Heavy enemy tank
        "speed": 1,
        "health": 3,
        "max_bullets": 1,
        "points": 300
    },
    4: {  # Artillery enemy tank
        "speed": 1,
        "health": 1,
        "max_bullets": 2,
        "points": 400
    }
}
