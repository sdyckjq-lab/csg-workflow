# Changelog

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
