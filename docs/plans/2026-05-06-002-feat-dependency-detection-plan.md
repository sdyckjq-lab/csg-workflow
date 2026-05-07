---
title: "feat: Add dependency detection, install guidance, and update support"
type: feat
status: completed
date: 2026-05-06
---

# feat: Add dependency detection, install guidance, and update support

## Overview

Add first-run dependency detection and user-initiated update support to csg-workflow. A new Python script checks whether Compound, Superpowers, and Gstack are installed. A new reference document tells the LLM how to prompt the user to install missing plugins or update all three. SKILL.md gets an extra step in its Start Here flow.

---

## Problem Frame

V1 assumes all three plugin suites (Compound, Superpowers, Gstack) are already installed. New users who just installed csg-workflow may have zero, one, or two of them. The skill currently has no way to detect this gap or guide the user toward installation. This creates a confusing first-run experience where the LLM recommends skills that don't exist.

---

## Requirements Trace

- R1. On first run (no dependency check record in state.md), detect which of the three plugin suites are installed locally.
- R2. When one or more plugins are missing, prompt the user with a clear summary and offer to install them with a single confirmation.
- R3. Installation commands must be exact and runnable — the user only needs to confirm, not figure out command syntax.
- R4. Support user-initiated one-click update for all three plugins.
- R5. Do not auto-install, auto-update, or auto-detect new versions without user request.
- R6. Follow existing script patterns (Python, argparse, pathlib, exit codes, no third-party imports).
- R7. Follow existing reference doc patterns (LLM-oriented, procedural, with tables).
- R8. All new files must pass validate_package.py (no forbidden patterns, required content).
- R9. Tests must use unittest, no additional dependencies.

---

## Scope Boundaries

- No auto-install script — the LLM runs install commands after user confirmation.
- No automatic version checking or background update detection.
- No changes to the V1 Boundary section (the does/does-not lists) in SKILL.md. The Start Here step sequence may be extended.
- No plugin, dashboard, or kanban features.
- No Codex/OpenAI agent changes in this iteration.

### Deferred to Follow-Up Work

- Codex agent definition update for dependency detection: future iteration, since Codex CLI has different plugin mechanics.

---

## Context & Research

### Relevant Code and Patterns

- `skills/csg-workflow/scripts/validate_package.py` — script pattern: `main(argv) -> int`, `argparse`, `pathlib.Path`, exit codes 0/1/2, `from __future__ import annotations`.
- `skills/csg-workflow/scripts/apply_rule_block.py` — dataclass result pattern: `ApplyResult(changed, written, action, content)`.
- `skills/csg-workflow/references/missing-skills.md` — existing fallback table for missing skills; the new reference doc extends this concept.
- `skills/csg-workflow/references/stage-router.md` — reference doc format: title, "Use this file when..." opener, decision tables, numbered procedural steps.
- `tests/test_csg_workflow_package.py` — test pattern: `importlib.util.spec_from_file_location` to load scripts, `tempfile.TemporaryDirectory` for isolation.

### Plugin Detection Facts

| Plugin | Type | Detection source | Install command | Update command |
|--------|------|-----------------|-----------------|----------------|
| Compound | Claude plugin | `~/.claude/plugins/installed_plugins.json` key `compound-engineering@compound-engineering-plugin` | `claude plugin install compound-engineering@compound-engineering-plugin` | `claude plugin update compound-engineering@compound-engineering-plugin` |
| Superpowers | Claude plugin | `~/.claude/plugins/installed_plugins.json` key `superpowers@claude-plugins-official` | `claude plugin install superpowers@claude-plugins-official` | `claude plugin update superpowers@claude-plugins-official` |
| Gstack | Skill directory | `~/.claude/skills/gstack/SKILL.md` file existence | `git clone https://github.com/garrytan/gstack.git ~/.claude/skills/gstack` | `cd ~/.claude/skills/gstack && git pull` |

---

## Key Technical Decisions

- **Detection script is read-only**: It checks state and reports. It never installs, updates, or modifies anything. This follows the safety-first pattern of `apply_rule_block.py` (preview by default).
- **Installation is LLM-driven**: The reference doc provides exact commands for the LLM to present and run after user confirmation. No bash wrapper script that could run unsupervised.
- **State flag prevents repeated checks**: A dependency check record in `state.md` marks that detection has run. The LLM only re-runs detection when the user explicitly asks.
- **`--json` output mode**: Machine-readable output for LLM parsing, plus human-readable default output.
- **Gstack detection uses SKILL.md existence, not directory existence**: A directory could exist from a failed clone. SKILL.md presence is a stronger signal.

