#================================================================================>
# FILE NAME:  settings.py
#
# PURPOSE:
# Settings for BreakOut game.
#
# CREATED DATE: 2022-03-18
# AUTHOR:       @hedgenull
#================================================================================>

import pygame.color


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
        self.bar_color = (233, 215, 0)  # Yellow bar

        # Ball settings
        self.ball_speed = 1
        self.lives = 5

        # Brick settings
        self.brick_color = (233, 215, 0)  # Yellow bricks
        self.brick_color_increase = (15, 7, 7)
        self.brick_points = 10
        self.brick_hitpoints = 1
        self.brick_hp_scale = 1.2

        # Help-menu settings
        self.menu_color = (255, 0, 0)  # Red menu background

        # Sound effects
        self.volume = 0.6
        self.destroy_sound = "assets/destroy.mp3"
        self.break_sound = "assets/break.mp3"

    def speedup(self):
        """Speed up the ball and bar."""
        self.bar_speed *= self.speedup_scale
        self.ball_speed *= self.speedup_scale
        self.brick_hitpoints = round(
            self.brick_hitpoints * self.brick_hp_scale, 2)
        self.brick_points = int(round(self.brick_points * 1.5, -1))
