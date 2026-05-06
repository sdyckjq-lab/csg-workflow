# Handoff State

Use this file when creating or updating the project recovery files.

## File Roles

| File | Role | Update When | Keep Out |
|---|---|---|---|
| `docs/workflow/state.md` | Current state and next action | At start repair, stage change, stage completion, verification result | Full history, long explanations, full Skill tables |
| `docs/workflow/decisions.md` | Long-term decisions | A durable decision should not be reopened by default | Temporary progress |
| `docs/workflow/log.md` | Stage history | A stage starts, ends, verifies, fails, or captures learning | Current-next-action-only content |

## `state.md` Required Shape

Keep the file short. It should answer:

- What stage are we in?
- What is the project goal?
- Which documents matter right now?
- What is the next action?
- What is blocked?
- What was recently verified?
- What should not be reopened unless new facts appear?

If `state.md` does not answer current stage or next action, repair it before advancing.

## `decisions.md` Required Shape

Record durable decisions as:

- Date
- Decision
- Reason
- Source document or conversation

Use this for decisions like "V1 is a Skill, not a plugin" or "existing project rules win over CSG rules".

## `log.md` Required Shape

Append stage events as:

- Date
- Stage
- Result
- Verification
- Next action

Use this to preserve history without making `state.md` long.

## Update Rules

- At project start: create all three files if absent, using `assets/templates/workflow/`.
- At stage completion: update `state.md` and append `log.md`.
- At durable decision: append `decisions.md`.
- At verification: record the exact check in `state.md` and the stage event in `log.md`.
- At learning capture: recommend `ce-compound`, then record the learning pointer.
- At new session: read project rules first, then `state.md`, then continue from the next action.

## Staleness Signals

Treat state as stale when:

- It names a next action that contradicts the latest completed plan or review.
- It has no current stage.
- It has no next action.
- It contains long historical notes better suited to `log.md`.
- It ignores a known blocking question.

When stale, summarize what is wrong, repair the state file, and only then continue routing.
