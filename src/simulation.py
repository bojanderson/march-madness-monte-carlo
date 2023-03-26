import argparse
from typing import List

import pandas as pd

from src.team import Team
from src.tournament import Tournament


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(
        description="Run a simulation of the NCAA tournament"
    )
    parser.add_argument(
        "filename",
        type=str,
        help="The name of the file containing the teams and their elo ratings",
    )
    parser.add_argument(
        "--num_sims",
        type=int,
        default=10000,
        help="The number of simulations to run",
    )

    return parser.parse_args()


def load_teams_from_538file(filename: str, slot_provided: bool) -> List[Team]:
    """
    Load teams from a JSON file in the format used by FiveThirtyEight
    """
    teams_df = pd.read_csv(filename)

    earliest_forecast_date = teams_df["forecast_date"].min()

    # Filter out teams that were not forecasted on the earliest date
    teams_df = teams_df[teams_df["forecast_date"] == earliest_forecast_date]

    if slot_provided:
        max_value = teams_df["team_slot"].max() + 1
    else:
        num_rows = len(teams_df.index)
        # Calculate the next power of 2
        max_value = 2 ** (num_rows - 1).bit_length()

    teams = [None] * max_value

    if slot_provided:
        for row in teams_df.itertuples():
            teams[row.team_slot] = Team(row.team_name, row.team_elo, row.team_seed)
    else:
        # If team slots are not provided, we have to figure out team slots by ourselves
        # and I have to figure that out later
        raise NotImplementedError

    return teams


def run_simulation(num_simulations: int, teams: List[Team]) -> List[List[List[Team]]]:
    """
    Run a simulation of the tournament and return the winner
    """
    results = []
    tournament = Tournament(teams)
    for i in range(num_simulations):
        results.append(tournament.play_tournament())
    return results


def analyze_simulation(results: List[List[List[Team]]]) -> List[pd.DataFrame]:
    """
    Analyze the results of a simulation and return a list of dataframes of interesting
    statistics

    1. A dataframe of each team and their probability of winning each round
    2. A dataframe of each team and the number of teams they got X wins
    3. A dataframe of each seed and their average number of wins
    4.
    """

    # Given a list of simulations, where each simulation is a list of rounds, where
    # each round is a list of teams, return a dataframe of each team and their]
    # probability of winning each round
    def get_probabilities(results: List[List[List[Team]]]) -> pd.DataFrame:
        # Create a dataframe with the number of teams as the index and the number of
        # rounds as the columns, ignoring None and the First round

        # Num of teams would be the number of teams in the first round of the first
        # simulation excluding None values
        num_teams = len([team for team in results[0][0] if team is not None])
        # Num of rounds would be the number of rounds in the first simulation excluding
        # the first round
        num_rounds = len(results[0]) - 1
        df = pd.DataFrame(index=range(num_teams), columns=range(num_rounds))

        # Fill the dataframe with the number of times each team won each round
        for simulation in results:
            for round_num, round in enumerate(simulation):
                for team in round:
                    if team is not None:
                        df.loc[team.id, round_num] = (
                            df.loc[team.id, round_num] + 1
                            if df.loc[team.id, round_num] is not None
                            else 1
                        )

        # Divide each cell by the number of simulations to get the probability of
        # winning each round
        df = df / len(results)

        return df

    def get_wins(results: List[List[List[Team]]]) -> pd.DataFrame:
        # Create a dataframe with the number of teams as the index and the number of
        # wins as the columns

        teams = [team for team in results[0][0] if team is not None]

        num_teams = len(teams)
        # Num of wins would be the number of rounds in the first simulation excluding
        # the first round
        num_wins = len(results[0]) - 1
        df = pd.DataFrame(index=range(num_teams), columns=range(num_wins))

        # Fill the dataframe with the number of times each team got X wins, skip the
        # first round
        for simulation in results:
            sim_wins = {team: 0 for team in teams}
            for i, round in enumerate(simulation):
                if i == 0:
                    continue
                else:
                    for team in round:
                        if team is not None:
                            sim_wins[team] += 1
            for team, wins in sim_wins.items():
                df.loc[team.id, wins] = (
                    df.loc[team.id, wins] + 1
                    if df.loc[team.id, wins] is not None
                    else 1
                )

        # Divide each cell by the number of simulations to get the probability of
        # winning each round
        df = df / len(results)

        return df

    def get_seed_wins(results: List[List[List[Team]]]) -> pd.DataFrame:

        teams = [team for team in results[0][0] if team is not None]

        seeds = set([team.seed for team in teams])

        # Count how many teams are in each seed
        seed_counts = {seed: 0 for seed in seeds}
        for team in teams:
            seed_counts[team.seed] += 1

        num_seeds = len(seeds)

        num_wins = len(results[0]) - 1
        df = pd.DataFrame(index=range(num_seeds), columns=range(num_wins))

        # Fill the dataframe with the number of times each team got X wins, skip the
        # first round
        for simulation in results:
            sim_wins = {seed: 0 for seed in teams}
            for i, round in enumerate(simulation):
                if i == 0:
                    continue
                else:
                    for team in round:
                        if team is not None:
                            sim_wins[team.seed] += 1
            for seed, wins in sim_wins.items():
                df.loc[seed, wins] = (
                    df.loc[seed, wins] + 1 if df.loc[seed, wins] is not None else 1
                )

        # Divide each cell by the number of simulations to get the probability of
        # winning each round
        for seed, count in seed_counts.items():
            df.loc[seed] = df.loc[seed] / count

        return df

    df1 = get_probabilities(results)
    df2 = get_wins(results)
    df3 = get_seed_wins(results)

    return [df1, df2, df3]


def main(filename: str, num_sims: int = 1000):
    # Get the teams
    teams = load_teams_from_538file(filename)
    # Run the simulation
    results = run_simulation(num_simulations=num_sims, teams=teams)

    # Analyze the results
    dataframes = analyze_simulation(results)

    # Print the results
    for df in dataframes:
        print(df)


if __name__ == "__main__":

    args = parse_args()

    input_file = args.input_file
    num_simulations = args.num_simulations

    main(input_file, num_simulations)
