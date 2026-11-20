"""The Rule protocol that every training mode implements (SPEC §8)."""

from collections.abc import Sequence
from typing import Protocol

from hevy_coach.models import Prescription, Session, Settings, WorkSet


class Rule[S: Settings](Protocol):
    def next(
        self,
        current: Sequence[WorkSet],
        history: Sequence[Session],
        settings: S,
    ) -> Prescription:
        """The next working sets, given the routine's current working sets and
        recent sessions (newest first). Pure: no I/O, inputs are not changed."""
        ...
