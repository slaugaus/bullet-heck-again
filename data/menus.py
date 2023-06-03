import arcade

class PauseView(arcade.View):

    def __init__(self, game_view):
        super().__init__()

        self.game_view = game_view

    def on_show_view(self):
        """Runs when the window is set to this View."""

    def on_draw(self):
        self.clear()
        
