# AI log

A short record of how I used AI tools on this project: what the tool did, what I
checked, and what I changed or rejected. The REPORT.md AI section is built from this
log.

**Tool:** Claude Code (Claude desktop app, Code tab), model Claude Opus 5.5, unless an
entry says otherwise.

Entries marked **TODO (me)** still need my own note on what I checked by hand.

## Places where the AI was wrong (candidates for the report)

- **Nov 19: inconsistent spec.** The AI wrote `make_plan(..., config: Config)` in
  SPEC.md, then gave it a `RoutineConfig` when writing the skeleton. The spec and the
  code disagreed until the spec was changed to match. Found by comparing the code with
  SPEC.md §9.
- **Nov 19: RPE table from memory.** The AI wrote the RTS RPE percentages into SPEC
  §8.2 from memory, without a source. It flagged them as unverified itself. **TODO
  (me):** check against the published chart and record any value that was wrong.
- **Nov 19: Hevy API schema from memory.** The endpoint names, field names (such as
  `weight_kg` and `page_count`) and the PUT body format were written without reading the
  docs. **TODO (me):** check against https://api.hevyapp.com/docs and a recorded
  response.

## Log

### Nov 5: choosing the project
- **Used for:** brainstorming Track 2 ideas built around Hevy.
- **AI suggested:** three ideas. It recommended an analytics CLI (#1), with a typed API
  client (#2) under it.
- **Rejected:** the recommendation. I chose #3 (a progression planner), because it's
  the one I would actually use.

### Nov 5: proposal
- **Used for:** drafting PROPOSAL.md.
- **Changed:**
  - I asked for two training modes (bodybuilding and powerlifting), each with its own
    rules, in place of the generic linear rule.
  - I asked for every weight to be in pounds.
  - I filled in my name and the date of the solo-permission email.
- **Learned:** I asked why the community Hevy MCP (TypeScript) can't meet the
  `pyproject.toml` requirement. Answer: TypeScript packages use `package.json` and
  npm, not uv or pip. So the project is a separate Python package that calls the
  Hevy REST API directly.

### Nov 19: module diagram
- **Used for:** a draw.io diagram of the planned modules (`resources/modules.drawio`).
- **Checked:** the AI checked that the XML parses. It did not check the layout.
- **Changed:** I rearranged the layout by hand in draw.io.

### Nov 19: SPEC.md
- **Used for:** writing the full spec from the proposal and the diagram.
- **Checked:**
  - **TODO (me):** read through the rules in §8, and the worked example (315 × 3 @ 8 →
    315 lb top set, 285 lb back-offs).
  - Still open: the RPE values and the API schema (see the section above).

### Nov 19: package skeleton
- **Used for:** pyproject.toml, typed stubs for every module, `units.py`, `models.py`,
  and the first 18 tests.
- **Checked:**
  - Commands run: `uv sync`, `uv run pytest` (18 passed), `uv run ty check` (clean),
    `uv build`, and a listing of the wheel's contents.
  - **TODO (me):** read `units.py` and `models.py` line by line, so I can explain
    them at the demo.
- **Design choice, kept:** the AI moved the settings types from `config.py` to
  `models.py`, so the pure core never imports the I/O layer.
- **Rejected:** the AI tried to commit, but Git had no author set. I committed it
  myself instead of letting the AI set a Git identity.

### Nov 19: checkpoint write-up
- **Used for:** CHECKPOINT.md and the checkpoint email text.
- **Checked:** **TODO (me):** what I edited before sending.

### Nov 24: AI log and project overview
- **Used for:** creating AI_Log.md (backfilled from Nov 5–19), a CLAUDE.md that tells
  Claude to keep the log up to date, and project_overview.md (a checklist for each
  module).
- **Checked:** "done" in the overview was based on commands that were run: `grep`
  for `NotImplementedError` (11 stubs left) and `uv run pytest` (18 passed).
- **Changed / rejected:** **TODO (me)**

<!-- New entries go above this line, newest last. Keep each one short:
### <date>: <task>
- **Used for:** ...
- **Checked:** ... (commands run, lines read, values compared against a source)
- **Changed / rejected:** ...
-->
