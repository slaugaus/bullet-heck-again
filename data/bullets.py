import arcade
import parameters as params


class Bullet(arcade.SpriteSolidColor):
    """A bullet fired by the player."""

    def __init__(
        self,
        player: arcade.Sprite,
        width=15,
        height=2,
        color=arcade.color.RED,
        damage=1,
        speed=20,
        y_offset=0,
    ):
        super().__init__(width, height, color)

        self.right = player.right
        self.center_y = player.center_y + y_offset

        self.change_x = speed


# class EnemyBullet():
