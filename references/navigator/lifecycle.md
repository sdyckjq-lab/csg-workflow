# Lifecycle Stages and Routing Matrix

This document defines the beginner-facing project lifecycle and the minimum routing matrix for Skill GPS.

## Lifecycle Enum

Gate 1 uses this exact project-stage enum:

- `bootstrap`
- `idea`
- `requirements`
- `plan`
- `work`
- `review`
- `qa`
- `delivery`
- `learning`

`recovery` is **not** a project stage. It is a cross-cutting recovery mode/card type. Recovery cards use `status: recovery_needed`, identify the stage being repaired, and route back to that preserved stage or the earliest trustworthy stage after repair.

## Simplification Constraint

Every lifecycle rule must reduce what the beginner has to understand or choose. If a detail only makes the internal system more complete but does not make the next user-visible step calmer, safer, or clearer, defer it.

## Routing Matrix

Every stage needs one default route, one canonical card example, one expected output, one not-now list, and one missing-skill fallback.

| Stage | Trigger signals | Stable role alias | Default concrete Skill | Confidence rule | Expected output | Not now | Missing-skill fallback |
|---|---|---|---|---|---|---|---|
| `bootstrap` | no `docs/workflow/state.md`, first run, dependency status unknown | `setup-state` | `csg-workflow` | high when state is absent | initialized state/log/decisions and dependency report | coding, ship | create files from templates and show manual dependency commands |
| `idea` | vague idea, audience or scope unclear | `requirements-discovery` | `ce-brainstorm` | high when no accepted requirements exist | requirements, actors, flows, success criteria, non-goals | `ce-work`, ship | use manual brainstorm prompts from `references/missing-skills.md` |
| `requirements` | direction exists, requirements not accepted | `plan-prep` | `ce-plan` | high when requirements doc exists and blockers are answered | implementation plan with units and tests | direct build, ship | ask manual planning questions and write a plan outline |
| `plan` | plan exists, user wants implementation | `implementation` | `ce-work` | high when plan has implementation units and verification expectations | changed files and verification notes | ship, canary | provide manual implementation checklist |
| `work` | implementation is underway or just completed | `code-review` | `ce-code-review` | high when files changed and tests or checks are available | review findings or explicit no-finding result | ship before review | manual review checklist using changed files |
| `review` | review complete or fixes requested | `qa` | `qa-only` | medium unless user-facing behavior exists, high for UI/workflow changes | QA report or smoke-test result | deploy without smoke check | manual smoke checklist; use `qa` as optional full QA when available |
| `qa` | QA passed and user wants delivery | `delivery` | `ce-commit-push-pr` | high when verification is recorded and no blockers remain | commit/PR/delivery package | new scope, ideation | manual commit and PR checklist |
| `delivery` | work landed or released | `post-release-check` | `canary` | medium unless deployment exists, high when release is live | post-release health result | new feature work | manual smoke or monitoring checklist |
| `learning` | stage ended with reusable lesson | `learning-capture` | `ce-compound` | medium, high after a repeated mistake or durable decision | learning note or decision pointer | ignoring state update | append concise log/decision entry manually |

## Tie-Break Rule

When multiple stages look plausible, choose the **earliest unmet stage** in the lifecycle.

Example: if the user asks to code but has no accepted requirements, recommend `requirements-discovery`, not `implementation`.

## Stage Notation

All stage values in cards, state files, and validators must use the exact lowercase strings from the enum above. No synonyms, no title case, no hyphens.

## Recovery Mode

Recovery is a cross-cutting mode that can occur at any stage. It preserves the underlying `current_stage` and does not create a new lifecycle position.

Recovery-mode canonical examples are capped to these scenarios:

1. **Post-compact active-card recovery**: `state.md` has an active card but the session context is lost. Resume or clear the card.
2. **Old-state migration**: `state.md` uses the pre-navigator field layout. Detect and propose migration or fresh diagnosis.
3. **Repeat confirmation**: User confirms the same active card again. Re-show or resume without duplicate log or stage advance.
4. **Conflicting evidence**: `state.md` and `log.md` disagree. Ask the user which source of truth to use.

Other degraded-state classes are deferred to Gate 2.
