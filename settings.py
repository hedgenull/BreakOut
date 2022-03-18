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
        self.bg_color = (0, 0, 0)   # Black background
        self.speedup = 1.1
        self.lives = 3
        self.score = 0
