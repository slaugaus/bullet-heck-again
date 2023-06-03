"""Everything related to the game audio (sounds/music)"""

import arcade
from settings import Settings

class GameAudio():
    def __init__(self):
        self.pew = arcade.Sound("audio/pew.ogg")
        self.boom = {
            's': arcade.Sound("audio/boom_small.ogg"),
            'l': arcade.Sound("audio/boom_med.ogg")
        }
        self.enemy_hit = arcade.Sound("audio/enemy_hit.ogg")
        self.ship_hit = arcade.Sound("audio/ship_hit.ogg")
        self.levelup = arcade.Sound("audio/levelup.ogg")
        self.leveldown = arcade.Sound("audio/leveldown.ogg")

        self.bgm = arcade.Sound("audio/bgm.ogg", streaming=True)

    def play_at(self, settings: Settings, sound: arcade.Sound, x):
        """Wrapper for Arcade's play_sound() that checks the mute setting and pans based on a position"""
        if not settings.mute_sound:
            # Calculate pan value based on an x coordinate
            pan_value = (x / settings.screen_width) * 2 - 1
            # print(pan_value)

            arcade.play_sound(sound, pan=pan_value)