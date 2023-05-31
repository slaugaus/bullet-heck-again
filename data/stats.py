import parameters as params


class Stats:
    """Variables that the game needs access to. Not to be confused with settings or parameters."""

    def __init__(self):
        # TODO load/save high score from file
        self.game_active = False
        self.done = False
        self.fps = 0
        self.reset_stats()

    def reset_stats(self):
        """Reset the stats that will change."""
        self.score = 0
        self.player_bullet_cooldown = 0
        self.ship_health = params.SHIP_HEALTH
        self.ship_lives = params.SHIP_LIVES
        self.ship_level = 8
        self.ship_inv = False
        self.ship_inv_timer = 1
        self.game_level = 1
        self.next_score = 0
        self.next_score_increment = 1000
        self.enemy_timer = params.ENEMY_TIMER
        self.next_enemy_timer = 120
