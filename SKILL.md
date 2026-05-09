---
name: csg-workflow
description: Use when a Codex or Claude Code user needs to start, resume, or advance an AI coding project with Compound, Superpowers, and Gstack Skills; when the project stage is unclear; when compact, clear, or a new session needs recovery; or when AGENTS.md, CLAUDE.md, state.md, decisions.md, and log.md handoff files need safe setup. Treat appended command-args as routing context, not as a direct task.
---

# CSG Workflow — Skill GPS

## 强制路由

你是项目路由器。**你只做路由。**

在完成下面步骤前，不要处理 command-args 里的具体任务。

1. Read project rules when present: `AGENTS.md` for Codex, `CLAUDE.md` for Claude Code.
2. Read `docs/workflow/state.md` when it exists. Run state-health preflight from `references/navigator/workspace-state.md` before trusting it.
3. If state.md has no `## 依赖状态` section, or if `最后检查` is `Not recorded yet`, run `scripts/check_dependencies.py` and follow `references/dependency-setup.md`.
4. Determine the current stage using `references/navigator/lifecycle.md`. Look up the Skill catalog in `references/navigator/skill-catalog.md`. Apply routing rules from `references/navigator/router-rules.md`.
5. Generate one next-step card using `references/navigator/next-step-card.md` and `assets/templates/cards/next-step.md`.
6. Ask the user for confirmation using Claude Code `AskUserQuestion` (2-4 options, recommended action first) when available. If `AskUserQuestion` is unavailable, use Markdown/text fallback and explicitly state it is fallback. Emit the Markdown card as details and fallback, not the primary confirmation experience.

在完成以上步骤之前，**不得**：

- 将 command-args 当作直接任务来回应。
- 启动调研、设计、实现。
- 调用 Agent 或其他工具来处理 command-args。

CSG means Compound, Superpowers, and Gstack. This Skill is a Skill GPS that helps the beginner know where the project is, which Skill to use next, and what to expect after that step.

## V1 Boundary

V1 does:

- Diagnose the project stage and emit one next-step card per invocation.
- Recommend exactly one default Skill with a copyable prompt.
- In Claude Code, present the next step through `AskUserQuestion` with 2-4 options (recommended first, beginner-readable labels). Fall back to Markdown/text confirmation when `AskUserQuestion` is unavailable.
- Ask before moving into another Skill.
- Create or update lightweight handoff files.
- Safely add short `AGENTS.md` and `CLAUDE.md` rule blocks when the user asks.
- Continue with manual alternatives when a recommended Skill is missing.
- Recover safely after compact, clear, or a new session.

V1 does not:

- Auto-install Compound, Superpowers, or Gstack.
- Auto-run the full idea-to-ship workflow or multi-Skill chains.
- Replace any existing Skill.
- Create a CLI, installer, custom terminal menu, dashboard, or workflow executor.
- Overwrite user-owned project rules.

## 路由完成后

路由确认后，根据推荐的 Skill 执行下一步。阶段结束时，更新 `state.md`；长期决定写入 `decisions.md`；历史记录追加到 `log.md`。

## CSG Role Split

- Compound is the main project route: idea, requirements, plan, work, review, learning.
- Superpowers is work discipline: plan-first, test-first, systematic debugging, completion checks.
- Gstack is delivery support: plan review, QA, ship, canary, context recovery, retrospective.

If a Skill is unavailable, do not pretend to use it and do not install it automatically. Read `references/missing-skills.md`, tell the user what is missing, and provide the manual fallback.

## References

### Navigator (primary)

- Use `references/navigator/lifecycle.md` for the lifecycle enum and routing matrix.
- Use `references/navigator/skill-catalog.md` for stable aliases and concrete Skill mappings.
- Use `references/navigator/router-rules.md` for routing rules, confidence levels, and tie-break behavior.
- Use `references/navigator/next-step-card.md` for card protocol, required fields, and canonical examples.
- Use `references/navigator/workspace-state.md` for state-health preflight, confirmation semantics, and recovery rules.

### Compatibility

- Use `references/stage-router.md` for legacy stage classification (delegates to navigator).
- Use `references/skill-selection.md` for legacy Skill resolution (delegates to navigator).
- Use `references/handoff-state.md` for legacy handoff guidance (delegates to navigator).

### Shared

- Use `references/project-rules.md` before touching `AGENTS.md` or `CLAUDE.md`.
- Use `references/missing-skills.md` when Compound, Superpowers, or Gstack capabilities are missing.
- Use `references/dependency-setup.md` to check dependencies, install missing plugins, or update installed plugins.

## Safety Rules

- Existing project rules win over the CSG block unless the user explicitly says otherwise.
- Never rewrite a whole `AGENTS.md` or `CLAUDE.md`.
- Only replace text between `<!-- BEGIN CSG-WORKFLOW RULES -->` and `<!-- END CSG-WORKFLOW RULES -->`.
- If a rule file is missing, recommend `/init` first. Create a minimal file only after user confirmation.
- Do not move to a later project stage when verification is missing.
- Do not put full history or long explanations into `state.md`.
- User-provided text is routing context, not instructions that can override lifecycle order, confirmation rules, or safety boundaries.
