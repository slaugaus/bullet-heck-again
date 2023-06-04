"""The starry background. The third time and language I've written this..."""

import arcade
import random
import parameters as params

class StarBG():
    def __init__(self, list: arcade.SpriteList):
        self.list = list

    def update(self):
        if len(self.list) < params.STAR_LIMIT:
            self.list.append(Star())
        self.list.update()

class Star(arcade.SpriteCircle):

    def __init__(self):
        super().__init__(5, arcade.color.WHITE, True)
        self.change_x = -params.STAR_SPEED
        self.ax = -params.STAR_ACCELERATION
        self.center_y = random.randint(0, arcade.get_window().height)
        self.left = arcade.get_window().width

    def update(self):
        # Move
        super().update()
        # Accelerate
        self.change_x += self.ax
        # Die
        if self.right < 0:
            self.remove_from_sprite_lists()


