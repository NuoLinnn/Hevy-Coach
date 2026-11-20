"""Render a Plan as the before/after table (SPEC §2.3)."""

from hevy_coach.models import Plan


def render(plan: Plan, applied: bool) -> str:
    """The table and any warnings, ready to print."""
    raise NotImplementedError
