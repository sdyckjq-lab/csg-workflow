# Handoff State

Use this file when creating or updating the project recovery files.

## File Roles

| File | Role | Update When | Keep Out |
|---|---|---|---|
| `docs/workflow/state.md` | Current state and next action | At start repair, stage change, stage completion, verification result | Full history, long explanations, full Skill tables |
| `docs/workflow/decisions.md` | Long-term decisions | A durable decision should not be reopened by default | Temporary progress |
| `docs/workflow/log.md` | Stage history | A stage starts, ends, verifies, fails, or captures learning | Current-next-action-only content |

## `state.md` Required Shape

Keep the file short: target 40 lines or fewer, hard limit 60 lines. It should answer:

- What stage are we in?
- What is the project goal?
- Which documents matter right now?
- What is the next action?
- What was the last completed task?
- Are we in the middle of a confirmed Skill or task?
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
- Before invoking or routing into a confirmed next Skill: update `state.md` with an in-progress checkpoint.
- Before any long-running task: update `state.md` with an in-progress checkpoint.
- At stage completion: clear or replace the in-progress checkpoint, update `state.md`, and append `log.md`.
- At durable decision: append `decisions.md`.
- At verification: record the exact check in `state.md` and the stage event in `log.md`.
- At learning capture: recommend `ce-compound`, then record the learning pointer.
- After compact, clear, or a new session: route only. Read project rules first, then `state.md`, run the state-health preflight, identify the current stage, name the exact default next Skill, and stop with a confirmation question. If `state.md` has an in-progress checkpoint, compare it with `docs/workflow/log.md` and recent verification before trusting it. Resume the checkpoint only when it is not already recorded as complete; otherwise clear or replace it before routing. Do not describe the next step only as a generic task or stage. Do not design, plan, research, implement, or call/read another Skill until the user confirms.

## State Health Preflight

Run this before trusting `state.md` after compact, clear, a new session, or an explicit `csg-workflow` invocation.

Check only high-signal evidence:

- current stage and next action exist
- next action names one exact Skill when a Skill is applicable
- active checkpoint is idle, or points to a concrete Skill/task and resume action
- active checkpoint is not already recorded as complete in `docs/workflow/log.md`
- current documents listed by state exist when they are repo files
- recent verification claims do not contradict known validation notes or pressure scenarios
- state is short enough to scan, target 40 lines or fewer and hard limit 60 lines

If there is an obvious mismatch, summarize it, repair `state.md`, then route. If evidence is ambiguous, ask which source of truth to use and do not rewrite state silently.

## Completed Task Snapshot

When a task or stage completes, collapse `state.md` to a short idle or next-action snapshot:

- current stage: idle or next stage
- last completed task: one sentence
- result: one sentence
- recent verification: exact command or check
- next action: waiting for a new request or one exact recommended Skill
- in-progress checkpoint: idle

Detailed history belongs in `log.md`; durable decisions belong in `decisions.md`.

## In-Progress Checkpoint

Use this checkpoint to survive compact during the middle of work, before a stage has completed.

Keep it short:

- status: idle, in progress, blocked, or complete
- active Skill or task
- user-confirmed route
- resume action
- last meaningful verification, if any

When a stage completes, replace this section with idle or clear the active Skill/task. Do not leave a completed task marked as in progress.

## Staleness Signals

Treat state as stale when:

- It names a next action that contradicts the latest completed plan or review.
- It has no current stage.
- It has no next action.
- It contains long historical notes better suited to `log.md`.
- It ignores a known blocking question.

When stale, follow the preflight rule: repair obvious stale state before routing, and ask first when evidence is ambiguous.
