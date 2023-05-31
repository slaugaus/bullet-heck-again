import arcade
import parameters as params
import os

# Directions for animating
UP = 1
DOWN = -1


class Player(arcade.Sprite):
    """The player ship."""

    def __init__(self):
        super().__init__()

        self.facing = UP

        # Adjust the collision box. Default includes too much empty space
        # side-to-side. Box is centered at sprite center, (0, 0)
        # Your sprite is 75 x 50
        # self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        MAIN_PATH = "anims/ship/"

        for file in os.listdir(MAIN_PATH):
            self.textures.append(arcade.load_texture(MAIN_PATH + file))

        self.LAST_FRAME_IDX = len(self.textures) - 1

        self.texture = self.textures[0]

        self.SCREEN_WIDTH = arcade.get_window().get_size()[0]
        self.SCREEN_HEIGHT = arcade.get_window().get_size()[1]

    def update(self):
        # Move based on delta values
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Check for out-of-bounds (in this case, screen edges)
        if self.left < 0:
            self.left = 0
        elif self.right > self.SCREEN_WIDTH - 1:
            self.right = self.SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > self.SCREEN_HEIGHT - 1:
            self.top = self.SCREEN_HEIGHT - 1

    def update_animation(self, delta_time: float = 1 / 60):
        # Did the player just change the direction they were facing?
        if self.change_y < 0 and self.facing == UP:
            self.facing = DOWN
        elif self.change_y > 0 and self.facing == DOWN:
            self.facing = UP

        # Either increment or decrement animation index based on direction
        self.cur_texture_index += self.facing

        # TODO this may not be framerate-independent? look into AnimatedTimeBasedSprite
        # TODO https://www.youtube.com/watch?v=Iw51tl4pyNU

        # Wrap around when either edge is hit
        if self.cur_texture_index > self.LAST_FRAME_IDX:
            self.cur_texture_index = 0
        elif self.cur_texture_index < 0:
            self.cur_texture_index = self.LAST_FRAME_IDX

        self.texture = self.textures[self.cur_texture_index]
