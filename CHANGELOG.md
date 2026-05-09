# Changelog

## [0.0.5.0] - 2026-05-09

### Added

- Gate 2 Claude Code Interactive Card: `AskUserQuestion` is now the primary next-step confirmation experience in Claude Code, replacing Markdown `yes/no/skip`. Shows 2-4 options with the recommended action first and beginner-readable labels.
- Canonical option sets in `router-rules.md`: normal recommendation (4 options), missing Skill (4 options), recovery menus for proposed/in-progress/conflict states.
- Gate 2 choice semantics in `workspace-state.md`: confirm writes `in_progress`, view details is read-only loop, adjust route regenerates card, skip is terminal.
- Recovery menu variants as structured tables (Proposed Checkpoint Recovery, In-Progress Checkpoint Recovery, Conflict/Recovery-Needed).
- Manual fallback state recording in `skill-catalog.md` for missing Skill scenarios.
- `claude_question` rendering validation in `validate_package.py`: all canonical cards must include both `markdown: required` and `claude_question: required`.
- `not_now` non-empty validation in `validate_package.py`.
- Rendering value validation: checks that rendering fields equal `required`.
- 6 new pressure scenarios (AE22–AE27) covering Gate 2: Claude Code native menu, confirmation semantics, missing Skill fallback, active card recovery, skip/adjust behavior, CLI wording simplification.
- 12 new Gate2Test methods covering U1–U5 requirements.
- Skip/Stop label convention documented in `router-rules.md`.

### Changed

- Terminology unified: "primary confirmation experience" and "details and fallback" used consistently across SKILL.md, router-rules.md, next-step-card.md, and next-step.md.
- Missing-skills.md and next-step.md: menu tables replaced with cross-references to canonical source in router-rules.md, eliminating three-way duplication.
- `next-step-card.md`: removed renderer-neutral/future-CLI wording. `AskUserQuestion` is the Claude Code primary; Markdown is portable fallback.
- AE20 pressure scenario: corrected detection rule from `## 下一步卡片` to `## 执行中检查点`.
- README.md: updated to mention `AskUserQuestion` and "interactive layer" instead of "handoff layer".
- `validate_package.py`: pressure scenario range extended from 22 to 28.

## [0.0.4.0] - 2026-05-07

### Added

- Skill GPS Navigator: a card-based interaction protocol that gives beginners one clear next-step card per invocation across all stages (bootstrap, idea, requirements, plan, work, review, qa, delivery, learning).
- `references/navigator/` with five reference files: lifecycle stages, skill catalog with stable aliases, routing rules, next-step card protocol (17 required fields, 9 canonical examples, 4 recovery cards), and workspace state management.
- `assets/templates/cards/next-step.md` card template with display hierarchy for Markdown rendering.
- Fenced-block card parser in `validate_package.py` — dependency-free parser that extracts ```next-step-card blocks and validates schema (fields, stages, confidence, roles, routing trace).
- Compatibility wrappers: old reference files (`stage-router.md`, `skill-selection.md`, `handoff-state.md`) converted to thin delegates to navigator docs, with split-brain guard.
- 6 new pressure scenarios (AE16–AE21) covering Gate 1 routing: vague idea, completed requirements, missing Skill, post-compact recovery, old-state migration, prompt-injection bypass.
- `NESTED_MAP_FIELDS` constant replacing magic string tuple in card parser.
- 2 new parser edge-case tests: empty card block, list-inside-nested-map.

### Changed

- SKILL.md repositioned as "CSG Workflow — Skill GPS" with navigator-based routing.
- README.md updated for Skill GPS product positioning.
- `validate_cards()` now returns parsed cards alongside IDs, eliminating redundant parsing.
- Specialist review findings addressed: redundant parse, magic strings, weak assertions.

## [0.0.3.0] - 2026-05-07

### Changed

- Repository root is now the Skill root. `SKILL.md`, `references/`, `assets/`, `scripts/`, and `agents/` live at the top level instead of under `skills/csg-workflow/`. Users can clone the entire repo directly into their Skill directory (`git clone <repo> ~/.claude/skills/csg-workflow`) and it will be recognized immediately.
- Package validation now checks root-level paths and rejects old nested entries as a regression guard.
- README, CLAUDE.md, and all runtime references updated to reflect the new layout.

## [0.0.2.0] - 2026-05-07

### Added

- `csg-workflow` can now recover after compact, clear, or a new session by checking whether `state.md` is still current before recommending the next Skill.
- Added recovery cases for stale state and already-completed checkpoints, so the workflow does not restart finished work.
- Added planning records for dependency checks, routing interception, and state-health recovery.

### Changed

- `state.md` is now treated as a short current snapshot, with long history moved to `log.md` and durable decisions kept in `decisions.md`.
- Rule blocks for Codex and Claude Code now tell agents to verify active checkpoints against `log.md` before resuming.

### Fixed

- Strengthened validation so missing scenario headings, missing state headings, and stale recovery wording are caught before release.

## [0.0.1.0] - 2026-05-06

### Fixed

- `/csg-workflow` now treats appended command arguments as routing context first, so users are routed to the right next Skill before any embedded request is answered.

### Added

- Added a pressure scenario and regression checks for command-argument routing interception.
