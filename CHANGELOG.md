# Changelog

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
