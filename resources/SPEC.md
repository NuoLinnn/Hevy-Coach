# hevy-coach: specification

EC602 Final Project, Track 2. Nuo Lin. Version 0.1 (checkpoint, November 19, 2026).

## 1. Purpose

`hevy-coach` reads a lifter's recent workouts from Hevy, decides the next target weight
and reps for each exercise in a routine, and (only when asked) writes those targets back
into the routine in Hevy.

There are two **training modes**, each with its own progression rules:

- **bodybuilding:** double progression within a rep range, with a deload after a stall.
- **powerlifting:** an RPE-based top set plus back-off sets, with a deload when the
  estimated 1RM keeps falling.

The user sees and configures every weight in **pounds**.

### 1.1 Users

A lifter who logs workouts in Hevy, has a Hevy Pro plan (needed for API access), and
follows a routine-based program. The first user is the author.

### 1.2 Out of scope

A GUI, an MCP server, nutrition or cardio, creating new routines, changing the exercise
list or the set count of a routine, and any units other than lb for the user.

## 2. Installation and use

```bash
uv pip install git+https://github.com/NuoLinnn/Hevy-Coach
export HEVY_API_KEY=...            # from Hevy → Settings → Developer
hevy-coach plan --routine "Push A"           # dry run: prints the plan only
hevy-coach plan --routine "Push A" --apply   # also updates the routine in Hevy
```

### 2.1 Command line

```
hevy-coach plan --routine NAME [--config PATH] [--apply]
```

| Option | Default | Meaning |
|---|---|---|
| `--routine NAME` | required | Hevy routine title, matched exactly (case-sensitive) |
| `--config PATH` | `./hevy-coach.toml` | configuration file (§3) |
| `--apply` | off | send the new routine to Hevy. Without it, nothing is written. |

The API key is read from the environment variable `HEVY_API_KEY`. It is never read from
the config file and never printed.

### 2.2 Exit codes

| Code | Meaning |
|---|---|
| 0 | success (warnings, if any, were printed) |
| 1 | configuration error (missing file, invalid TOML, unknown mode, bad value) |
| 2 | API error (missing key, 401/403, network, unexpected response) |
| 3 | routine not found in Hevy, or not listed in the config |

Every error prints one line to stderr in the form `hevy-coach: error: <message>`. No
tracebacks are shown for the errors listed above.

### 2.3 Output

`plan` prints one row per exercise in routine order, then any warnings:

```
Routine: Push A (bodybuilding)                         DRY RUN: nothing sent
Exercise                  Mode           Before            After             Why
Bench Press (Barbell)     bodybuilding   3 × 10 @ 185 lb   3 × 11 @ 185 lb   +1 rep
Incline Press (Dumbbell)  bodybuilding   3 × 12 @ 60 lb    3 × 8 @ 65 lb     top of range
Lateral Raise (Dumbbell)  bodybuilding   3 × 15 @ 20 lb    3 × 15 @ 20 lb    no change

warning: Cable Fly: no sessions found in the last 6 workouts; left unchanged
```

`Before` and `After` show only the working sets. For powerlifting exercises, the top set
and back-off sets are shown separately (`1 × 3 @ 365 lb, 3 × 3 @ 330 lb`). With
`--apply`, the header reads `APPLIED` and is printed only after the API accepts the PUT.

## 3. Configuration file

The file is TOML. Every weight is in lb. Exercises are identified by their Hevy title,
exactly as shown in the app.

```toml
[defaults]
plate_increment_lb = 5      # every planned weight is rounded to a multiple of this
lookback_sessions = 6       # how many recent sessions of each exercise to read

[routines."Push A"]
mode = "bodybuilding"
rep_min = 8
rep_max = 12
increment_lb = 5
stall_sessions = 3
deload_pct = 10

[routines."Push A".exercises."Lateral Raise (Dumbbell)"]
rep_min = 12                # per-exercise override; any key may be overridden
rep_max = 15

[routines."Squat Day"]
mode = "powerlifting"
target_reps = 3
target_rpe = 8
backoff_drop_pct = 10
backoff_reps = 3
drop_sessions = 2
deload_pct = 10

[routines."Squat Day".exercises."Leg Extension (Machine)"]
mode = "bodybuilding"       # an override may also switch the mode
rep_min = 10
rep_max = 15
increment_lb = 5
stall_sessions = 3
deload_pct = 10
```

