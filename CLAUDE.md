# hevy-coach

EC602 final project (Track 2). SPEC.md is the source of truth. If the code and the spec
disagree, say so instead of silently changing either one.

## AI log

AI_Log.md is graded. At the end of every task that writes code or docs, add a short
entry above the comment template at the bottom:

- **Used for:** what was asked
- **Checked:** only what was actually verified (commands run and their results). Do not
  claim the user checked anything. Leave a **TODO (me)** for the user's own checks.
- **Changed / rejected:** anything the user changed, overrode or turned down

When the AI gets something wrong (a wrong value, a spec mismatch, a failing assumption),
also add it to "Places where the AI was wrong", with how it was found.

## Commands (run in WSL, from the repository root)

- `uv sync`: install
- `uv run pytest`: tests, all offline
- `uv run ty check`: type check, must stay clean
