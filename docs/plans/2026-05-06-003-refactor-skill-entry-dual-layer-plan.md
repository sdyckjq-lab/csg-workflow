---
title: "refactor: csg-workflow SKILL.md dual-layer entry"
type: refactor
status: completed
date: 2026-05-06
origin: docs/brainstorms/2026-05-06-skill-entry-redesign.md
deepened: 2026-05-06
---

# refactor: csg-workflow SKILL.md dual-layer entry

## Overview

Restructure SKILL.md into a two-layer entry: a mandatory routing intercept (Layer 1) that blocks all other actions until complete, followed by the current guidance content (Layer 2). Prevents the model from skipping routing when users append requirements in command-args.

## Problem Frame

Session `ae1927e2` (2026-05-06): user invoked `/csg-workflow [design question]`, model skipped routing and directly answered the design question. Root cause: "Start Here" is a numbered list without enough constraint to override the model's tendency to prioritize specific, actionable requests over abstract workflow steps.

## Requirements Trace

- R1. Model must complete routing (read state → determine stage → recommend Skill → wait for confirmation) before doing anything else (origin: Goal)
- R2. Model must not treat command-args as a direct task (origin: Approach Layer 1)
- R3. Routing without command-args must still work (origin: Success Criteria 2)
- R4. Validation and tests must pass (origin: Success Criteria 3-4)

## Scope Boundaries

- Modify `skills/csg-workflow/SKILL.md` as the behavior change.
- Modify `tests/pressure-scenarios/csg-workflow-v1.md` to add the command-args regression scenario that caused this work.
- Modify `tests/test_csg_workflow_package.py` to add structural checks for the intercept and pressure scenario coverage.
- Do not modify references, assets, scripts, or other files unless implementation discovers an existing validation rule must be strengthened to enforce the new entry contract.
- SKILL.md may reference existing files like `check_dependencies.py` or `dependency-setup.md` — the scope boundary means "don't modify those files", not "don't reference them".

## Context & Research

### Relevant Code and Patterns

- `skills/csg-workflow/SKILL.md` — target file, current "Start Here" section has 9 ordered steps:
  1. Read project rules
  2. Read `docs/workflow/state.md`
  3. Repair handoff if state is missing or stale
  4. Run dependency check when the dependency section is missing or unrecorded
  5. Determine the current stage
  6. Recommend one next Skill, optional alternatives, and Skills to avoid
  7. Explain the recommendation in simple language
  8. Ask the user before invoking or routing into the next Skill — **this is the validation-required string**
  9. Update state, decisions, and log at stage end
- `tests/pressure-scenarios/csg-workflow-v1.md` — currently contains AE1-AE10, but lacks a scenario for `/csg-workflow` invoked with appended command-args. This is the actual regression from session `ae1927e2`.
- `skills/csg-workflow/scripts/validate_package.py` — checks 4 required strings in SKILL.md (lines 111-121):
  - "CSG means Compound, Superpowers, and Gstack"
  - "V1 does not"
  - "Ask the user before invoking or routing into the next Skill"
  - "Never rewrite a whole `AGENTS.md` or `CLAUDE.md`"
- Installed `dbs` Skill — proven routing Skill with effective "你只做路由" constraint pattern. Treat it as an external pattern reference, not a target file.

### Key Design Reference

The `dbs` Skill uses a bold constraint at the top: "**你不做诊断，不做分析，不给建议。你只做路由。**" This pattern works because it's short, imperative, and placed before any other content.

## Key Technical Decisions

- **Intercept placement**: immediately after frontmatter and title, before all other sections. This ensures the model reads the constraint before any guidance content.
- **Description may be strengthened**: preserve `name: csg-workflow`, but allow the frontmatter description to mention that even appended command-args are routing input, not a direct task. This gives the model the same boundary before and after the full Skill body is loaded.
- **Prohibition list format**: explicit "DO NOT" bullet list, modeled after `dbs`. Shorter and more scannable than prose.
- **Preserve validation strings**: all 4 required strings will remain in the restructured file. "Ask the user before invoking or routing into the next Skill" (current step 8) becomes the last line of the routing steps in the intercept layer, phrased as: "5. Ask the user before invoking or routing into the next Skill."
- **Remove "Start Here" heading**: the intercept layer replaces it entirely. Current step 9 (update state at stage end) becomes a "路由完成后" section in Layer 2.
- **Dependency check is conditional**: the intercept layer's dependency check step preserves the current conditional phrasing: only run `scripts/check_dependencies.py` when `state.md` lacks `## 依赖状态` or `最后检查` is `Not recorded yet`. This ensures the check is non-blocking when already completed.
- **Regression scenario is part of the plan**: add an AE11 pressure scenario for `/csg-workflow <design question>` so future reviewers can see the exact behavior this refactor protects.

## Step Migration Map

