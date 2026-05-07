# Skill Selection

Use this file when multiple Skills appear to fit the current stage.

## Default Roles

| Source | Role | Use For | Do Not Use For |
|---|---|---|---|
| Compound | Main project route | idea, requirements, planning, work, code review, learning | replacing local project rules |
| Superpowers | Work discipline | test-first habits, debugging discipline, finishing checks | product routing by itself |
| Gstack | Delivery support | product challenge, plan review, QA, ship, canary, recovery, retrospective | replacing Compound mainline |

## Category Choices

| Category | Default | Optional | Complex Project Only | Discouraged Right Now |
|---|---|---|---|---|
| Idea | `ce-ideate` | office-hours for founder-style challenge | product-lens review after docs exist | `ce-work` |
| Requirements | `ce-brainstorm` | `pm-spec` for polished product spec | plan-ceo-review after requirements exist | coding Skills |
| Plan | `ce-plan` | plan-eng-review after plan exists | plan-design-review for UI, plan-ceo-review for product bets | direct build |
| Work | `ce-work` | Superpowers TDD/debugging skills when needed | `ce-work-beta` only when external delegation is intentional | ship |
| Code review | `ce-code-review` | Superpowers requesting-code-review | `gstack review` before landing | QA without fixes |
| QA | `qa` or `qa-only` | `ce-test-browser` for web flows | canary after release | release without smoke checks |
| PR or delivery | `ce-commit-push-pr` | GitHub Skills | ship flow when configured | more ideation |
| Recovery | `csg-workflow` with `state.md` | `ce-sessions` for historical context | context-save/context-restore where installed | restarting from zero |
| Learning | `ce-compound` | retro for broader project review | document-release after shipped work | moving on without state update |

## Review Choice Rule

When the user asks which review tool to use:

1. Use `ce-code-review` for normal code review after implementation.
2. Use Gstack review near merge, release, or high-risk delivery.
3. Use Superpowers review Skills to enforce the habit of completing review before claiming done.

Explain this in plain language:

"Use `ce-code-review` first because the code has to be checked before delivery. Use Gstack review later when you are close to merging or shipping. Superpowers helps keep the review habit strict, but it is not the main review route here."

## Recommendation Format

When recommending a Skill, answer in this shape:

- Current stage: name the stage.
- Default next Skill: one Skill.
- Why: one or two short sentences.
- Optional: one or two alternatives only when they matter.
- Not now: name Skills that would be premature.
- Confirmation: ask before routing to the next Skill.

## Avoid Over-Routing

Do not list every possible Skill. New users need the next step, not a catalog.

Do not chain multiple Skills automatically. V1 recommends and waits.
