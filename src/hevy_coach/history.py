"""Select recent sessions of one exercise (SPEC §7)."""

from collections.abc import Sequence

from hevy_coach.models import Session, Workout


def recent_sessions(
    workouts: Sequence[Workout], template_id: str, lookback: int
) -> list[Session]:
    """Up to lookback sessions of one exercise, newest first, warm-ups removed."""
    raise NotImplementedError