---

## Open Questions

### Resolved During Planning

- Script language: Python (matches existing scripts, confirmed by user).
- Gstack install method: git clone (confirmed by user).
- Update trigger: user-initiated only (confirmed by user).

### Deferred to Implementation

- Exact wording of the dependency-setup.md prompt template — the LLM should test the interaction during implementation.
- Whether Gstack clone should use `--depth 1` for faster download — implementation-time optimization decision.

---

## Implementation Units

- U1. **Create dependency detection script**

**Goal:** A Python script that checks whether Compound, Superpowers, and Gstack are installed and reports status.

**Requirements:** R1, R6

**Dependencies:** None

**Files:**
- Create: `skills/csg-workflow/scripts/check_dependencies.py`

**Approach:**
- Single function `check_dependencies(home: Path) -> dict` returns a dict keyed by plugin name, each with `installed` (bool), `version` (str or None), `source` (str describing where the info came from). The `source` field must use a fixed descriptive string (e.g., `'installed_plugins.json'` or `'SKILL.md file check'`), never absolute paths from the JSON file.
- `main(argv)` uses argparse with `--json` flag for machine-readable output and `--home` to override home directory (for testing).
- Default output: one line per plugin, e.g. `compound: installed (v3.0.1)` or `gstack: missing`.
- Exit code: 0 if all installed, 1 if any missing, 2 on internal error (e.g. malformed JSON).
- Plugin detection reads `~/.claude/plugins/installed_plugins.json` for Compound/Superpowers (parse JSON, match key prefix, extract version).
- Gstack detection checks `~/.claude/skills/gstack/SKILL.md` existence.

**Patterns to follow:**
- `skills/csg-workflow/scripts/validate_package.py`: `main(argv) -> int`, `argparse`, `from __future__ import annotations`, `pathlib.Path`, `raise SystemExit(main())`.
- `skills/csg-workflow/scripts/apply_rule_block.py`: dataclass result, exit code convention (0/1/2).

**Test scenarios:**
- Happy path: all three plugins installed — JSON output has all `installed: true`, exit code 0.
- Happy path: no plugins installed — all `installed: false`, exit code 1.
- Partial install: only Compound — JSON shows compound installed, others missing, exit code 1.
- Edge case: installed_plugins.json missing — treat as no plugins, exit code 1 (not error code 2).
- Edge case: installed_plugins.json malformed — exit code 2 with error message.
- Edge case: gstack directory exists but SKILL.md missing — gstack reported as missing.
- Edge case: `--home` flag points to empty temp dir — all reported missing, exit code 1.
- Human-readable output format: plain text output has expected line format.

**Verification:**
- Script runs with `python3 skills/csg-workflow/scripts/check_dependencies.py` and reports correct status for current machine.
- Script runs with `--json` and produces valid JSON.
- All new tests pass (implemented in U4).

---

- U2. **Create dependency setup reference document**

**Goal:** A reference document that tells the LLM when and how to check dependencies, prompt for installation, and run updates.

**Requirements:** R2, R3, R4, R5, R7

**Dependencies:** U1 (references the script)

**Files:**
- Create: `skills/csg-workflow/references/dependency-setup.md`

**Approach:**
- Follow existing reference doc pattern: title, "Use this file when..." opener, numbered procedural steps, decision tables.
- Content sections:
  1. **When to check**: first run (no dependency record in state.md) or user explicitly asks.
  2. **How to check**: run `scripts/check_dependencies.py`, interpret JSON output.
  3. **How to install missing plugins**: exact commands per plugin, presented as a prompt template the LLM uses to ask the user.
  4. **How to update**: exact update commands per plugin, triggered only when user asks.
  5. **State update**: after checking, record results in state.md dependency section.
  6. **Safety rules**: never install without user confirmation; never auto-update.

**Patterns to follow:**
- `skills/csg-workflow/references/missing-skills.md`: fallback table format, safety rules.
- `skills/csg-workflow/references/stage-router.md`: "Use this file when..." opener, decision table, procedural steps.

**Test scenarios:**
- Test expectation: none — this is a Markdown reference document for the LLM, not executable code. Verified by `validate_package.py` (required content check, forbidden pattern check).

