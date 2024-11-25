import random


def get_mock_board():
    # Generate a list of 100 elements, mostly "."
    weighted_choices = (
        ["."] * 85
        + [{"type": t, "hp": 1} for t in ["WB", "WC", "BB", "BC"]] * 2
        + ["H"] * 5
    )
    return [random.choice(weighted_choices) for _ in range(100)]
