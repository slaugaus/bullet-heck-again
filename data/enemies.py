"""Enemies and enemy accessories"""

import arcade
import parameters as params
import random
import os


class SpritePreloader:
    """Preloads the textures of recurring things so the work doesn't get done every time one spawns."""

    def __init__(self):
        # Enemies
        self.enemies = []
        # Spritesheet metadata for the enemies
        # (width each, height each, # columns, # sprites)
        ENEMY_SHEET_DATA = [
            (50, 50, 6, 30),
            (100, 100, 12, 60),
            (50, 28, 5, 30),
            (50, 50, 12, 60),
            (50, 50, 5, 30),
            (50, 50, 5, 20),
        ]
        for id in range(1, 7):
            w, h, c, n = ENEMY_SHEET_DATA[id - 1]
            self.enemies.append(
                arcade.load_spritesheet(f"spritesheets/enemy{id}.png", w, h, c, n)
            )

        # Explosions
        self.explosion = arcade.load_spritesheet(
            "spritesheets/explosion.png", 128, 128, 5, 45
        )
        self.explosion_large = arcade.load_spritesheet(
            "spritesheets/explosion_large.png", 256, 256, 9, 45
        )


class Enemy(arcade.Sprite):
    """One of six enemies.   \n
    IDs: 1 - Small tri-torus \n
         2 - Big tri-torus   \n
         3 - Evil ship       \n
         4 - Spinning theta  \n
         5 - Spinning plus   \n
         6 - Spinning star"""

    def __init__(
        self,
        preloader: SpritePreloader,
        id,
        start_x=0,
        start_y=0,
        custom_velocity_angle: tuple[float, float, float] = None,
    ):
        super().__init__()

        self.id = id
        self.idx = id - 1  # Tiny optimization?

        # Grab this enemy's info from params
        self.health = params.ENEMY_HEALTHS[self.idx]
        # Randomized for variety
        self.fire_cooldown = params.ENEMY_FIRE_COOLDOWNS[self.idx] + random.randint(
            -10, 10
        )
        self.change_x = -params.ENEMY_SPEEDS[self.idx]

        # Used for the children of enemy 2
        if custom_velocity_angle:
            self.change_x += custom_velocity_angle[0]
            self.change_y = custom_velocity_angle[1]
            self.angle = custom_velocity_angle[2]

        # Grab preloaded textures
        self.textures = preloader.enemies[self.idx]

        self.texture = self.textures[0]
        self.LAST_FRAME_IDX = len(self.textures) - 1

        self.SCREEN_WIDTH = arcade.get_window().get_size()[0]

        # Start at position specified
        if start_x:
            self.center_x = start_x
        else:
            self.left = self.SCREEN_WIDTH
        self.center_y = start_y

    def update(self):
        # Move
        super().update()
        # "Die" if offscreen
        # TODO small score penalty for letting one get through, UNLESS it's vertically offscreen
        if self.right < 0 or self.left > self.SCREEN_WIDTH:
            print("Defenses breached :(")
            self.remove_from_sprite_lists()

    def update_animation(self, delta_time: float = 1 / 60):
        self.cur_texture_index += 1

        # Loop
        if self.cur_texture_index > self.LAST_FRAME_IDX:
            self.cur_texture_index = 0

        self.texture = self.textures[self.cur_texture_index]


# TODO powerup system...
class Powerup(arcade.Sprite):
    pass


class Explosion(arcade.Sprite):
    """Boom! Can be (s)mall or (l)arge."""

    def __init__(self, preloader: SpritePreloader, center_x, center_y, size="s"):
        super().__init__(center_x=center_x, center_y=center_y)
        if size == "s":
            self.textures = preloader.explosion
        elif size == "l":
            self.textures = preloader.explosion_large

        self.texture = self.textures[0]
        self.LAST_FRAME_IDX = len(self.textures) - 1

    def update_animation(self, delta_time: float = 1 / 60):
        self.cur_texture_index += 1

        # Die at end
        if self.cur_texture_index >= self.LAST_FRAME_IDX:
            self.remove_from_sprite_lists()

        self.texture = self.textures[self.cur_texture_index]
