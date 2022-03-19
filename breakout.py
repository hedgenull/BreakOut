#================================================================================>
# FILE NAME:  breakout.py
#
# PURPOSE:
# Main game file for BreakOut game.
#
# CREATED DATE: 2022-03-18
# AUTHOR:       Greyson Smith (mathopotamus@bearcreek.family)
#================================================================================>

import pygame
from settings import Settings
from bar import Bar


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

    def run(self):
        while True:
            self.screen.fill(self.settings.bg_color)
            self.bar.blitme()
            pygame.display.flip()
    
    


if __name__ == "__main__":
    breakout = BreakOut()
    breakout.run()