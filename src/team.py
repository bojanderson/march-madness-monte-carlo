class Team:
    def __init__(self, name: str, elo_rating: float, seed: int) -> None:
        self.name = name
        self.elo_rating = elo_rating
        self.seed = seed

    def update_elo_rating(self, opponent_rating: float, result: bool) -> None:
        """
        Update the team's elo rating based on the result of the game
        """
        k_factor = 32
        expected_score = 1 / (1 + 10 ** ((opponent_rating - self.elo_rating) / 400))
        self.elo_rating += k_factor * (result - expected_score)

    def __str__(self) -> str:
        return f"{self.name}: {self.elo_rating}"
