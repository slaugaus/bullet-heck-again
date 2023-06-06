import arcade
from game import GameView
from settings import Settings
import os


def main():
    """Main function"""
    settings = Settings()

    window = arcade.Window(
        settings.screen_width, settings.screen_height, "Bullet Heck!"
    )

    # Game may not be running from the data dir
    if os.getcwd().find("data") == -1:
        os.chdir("data")

    game = GameView(settings)
    game.setup()

    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()
