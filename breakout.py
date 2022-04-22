#================================================================================>
# FILE NAME:  breakout.py
#
# PURPOSE:
# Main game file for BreakOut game.
#
# CREATED DATE: 2022-03-18
# AUTHOR:       @hedgenull
#================================================================================>

import pygame, sys, time, random

from settings import Settings
from bar import Bar
from ball import Ball
from brick import Brick
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from help_menu import HelpMenu

from pygame.sprite import Group
import pygame.mixer


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

        # Create an instance to store game stats, and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Initialize bar.
        self.bar = Bar(self)

        # Initialize ball.
        self.ball = Ball(self)
        self.ball.initialize_position_settings()

        # Make the Play button.
        self.play_button = Button(self, "Play")

        # Make the help menu.
        self.menu = HelpMenu(self)

        # Load brick sounds
        pygame.mixer.init()
        pygame.mixer.music.set_volume(self.settings.volume)

        # Hard mode?
        self.hard_mode = False
        self.hard_mode_button = Button(self, "Hard Mode")
        self.hard_mode_button.rect.midtop = (
            self.play_button.rect.midbottom[0],
            self.play_button.rect.midbottom[1] + 40)
        self.hard_mode_button._prep_msg("Hard Mode")

        # Initialize group of bricks.
        self.bricks: Group[Brick] = Group()
        self._create_array()

    def run(self):
        """Run the game."""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.bar.update()
                self.ball.update()
            self._update_screen()

    def _update_screen(self):
        """Update the screen and assets and fill the background."""
        self.screen.fill(self.settings.bg_color)

        # Draw the score information.
        self.sb.show_score()

        # Draw the bar, ball, and bricks.
        self.bar.blitme()
        self.ball.blitme()
        self.bricks.update()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.menu.button.draw_button()
            self.hard_mode_button.draw_button()
            if self.menu.drawn:
                self.menu.draw()

        pygame.display.flip()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_game()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_buttons(mouse_pos)
        self._check_ball_brick_hit()

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.bar.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.bar.moving_left = True
        elif event.key == pygame.K_p or event.key == pygame.K_RETURN:
            if not self.stats.game_active:
                self._make_normal()
                self._start_game()
        elif event.key == pygame.K_h:
            if not self.stats.game_active:
                self._make_hard()
                self._start_game()
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            self._quit_game()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.bar.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.bar.moving_left = False

    def _check_buttons(self, mouse_pos):
        """Respond when the player clicks the play button."""
        if self.play_button.rect.collidepoint(
                mouse_pos
        ) and not self.stats.game_active and not self.menu.drawn:
            self._make_normal()
            self._start_game()
        if self.menu.button.rect.collidepoint(
                mouse_pos) and not self.menu.drawn:
            self.menu.drawn = True
        elif self.menu.button.rect.collidepoint(mouse_pos) and self.menu.drawn:
            self.menu.drawn = False
        elif self.hard_mode_button.rect.collidepoint(
                mouse_pos) and not self.menu.drawn:
            self.hard_mode = True
            self._start_game()

    def _start_game(self):
        """Start a new game."""
        # Reset the game statistics.
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ball_group()

        # Get rid of any remaining bricks.
        self.bricks.empty()

        # Create a new array of bricks and center the bar/ball.
        self._create_array()
        self._new_round()

        # Hide the mouse cursor.K
        pygame.mouse.set_visible(False)

        if self.hard_mode:
            self._make_hard()
        else:
            self._make_normal()

    def _make_hard(self):
        """Change the settings to a hard state."""
        self.hard_mode = True
        self.settings.bar_speed = 4
        self.settings.ball_speed = 1.65
        self.settings.brick_hp = 2
        self.settings.brick_points = 30
        self.settings.brick_hp_scale = 1.75
        self.settings.bar_color, self.settings.brick_color = (255, 255,
                                                              255), (255, 255,
                                                                     255)

        self.bricks.empty()
        self._create_array()
        self._new_round()

    def _make_normal(self):
        """Make sure we use the normal settings."""
        self.hard_mode = False
        self.settings.bar_speed = 3
        self.settings.ball_speed = 1
        self.settings.brick_hp = 1
        self.settings.brick_points = 10
        self.settings.brick_hp_scale = 1.2
        self.brick_color_decrease = (random.randint(25, 50),
                                     random.randint(25, 50),
                                     random.randint(25, 50))
        col = random.randint(200, 255)
        self.settings.bar_color, self.settings.brick_color = [col] * 3, [col
                                                                         ] * 3
        self.bricks.empty()
        self._create_array()
        self._new_round()

    def _ball_lost(self):
        """Respond to when the ball goes off of the screen."""
        if self.stats.lives_left > 0:
            # Decrement lives left
            self.stats.lives_left -= 1

            # Start a new round
            self._new_round(3)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _new_round(self, secs=0):
        """Center the elements on the screen and initialize some settings."""
        # Center the bar
        self.bar.center_rect()

        self.bar.color = self.bricks.sprites()[0].color

        # Reset ball's position and speed, and update balls left on the scoreboard
        self.ball.initialize_position_settings()
        self.sb.prep_ball_group()

        # Pause
        time.sleep(secs)

    def _create_array(self):
        """Create the array of bricks."""
        # Create a brick and find the number of bricks in a row.
        # Spacing between each brick is equal to one brick width.
        self.settings.brick_color_decrease = (random.choice([25, 50]),
                                              random.choice([25, 50]),
                                              random.choice([25, 50]))
        brick = Brick(self)
        brick_width, brick_height = brick.rect.size
        available_space_x = self.settings.screen_width - brick_width
        number_bricks_x = available_space_x // brick_width - 7

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
        brick.rect.y = (brick_height + 2 * brick.rect.height * row_number) + 35
        self.bricks.add(brick)

    def _check_ball_brick_hit(self):
        """Check for collisions between the ball and any bricks."""
        # Respond to the ball hitting a brick

        for brick in self.bricks:
            if self.ball.rect.colliderect(brick.rect):
                self.sb.check_high_score()

                brick.hp -= 1
                brick.update_color()
                if brick.hp <= 0:
                    pygame.mixer.music.load(self.settings.destroy_sound)
                    brick.kill()
                    self.stats.score += self.settings.brick_points
                    self.sb.prep_score()
                else:
                    pygame.mixer.music.load(self.settings.break_sound)

                pygame.mixer.music.play(fade_ms=100)

                # Bounce the ball off the brick.
                dx, dy = self.ball.direction
                if self.hard_mode:
                    n1, n2 = random.choice([1, -1]), random.choice([1, -1])
                    self.ball.direction = dx * n1, dy * n2
                else:
                    self.ball.direction = dx, -dy

        self.sb.check_high_score()

        if len(self.bricks) <= 0:
            # Create a new array of bricks.
            self._create_array()
            self.stats.lives_left += 1
            self.settings.speedup()
            # Increment level
            self.stats.level += 1
            self.sb.prep_level()
            self._new_round(3)

    def _quit_game(self):
        """Quit the game and save the high score."""
        # Save high score
        self.stats.save_high_score()

        # Quit the program
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    breakout = BreakOut()
    breakout.run()
