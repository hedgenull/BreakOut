#================================================================================>
# FILE NAME:  settings.py
#
# PURPOSE:
# Settings for BreakOut game.
#
# CREATED DATE: 2022-03-18
# AUTHOR:       @hedgenull
#================================================================================>

from random import randint as rnd


class Settings:
    """Settings class for BreakOut game."""
    def __init__(self):
        """Initialize settings class for BreakOut game."""
        # Main settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (40, 40, 40)  # Gray background
        self.speedup_scale = 1.07
        self.score = 0

        # Bar settings
        self.bar_speed = 3
        col = rnd(200, 255)
        self.bar_color = (col, col, col)

        # Ball settings
        self.ball_speed = 1
        self.lives = 5

        # Brick settings
        self.brick_color = self.bar_color
        self.brick_color_decrease = (rnd(25, 50), rnd(25, 50), rnd(25, 50))
        self.brick_points = 10
        self.brick_hp = 3
        self.brick_hp_scale = 1.2

        # Help-menu settings
        self.menu_color = (40, 40, 40)  # Gray menu background

        # Sound effects
        self.volume = 0.6
        self.destroy_sound = "assets/destroy.mp3"
        self.break_sound = "assets/break.mp3"

    def speedup(self):
        """Speed up the ball and bar."""
        self.bar_speed *= self.speedup_scale
        self.ball_speed *= self.speedup_scale
        self.brick_hp = round(self.brick_hp * self.brick_hp_scale, 2)
        self.brick_points = int(round(self.brick_points * 1.5, -1))
