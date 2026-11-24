# Project overview

A checklist for each module in `src/hevy_coach/`: what's done and what's left. `§`
numbers refer to [SPEC.md](SPEC.md), and the layout is in
[resources/modules.drawio](resources/modules.drawio).

Status as of Nov 24: **18 tests pass, `ty check` is clean, and 11 functions are still
stubs.**

| Module | Layer | Status |
|---|---|---|
| [units.py](src/hevy_coach/units.py) | shared | ✅ done |
| [models.py](src/hevy_coach/models.py) | shared | ✅ done |
| [progression/base.py](src/hevy_coach/progression/base.py) | core | ✅ done |
| [cli.py](src/hevy_coach/cli.py) | I/O | 🟡 parsing done, `plan` not wired |
| [progression/rpe.py](src/hevy_coach/progression/rpe.py) | core | 🟡 `e1rm` done, table not entered |
| [client.py](src/hevy_coach/client.py) | I/O | ⬜ stub |
| [config.py](src/hevy_coach/config.py) | I/O | ⬜ stub |
| [history.py](src/hevy_coach/history.py) | core | ⬜ stub |
| [progression/bodybuilding.py](src/hevy_coach/progression/bodybuilding.py) | core | ⬜ stub |
| [progression/powerlifting.py](src/hevy_coach/progression/powerlifting.py) | core | ⬜ stub |
| [planner.py](src/hevy_coach/planner.py) | core | ⬜ stub |
| [report.py](src/hevy_coach/report.py) | I/O | ⬜ stub |

Suggested order: **fixtures → client → history → config → rpe → bodybuilding →
powerlifting → planner → report → cli**. Each step needs only the steps before it.

---

## Packaging and setup
- [x] `pyproject.toml`: hatchling, `src/` layout, `hevy-coach` script, httpx; dev
      group with pytest, pytest-httpx and ty
- [x] `.gitignore` (ignores the personal `hevy-coach.toml`)
- [x] `uv sync`, `uv build`, and the wheel contains every module + `py.typed`
- [x] `ty check` is clean
- [ ] `hevy-coach.example.toml` with both modes and an override, copied from SPEC §3
- [ ] Check the install from GitHub in a fresh folder:
      `uv pip install git+https://github.com/NuoLinnn/Hevy-Coach`

## Fixtures (`tests/fixtures/`), needed before client and history
- [x] Folder created
- [ ] Record `GET /v1/routines` and `GET /v1/workouts` (at least 2 pages) from my
      account with `curl`, and remove anything private
- [ ] Hand-made workout histories for the rule tests: a bodybuilding plateau, a
      progression, a powerlifting e1RM drop, a top set with no RPE
- [ ] Compare the real field names with SPEC §6 and fix the spec where they differ
      (**AI log:** record any difference as an AI mistake)

## `units.py`: kg↔lb and plate rounding (§5) ✅
- [x] `kg_to_lb` rounds to 0.1 lb
- [x] `lb_to_kg` keeps full precision
- [x] `round_to_plate` sends ties up and rejects an increment ≤ 0
- [x] Tests: rounding examples, ties, bad increment, round trip for every 0.5 lb
      step up to 1500 lb
- [ ] Re-check the round trip against what Hevy actually stores (open question,
      §12)

## `models.py`: data types (§4) ✅
- [x] `WorkSet` (with `is_working`), `Session`, `Workout`, `RoutineExercise`,
      `Routine`
- [x] `BodybuildingSettings`, `PowerliftingSettings`, `Settings`, `RoutineConfig`
      (`settings_for`), `Config`
- [x] `Prescription`, `ExercisePlan`, `Plan`
- [x] Tests: warm-up check, override lookup, mode on the class
- [ ] Add fields if the recorded fixtures show something needed (e.g. rest times
      kept in `raw`)

## `client.py`: Hevy API (§6)
- [x] `HevyAPIError`, constructor with an injectable `httpx.Client`
- [ ] `get_routines()`: read pages until `page_count`; parse into `Routine`
- [ ] `get_workouts(limit)`: newest first, stop once `limit` is reached
- [ ] Parse JSON into models, converting kg → lb **here only**
- [ ] `put_routine()`: send back every `raw` field, change only the working sets'
      `weight_kg`/`reps`, converting lb → kg
- [ ] Errors: 401/403 → "check HEVY_API_KEY … Hevy Pro"; 429 → retry once; missing
      field → "unexpected response"
- [ ] Tests (`pytest-httpx`): pagination, every error case, the PUT body keeps the
      `raw` fields and holds kg

## `history.py`: recent sessions (§7)
- [ ] `recent_sessions()`: match on `exercise_template_id` across all workouts,
      newest first, drop warm-ups, skip sessions left empty, respect `lookback`
