class GameStats:
    """Track game stats for Alien Invasion."""
    def __init__(self, game):
        """Initialize statistics."""
        self.settings = game.settings

        # Start game in an inactive state.
        self.game_active = False
        self.reset_stats()

        # High score should never be reset.
        with open("high_score.txt", "r") as f:
            self.high_score = int(f.read())

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.lives_left = self.settings.lives
        self.score = 0
        self.level = 1