| Old Start Here | New Location | Notes |
|---|---|---|
| 1. Read project rules | Intercept step 1 | Unchanged |
| 2. Read state.md | Intercept step 2 | Unchanged |
| 3. Repair if stale | Intercept step 2 (merged) | Combined with "read state.md" — if missing/stale, repair first |
| 4. Dependency check (conditional) | Intercept step 3 | Preserves current `## 依赖状态` / `最后检查` condition |
| 5. Determine stage | Intercept step 4 | Unchanged |
| 6. Recommend Skill | Intercept step 4 (merged) | Combined with "determine stage" — recommend based on stage |
| 7. Explain recommendation | Intercept step 4 (merged) | Keep the simple-language expectation inside the recommendation output |
| 8. Ask the user before invoking | Intercept step 5 | Validation-required string preserved here |
| 9. Update state at stage end | Layer 2 "路由完成后" | Post-routing guidance |

Intercept layer has 5 steps (not 7) because some original steps are merged. The "5 steps" in the Approach correspond to: (1) read rules, (2) read/repair state, (3) dependency check, (4) determine stage & recommend Skill, (5) ask user before invoking.

## Implementation Units

- U1. **Restructure SKILL.md with dual-layer entry**

**Goal:** Replace "Start Here" section with a mandatory routing intercept, reorganize remaining content as post-routing guidance.

**Requirements:** R1, R2, R3, R4

**Dependencies:** None

**Files:**
- Modify: `skills/csg-workflow/SKILL.md`
- Modify: `tests/pressure-scenarios/csg-workflow-v1.md`
- Test: `tests/test_csg_workflow_package.py` (add structural and pressure-scenario coverage checks + run existing tests)

**Approach:**
1. Keep `name: csg-workflow` and the title line unchanged; optionally strengthen the frontmatter description with the routing-only command-args boundary
2. Insert intercept layer immediately after title, before V1 Boundary
3. Intercept layer structure:
   - Section heading: `## 强制路由`
   - One-line constraint: "你是项目路由器。**你只做路由。**"
   - Mandatory routing steps (numbered list, 5 steps):
     1. Read project rules when present (`AGENTS.md` for Codex, `CLAUDE.md` for Claude Code)
     2. Read `docs/workflow/state.md` when it exists. If state is missing or stale, repair the handoff first using `assets/templates/workflow/`
     3. If state.md has no `## 依赖状态` section, or if `最后检查` is `Not recorded yet`, run `scripts/check_dependencies.py` and follow `references/dependency-setup.md`
     4. Determine the current stage (if unclear, read `references/stage-router.md`). Recommend one next Skill, optional alternatives, and Skills to avoid right now. Explain the recommendation in simple language.
     5. Ask the user before invoking or routing into the next Skill
   - Prohibition list: "在完成以上步骤之前，**不得**：将 command-args 当作直接任务来回应；启动调研、设计、实现；调用 Agent 或其他工具"
4. Remove "Start Here" heading and old steps 1-9
5. Keep V1 Boundary, CSG Role Split, References, Safety Rules in order
6. Add "路由完成后" section after intercept (before or after CSG Role Split), containing: "路由确认后，根据推荐的 Skill 执行下一步。阶段结束时，更新 `state.md`；长期决定写入 `decisions.md`；历史记录追加到 `log.md`。"
7. Preserve all 4 validation-required strings (verify after edit)
8. Add pressure scenario AE11:
   - Input: `/csg-workflow 我想加一个功能...如何设计？`
   - Expected: Skill reads routing state first, determines the current stage, recommends one next Skill, asks before routing, and does not directly answer the embedded design question
9. Add or update unit tests so the package tests verify:
   - `你只做路由` appears before `## V1 Boundary`
   - command-args prohibition appears before post-routing guidance
   - the validation-required ask string appears in the intercept layer
   - AE11 exists in `tests/pressure-scenarios/csg-workflow-v1.md`

**Patterns to follow:**
- Installed `dbs` Skill — top-level routing constraint pattern
- Current SKILL.md content — keep existing language and references unchanged where possible

**Test scenarios:**
- Happy path: `validate_package.py` passes after restructuring
- Happy path: existing tests in `test_csg_workflow_package.py` pass
- Edge case: all 4 required strings are present in new structure
- Edge case: no forbidden unfinished markers or local-only paths introduced
- Regression: AE11 records the exact `/csg-workflow <design question>` command-args failure mode
- Structural: intercept layer appears before the first `## ` heading after the title — verify by checking that "你只做路由" appears before any `## V1 Boundary` or `## CSG` text
- Structural: "Ask the user before invoking or routing into the next Skill" appears in the intercept layer (before the first `## ` heading after title)
- Structural: the command-args prohibition appears in the intercept layer, not only in later prose

**Verification:**
- `python3 skills/csg-workflow/scripts/validate_package.py` passes
- `python3 -m unittest tests/test_csg_workflow_package.py` passes
- `tests/pressure-scenarios/csg-workflow-v1.md` includes AE11 for appended command-args
- Visual review: intercept layer is the first content section after title, before any other guidance

## Risks & Dependencies

| Risk | Mitigation |
|------|------------|
| Model still ignores intercept | Keep intercept under 15 lines, use strong imperative language, place before all other content |
| Validation fails on required strings | Explicitly preserve all 4 strings during restructuring; run validation immediately after edit |

## Sources & References

- **Origin document:** [docs/brainstorms/2026-05-06-skill-entry-redesign.md](docs/brainstorms/2026-05-06-skill-entry-redesign.md)
- Evidence session: `ae1927e2` (2026-05-06)
- Pattern reference: installed `dbs` Skill entry constraint
