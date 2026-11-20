"""Typed data shared by every module (SPEC §4). Every weight here is in lb."""

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Any, ClassVar, Literal

SetType = Literal["warmup", "normal", "failure", "dropset"]
Mode = Literal["bodybuilding", "powerlifting"]


@dataclass(frozen=True)
class WorkSet:
    type: SetType
    weight_lb: float | None  # None for bodyweight-only sets
    reps: int | None
    rpe: float | None = None

    @property
    def is_working(self) -> bool:
        return self.type != "warmup"


@dataclass(frozen=True)
class Session:
    """One exercise within one logged workout."""

    exercise_title: str
    exercise_template_id: str
    start_time: datetime
    sets: tuple[WorkSet, ...]


@dataclass(frozen=True)
class Workout:
    """One logged workout, as returned by the API."""

    id: str
    title: str
    start_time: datetime
    sessions: tuple[Session, ...]


@dataclass(frozen=True)
class RoutineExercise:
    exercise_title: str
    exercise_template_id: str
    sets: tuple[WorkSet, ...]
    raw: Mapping[str, Any]  # every other API field, sent back unchanged


@dataclass(frozen=True)
class Routine:
    id: str
    title: str
    exercises: tuple[RoutineExercise, ...]
    raw: Mapping[str, Any]


@dataclass(frozen=True)
class BodybuildingSettings:
    """Resolved settings for one exercise in bodybuilding mode (SPEC §3.1)."""

    mode: ClassVar[Mode] = "bodybuilding"

    rep_min: int
    rep_max: int
    increment_lb: float = 5
    stall_sessions: int = 3
    deload_pct: float = 10
    plate_increment_lb: float = 5
    lookback_sessions: int = 6


@dataclass(frozen=True)
class PowerliftingSettings:
    """Resolved settings for one exercise in powerlifting mode (SPEC §3.1)."""

    mode: ClassVar[Mode] = "powerlifting"

    target_reps: int
    target_rpe: float
    backoff_reps: int
    backoff_drop_pct: float = 10
    drop_sessions: int = 2
    deload_pct: float = 10
    plate_increment_lb: float = 5
    lookback_sessions: int = 6


Settings = BodybuildingSettings | PowerliftingSettings


@dataclass(frozen=True)
class RoutineConfig:
    settings: Settings  # routine-level settings
    exercises: Mapping[str, Settings]  # per-exercise overrides, already resolved

    def settings_for(self, exercise_title: str) -> Settings:
        return self.exercises.get(exercise_title, self.settings)


@dataclass(frozen=True)
class Config:
    routines: Mapping[str, RoutineConfig]


@dataclass(frozen=True)
class Prescription:
    """The new working sets for one exercise."""

    sets: tuple[WorkSet, ...]
    reason: str  # shown in the "Why" column
    warning: str | None = None


@dataclass(frozen=True)
class ExercisePlan:
    exercise_title: str
    mode: Mode
    before: tuple[WorkSet, ...]
    after: Prescription


@dataclass(frozen=True)
class Plan:
    routine: Routine
    exercises: tuple[ExercisePlan, ...]
