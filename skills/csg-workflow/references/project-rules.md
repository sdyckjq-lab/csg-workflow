# Project Rules

Use this file before touching `AGENTS.md` or `CLAUDE.md`.

## Ownership Rule

`AGENTS.md` belongs to the project and Codex. `CLAUDE.md` belongs to the project and Claude Code. `csg-workflow` only owns the text between its markers:

```markdown
<!-- BEGIN CSG-WORKFLOW RULES -->
...
<!-- END CSG-WORKFLOW RULES -->
```

Everything outside those markers is user-owned and must remain unchanged.

## Conflict Rule

If the CSG block conflicts with existing project rules, existing project rules win unless the user explicitly asks to change them.

## Missing File Rule

If `AGENTS.md` or `CLAUDE.md` is missing:

1. Recommend the tool's `/init` command first.
2. Explain that `/init` creates the normal project rule file.
3. Create a minimal file only after user confirmation.
4. Keep the file short.

## Safe Helper

Use `scripts/apply_rule_block.py` for rule-block changes.

The helper defaults to preview mode. It writes only when called with an explicit write option.

Expected behavior:

- Existing marker pair: replace only the marked block.
- No marker pair: append the block.
- Missing target file: recommend `/init` unless explicit creation is requested.
- Broken marker pair: refuse to edit and ask for manual repair.

## Block Requirements

Rule blocks must:

- Stay short.
- Point to `docs/workflow/state.md`.
- Tell the agent to run the state-health preflight before trusting recorded state.
- Tell the agent to check `docs/workflow/log.md` before resuming an active checkpoint.
- Tell the agent to update state at stage end.
- Mention that original project rules take priority.
- Avoid stage tables, Skill catalogs, history, or long explanations.

The packaged templates in `assets/templates/AGENTS.md.block` and `assets/templates/CLAUDE.md.block` are the source of truth for exact rule-block wording.
