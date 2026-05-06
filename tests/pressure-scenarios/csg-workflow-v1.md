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
