"""Constants that the user can't change, but I might want to."""

# Colors
# WHITE = pygame.Color(255, 255, 255, 255)
# BLACK = pygame.Color(0, 0, 0, 255)
# RED = pygame.Color(255, 0, 0, 255)
# GREEN = pygame.Color(0, 255, 0, 255)
# BLUE = pygame.Color(0, 0, 255, 255)
# Performance
STAR_LIMIT = 100
FPS_LIMIT = 60
# Ship
SHIP_SPEED = 10  # pixels/frame
SHIP_HEALTH = 3
SHIP_LIVES = 3
DIAG_FACTOR = 2 ** 0.5 / 2  # (root2)/2
STAR_SPEED = 5
STAR_ACCELERATION = 0.5
MAX_SHIP_LEVEL = 8
SHIP_MERCY_INV = 60  # frames
# Bullets
PLAYER_BULLET_LIMIT = 100
PLAYER_BULLET_COOLDOWN = 6  # frames?
ENEMY_BULLET_LIMIT = 100
# Enemies
ENEMY_SPEEDS = [5, 4, 5, 1, 2, 3]
ENEMY_HEALTHS = [4, 9, 3, 8, 6, 4]
ENEMY_FIRE_COOLDOWNS = [-1, -1, 90, 90, 90, 90]
ENEMY_POINTS = [50, 100, 25, 75, 75, 75]
ENEMY_TIMER = 150  # 2.5 seconds before first enemy
ENEMY_TIMER_MIN = 20
PICKUP_CHANCE = 20  # percent