### 3.1 Settings

How a setting is resolved for an exercise: the exercise override, then the routine
section, then `[defaults]`, then the built-in default. If a required setting has no value
at any level, that is a configuration error.

| Key | Mode | Type | Built-in default | Valid values |
|---|---|---|---|---|
| `mode` | both | str | none (required) | `"bodybuilding"`, `"powerlifting"` |
| `plate_increment_lb` | both | float | 5 | > 0 |
| `lookback_sessions` | both | int | 6 | ≥ 2 |
| `rep_min` | bb | int | none (required) | ≥ 1 |
| `rep_max` | bb | int | none (required) | ≥ `rep_min` |
| `increment_lb` | bb | float | 5 | > 0 |
| `stall_sessions` | bb | int | 3 | ≥ 1 |
| `deload_pct` | both | float | 10 | 0 < x < 50 |
| `target_reps` | pl | int | none (required) | 1–8 |
| `target_rpe` | pl | float | none (required) | 7–10, in steps of 0.5 |
| `backoff_drop_pct` | pl | float | 10 | 0 ≤ x < 50 |
| `backoff_reps` | pl | int | `target_reps` | ≥ 1 |
| `drop_sessions` | pl | int | 2 | ≥ 1 |

Unknown keys are a configuration error, so that a typo such as `rep_mx` is not silently
ignored. An exercise in the routine with no override uses the routine's settings.

## 4. Data model

All of these are frozen dataclasses in `models.py`. Every weight in them is in **lb**.

```python
SetType = Literal["warmup", "normal", "failure", "dropset"]

@dataclass(frozen=True)
class WorkSet:
    type: SetType
    weight_lb: float | None      # None for bodyweight-only sets
    reps: int | None
    rpe: float | None

@dataclass(frozen=True)
class Session:                   # one exercise within one logged workout
    exercise_title: str
    exercise_template_id: str
    start_time: datetime
    sets: tuple[WorkSet, ...]

@dataclass(frozen=True)
class Workout:                   # one logged workout, as returned by the API
    id: str
    title: str
    start_time: datetime
    sessions: tuple[Session, ...]

@dataclass(frozen=True)
class RoutineExercise:
    exercise_title: str
    exercise_template_id: str
    sets: tuple[WorkSet, ...]
    raw: dict[str, Any]          # every other API field, sent back unchanged

@dataclass(frozen=True)
class Routine:
    id: str
    title: str
    exercises: tuple[RoutineExercise, ...]
    raw: dict[str, Any]

@dataclass(frozen=True)
class Prescription:              # the new working sets for one exercise
    sets: tuple[WorkSet, ...]
    reason: str                  # shown in the "Why" column
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
```

**Working sets** are all sets whose type is not `"warmup"`. Warm-up sets in a routine
are copied through unchanged and never shown in the output.

## 5. Units and rounding (`units.py`)

```python
LB_PER_KG: Final = 2.20462262185

def kg_to_lb(kg: float) -> float      # round(kg * LB_PER_KG, 1)
def lb_to_kg(lb: float) -> float      # lb / LB_PER_KG, not rounded
def round_to_plate(lb: float, increment: float) -> float
```

- Conversion happens **only** in `client.py`: kg → lb when a response is parsed, and
  lb → kg when the PUT body is built. No other module ever sees kg.
- `kg_to_lb` rounds to 0.1 lb. This guarantees the round trip:
  `kg_to_lb(lb_to_kg(x)) == x` for every multiple of 0.5 lb up to 1500 lb.
- `round_to_plate` rounds to the **nearest** multiple of `increment`, with ties going
  up: `round_to_plate(137.2, 5) == 135`, `round_to_plate(137.5, 5) == 140`. It does not
  use Python's `round()`, which rounds ties to the even number.
- Every weight a rule produces passes through `round_to_plate` exactly once, as the
  last step.

## 6. Hevy API client (`client.py`)

Base URL `https://api.hevyapp.com`. Every request sends the header `api-key: <key>`.

```python
class HevyClient:
    def __init__(self, api_key: str, http: httpx.Client | None = None) -> None
    def get_routines(self) -> list[Routine]
    def get_workouts(self, limit: int) -> list[Workout]   # newest first
    def put_routine(self, routine: Routine) -> None
```

