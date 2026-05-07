# Stage Router

Use this file when the user invokes `csg-workflow` and the current project stage is unclear, missing, or ready to advance.

## Routing Rule

Do not start by picking a tool. Start by deciding the stage:

1. Read `AGENTS.md` or `CLAUDE.md` when present.
2. Read `docs/workflow/state.md` when present.
3. Run the state-health preflight in `references/handoff-state.md` before trusting recorded state.
4. Compare the user's current request with the stage table below.
5. Recommend exactly one next Skill as the default.
6. Explain why that Skill fits the current stage.
7. Ask before invoking or routing to that Skill.
8. Update handoff files when the stage changes.

If `state.md` is missing in an existing project, repair state before advancing. If `state.md` exists but does not say a current stage or next action, treat it as incomplete.

## Route Depth

### Beginner Small Project

Use this route when the user is building a personal script, small demo, learning project, or a one-person tool with low release risk.

Keep only:

- Idea or requirements
- Plan
- Work
- Verification
- Review
- State update
- Learning capture when useful

Do not default to release review, canary, deployment, or heavy plan review.

### Complex Project

Use this route when the work is public, open-source, user-facing, cross-file, release-sensitive, or likely to be reused.

Keep the full route:

idea -> requirements -> plan -> plan review -> work -> code review -> QA -> PR or delivery -> post-release check -> learning

## Stage Table

| Stage | Signals | Default Skill | Optional Skills | Avoid Now | Pass Criteria | If Not Passed |
|---|---|---|---|---|---|---|
| Entry judgment | User says they want to start or continue but stage is unclear | `csg-workflow` | `ce-sessions` for recovery context | coding Skills | Current stage and next action are known | Repair state or ask one stage question |
| Idea exploration | User has a vague idea, audience or outcome unclear | `ce-ideate` | `ce-brainstorm` | coding, QA, ship | A concrete direction exists | Stay in idea exploration |
| Requirements | User has a direction but no accepted scope | `ce-brainstorm` | office-hours for product challenge | coding, release | Requirements doc has actors, flows, requirements, success criteria, boundaries | Continue requirements |
| Plan | Requirements are ready and no planning blockers remain | `ce-plan` | plan reviews after plan exists | coding | Plan file exists with implementation units and tests | Return to requirements or planning |
| Plan review | Plan exists and carries scope or product risk | `plan-ceo-review` or `ce-doc-review` | plan-eng-review, plan-design-review | coding | Required changes are applied or consciously deferred | Revise plan |
| Work | Plan is ready and user asks to implement | `ce-work` | Superpowers TDD/debugging skills as needed | ship | Files are changed, tests pass, verification is recorded | Continue work or debug |
| Code review | Work is complete enough to inspect | `ce-code-review` | `gstack review` near landing | ship without review | Findings are resolved or accepted | Fix or document accepted risk |
| QA | User-facing or workflow behavior needs real use checks | `qa` or `ce-test-browser` when UI exists | `qa-only` for report-only | release without QA | Representative flows pass | Fix and rerun QA |
| PR or delivery | Review and QA are done | `ce-commit-push-pr` or `github:yeet` | ship flow when repo is configured | rewriting product scope | Changes are packaged for review or delivery | Return to review or QA |
| Post-release check | Work has landed or been released | `canary` when configured | manual smoke check | new feature work | Release health is checked | Fix, rollback, or monitor |
| Learning capture | Stage ended or a useful mistake was found | `ce-compound` | retro for team/project review | skipping state update | Learning is captured or explicitly not needed | Add note to log/state |

## Stage Advancement Gates

- Requirements cannot advance to plan while product blockers remain.
- Plan cannot advance to work if implementation units or verification expectations are missing.
- Work cannot advance to delivery without real verification for behavior-bearing changes.
- QA and ship stages are recommendations in V1, not automatic execution.
- Learning capture should be recommended after stage completion or a meaningful error.

## Common Inputs

### Vague Idea

Input: "I want to build an AI coding workflow but not sure where to start."

Route: idea exploration or requirements. Recommend `ce-ideate` if the product direction is unclear. Recommend `ce-brainstorm` if the direction is clear but scope is not.

### No Verification

Input: "The code is done."

Route: work verification. Ask what was actually run or inspected. Do not move to delivery until verification exists.

### Small Script

Input: "This is just a personal cleanup script."

Route: beginner small project. Keep requirements and plan light, but still keep state and verification.

### Resuming After Clear

Input: "Continue this project."

Route: context recovery. Read project rules and `docs/workflow/state.md` first, then run the state-health preflight from `references/handoff-state.md`. If state is stale, repair obvious mismatches or ask when evidence is ambiguous. If a checkpoint is active, check `docs/workflow/log.md` before resuming it. Name one exact next Skill and stop with a confirmation question.
