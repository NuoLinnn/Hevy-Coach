"""Powerlifting mode: RPE top set, back-off sets, e1RM deload (SPEC §8.2)."""

from collections.abc import Sequence

from hevy_coach.models import Prescription, PowerliftingSettings, Session, WorkSet


class PowerliftingRule:
    def next(
        self,
        current: Sequence[WorkSet],
        history: Sequence[Session],
        settings: PowerliftingSettings,
    ) -> Prescription:
        raise NotImplementedError
