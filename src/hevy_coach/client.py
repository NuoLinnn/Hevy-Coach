"""HTTP client for the Hevy API (SPEC §6). The only module that sees kg."""

import httpx

from hevy_coach.models import Routine, Workout

BASE_URL = "https://api.hevyapp.com"
PAGE_SIZE = 10


class HevyAPIError(Exception):
    """Any failure talking to the Hevy API, with a message for the user."""


class HevyClient:
    def __init__(self, api_key: str, http: httpx.Client | None = None) -> None:
        self._http = http or httpx.Client(base_url=BASE_URL, timeout=10.0)
        self._headers = {"api-key": api_key}

    def get_routines(self) -> list[Routine]:
        """Every routine on the account, reading all pages."""
        raise NotImplementedError

    def get_workouts(self, limit: int) -> list[Workout]:
        """Up to limit workouts, newest first."""
        raise NotImplementedError

    def put_routine(self, routine: Routine) -> None:
        """Replace the routine in Hevy, keeping every field we did not change."""
        raise NotImplementedError
