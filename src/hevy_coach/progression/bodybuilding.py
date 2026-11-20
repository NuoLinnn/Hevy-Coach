"""Bodybuilding mode: double progression with a stall deload (SPEC §8.1)."""

from collections.abc import Sequence

from hevy_coach.models import BodybuildingSettings, Prescription, Session, WorkSet


class BodybuildingRule:
    def next(
        self,
        current: Sequence[WorkSet],
        history: Sequence[Session],
        settings: BodybuildingSettings,
    ) -> Prescription:
        raise NotImplementedError
