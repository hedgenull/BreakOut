# ================================================================================>
# FILE NAME:  ball.py
#
# PURPOSE:
# Ball class for the BreakOut game.
#
# CREATED DATE: 2022-03-19
# AUTHOR:       @hedgenull
# ================================================================================>

########################################
# Dependencies
########################################

import random

import pygame
from pygame.sprite import Sprite


########################################
# Ball class
########################################
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
        # The ball is not inside the bar to start.
        self.in_bar = False

    def initialize_position_settings(self):
        """Initialize the ball's speed, position and direction."""
        # Center the ball on the bar.
        self.rect.midbottom = self.game.bar.rect.midtop

        # Set starting direction and speed of the ball.
        self.direction = random.choice([1, -1]), -1
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

        # Bounce the ball off the top wall or the bar
        if self.rect.top <= 0:
            self.direction = dx, -dy

        # Bounce the ball off the bar
        if self.rect.colliderect(self.game.bar.rect):
            if not self.in_bar:
                # If it doesn't think it's inside the bar...
                # Make sure it's still correct.
                if self.rect.bottom >= self.game.bar.rect.top - self.speed:
                    # Bounce off of the top.
                    self.direction = dx, -dy
                    self.in_bar = True
                elif (
                    self.rect.right >= self.game.bar.rect.left + self.speed
                    or self.rect.left <= self.game.bar.rect.right - self.speed
                ):
                    # Bounce off of the sides.
                    self.direction = -dx, dy
                    self.in_bar = True
        else:
            # It's not colliding with the bar....
            if self.in_bar:
                # We obviously won't be in the bar.
                self.in_bar = False

        # Respond to the ball going off the screen.
        if self.rect.top > self.screen_rect.bottom:
            self.game._ball_lost()
