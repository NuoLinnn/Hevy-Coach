# EC602 Final Project Checkpoint: `hevy-coach`

**Nuo Lin** (solo) · Track 2 · November 19, 2026
Repository: https://github.com/NuoLinnn/Hevy-Coach

## Checkpoint requirements

| Requirement | Status | Where |
|---|---|---|
| SPEC.md | done | [SPEC.md](SPEC.md) |
| The package installs | done: `uv sync` and `uv build` work; `hevy-coach --version` runs | [pyproject.toml](pyproject.toml) |
| The first tests run | 18 pass, 0 fail; `ty check` is clean | [tests/](tests/) |

To check it:

```bash
git clone https://github.com/NuoLinnn/Hevy-Coach && cd Hevy-Coach
uv sync
uv run pytest
uv run ty check
uv run hevy-coach plan --help
```

## What is built so far

- **Done and tested:** `units.py` (kg↔lb, plate rounding), `models.py` (every data type
  in SPEC §4), and argument parsing in `cli.py`.
- **Typed stubs** (signature and docstring, body raises `NotImplementedError`): `config`,
  `client`, `history`, `planner`, `report`, `progression/bodybuilding`,
  `progression/powerlifting`, `progression/rpe`. The module layout follows
  [resources/modules.drawio](resources/modules.drawio).

## What has changed since the proposal, and why

1. **I am behind my own timeline.** The proposal planned the API client and recorded
   fixtures by November 12, and client tests running by today. The client is still a
   stub and no fixtures are recorded yet. I spent the time writing the spec in enough
   detail that every rule maps directly to tests (the rule checks are ordered, with
   exact thresholds), because the logic is the hardest part to get right. The revised
   plan below catches up before Thanksgiving.
2. **The settings types moved from `config.py` to `models.py`.** In the planned layout,
   the progression rules (pure logic) would have had to import `config.py`, which reads
   files. With the types in `models.py`, the core never imports the I/O layer, so it can
   be tested without a config file.
3. **`make_plan` takes one routine's settings (`RoutineConfig`), not the whole
   `Config`.** The planner only ever works on one routine, so this keeps its input
   smaller and its tests simpler.
4. **Decisions made while writing the spec** that the proposal did not cover:
   - History is matched by Hevy's `exercise_template_id` across **all** workouts, not
     only those started from the routine. A bench press done on another day still
     counts, and renaming an exercise or routine doesn't lose the history.
   - `kg_to_lb` rounds to 0.1 lb. Without that, 135 lb → kg → lb gives 134.99999…
     and the output looks wrong. A test checks the round trip for every 0.5 lb step up
     to 1500 lb.
   - Plate rounding sends ties up (137.5 → 140) and does not use Python's `round()`,
     which rounds ties to the even number.
   - The RPE table covers only reps 1–8 and RPE 7–10, which covers powerlifting top
     sets. Anything outside it gives a warning and that exercise is left unchanged.
   - Unknown keys in the config file are errors, so a typo is not silently ignored.
   - The API key is read only from the `HEVY_API_KEY` environment variable, never
     from the config file, so it cannot end up in the repository.
   - The `PUT` must send back every routine field it did not change, because the API
     replaces the whole routine.

## Open questions (SPEC §12)

- The exact Hevy routine `PUT` schema, to be confirmed against the API docs and
  responses recorded from my account.
- Whether Hevy stores `weight_kg` at full precision.
- The RPE table values must be checked against the published RTS chart before
  `rpe.py` is written.
- Bodyweight exercises (no weight): currently planned as "unchanged, with a warning".

## Revised plan

| By | Milestone |
|----|-----------|
| Nov 23 | Record fixtures from my account; `client.py` + `history.py` + `config.py` with tests |
| Nov 26 | `rpe.py`, bodybuilding and powerlifting rules, with tests |
| Dec 3 | `planner.py`, `report.py`, full `cli.py`, golden-file tests, README |
| Dec 10 | REPORT.md, AI log, demo against my real account |

The "if time runs short" order is the same as in the proposal: the per-exercise mode
override goes first, then microplate rounding.
