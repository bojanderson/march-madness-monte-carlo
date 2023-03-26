import random

from src.team import Team


class Game:
    def __init__(self, team1: Team = None, team2: Team = None) -> None:
        self.team1 = team1
        self.team2 = team2

        if team1 is None and team2 is None:
            raise ValueError("Both teams cannot be None")

    def win_probability(self, team1_rating, team2_rating):
        return 1 / (1 + 10 ** ((team2_rating - team1_rating) / 400))

    def play(self) -> bool:
        if self.team1 is None:
            return False
        elif self.team2 is None:
            return True
        else:
            team1_win_prob = self.win_probability(
                self.team1.elo_rating, self.team2.elo_rating
            )

            team1_win = random.random() < team1_win_prob

            return team1_win

    def update_elo_ratings(self, team1_win: bool) -> None:
        if team1_win and self.team2 is not None:
            self.team1.update_elo_rating(self.team2.elo_rating, 1)
            self.team2.update_elo_rating(self.team1.elo_rating, 0)
        elif not team1_win and self.team1 is not None:
            self.team1.update_elo_rating(self.team2.elo_rating, 0)
            self.team2.update_elo_rating(self.team1.elo_rating, 1)

    def __str__(self) -> str:
        if self.team1 is None:
            return f"Bye vs {self.team2}"
        elif self.team2 is None:
            return f"{self.team1} vs Bye"
        else:
            return f"{self.team1} vs {self.team2}"
