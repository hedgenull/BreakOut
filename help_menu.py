#================================================================================>
# FILE NAME:  help_menu.py
#
# PURPOSE:
# Help menu for the BreakOut game.
#
# CREATED DATE: 2022-03-30
# AUTHOR:       @hedgenull
#================================================================================>

import pygame
import pygame.font
from pygame.sprite import Group


class HelpMenu:
    """A class to show the game controls."""
    def __init__(self, game):
        """Initialize attributes."""
        pygame.font.init()
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        
        # Menu settings
        self.bg_color = self.game.settings.menu_color
        self.rect = pygame.Rect(0, 0, self.screen_rect.width, self.screen_rect.height)

        # Font settings for scoring information.
        self.text_color = (255, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

    def draw(self):
        """Draw the help menu onto the screen."""
        pygame.draw.rect(self.screen, self.bg_color, self.rect)