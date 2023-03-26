from src import team


def test_team() -> None:
    """
    Test that the team class is initialized correctly
    """
    t = team.Team("Test Team", 1200, 1)
    assert t.name == "Test Team"
    assert t.elo_rating == 1200
    assert t.seed == 1


def test_update_elo_rating() -> None:
    """
    Test that the team's elo rating can be updated
    """
    t = team.Team("Test Team", 1200, 1)
    t.update_elo_rating(1300, 1)
    assert t.elo_rating == 1200 + 32 * (1 - 1 / (1 + 10 ** ((1300 - 1200) / 400)))


def test_team_str() -> None:
    """
    Test that the team's string representation is correct
    """
    t = team.Team("Test Team", 1200, 1)
    assert str(t) == "Test Team: 1200"
