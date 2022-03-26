#================================================================================>
# FILE NAME:  breakout.py
#
# PURPOSE:
# Main game file for BreakOut game.
#
# CREATED DATE: 2022-03-18
# AUTHOR:       @hedgenull
#================================================================================>

import pygame, sys, time

from settings import Settings
from bar import Bar
from ball import Ball
from brick import Brick
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button

from pygame.sprite import Group


class BreakOut:
    """Base class for BreakOut game."""
    def __init__(self):
        """Initialize BreakOut assets and objects."""
        # Initialize settings.
        self.settings = Settings()

        # Initialize screen.
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("BreakOut")
        self.screen_rect = self.screen.get_rect()

        self.score = self.settings.score

        # Initialize bar.
        self.bar = Bar(self)

        # Initialize ball.
        self.ball = Ball(self)
        self.lives = self.settings.lives

        # Initialize group of bricks.
        self.bricks = Group()
        self._create_array()

    def run(self):
        """Run the game."""
        while True:
            self._check_events()
            self._update_screen()

    def _update_screen(self):
        """Update the screen, assets, and fill the background."""
        self.screen.fill(self.settings.bg_color)
        self._check_ball_brick_hit()
        self.bar.update()
        self.ball.update()
        self.bar.blitme()
        self.ball.blitme()
        self.bricks.update()
        pygame.display.flip()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.bar.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.bar.moving_left = True
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.bar.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.bar.moving_left = False

    def _ball_lost(self):
        """Respond to when the ball goes off of the screen."""
        time.sleep(3)
        if self.lives > 0:
            # Decrement lives left
            self.lives -= 1

            # Center the bar
            self.bar.center_rect()

            # Reset ball's position and speed
            self.ball.initialize_position_settings()
        else:
            sys.exit()

    def _create_array(self):
        """Create the array of bricks."""
        # Create a brick and find the number of bricks in a row.
        # Spacing between each brick is equal to one brick width.
        brick = Brick(self)
        brick_width, brick_height = brick.rect.size
        available_space_x = self.settings.screen_width - brick_width
        number_bricks_x = available_space_x // brick_width - 4

        # Determine the number of rows of bricks that fit on the screen.
        bar_height = self.bar.rect.height
        available_space_y = (self.settings.screen_height - (brick_height) -
                             (5 * bar_height))
        number_rows = available_space_y // brick_height - 13

        # Create the fleet of bricks.
        for row_number in range(int(number_rows)):
            for brick_number in range(number_bricks_x):
                self._create_brick(brick_number, row_number)

    def _create_brick(self, brick_number, row_number):
        """Create an brick and place it in the row."""
        brick = Brick(self)
        brick_width, brick_height = brick.rect.size
        brick.x = brick_width + 2 * brick_width * brick_number
        brick.rect.x = brick.x
        brick.rect.y = brick_height + 2 * brick.rect.height * row_number
        self.bricks.add(brick)

    def _check_ball_brick_hit(self):
        """Check for collisions between the ball and any bricks."""
        # Respond to the ball hitting a brick
        collisions = pygame.sprite.spritecollide(self.ball, self.bricks, True)

        if collisions:
            for brick in collisions:
                self.score += self.settings.brick_points
            dx, dy = self.ball.direction
            self.ball.direction = dx, -dy

        if not self.bricks:
            # Destroy existing bricks and create a new array of bricks.
            self._create_fleet()


if __name__ == "__main__":
    breakout = BreakOut()
    breakout.run()
