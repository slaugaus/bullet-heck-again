import arcade
import parameters as params
from player import Player
from settings import Settings
from stats import Stats
from bullets import Bullet
from enemies import *
import random
from audio import GameAudio


class GameView(arcade.View):
    # def __init__(self, settings: Settings, stats: Stats): # settings is of type Settings - for IDE features
    def __init__(self, settings: Settings):  # settings is of type Settings - for IDE features

        super().__init__()

        self.settings = settings

        self.stats = Stats()

        arcade.set_background_color(arcade.color.BLACK)

        # Preload textures that will appear on multiple objects
        self.preloader = SpritePreloader()

        # Preload(?) BGM and SFX
        self.audio = GameAudio()

        # If you have sprite lists, you should create them here,
        # and set them to None
        self.player_list = None
        self.bullet_list = None
        self.enemy_list = None
        self.explosion_list = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.fire_pressed = False

        self.SCREEN_WIDTH = arcade.get_window().get_size()[0]
        self.SCREEN_HEIGHT = arcade.get_window().get_size()[1]

    def setup(self):
        """Set up the game variables. Call to re-start the game."""
        # Create your sprites and sprite lists here
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.explosion_list = arcade.SpriteList()

        # Set up player
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
        self.enemy_list.draw_hit_boxes(arcade.color.RED)
        self.explosion_list.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.player_list.update()
        self.player_list.update_animation()

        self.bullet_list.update()

        self.enemy_list.update()
        self.enemy_list.update_animation()
        
        self.explosion_list.update_animation()

        self.update_bullets()
        self.do_player_enemy_collisions()

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

            # TODO "secret" debug keys!
            # Player level (be careful not to break this!)
            case arcade.key.NUM_ADD:
                self.stats.ship_level += 1
                self.audio.play_at(self.settings, self.audio.levelup, 0)
            case arcade.key.NUM_SUBTRACT:
                self.stats.ship_level -= 1
                self.audio.play_at(self.settings, self.audio.leveldown, 0)
            # Enemy spawning
            case arcade.key.NUM_1:
                self.enemy_list.append(Enemy(self.preloader, 1, start_y=random.randint(0, self.SCREEN_HEIGHT)))
            case arcade.key.NUM_2:
                self.enemy_list.append(Enemy(self.preloader, 2, start_y=random.randint(0, self.SCREEN_HEIGHT)))
            case arcade.key.NUM_3:
                self.enemy_list.append(Enemy(self.preloader, 3, start_y=random.randint(0, self.SCREEN_HEIGHT)))
            case arcade.key.NUM_4:
                self.enemy_list.append(Enemy(self.preloader, 4, start_y=random.randint(0, self.SCREEN_HEIGHT)))
            case arcade.key.NUM_5:
                self.enemy_list.append(Enemy(self.preloader, 5, start_y=random.randint(0, self.SCREEN_HEIGHT)))
            case arcade.key.NUM_6:
                self.enemy_list.append(Enemy(self.preloader, 6, start_y=random.randint(0, self.SCREEN_HEIGHT)))

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
        if 8 == self.stats.ship_level:
            bullet1 = Bullet(self.player, y_offset=6)
            bullet2 = Bullet(self.player, y_offset=-6)
            # bullet3 = Bullet(self.player, 0, 4, 15, 2, 21)
            bullet3 = Bullet(self.player, damage=2, height=4, speed=21)
            self.bullet_list.append(bullet2)
            self.bullet_list.append(bullet3)
        # Only used if messing with debug keys. You gon' learn today
        if self.stats.ship_level > 8 or self.stats.ship_level < 0:
            bullet1 = bullet1 = Bullet(self.player, damage=0, height=abs(self.stats.ship_level))
        self.bullet_list.append(bullet1)
        # Pew!
        self.audio.play_at(self.settings, self.audio.pew, self.player.right)

    def explode_at_entity(self, entity: arcade.Sprite, size = "s"):
        """Boom!"""
        self.explosion_list.append(Explosion(self.preloader, entity.center_x, entity.center_y, size))
        self.audio.play_at(self.settings, self.audio.boom[size], entity.center_x)

    def do_player_enemy_collisions(self):
        hit_list = arcade.check_for_collision_with_list(self.player, self.enemy_list)

        if len(hit_list) > 0:
            # TODO better player HP logic (and UI), only explode once
            self.explode_at_entity(self.player, "l")
            self.player.remove_from_sprite_lists()

    def do_bullet_enemy_collisions(self):
        # Collide with enemies
        for bullet in self.bullet_list:
            # Check this bullet to see if it hit an enemy
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()

            # For every enemy we hit, add to the score and hurt it
            for enemy in hit_list:
                enemy.health -= bullet.damage
                self.stats.score += params.ENEMY_POINTS[enemy.idx]

                # Kill; spawn children and explode
                if enemy.health <= 0:
                    match(enemy.id):
                        case(2):
                            self.explode_at_entity(enemy, 'l')
                            self.enemy_list.append(Enemy(self.preloader, 1, enemy.center_x-25, enemy.center_y-25))
                            self.enemy_list.append(Enemy(self.preloader, 1, enemy.center_x-25, enemy.center_y+25))
                            self.enemy_list.append(Enemy(self.preloader, 1, enemy.center_x+25, enemy.center_y))
                        case(5):
                            self.explode_at_entity(enemy)
                            self.enemy_list.append(Enemy(self.preloader, 4, enemy.center_x, enemy.center_y))
                        case(6):
                            self.explode_at_entity(enemy)
                            self.enemy_list.append(Enemy(self.preloader, 5, enemy.center_x, enemy.center_y))
                        case(_):
                            self.explode_at_entity(enemy)
                    
                    enemy.remove_from_sprite_lists()

                # Hit Sound (uses left to prevent a >1 error)
                self.audio.play_at(self.settings, self.audio.enemy_hit, enemy.left)

            # If the bullet flies off-screen, remove it.
            if bullet.left > self.SCREEN_WIDTH:
                bullet.remove_from_sprite_lists()

    def update_bullets(self):
        """This would be in the Bullets class if it wasn't handling the bullet-enemy collisions.\n
           Also fires them when appropriate"""
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

        self.do_bullet_enemy_collisions()