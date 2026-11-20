"""RPE percentage table and estimated 1RM (SPEC §8.2).

The table values in SPEC.md must be checked against the published RTS chart
before they are entered here.
"""


def rpe_percent(reps: int, rpe: float) -> float:
    """Fraction of 1RM for reps @ rpe, e.g. 0.863. ValueError outside the table."""
    raise NotImplementedError


def e1rm(weight_lb: float, reps: int, rpe: float) -> float:
    """Estimated 1RM: weight / rpe_percent(reps, rpe)."""
    return weight_lb / rpe_percent(reps, rpe)
