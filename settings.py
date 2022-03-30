#================================================================================>
# FILE NAME:  settings.py
#
# PURPOSE:
# Settings for BreakOut game.
#
# CREATED DATE: 2022-03-18
# AUTHOR:       @hedgenull
#================================================================================>


class Settings:
    """Settings class for BreakOut game."""
    def __init__(self):
        """Initialize settings class for BreakOut game."""
        # Main settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (40, 40, 40)  # Gray background
        self.speedup = 1.1
        self.score = 0

        # Bar settings
        self.bar_speed = 3
        self.bar_color = (233, 215, 0)  # Yellow bar

        # Ball settings
        self.ball_speed = 1
        self.lives = 6

        # Brick settings
        self.brick_color = 	(233, 215, 0) # Yellow bricks
        self.brick_points = 10
        self.brick_hitpoints = 1
    
    def speedup(self):
        self.bar_speed *= self.speedup
        self.ball_speed *= self.speedup