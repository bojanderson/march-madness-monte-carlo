from src import game, team


def test_game() -> None:
    team1 = team.Team("Team 1", 1200, 1)
    team2 = team.Team("Team 2", 1100, 2)
    g = game.Game(team1, team2)

    assert g.team1 == team1
    assert g.team2 == team2


def test_play() -> None:
    team1 = team.Team("Team 1", 1200, 1)
    team2 = team.Team("Team 2", 1100, 2)
    g = game.Game(team1, team2)

    assert g.play() in [True, False]


def test_update_elo_ratings() -> None:
    team1 = team.Team("Team 1", 1200, 1)
    team2 = team.Team("Team 2", 1100, 2)

    g = game.Game(team1, team2)

    g.update_elo_ratings(True)
    assert team1.elo_rating > 1200
    assert team2.elo_rating < 1100

    g.update_elo_ratings(False)
    assert team1.elo_rating < 1200
    assert team2.elo_rating > 1100
