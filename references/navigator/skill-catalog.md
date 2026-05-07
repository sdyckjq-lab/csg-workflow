# Skill Catalog and Availability Discovery

This document defines the stable Skill alias layer and concrete Skill mappings for each lifecycle stage.

## Stable Alias Layer

Gate 1 uses stable role aliases in card logic, then maps aliases to concrete Skills. This prevents external Skill name changes from breaking the product language.

| Stable alias | Primary concrete Skill | Source family | Fallback when missing or renamed |
|---|---|---|---|
| `setup-state` | `csg-workflow` | `csg` | manual state initialization from templates |
| `resume-or-clear` | `csg-workflow` | `csg` | manual state/log reconciliation fallback |
| `requirements-discovery` | `ce-brainstorm` | `compound` | manual brainstorm prompts from `references/missing-skills.md` |
| `plan-prep` | `ce-plan` | `compound` | manual plan outline card |
| `implementation` | `ce-work` | `compound` | manual implementation checklist |
| `code-review` | `ce-code-review` | `compound` | manual changed-file review checklist |
| `qa` | `qa-only` | `gstack` | manual smoke checklist; use `qa` as optional full QA when available |
| `delivery` | `ce-commit-push-pr` | `compound` | manual commit/PR checklist |
| `post-release-check` | `canary` | `gstack` | manual post-release smoke checklist |
| `learning-capture` | `ce-compound` | `compound` | manual log/decision capture |
| `work-discipline` | Superpowers TDD/debugging/review Skills | `superpowers` | manual discipline checklist |

Cards should show both alias and concrete Skill when useful:

```text
Recommended role: requirements-discovery
Default Skill: ce-brainstorm
```

If a concrete Skill is unavailable, the card keeps the alias and switches to fallback instructions.

## Resolution Order

When resolving a stable alias to an actionable Skill recommendation:

1. **Stable alias** from this catalog.
2. **Static primary concrete Skill** from the same row.
3. **Local availability result** for that concrete Skill (read-only discovery).
4. **Dependency family status** from `scripts/check_dependencies.py`.
5. **Optional concrete Skill** only when the catalog marks it optional and the family is present and verified.
6. **Manual fallback** from `references/missing-skills.md` when the family is missing, renamed, or unverified.

## Source Families

Gate 1 recognizes these source families:

- `compound` — main project route (idea through delivery)
- `superpowers` — work discipline (TDD, debugging, review)
- `gstack` — delivery support (plan review, QA, ship, canary, context recovery)
- `csg` — internal csg-workflow operations (setup, recovery)
- `manual` — fallback when no Skill is available

## Availability Discovery Boundaries

### Allowed

- Read local Skill entry-point names from known Claude/Codex Skill locations.
- Record whether the catalog's concrete Skill names are visible in installed Skill entry points.
- Check dependency family status through existing `scripts/check_dependencies.py` output.
- Mark a catalog Skill as `available`, `missing`, `renamed`, or `unverified`.

### Not Allowed

- Install dependencies or external Skills.
- Modify external Skill directories.
- Read external Skill implementation internals.
- Infer new lifecycle routes from external metadata.
- Auto-run discovered Skills.
- Replace the stable alias catalog with generated metadata.

## Not-Now Skills per Stage

These Skills should not be recommended when the project is in the given stage:

| Stage | Not now |
|---|---|
| `bootstrap` | coding, ship |
| `idea` | `ce-work`, `ship` |
| `requirements` | direct build, `ship` |
| `plan` | `ship`, `canary` |
| `work` | `ship` before review |
| `review` | deploy without smoke check |
| `qa` | new scope, ideation |
| `delivery` | new scope, ideation |
| `learning` | ignoring state update |
