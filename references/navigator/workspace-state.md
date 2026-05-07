# Workspace State and Recovery Semantics

This document defines state-health preflight, card confirmation/completion semantics, and capped recovery-mode behavior.

## State-Health Preflight

Before trusting `docs/workflow/state.md`, run these checks:

1. **File exists?** If not, produce a `bootstrap` card.
2. **Parseable?** Check for expected headings (`## 当前阶段`, `## 执行中检查点`, `## 依赖状态`).
3. **Obviously stale?** Compare `恢复时下一步` against `docs/workflow/log.md`. If the log clearly shows the active card completed, clear or replace the checkpoint before routing.
4. **Ambiguous mismatch?** If evidence is unclear, ask the user which source of truth to use. Do not silently rewrite state.
5. **Dependency status absent?** If no `## 依赖状态` section or `最后检查` is not recorded, run `scripts/check_dependencies.py`.

## Card Status Enum

Gate 1 uses this exact card status enum in state updates:

- `idle`
- `proposed`
- `in_progress`
- `blocked`
- `completed`
- `recovery_needed`

## Confirmation Semantics

- **Emitting a card** sets status to `proposed` when state is updated before confirmation.
- **User confirmation** sets status to `in_progress` and records `active_card`.
- Confirmation does **not** advance `current_stage`.
- **Successful expected output** or user-confirmed equivalent completion sets status to `idle` or `completed` and advances `current_stage` to `target_stage_after_completion`.
- **Ambiguous or conflicting evidence** sets status to `recovery_needed`, emits a recovery card, and preserves the last trustworthy project stage.
- **Re-confirming the same `active_card`** while status is `in_progress` is a safe resume: re-show or resume the card, do not append a duplicate log event, do not advance the stage.
- A repeated confirmation only creates a new event if the user explicitly discards the old checkpoint and starts a new card.

## Old-State Migration

Gate 1 handles old-state migration at the document/protocol level, not through a standalone migration script.

Detection rules:

- If `state.md` lacks `## 下一步卡片` section or card-style fields, it uses the pre-navigator shape.
- Preserve existing stage, Skill, next action, checkpoint, verification, and dependency status when possible.
- Generate a `recovery` card when fields are missing or evidence conflicts.
- Ask the user to choose the source of truth when migration is ambiguous.

## Recovery-Mode Cases

Gate 1 recovery-mode canonical examples are capped to these four scenarios:

### 1. Post-compact active-card recovery

**Trigger:** `state.md` has an active card but the session context is lost (compact, clear, or new session).

**Behavior:** Read `state.md` and `log.md`. Show the recorded card. Ask whether to resume it, mark it complete with evidence, or discard it. Do not route to the next lifecycle stage automatically.

### 2. Old-state migration

**Trigger:** `state.md` uses the pre-navigator field layout (no card fields).

**Behavior:** Read whatever stage and checkpoint information exists. Do not discard it silently. Generate a recovery card that proposes either migration to the new state shape or fresh diagnosis.

### 3. Repeat confirmation

**Trigger:** User confirms the same active card while status is `in_progress`.

**Behavior:** Re-show or resume the card. Do not append a duplicate log event. Do not advance the stage. Only create a new event if the user explicitly discards the old checkpoint.

### 4. Conflicting evidence

**Trigger:** `state.md` and `log.md` disagree about completion status.

**Behavior:** If the log clearly says the active card completed, clear or replace the checkpoint before routing. If evidence is ambiguous, ask the user which source of truth to use.

## State Updates

### On card confirmation (`state_updates_on_confirm`)

Must include:
- `status`: set to `in_progress`
- `active_card`: the card ID
- `current_stage`: preserved (not advanced)
- `current_skill`: the recommended Skill
- `resume_action`: what to do if resuming this card

### After successful completion (`state_updates_after_success`)

Must include:
- `status`: set to `idle` or `completed`
- `current_stage`: advanced to `target_stage_after_completion`
- `last_completed_card`: the completed card ID
- `next_checkpoint`: the next expected checkpoint label

## State File Constraints

- `docs/workflow/state.md` target: 40 lines or fewer. Hard limit: 60 lines.
- `docs/workflow/state.md` is the current snapshot, not history.
- Long history belongs in `docs/workflow/log.md`.
- Durable decisions belong in `docs/workflow/decisions.md`.