**Verification:**
- Document follows reference doc format (title, opener, tables, steps).
- Contains exact install commands for all three plugins.
- Contains exact update commands for all three plugins.
- Passes `validate_package.py` (no forbidden patterns, no absolute paths).

---

- U3. **Update SKILL.md, state template, and validation script**

**Goal:** Wire the new detection step into the Start Here flow, add a dependency section to the state template, and register new files with the validator.

**Requirements:** R1, R8

**Dependencies:** U1, U2

**Files:**
- Modify: `skills/csg-workflow/SKILL.md`
- Modify: `skills/csg-workflow/assets/templates/workflow/state.md`
- Modify: `examples/minimal-project/docs/workflow/state.md`
- Modify: `skills/csg-workflow/scripts/validate_package.py`

**Approach:**
- **SKILL.md**: Add step 2.5 between current step 2 (read state.md) and step 3 (determine stage): "If state.md has no dependency check record, run `scripts/check_dependencies.py` and follow `references/dependency-setup.md`." Also add a corresponding entry in the References section: "Use `references/dependency-setup.md` to check dependencies, install missing plugins, or update installed plugins."
- **state.md template**: Add a `## 依赖状态` section with placeholder fields: `最后检查` (date), `compound` (version/status), `superpowers` (version/status), `gstack` (version/status). Apply the same section to `examples/minimal-project/docs/workflow/state.md`.
- **validate_package.py**: Add `check_dependencies.py` and `dependency-setup.md` to `REQUIRED_FILES`. Add required-content checks for the new reference doc (must contain "compound-engineering", "superpowers", "gstack", install command fragments).

**Patterns to follow:**
- SKILL.md Start Here step numbering and brevity.
- state.md template field format (Chinese section headers, placeholder values).
- validate_package.py `REQUIRED_FILES` list and `require_contains` helper.

**Test scenarios:**
- Happy path: `validate_package.py` passes with all new files present and valid.
- Regression: removing a required file from REQUIRED_FILES causes test failure.
- Regression: removing required content from dependency-setup.md causes validation failure.

**Verification:**
- `python3 skills/csg-workflow/scripts/validate_package.py` passes.
- SKILL.md Start Here flow now mentions dependency checking at step 2.5.

---

- U4. **Add tests for check_dependencies.py**

**Goal:** Unit tests covering all detection scenarios for the new script.

**Requirements:** R9

**Dependencies:** U1

**Files:**
- Modify: `tests/test_csg_workflow_package.py`

**Approach:**
- Add a new `TestCase` class `CheckDependenciesTest`.
- Load the script module via `importlib.util.spec_from_file_location` (same pattern as existing tests).
- Use `tempfile.TemporaryDirectory` for each test to create isolated home directories.
- Test helper functions construct mock `installed_plugins.json` files and mock skill directories.
- Cover all scenarios listed in U1's test scenarios section.

**Patterns to follow:**
- `tests/test_csg_workflow_package.py`: `ValidatePackageTest` and `ApplyRuleBlockTest` classes, `importlib.util` loading, `tempfile.TemporaryDirectory`.

**Test scenarios:**
- (Listed in U1 — these are the same scenarios, implemented here.)

**Verification:**
- `python3 -m unittest tests/test_csg_workflow_package.py` passes with all new tests.
- All existing tests still pass.

---

## Risks & Dependencies

| Risk | Mitigation |
|------|------------|
| `claude plugin install` requires interactive auth or user confirmation | The LLM runs the command in the user's session where auth is already established. Reference doc notes this dependency. |
| Gstack repo is large, git clone may be slow | Reference doc suggests user can run `git clone --depth 1` for faster download. Not automated. |
| `installed_plugins.json` format may change in future Claude Code versions | Script treats unexpected format as "missing" (safe default), doesn't crash. |
| Detection script path to `~/.claude` differs on Windows | `--home` flag + `Path.home()` handles this. V1 targets macOS/Linux only per CLAUDE.md. |

---

## Sources & References

- Existing V1 plan: `docs/plans/2026-05-06-001-feat-csg-workflow-skill-plan.md`
- V1 requirements: `docs/brainstorms/2026-05-06-csg-workflow-requirements.md`
- Plugin registry: `~/.claude/plugins/installed_plugins.json`
- Gstack repo: `https://github.com/garrytan/gstack.git`
