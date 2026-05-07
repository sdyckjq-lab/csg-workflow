# Missing Skills

Use this file when a recommended Compound, Superpowers, or Gstack Skill is not available in the current environment.

## Hard Rules

- Do not auto-install external plugins or Skills.
- Do not pretend a missing Skill ran.
- Do not stop the whole workflow if a manual fallback can continue the stage.
- Tell the user what is missing, why it matters, and how to continue manually.
- Keep the recorded next action honest in `docs/workflow/state.md`.

## Fallback Table

| Missing Capability | What To Say | Manual Fallback |
|---|---|---|
| `ce-ideate` | "Idea exploration Skill is unavailable." | Ask the user for audience, problem, alternatives, and success signal, then write a short direction note. |
| `ce-brainstorm` | "Requirements Skill is unavailable." | Create a requirements doc with problem, actors, flows, requirements, success criteria, boundaries, decisions, and questions. |
| `ce-plan` | "Planning Skill is unavailable." | Write a plan with scope, file list, implementation units, tests, risks, and verification. |
| `ce-work` | "Work execution Skill is unavailable." | Follow the saved plan manually, one implementation unit at a time, verifying after each unit. |
| `ce-code-review` | "Code review Skill is unavailable." | Review the diff for bugs, regressions, missing tests, unsafe file edits, and scope drift. |
| Gstack QA | "Gstack QA is unavailable." | Run manual smoke checks or project tests and record exact verification in `state.md`. |
| Gstack ship/canary | "Gstack ship or canary is unavailable." | Treat ship/canary as a recommendation, not a blocker; write manual release and follow-up checks. |
| Superpowers discipline | "Superpowers is unavailable." | Keep the same habit manually: plan before work, verify tests, debug from root cause, and check completion before reporting. |

## Missing Gstack Example

If the user has Compound but not Gstack:

1. Continue with Compound for requirements, planning, work, review, and learning.
2. Mark Gstack QA, ship, and canary as install-dependent recommendations.
3. Offer manual QA or release checks.
4. Do not block requirements, plan, or work stages just because Gstack is missing.

Suggested wording:

"Gstack is not available here, so I will not route into its QA or ship Skills. We can still continue on the Compound main route. For QA, I will ask for or run manual checks and record the result."

## State Update

When a fallback is used, add a short note:

- Missing capability.
- Manual fallback chosen.
- Verification still required before stage completion.
