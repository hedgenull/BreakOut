#================================================================================>
# FILE NAME:  breakout.py
#
# PURPOSE:
# Main game file for BreakOut game.
#
# CREATED DATE: 2022-03-18
# AUTHOR:       Greyson Smith (mathopotamus@bearcreek.family)
#================================================================================>

import pygame, sys
from settings import Settings
from bar import Bar
from ball import Ball


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

        # Initialize bar.
        self.bar = Bar(self)

        # Initialize ball.
        self.ball = Ball(self)

    def run(self):
        while True:
            self._check_events()

            self._update_screen()

    def _update_screen(self):
        """Update the screen, assets, and fill the background."""
        self.screen.fill(self.settings.bg_color)
        self.bar.update()
        self.ball.update()
        self.bar.blitme()
        self.ball.blitme()
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


if __name__ == "__main__":
    breakout = BreakOut()
    breakout.run()