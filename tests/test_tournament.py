from src.team import Team
from src.tournament import Tournament


def test_tournament() -> None:
    """
    Test that the tournament class is initialized correctly
    """
    team1 = Team("Team 1", 1200, 1)
    team2 = Team("Team 2", 1100, 2)
    team3 = Team("Team 3", 1000, 3)

    t = Tournament([team1, team2])
    assert t.teams == [team1, team2]

    t = Tournament(
        [
            team1,
            None,
            team2,
            team3,
        ]
    )
    assert t.teams == [
        team1,
        None,
        team2,
        team3,
    ]


def test_tournament_one_team() -> None:
    """
    Test that the tournament class raises a Value Error when initialized with only one
    team
    """
    try:
        Tournament([Team("Team 1", 1200, 1)])
    except ValueError:
        pass
    else:
        raise AssertionError("ValueError not raised")


def test_tournament_non_log2_teams() -> None:
    """
    Test that the tournament class raises a Value Error when initialized with a number
    of teams that is not a power of 2
    """
    try:
        Tournament(
            [
                Team("Team 1", 1200, 1),
                Team("Team 2", 1100, 2),
                Team("Team 3", 1000, 3),
            ]
        )
    except ValueError:
        pass
    else:
        raise AssertionError("ValueError not raised")


def test_play_round() -> None:
    """
    Test that the tournament class can play a round
    """
    team1 = Team("Team 1", 1200, 1)
    team2 = Team("Team 2", 1100, 2)
    team3 = Team("Team 3", 1000, 3)
    team4 = Team("Team 4", 900, 4)

    teams = [team1, team2, team3, team4]

    t = Tournament(teams)
    winners = t.play_round(teams)
    assert len(winners) == 2
    assert winners[0] in [team1, team2]
    assert winners[1] in [team3, team4]

    winners = t.play_round([team1, team3])
    assert len(winners) == 1
    assert winners[0] in [team1, team3]


def test_play_round_bye() -> None:
    """
    Test that the tournament class can play a round with a bye and always advances the
    team with the bye
    """
    team1 = Team("Team 1", 1200, 1)
    team2 = Team("Team 2", 1100, 2)
    team3 = Team("Team 3", 1000, 3)
    team4 = Team("Team 4", 900, 4)
    team5 = Team("Team 5", 800, 5)

    teams = [team1, None, team2, team3, None, team4, team5, None]

    t = Tournament(teams)

    winners = t.play_round(teams)

    assert len(winners) == 4
    assert winners[0] == team1
    assert winners[1] in [team2, team3]
    assert winners[2] == team4
    assert winners[3] == team5
    # Check no value in winners is None
    assert all(winners)


def test_play_tournament() -> None:
    """
    Test that the tournament class can play a tournament
    """
    team1 = Team("Team 1", 1200, 1)
    team2 = Team("Team 2", 1100, 2)
    team3 = Team("Team 3", 1000, 3)
    team4 = Team("Team 4", 900, 4)

    teams = [team1, team2, team3, team4]

    t = Tournament(teams=teams)
    results = t.play_tournament()

    assert len(results) == 3
    assert results[0] == teams
    assert results[1][0] in [team1, team2]
    assert results[1][1] in [team3, team4]
    assert results[2][0] in teams
    assert len(results[0]) == 4
    assert len(results[1]) == 2
    assert len(results[2]) == 1
