#================================================================================>
# FILE NAME:  bar.py
#
# PURPOSE:
# Bar class that player controls in the BreakOut game.
#
# CREATED DATE: 2022-03-18
# AUTHOR:       Greyson Smith (mathopotamus@bearcreek.family)
#================================================================================>

import pygame
from pygame.sprite import Sprite


class Bar(Sprite):
    """Bar class that player controls in the BreakOut game."""
    def __init__(self, game):
        """Initialize the bar and set its properties."""
        self.game = game
        self.screen: pygame.Surface = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        width = self.settings.screen_width / 8
        height = self.settings.screen_height / 50
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.midbottom = self.screen_rect.midbottom

        # Movement flags
        self.moving_left = False
        self.moving_right = False
        self.speed = self.settings.bar_speed

    def update(self):
        """Update the bar based on the movement flags."""
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.speed
        if self.moving_right and self.rect.right < self.settings.screen_width:
            self.rect.x += self.speed

    def blitme(self):
        """Draw the bar at its current position."""
        pygame.draw.rect(self.screen, self.settings.bar_color, self.rect)

    def center(self):
        """Center the bar on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
    
    def update(self):
        """Update the bar's position based on the movement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.speed
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.speed