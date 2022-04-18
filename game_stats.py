#================================================================================>
# FILE NAME:  game_stats.py
#
# PURPOSE:
# Class to keep track of statistics for the BreakOut game.
#
# CREATED DATE: 2022-03-26
# AUTHOR:       @hedgenull
#================================================================================>

import json


class GameStats:
    """Track game stats for Alien Invasion."""
    def __init__(self, game):
        """Initialize statistics."""
        self.settings = game.settings

        # Start game in an inactive state.
        self.game_active = False
        self.reset_stats()

        # High score should never be reset.
        with open("high_score.json", "r") as f:
            data = json.load(f)
            self.high_score = int(data["high_score"])

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.lives_left = self.settings.lives
        self.settings.brick_hitpoints = 1
        self.settings.brick_points = 10
        self.score = 0
        self.level = 1

    def save_high_score(self):
        """Write the high score to the file for later retrieval."""
        with open("high_score.json", "w") as f:
            data = json.dumps({
                "high_score": str(self.high_score),
                "level": str(self.level),
                "lives_left": str(self.lives_left)
            })
            f.write(data)