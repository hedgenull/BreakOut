#================================================================================>
# FILE NAME:  bar.py
#
# PURPOSE:
# Bar class that player controls in the BreakOut game.
#
# CREATED DATE: 2022-03-18
# AUTHOR:       @hedgenull
#================================================================================>

import pygame
from pygame.sprite import Sprite


class Bar(Sprite):
    """Bar class that player controls in the BreakOut game."""
    def __init__(self, game):
        """Initialize the bar and set its properties."""
        super().__init__()
        self.game = game
        self.screen: pygame.Surface = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings

        # Center the bar
        width = self.settings.screen_width / 7
        height = self.settings.screen_height / 30
        self.rect = pygame.Rect(0, 0, width, height)

        # Movement flags
        self.moving_left = False
        self.moving_right = False
        self.speed = self.settings.bar_speed

        self.color = self.settings.bar_color

        # Center the rect.
        self.center_rect()

    def update(self):
        """Update the bar based on the movement flags."""
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.rect.x -= self.speed
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.speed

    def blitme(self):
        """Draw the bar at its current position."""
        pygame.draw.rect(self.screen, self.color, self.rect)

    def center_rect(self):
        """Center the bar on the bottom of the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
