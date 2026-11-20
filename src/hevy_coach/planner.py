"""Build a Plan for a routine and turn it into an updated Routine (SPEC §9)."""

from collections.abc import Sequence

from hevy_coach.models import Plan, Routine, RoutineConfig, Workout


def make_plan(
    routine: Routine, workouts: Sequence[Workout], config: RoutineConfig
) -> Plan:
    """Pick each exercise's rule by mode and compute its next prescription."""
    raise NotImplementedError


def apply_plan(plan: Plan) -> Routine:
    """The new Routine to send with put_routine: only working sets change."""
    raise NotImplementedError
