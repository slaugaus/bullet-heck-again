# TODO Can't be used in Sprites in class form. Probably needs to be a module instead of a class?

class Settings():
    """Holds values that can be changed by the user."""

    def __init__(self):
        # self.gamepad_connected = False
        self.screen_res = "1366 x 768"
        # Split resolution string into useful values (launcher will give a string like the above)
        reslist = self.screen_res.split()
        self.screen_width = int(reslist[0])
        self.screen_height = int(reslist[2])
        self.screen_center_x = self.screen_width / 2
        self.screen_center_y = self.screen_height / 2
        # self.gamepad_id = 0
        # self.deadzone = 0.2
        # self.axis_x = 0
        # self.axis_y = 1
        # self.hat_id = 0
        # self.but_A = 0
        # self.but_X = 2
        # self.but_Y = 3
        # self.but_S = 7
        self.show_fps = False
        self.autofire = False
        self.mute_music = False
        self.mute_sound = False