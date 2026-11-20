"""Load and validate hevy-coach.toml (SPEC §3)."""

from pathlib import Path

from hevy_coach.models import Config


class ConfigError(Exception):
    """A missing file, invalid TOML, unknown mode or key, or a bad value."""


def load_config(path: Path) -> Config:
    """Read the TOML file at path and resolve every routine's settings."""
    raise NotImplementedError
