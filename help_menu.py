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
from button import Button


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
        self.rect = pygame.Rect(0, 0, self.screen_rect.width,
                                self.screen_rect.height)
        self.rect.center = self.screen_rect.center

        # Font settings for controls/instructions.
        self.text_color = (233, 215, 0)  # Yellow text
        self.font = pygame.font.SysFont(None, 20)

        self.instructions_text = """
BreakOut: A Python clone of Atari Breakout!
BreakOut is a game where you control a yellow bar on the screen. Use the
left and right arrow keys to move the bar. Above the bar is a grid of bricks and
a ball. The ball bounces around the screen and breaks the bricks when it hits them,
gaining you points. Your job is to break all of the bricks before you run out of
lives. Each time the ball goes off of the screen, you lose a life. Once you destroy
all the bricks, they reappear and the game moves faster. If you lose all of your
lives, the 'Play' button appears on the center of the screen. Click it or press 'P'
or 'Enter' to restart the game. Press 'Q', 'Escape', or click the close button at
any time to quit the game.
        """
        # Prepare button and put it in the corner of the screen
        self.button = Button(self.game, "Help")
        self.button.rect.bottom = self.screen_rect.bottom - 10
        self.button.rect.right = self.screen_rect.right - 10

        self.prep_text()

    def draw(self):
        """Draw the help menu onto the screen."""
        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        self.screen.blit(self.text_image, self.text_rect)
        self.button.draw_button()
        

    def prep_text(self):
        """Turn the instruction text into a rendered image."""
        self.text_image = self.font.render(self.instructions_text, True,
                                           self.text_color, self.bg_color)

        # Display the score at the top right of the screen.
        self.text_rect = self.text_image.get_rect()
        self.text_rect.center = self.rect.center