"""kg <-> lb conversion and plate rounding (SPEC §5).

Conversion is only called from client.py; every other module works in lb.
"""

import math
from typing import Final

LB_PER_KG: Final = 2.20462262185


def kg_to_lb(kg: float) -> float:
    """Convert kg from the API to lb, rounded to 0.1 lb so lb -> kg -> lb is exact."""
    return round(kg * LB_PER_KG, 1)


def lb_to_kg(lb: float) -> float:
    """Convert lb to kg for the API. Not rounded, to keep full precision."""
    return lb / LB_PER_KG


def round_to_plate(lb: float, increment: float) -> float:
    """Round to the nearest multiple of increment, with ties going up.

    Python's round() sends ties to the even number (round(27.5) == 28 but
    round(26.5) == 26), so floor(x + 0.5) is used instead.
    """
    if increment <= 0:
        raise ValueError(f"increment must be > 0, got {increment}")
    return math.floor(lb / increment + 0.5) * increment
