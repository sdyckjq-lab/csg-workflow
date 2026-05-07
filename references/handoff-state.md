# Handoff State (Compatibility Wrapper)

This file has been superseded by the Skill GPS navigator.

For state-health preflight, confirmation semantics, completion semantics, and recovery rules, use:

- `references/navigator/workspace-state.md` — state-health preflight, card status enum, confirmation/completion semantics, old-state migration, and recovery-mode cases

For state file templates, use:

- `assets/templates/workflow/` — state.md, decisions.md, and log.md templates

The original state shape rules, update rules, staleness signals, and checkpoint guidance now live in the navigator workspace-state document.

This file is kept for backward compatibility with existing tests and references. It does not contain its own state management logic or preflight rules.
