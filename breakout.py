#================================================================================>
# FILE NAME:  breakout.py
#
# PURPOSE:
# Main game file for BreakOut game.
#
# CREATED DATE: 2022-03-18
# AUTHOR:       @hedgenull
#================================================================================>

########################################
# Dependencies
########################################

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

########################################
# Main game class
########################################


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

        # Prepare sound elements.
        pygame.mixer.init()
        pygame.mixer.music.set_volume(self.settings.volume)

        # Hard mode settings.
        self.hard_mode = False
        self.hard_mode_button = Button(self, "Hard Mode")
        # Set button position.
        self.hard_mode_button.rect.midtop = (
            self.play_button.rect.midbottom[0],
            self.play_button.rect.midbottom[1] + 40)
        self.hard_mode_button._prep_msg("Hard Mode")

        # Initialize group of bricks.
        self.bricks = Group()
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

        # Draw the buttons if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.menu.button.draw_button()
            self.hard_mode_button.draw_button()

            # If the menu is currently showing, draw it.
            if self.menu.drawn:
                self.menu.draw()

        pygame.display.flip()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit the game.
                self._quit_game()
            elif event.type == pygame.KEYDOWN:
                # Pass the event to the keydown callback.
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                # Pass the event to the keyup callback.
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Pass the event to the mouse click callback.
                mouse_pos = pygame.mouse.get_pos()
                self._check_buttons(mouse_pos)

        # Check collisions between the bricks and the ball.
        self._check_ball_brick_hit()

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            # Make the bar move right.
            self.bar.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Make the bar move left.
            self.bar.moving_left = True
        elif event.key == pygame.K_p or event.key == pygame.K_RETURN:
            # Activate the normal mode if the game isn't active.
            if not self.stats.game_active:
                self._make_normal()
                self._start_game()
        elif event.key == pygame.K_h:
            # Activate the hard mode  if the game isn't active.'
            if not self.stats.game_active:
                self._make_hard()
                self._start_game()
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            # Quit the game.
            self._quit_game()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.bar.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.bar.moving_left = False

    def _check_buttons(self, mouse_pos):
        """Respond when the player clicks the play button."""
        if self.play_button.rect.collidepoint(
                mouse_pos
        ) and not self.stats.game_active and not self.menu.drawn:
            # The player clicked the play button.
            self._make_normal()
            self._start_game()
        if self.menu.button.rect.collidepoint(
                mouse_pos) and not self.menu.drawn:
            # The player clicked the help button- prepare to draw the menu.
            self.menu.drawn = True
        elif self.menu.button.rect.collidepoint(mouse_pos) and self.menu.drawn:
            # The player clicked the help button while the menu is open- close it.
            self.menu.drawn = False
        elif self.hard_mode_button.rect.collidepoint(
                mouse_pos) and not self.menu.drawn:
            # The player clicked the hard mode button.
            self._make_hard()
            self._start_game()

    def _start_game(self):
        """Start a new game."""
        # Reset the game statistics.
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ball_group()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Create a new array of bricks.
        self.bricks.empty()
        self._create_array()

        # Reset positions.
        self._new_round()

    def _new_round(self):
        """Center the elements on the screen and initialize some settings."""
        # Change the colors.
        self._change_colors()

        # Center the bar.
        self.bar.center_rect()

        # Reset ball's position and speed, and update lives left on the scoreboard.
        self.ball.initialize_position_settings()
        self.sb.prep_ball_group()

    def _change_colors(self):
        """Change the colors of the bar and bricks."""
        self.settings.brick_color_decrease = (random.choice([25, 50]),
                                              random.choice([25, 50]),
                                              random.choice([25, 50]))

        self.settings.bar_color = self.settings.brick_color = (random.choice(
            [155, 255]), random.choice([155, 255]), random.choice([155, 255]))

    def _make_hard(self):
        """Change the settings to a hard state."""
        self.hard_mode = True
        self.settings.bar_speed = 4
        self.settings.ball_speed = 1.65
        self.settings.brick_hp = 2
        self.settings.brick_points = 30
        self.settings.brick_hp_scale = 1.75

    def _make_normal(self):
        """Make sure we use the normal settings."""
        self.hard_mode = False
        self.settings.bar_speed = 3
        self.settings.ball_speed = 1
        self.settings.brick_hp = 1
        self.settings.brick_points = 10
        self.settings.brick_hp_scale = 1.4

    def _ball_lost(self):
        """Respond to when the ball goes off of the screen."""
        if self.stats.lives_left > 0:
            # If we still have lives left...
            # Decrement lives.
            self.stats.lives_left -= 1

            # Pause and start a new round.
            time.sleep(3)
            self._new_round()
        else:
            # We're out of lives- stop the game.
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_array(self):
        """Create the array of bricks."""
        # Create a brick and find the number of bricks in a row.
        # Spacing between each brick is equal to one brick width.
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
        # Get the brick's size.
        brick_width, brick_height = brick.rect.size
        brick.x = brick_width + 2 * brick_width * brick_number
        brick.rect.x = brick.x
        # Position the brick in the row and add it to the group.
        brick.rect.y = (brick_height + 2 * brick.rect.height * row_number) + 35
        self.bricks.add(brick)

    def _check_ball_brick_hit(self):
        """Check for collisions between the ball and any bricks."""
        # Respond to the ball hitting a brick.
        for brick in self.bricks:
            if self.ball.rect.colliderect(brick.rect):
                # If the brick is hit...
                # Decrement its hitpoints
                brick.hp -= 1

                # Update its color
                brick.update_color()

                if brick.hp <= 0:
                    # If the brick is dead...
                    # Load the brick die sound.
                    pygame.mixer.music.load(self.settings.destroy_sound)

                    # Utterly maul, kill, ravage, maim, destroy, annihilate, disintegrate, etc., etc., the brick.
                    brick.kill()

                    # Increase score.
                    self.stats.score += self.settings.brick_points
                    self.sb.prep_score()
                else:
                    # Otherwise, it's still alive.
                    # Load the brick semi-destroy sound.
                    pygame.mixer.music.load(self.settings.break_sound)

                # Realize that we haven't actually played sound yet- just loaded it.
                # Play whatver sound we loaded.
                pygame.mixer.music.play()

                # Bounce the ball off the brick.
                dx, dy = self.ball.direction
                if self.hard_mode:
                    # If it's hard mode, bounce it off in a random direction.
                    n1, n2 = random.choice([1, -1]), random.choice([1, -1])
                    self.ball.direction = dx * n1, dy * n2
                else:
                    # Bounce the ball off at a nice, simple right angle.
                    self.ball.direction = dx, -dy

        # Check to see if the the high score has been beat.
        self.sb.check_high_score()

        # If the bricks are gone...
        self._check_bricks_gone()

    def _check_bricks_gone(self):
        """Check if the bricks are gone. If so, start a new round."""
        if len(self.bricks) <= 0:
            # If there are no more bricks...
            # We get another life!
            self.stats.lives_left += 1

            # Sadly, so do the bricks. (Starting at about level 3, that is.)
            self.settings.speedup()

            # Increment the level and start a new round.
            self.stats.level += 1
            self.sb.prep_level()
            self._new_round()

            # Create a new array of bricks, and pause.
            self._create_array()
            time.sleep(3)

    def _quit_game(self):
        """Quit the game and check the high score."""
        # Check the high score.
        self.sb.check_high_score()

        # Quit the program.
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    breakout = BreakOut()
    breakout.run()
