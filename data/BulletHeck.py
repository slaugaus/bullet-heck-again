import arcade
from game import Game
from settings import Settings


def main():
    """Main function"""
    # TODO probably don't need this here?
    # settings = Settings()

    game = Game()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
