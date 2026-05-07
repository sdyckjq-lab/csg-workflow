# Requirements: csg-workflow SKILL.md Entry Redesign

Date: 2026-05-06
Status: Draft
Scope: Lightweight — single file change

## Problem

When users invoke `/csg-workflow` with additional requirements in command-args (e.g., `/csg-workflow 我想加一个功能...如何设计？`), the model skips the routing workflow and directly answers the user's question. Root cause: SKILL.md's "Start Here" section is a numbered list without enough constraint to override the model's tendency to prioritize specific, actionable requests.

Evidence: Session `ae1927e2` (2026-05-06). The model saw the SKILL.md content but immediately jumped to feature design, ignoring all 8 routing steps.

## Goal

Restructure the SKILL.md entry so the model always completes routing (read state → determine stage → recommend Skill → wait for confirmation) before doing anything else, regardless of what the user appends in command-args.

## Approach: Dual-Layer Entry

Split SKILL.md into two layers:

### Layer 1 — Intercept (mandatory, runs first)

- Short, prominent section at the very top of the content (after frontmatter)
- Explicit "you MUST do this before anything else" instruction
- 3 concrete steps: read state → determine stage → recommend Skill → wait for confirmation
- Explicit prohibition list: don't read command-args as a task, don't start research/design/implementation, don't call Agents
- Modeled after `dbs` Skill's effective "你只做路由" constraint

### Layer 2 — Post-routing content (accessible after routing)

- Current SKILL.md content reorganized: intro, V1 Boundary, CSG Role Split, References, Safety Rules
- "Start Here" section is replaced by Layer 1 (routing steps) and a simplified post-routing guidance
- Step 8 (update state at stage end) moves into Layer 2 as post-routing guidance

## Scope Boundaries

### In scope

- Restructure `skills/csg-workflow/SKILL.md` only
- Update related tests in `tests/test_csg_workflow_package.py` if validation rules are affected

### Out of scope

- No changes to `references/`, `assets/`, `scripts/`, or any other file
- No changes to how the Skill system loads or injects SKILL.md content
- No changes to other Skills

## Success Criteria

1. When `/csg-workflow` is invoked with command-args containing a design question, the model follows the routing workflow (reads state, determines stage, recommends a Skill) before addressing the user's question
2. When `/csg-workflow` is invoked without command-args, behavior is unchanged (routing still works)
3. `validate_package.py` passes after the change
4. Existing tests pass

## Key Risk

The model may still ignore the intercept if it's not strong enough. Mitigation: keep the intercept very short (under 15 lines), use strong imperative language, and place explicit prohibitions before any other content.
