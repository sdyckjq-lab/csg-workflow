# CSG Workflow V1 Pressure Scenarios

These scenarios validate the Skill behavior described in `docs/brainstorms/2026-05-06-csg-workflow-requirements.md`.

## AE1: Fuzzy Idea Routing

Input: "I want to make an AI coding workflow, but I do not know where to start."

Expected:

- Current stage is idea exploration or requirements.
- Default recommendation is `ce-ideate` when direction is unclear, or `ce-brainstorm` when direction is clear but scope is not.
- The Skill explains why coding is premature.
- The Skill asks before routing.

## AE2: No Verification Stage Block

Input: "The code is done."

Expected:

- The Skill checks whether real verification exists.
- If no command, inspection, or QA result is recorded, it refuses to move to delivery.
- It asks for or runs verification and records the result in `state.md`.

## AE3: Review Skill Choice

Input: "Should I use `ce-code-review`, Gstack review, or Superpowers review?"

Expected:

- Default is `ce-code-review` for normal code review.
- Gstack review is suggested near merge, release, or high-risk delivery.
- Superpowers is described as review discipline, not the main review route.

## AE4: New Session Recovery

Input: "Continue this project" after a clear or new session.

Expected:

- The Skill reads `AGENTS.md` or `CLAUDE.md` when present.
- The Skill reads `docs/workflow/state.md`.
- It continues from the recorded next action instead of reopening settled product decisions.

## AE5: Small Script Route

Input: "This is just a small personal script."

Expected:

- The Skill chooses beginner small project route.
- It keeps requirements, plan, work, verification, review, and state update.
- It does not default to release, canary, or heavy plan review.

## AE6: Learning Capture

Input: "We finished the stage and found a mistake worth remembering."

Expected:

- The Skill recommends `ce-compound`.
- It records the learning pointer in `state.md` or `log.md`.
- It does not leave the stage without updating handoff files.

## AE7: Existing Rule File Safety

Input: Existing `AGENTS.md` and `CLAUDE.md` already contain user rules.

Expected:

- The Skill only appends or replaces the marked CSG block.
- Existing user content outside markers is preserved.
- The rule block stays short and does not include the full workflow.

## AE8: Missing Rule File Behavior

Input: No `AGENTS.md` exists in a Codex project.

Expected:

- The Skill recommends Codex `/init` first.
- It creates a minimal file only after explicit user confirmation.
- It never silently writes a long rule file.

## AE9: Missing Gstack Fallback

Input: Compound is available but Gstack is missing.

Expected:

- The Skill continues on the Compound main route.
- It marks Gstack QA, ship, and canary as install-dependent recommendations.
- It offers manual QA and delivery checks.

## AE10: README First Screen

Input: A new GitHub reader opens the repository.

Expected:

- First screen explains CSG, target user, install path, V1 boundary, dependency expectations, missing-Skill fallback, license, and minimum example.
- It is clear this Skill does not replace Compound, Superpowers, or Gstack.

## AE11: Command Args Routing Intercept

Input: `/csg-workflow 我想加一个功能...如何设计？`

Expected:

- The Skill treats the appended command-args as routing context, not as a direct design task.
- The Skill reads project rules and `docs/workflow/state.md` before answering the embedded request.
- The Skill determines the current stage and recommends one next Skill before any research, design, implementation, or Agent call.
- The Skill asks before invoking or routing into the next Skill.

## AE12: Post-Compact Routing Recovery

Input: A long session has compacted or a new session starts. The user says: "继续，顺便帮我设计下一个功能。"

Expected:

- The agent uses the persisted project rules and `docs/workflow/state.md` instead of relying on chat history.
- The agent treats the embedded feature-design request as routing context first.
- The agent identifies the current project stage from `state.md`.
- The agent names one exact next Skill and explains why that Skill fits the stage.
- The agent stops with a confirmation question before answering the embedded feature-design request or routing into another Skill.
- The first recovery response does not contain a feature design, implementation plan, research pass, or downstream Skill execution.

## AE13: In-Progress Compact Recovery

Input: The user had already confirmed routing into `ce-plan`, `state.md` says an in-progress checkpoint is active for `ce-plan`, and compact happens before the plan is saved. After compact, the user says: "继续，也帮我想想还有没有别的功能。"

Expected:

- The agent reads the in-progress checkpoint before treating the new request as fresh.
- The agent names `ce-plan` and recommends resuming that recorded work first.
- The agent does not switch back to ideation or start designing new features unless the user confirms a direction change.
- The first recovery response stops with a confirmation question.

## AE14: Stale State Recovery

Input: `state.md` says the next action is `ce-plan`, but a newer completed plan exists and `log.md` records that planning already finished. After compact, the user says: "继续，下一步做什么？"

Expected:

- The agent runs a state-health preflight before trusting the recorded next action.
- The agent detects the obvious mismatch between stale `state.md` and newer repo evidence.
- The agent repairs `state.md` before routing.
- The agent does not blindly route from the stale next action.
- The first recovery response names one exact next Skill or idle state and stops with a confirmation question.

## AE15: Completed State Recovery

Input: `state.md` in-progress checkpoint says `ce-plan`, but the plan is recorded as complete in `docs/workflow/log.md`. After compact, the user says: "继续刚才的任务。"

Expected:

- The agent checks `docs/workflow/log.md` before resuming the checkpoint when state appears stale.
- The agent sees that the recorded task is already complete.
- The agent clears or replaces the checkpoint.
- The agent does not resume already-completed work.
- The first recovery response names the current next Skill or idle state and stops with a confirmation question.
