#================================================================================>
# FILE NAME:  ball.py
#
# PURPOSE:
# Ball class for the BreakOut game.
#
# CREATED DATE: 2022-03-19
# AUTHOR:       Greyson Smith (mathopotamus@bearcreek.family)
#================================================================================>

import pygame
from pygame.sprite import Sprite


class Ball(Sprite):
    """Ball class for the BreakOut game."""
    def __init__(self, game):
        """Initialize the ball and set its properties."""
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.speed = self.settings.ball_speed
        self.image = pygame.image.load("assets/ball.png")
        self.rect = self.image.get_rect()

        # Center the ball on the bar.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.game.bar.rect.top - 10

    def blitme(self):
        """Draw the ball's image at its rect."""
        self.screen.blit(self.image, self.rect)