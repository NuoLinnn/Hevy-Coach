import pytest

from hevy_coach.units import kg_to_lb, lb_to_kg, round_to_plate


@pytest.mark.parametrize(
    ("lb", "increment", "expected"),
    [
        (137.2, 5, 135),
        (137.5, 5, 140),  # tie goes up
        (132.5, 5, 135),  # tie goes up, not to even (round(26.5) == 26)
        (137.4, 2.5, 137.5),
        (136.2, 2.5, 135),
        (135, 5, 135),
        (0, 5, 0),
    ],
)
def test_round_to_plate(lb: float, increment: float, expected: float) -> None:
    assert round_to_plate(lb, increment) == expected


@pytest.mark.parametrize("increment", [0, -5])
def test_round_to_plate_rejects_bad_increment(increment: float) -> None:
    with pytest.raises(ValueError):
        round_to_plate(100, increment)


def test_kg_to_lb_rounds_to_tenth() -> None:
    assert kg_to_lb(100) == 220.5
    assert kg_to_lb(20) == 44.1


def test_lb_kg_round_trip_has_no_drift() -> None:
    # every multiple of 0.5 lb from 0 to 1500 lb comes back exactly
    for half_lbs in range(0, 3001):
        lb = half_lbs / 2
        assert kg_to_lb(lb_to_kg(lb)) == lb, lb


def test_135_lb_round_trip() -> None:
    assert kg_to_lb(lb_to_kg(135)) == 135
