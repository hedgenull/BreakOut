#================================================================================>
# FILE NAME:  brick.py
#
# PURPOSE:
# Brick class for BreakOut game.
#
# CREATED DATE: 2022-03-22
# AUTHOR:       @hedgenull
#================================================================================>

import pygame
from pygame.sprite import Sprite


class Brick(Sprite):
    """Brick class for BreakOut game."""
    def __init__(self, game):
        """Create a new Brick and initialize its attributes."""
        super().__init__()
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # Rectangle attributes
        self.color = self.settings.brick_color
        self.width = self.screen_rect.width // 15
        self.height = self.screen_rect.height // 25
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        # Scoring and hitpoints
        self.point_value = self.settings.brick_points
        self.hp = self.settings.brick_hp

        self.update_color()

    def update(self):
        """Draw the brick at its current position."""
        pygame.draw.rect(self.screen, self.color, self.rect)

    def update_color(self):
        """Update the color of the brick based on its health."""
        r, g, b = self.color
        dr, dg, db = self.settings.brick_color_decrease
        for _ in range(1, int(self.hp)):
            self.color = (r - dr, g - dg, b - db) if r - dr > 0 else (0, 0, 0)
