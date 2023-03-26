from math import log2
from typing import List

from src.game import Game
from src.team import Team


class Tournament:
    def __init__(self, teams: List[Team]) -> None:
        if len(teams) % 2 != 0:
            raise ValueError("Number of teams must be even")
        # Check if number of teams is a power of 2 (ex: 2, 4, 8, 16, 32, 64, etc.)
        if log2(len(teams)) % 1 != 0:
            raise ValueError("Number of teams must be a power of 2")

        # The list of teams must be in order of how the games will be played, and the
        # teams will be paired up in order. If a team is a bye, the value None should
        # be used in the opponents list.

        # Example of a tournament with 7 teams and a bye in the first round:
        # [Team1, None, Team2, Team3, Team4, Team5, Team6, Team7]
        # The first round will be:
        # Team1 vs Bye
        # Team2 vs Team3
        # Team4 vs Team5
        # Team6 vs Team7
        # The second round will be:
        # Winner of (Team1 vs Bye) vs Winner of (Team2 vs Team3)
        # Winner of (Team4 vs Team5) vs Winner of (Team6 vs Team7)
        # ... and so on

        self.teams = teams

    def play_round(self, round_teams: List[Team]) -> List[Team]:
        """
        Play a round of the tournament. The teams in the round_teams list will be
        paired up in order, and the winner of each game will be returned in a list.
        """
        winners = []

        for i in range(0, len(round_teams), 2):
            team1 = round_teams[i]
            team2 = round_teams[i + 1]
            game = Game(team1, team2)
            winner = game.play()
            game.update_elo_ratings(winner)
            if winner:
                winners.append(team1)
            else:
                winners.append(team2)
        return winners

    def play_tournament(self) -> List[List[Team]]:
        """
        Play the entire tournament, and return a dictionary each round as a key, and
        the teams in that round as a list.
        """
        round_teams = self.teams
        results = [round_teams]

        while len(round_teams) > 1:
            winners = self.play_round(round_teams)
            if len(winners) == 1:
                results.append(winners)
            else:
                results.append(winners)
            round_teams = winners

        return results
