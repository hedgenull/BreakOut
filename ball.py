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
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.image = pygame.image.load("assets/ball.png")
        self.rect = self.image.get_rect()

        # Center the ball on the bar.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.game.bar.rect.top - 10

        # Starting direction and speed of the ball
        self.possible_x_directions = [1, -1]
        self.direction = random.choice(self.possible_x_directions), -1
        self.speed = self.settings.ball_speed

    def blitme(self):
        """Draw the ball's image at its rect."""
        self.screen.blit(self.image, self.rect)

    def update(self):
        # Move the ball along its current direction at its current speed
        dx, dy = self.direction
        self.rect.move_ip(self.speed * dx, self.speed * dy)

        # Bounce the ball off the left or right walls
        if self.rect.right >= self.screen_rect.width or self.rect.left <= 0:
            self.direction = -dx, dy
            self.speed *= self.settings.speedup

        # Bounce the ball off the top or bottom walls
        if self.rect.top <= 0 or self.rect.bottom >= self.screen_rect.bottom:
            self.direction = dx, -dy
            self.speed *= self.settings.speedup