| Method | Endpoint | Notes |
|---|---|---|
| `get_routines` | `GET /v1/routines?page=N&pageSize=10` | follows `page_count` until every page has been read |
| `get_workouts` | `GET /v1/workouts?page=N&pageSize=10` | stops once `limit` workouts are collected or the pages run out |
| `put_routine` | `PUT /v1/routines/{id}` | body `{"routine": {...}}` built from `raw` plus the new sets |

Errors are all raised as `HevyAPIError(message)`:

| Situation | Message contains |
|---|---|
| 401 or 403 | `check HEVY_API_KEY and that the account has Hevy Pro` |
| 429 | `rate limited`; the request is retried once after 2 s, then this error |
| other 4xx/5xx, timeout, network | the status code or exception name |
| JSON missing a required field | `unexpected response` and the field name |

`put_routine` sends every routine field back unchanged (title, notes, folder, rest times,
superset ids) and changes only the `weight_kg` and `reps` of working sets. Because the
API's PUT replaces the whole routine, leaving out a field would erase it.

> **To confirm before the client is finished:** check the exact field names and the PUT
> schema against the official API docs (`https://api.hevyapp.com/docs`) and against
> fixtures recorded from my own account. Any difference is recorded in this section.

## 7. History (`history.py`)

```python
def recent_sessions(workouts: Sequence[Workout], template_id: str,
                    lookback: int) -> list[Session]
```

This returns up to `lookback` sessions of one exercise, newest first, collected from
**all** workouts (not only those started from this routine). It matches on
`exercise_template_id`, so renaming a routine does not lose the history. Warm-up sets are
removed. A session left with no working sets is skipped.

## 8. Progression rules (`progression/`)

```python
class Rule(Protocol):
    def next(self, current: Sequence[WorkSet], history: Sequence[Session],
             settings: Settings) -> Prescription: ...
```

`current` holds the routine's current working sets for the exercise; `history` holds the
recent sessions, newest first. A rule is a pure function: it does no I/O and does not
change its inputs. The set count of the routine is always kept.

If `history` is empty, every rule returns `current` unchanged with reason `no change`
and a warning `no sessions found in the last <lookback> workouts`.

### 8.1 Bodybuilding (`bodybuilding.py`)

Let `w` be the current routine weight and `t` the current target reps (taken from the
first working set of `current`). Let `S` be the newest session.

