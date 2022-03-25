#================================================================================>
# FILE NAME:  ball.py
#
# PURPOSE:
# Ball class for the BreakOut game.
#
# CREATED DATE: 2022-03-19
# AUTHOR:       Greyson Smith (mathopotamus@bearcreek.family)
#================================================================================>

import random

import pygame
from pygame.sprite import Sprite


class Ball(Sprite):
    """Ball class for the BreakOut game."""
    def __init__(self, game):
        """Initialize the ball and set its properties."""
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.image = pygame.image.load("assets/ball.png")
        self.rect = self.image.get_rect()

        self.initialize_position_settings()

    def initialize_position_settings(self):
        """Initialize the ball's speed, position and direction."""
        # Center the ball on the bar.
        self.rect.midbottom = self.game.bar.rect.midtop

        # Starting direction and speed of the ball
        possible_x_directions = [1, -1]
        self.direction = random.choice(possible_x_directions), -1
        self.speed = self.settings.ball_speed

    def blitme(self):
        """Draw the ball's image at its rect."""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Move the ball and bounce it off of the walls."""
        # Code found at https://wall-ball.readthedocs.io/en/latest/steps/step01.html
        dx, dy = self.direction
        self.rect.move_ip(self.speed * dx, self.speed * dy)

        # Bounce the ball off the left or right walls
        if self.rect.right >= self.screen_rect.width or self.rect.left <= 0:
            self.direction = -dx, dy
            self.speed *= self.settings.speedup

        # Bounce the ball off the top wall or the bar
        if self.rect.top <= 0 or self.rect.colliderect(self.game.bar.toprect):
            self.direction = dx, -dy
            self.speed *= self.settings.speedup

        # Respond to the ball going off the screen
        if self.rect.top > self.screen_rect.bottom:
            self.game._ball_lost()