- [ ] Tests: each of those behaviors

## `config.py`: TOML loading (§3)
- [x] `ConfigError`, `load_config` signature
- [ ] Read with `tomllib`; a missing file or invalid TOML → `ConfigError`
- [ ] Resolve settings in order: exercise override → routine → `[defaults]` → built-in
- [ ] A per-exercise override can switch the mode
- [ ] Validate every value against the §3.1 table; an unknown key, an unknown mode, or
      a missing required key → `ConfigError` naming the key
- [ ] Default `backoff_reps` to `target_reps`
- [ ] Tests: override order, mode switch, each kind of error

## `progression/base.py`: Rule protocol (§8) ✅
- [x] Generic `Rule[S]` protocol with `next(current, history, settings)`

## `progression/rpe.py`: RPE table (§8.2)
- [x] `e1rm()` = weight / `rpe_percent`
- [ ] **Check every table value against the published RTS chart first** (the AI wrote
      them from memory)
- [ ] `rpe_percent()`: look up by effective reps = reps + (10 − RPE); `ValueError`
      outside reps 1–8 / RPE 7–10
- [ ] Tests: hand-checked rows, out-of-range inputs

## `progression/bodybuilding.py`: double progression (§8.1)
- [ ] Session score (top weight, total reps at that weight) and stall detection
- [ ] In order: deload → top of range → +1 rep → no change
- [ ] Empty history → unchanged + warning
- [ ] Every result weight goes through `round_to_plate` once
- [ ] Tests: each outcome; deload at exactly N stalls, not N−1; only some sets at
      the top of the range → +1 rep

## `progression/powerlifting.py`: top set + back-offs (§8.2)
- [ ] Top set = heaviest working set (ties go to the earlier set)
- [ ] No RPE, or outside the table → unchanged + warning
- [ ] e1RM series; deload after `drop_sessions` drops in a row
- [ ] Top set from e1RM × `rpe_percent(target)`; back-offs at −`backoff_drop_pct`
- [ ] Tests: the worked example (315 × 3 @ 8 → 315 / 285), deload at exactly N,
      missing RPE

## `planner.py`: build and apply the plan (§9)
- [ ] `make_plan()`: settings per exercise → rule by mode → `recent_sessions` →
      `rule.next`
- [ ] `apply_plan()`: keep warm-up sets and `raw`; replace only working sets; keep
      the set count
- [ ] Tests: mixed-mode routine, warm-ups kept, an exercise with a warning stays
      unchanged

## `report.py`: output table (§2.3)
- [ ] Columns: Exercise / Mode / Before / After / Why; powerlifting shows the top set
      and back-offs separately
- [ ] Header shows `DRY RUN: nothing sent` or `APPLIED`
- [ ] Warnings listed after the table
- [ ] Tests: golden files in `tests/golden/`

## `cli.py`: entry point (§2)
- [x] `plan --routine NAME [--config PATH] [--apply]`, `--version`
- [x] Exit-code constants
- [x] Tests: version, defaults, `--routine` required
- [ ] Read `HEVY_API_KEY` from the environment; if missing → exit 2
- [ ] Wire config → client → planner → report
- [ ] Routine not found or not in the config → exit 3
- [ ] Map `ConfigError` → 1 and `HevyAPIError` → 2, as one stderr line with no
      traceback
- [ ] `--apply`: exactly one `put_routine`; print `APPLIED` only after it succeeds
- [ ] Tests: end to end on fixtures for both modes; dry run sends no PUT

---

## Write-up and submission
- [x] PROPOSAL.md (Nov 5)
- [x] SPEC.md
- [x] CHECKPOINT.md written
- [ ] **Commit and push CHECKPOINT.md, the SPEC.md URL fix, AI_Log.md, CLAUDE.md and
      this file**
- [ ] README.md: install, API key setup, an example config, one example per mode,
      and the source of the RPE chart
- [ ] AI_Log.md: fill in the **TODO (me)** entries; keep it up to date
- [ ] REPORT.md (2–3 pages): what's done and what's left, two design decisions, the AI
      log plus one AI mistake, what I did
- [ ] Demo dry run against my real account; be ready to explain every line
- [ ] Final check: `uv run pytest` and `uv run ty check` clean on a fresh clone

### Deadlines
| By | Milestone |
|----|-----------|
| ~~Nov 23~~ | fixtures, client, history, config (**overdue**) |
| Nov 26 | rpe, bodybuilding, powerlifting |
| Dec 3 | planner, report, cli, golden tests, README |
| Dec 10, 1:30 pm | repository + REPORT.md; demo in class |