A session's **score** is the pair `(top weight, total reps of the working sets at that
weight)`, compared in order: weight first, then reps. A session is a **stall** if its
score is not greater than the score of the session before it.

The rules are checked in this order. The first one that applies wins:

1. **Deload.** If the newest `stall_sessions` sessions are all stalls (this needs
   `stall_sessions + 1` sessions of history): weight = `round_to_plate(w × (1 −
   deload_pct/100))`, reps = `rep_min`. Reason: `deload after N stalls`.
2. **Top of range.** If every working set in `S` has `reps ≥ rep_max` and
   `weight ≥ w`: weight = `round_to_plate(w + increment_lb)`, reps = `rep_min`.
   Reason: `top of range`.
3. **Add a rep.** If every working set in `S` has `reps ≥ t` and `weight ≥ w`: weight
   = `w`, reps = `min(t + 1, rep_max)`. Reason: `+1 rep`.
4. **Otherwise** nothing changes. Reason: `no change`.

All working sets in the result have the same weight and reps.

### 8.2 Powerlifting (`powerlifting.py`, `rpe.py`)

The **top set** of a session is its heaviest working set. If two sets tie, the earlier
one is the top set. In the routine, the first working set is the top set and the
remaining working sets are back-off sets.

```python
def rpe_percent(reps: int, rpe: float) -> float   # fraction of 1RM, e.g. 0.863
def e1rm(weight_lb: float, reps: int, rpe: float) -> float  # weight / rpe_percent
```

`rpe_percent` uses the table below. It is indexed by **effective reps** = `reps + (10 −
rpe)`, so for example 3 @ RPE 8 is read at index 5. It is defined for reps 1–8 and RPE
7–10 in steps of 0.5. Anything outside that range raises `ValueError`.

| eff. reps | 1 | 1.5 | 2 | 2.5 | 3 | 3.5 | 4 | 4.5 | 5 | 5.5 | 6 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| % 1RM | 100.0 | 97.8 | 95.5 | 93.9 | 92.2 | 90.7 | 89.2 | 87.8 | 86.3 | 85.0 | 83.7 |

| eff. reps | 6.5 | 7 | 7.5 | 8 | 8.5 | 9 | 9.5 | 10 | 10.5 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|
| % 1RM | 82.4 | 81.1 | 79.9 | 78.6 | 77.4 | 76.2 | 75.1 | 73.9 | 72.3 | 70.7 |

> These values come from the widely used RTS (Reactive Training Systems) RPE chart. I
> will check every value against the published chart before `rpe.py` is written, and
> cite the source in the README.

The rules for each exercise, checked in this order:

1. **No RPE.** If the top set of `S` has no RPE, or its reps/RPE are outside the table:
   return unchanged, reason `no change`, warning `<exercise>: top set has no RPE logged`
   (or `outside RPE table`).
2. Compute `E` = the e1RM of the top set of each session that has a usable RPE.
3. **Deload.** If the newest `drop_sessions` values of `E` are each strictly lower than
   the value before them: top weight = `round_to_plate(E[0] × rpe_percent(target_reps,
   target_rpe) × (1 − deload_pct/100))`. Reason: `deload after N e1RM drops`.
4. **Otherwise:** top weight = `round_to_plate(E[0] × rpe_percent(target_reps,
   target_rpe))`. Reason: `e1RM <E[0]> lb`.
5. **Back-off sets:** weight = `round_to_plate(top × (1 − backoff_drop_pct/100))`,
   reps = `backoff_reps`. The top set gets reps = `target_reps` and RPE =
   `target_rpe`.

Example: a top set of 315 lb × 3 @ RPE 8 → `E = 315 / 0.863 = 365.0`. A target of
3 @ 8 → `365.0 × 0.863 = 315.0` → 315 lb. Back-offs at −10% → 283.5 → 285 lb.

## 9. Planner (`planner.py`)

```python
def make_plan(routine: Routine, workouts: Sequence[Workout],
              config: RoutineConfig) -> Plan
def apply_plan(plan: Plan) -> Routine     # the new Routine to send with put_routine
```

For each exercise in the routine: resolve its settings (§3.1), pick the rule for its
mode, call `recent_sessions`, then `rule.next`. An exercise with a warning is still part
of the plan, with its sets unchanged. `apply_plan` keeps warm-up sets and every `raw`
field, and replaces only the working sets.

## 10. Module layout

The planned layout is in `resources/modules.drawio`.

```
src/hevy_coach/
  cli.py  config.py  client.py  report.py      # I/O
  models.py  units.py                          # shared
  history.py  planner.py                       # core (pure)
  progression/base.py  bodybuilding.py  powerlifting.py  rpe.py
tests/
  fixtures/*.json   golden/*.txt   test_<module>.py
```

## 11. Tests

`uv run pytest` runs the whole suite offline. HTTP is mocked with `pytest-httpx`, and
the fixtures are API responses recorded from my account, with the API key removed.

| Area | Must show |
|---|---|
| units | the rounding examples in §5; ties round up; lb→kg→lb round trip over 0–1500 lb |
| client | pagination reads every page; 401 → clear error; 429 retried once; PUT body keeps every `raw` field and holds kg |
| history | warm-ups dropped; newest first; `lookback` respected; matched by template id |
| bodybuilding | each of the four outcomes in §8.1; deload at exactly N stalls, not N−1; only some sets at the top → +1 rep |
| powerlifting | `rpe_percent` on hand-checked rows; the §8.2 example; deload at exactly N drops; missing RPE → unchanged + warning |
| config | override precedence; mode switch per exercise; unknown key, unknown mode, missing required key → exit 1 |
| cli | golden output for one bodybuilding and one powerlifting routine; dry run sends no PUT; `--apply` sends exactly one |

Also required: `ty check` is clean, and every public function has type annotations.

## 12. Open questions

- The exact Hevy routine PUT schema (§6), to be confirmed with recorded fixtures.
- Whether Hevy stores `weight_kg` at full precision. If it does not, §5's round trip is
  instead tested against what Hevy actually returns.
- Bodyweight and assisted exercises (`weight_lb` is None): planned behavior is "left
  unchanged with a warning"; still to be decided.
