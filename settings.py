#================================================================================>
# FILE NAME:  settings.py
#
# PURPOSE:
# Settings for BreakOut game.
#
# CREATED DATE: 2022-03-18
# AUTHOR:       Greyson Smith (mathopotamus@bearcreek.family)
#================================================================================>


class Settings:
    """Settings class for BreakOut game."""
    def __init__(self):
        """Initialize settings class for BreakOut game."""
        # Main settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (20, 20, 20)  # Gray background
        self.speedup = 1.001
        self.lives = 3
        self.score = 0

        # Bar settings
        self.bar_speed = 2.5
        self.bar_color = (255, 0, 0)  # Red bar

        # Ball settings
        self.ball_speed = 1.5
