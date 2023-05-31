import arcade
import parameters as params
from player import Player
from settings import Settings
from stats import Stats
from bullets import Bullet


class Game(arcade.Window):
    # def __init__(self, settings: Settings, stats: Stats): # settings is of type Settings - for IDE features
    def __init__(self):  # settings is of type Settings - for IDE features
        # Call arcade.Window init function
        self.settings = Settings()
        super().__init__(
            self.settings.screen_width, self.settings.screen_height, "Bullet Heck!"
        )

        self.stats = Stats()

        arcade.set_background_color(arcade.color.BLACK)

        # If you have sprite lists, you should create them here,
        # and set them to None
        self.player_list = None
        self.bullet_list = None
        self.enemy_list = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.fire_pressed = False

        self.SCREEN_WIDTH = arcade.get_window().get_size()[0]
        self.SCREEN_HEIGHT = arcade.get_window().get_size()[1]

        # self.should_fire_bullets = settings.autofire

    def setup(self):
        """Set up the game variables. Call to re-start the game."""
        # Create your sprites and sprite lists here
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        # self.player_sprite = Player("data/images/player_frame0.png")
        self.player = Player()
        self.player.center_x = self.settings.screen_center_x
        self.player.center_y = self.settings.screen_center_y
        self.player_list.append(self.player)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        # Call draw() on all your sprite lists below
        self.player_list.draw()
        self.player_list.draw_hit_boxes(arcade.color.AERO_BLUE)
        self.bullet_list.draw()
        self.enemy_list.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.player_list.update()
        self.player_list.update_animation()

        self.bullet_list.update()

        self.update_bullets()

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        # Map keys to booleans
        match key:
            case arcade.key.UP:
                self.up_pressed = True
            case arcade.key.DOWN:
                self.down_pressed = True
            case arcade.key.LEFT:
                self.left_pressed = True
            case arcade.key.RIGHT:
                self.right_pressed = True
            case arcade.key.Z:
                self.fire_pressed = True
            case arcade.key.A:
                self.settings.autofire ^= 1 # toggle

        self.update_player_speed()

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        # Map keys to booleans
        match key:
            case arcade.key.UP:
                self.up_pressed = False
            case arcade.key.DOWN:
                self.down_pressed = False
            case arcade.key.LEFT:
                self.left_pressed = False
            case arcade.key.RIGHT:
                self.right_pressed = False
            case arcade.key.Z:
                self.fire_pressed = False

        self.update_player_speed()

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass

    # TODO gamepad events (XInput doesn't work, DirectInput does)

    def update_player_speed(self):
        # By default, ensure player isn't moving
        self.player.change_x = 0
        self.player.change_y = 0

        # Vertical
        if self.up_pressed and not self.down_pressed:
            self.player.change_y = params.SHIP_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player.change_y = -params.SHIP_SPEED
        # Horizontal
        if self.left_pressed and not self.right_pressed:
            self.player.change_x = -params.SHIP_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player.change_x = params.SHIP_SPEED

        # TODO proper diagonals (ship.move_digital in old code)

    def spawn_player_bullet_pattern(self):
        """Spawn bullets based on the ship's level."""
        if 0 <= self.stats.ship_level:
            bullet1 = Bullet(self.player)
        if 2 <= self.stats.ship_level < 4:
            bullet1 = Bullet(self.player, damage=2, height=4)
        if 4 <= self.stats.ship_level < 6:
            bullet1 = Bullet(self.player, y_offset=6)
            bullet2 = Bullet(self.player, y_offset=-6)
            self.bullet_list.append(bullet2)
        if 6 <= self.stats.ship_level < 8:
            bullet1 = Bullet(self.player, y_offset=6)
            bullet2 = Bullet(self.player, y_offset=-6)
            bullet3 = Bullet(self.player, speed=21)
            self.bullet_list.append(bullet2)
            self.bullet_list.append(bullet3)
        if 8 <= self.stats.ship_level:
            bullet1 = Bullet(self.player, y_offset=6)
            bullet2 = Bullet(self.player, y_offset=-6)
            # bullet3 = Bullet(self.player, 0, 4, 15, 2, 21)
            bullet3 = Bullet(self.player, damage=2, height=4, speed=21)
            self.bullet_list.append(bullet2)
            self.bullet_list.append(bullet3)
        self.bullet_list.append(bullet1)
        # TODO sounds.pew.play()

    def update_bullets(self):
        # Update player bullet cooldown
        self.stats.player_bullet_cooldown -= 1
        if self.stats.player_bullet_cooldown < 0:
            self.stats.player_bullet_cooldown = params.PLAYER_BULLET_COOLDOWN

        if (
            # Autofire XOR fire button is pressed - if autofire is on, fire button will stop firing
            (self.settings.autofire ^ self.fire_pressed)
            and self.stats.player_bullet_cooldown == 0
            and len(self.bullet_list) < params.PLAYER_BULLET_LIMIT
        ):
            self.spawn_player_bullet_pattern()

        # TODO collide with enemies
        for bullet in self.bullet_list:
            # Check this bullet to see if it hit a coin
            # hit_list = arcade.check_for_collision_with_list(bullet, self.coin_list)

            # If it did, get rid of the bullet
            # if len(hit_list) > 0:
            #     bullet.remove_from_sprite_lists()

            # For every coin we hit, add to the score and remove the coin
            # for coin in hit_list:
            #     coin.remove_from_sprite_lists()
            #     self.score += 1

            #     # Hit Sound
            #     arcade.play_sound(self.hit_sound)

            # If the bullet flies off-screen, remove it.
            if bullet.left > self.SCREEN_WIDTH:
                bullet.remove_from_sprite_lists()
