# CSG Workflow

CSG Workflow is a lightweight Skill for AI coding projects.

CSG means Compound, Superpowers, and Gstack. The Skill helps a Codex or Claude Code user answer three practical questions:

- Where is this project right now?
- Which Skill should I use next?
- How do I continue after compact, clear, or a new session?

## What The First Version Does

第一版只做四件事：路由、交接、模板、示例。

- 判断项目当前阶段。
- 推荐下一步 Skill，并解释原因。
- 维护 `docs/workflow/state.md`、`decisions.md`、`log.md`。
- 安全追加 `AGENTS.md` 和 `CLAUDE.md` 的短规则块。
- 在缺少 Compound、Superpowers 或 Gstack 某个能力时，给出手动替代步骤。

第一版不做插件、不做看板、不自动执行完整流程、不自动安装外部 Skill、不覆盖用户已有规则文件。

## Who This Helps

适合已经装了很多 Skill，但仍然不知道项目该怎么推进的人：

- 新手用户：不知道每个阶段该用哪个 Skill。
- 熟练用户：想减少选择成本，让项目交接更稳定。
- 需要恢复上下文的用户：compact、clear 或新开对话后不想重新解释项目。

## Install

安装方式：

1. 把 `skills/csg-workflow/` 复制到你的 Codex Skill 目录，通常是 `$HOME/.codex/skills/`。
2. 重新打开 Codex，或开始一个新对话，让 Skill 被重新发现。
3. 在项目里使用 `$csg-workflow`，让它读取或创建 `docs/workflow/state.md`。

Claude Code 用户可以把同一个 Skill 目录复制到自己的 Claude Code Skill 目录。不同工具的项目规则文件不同：Codex 通常读 `AGENTS.md`，Claude Code 通常读 `CLAUDE.md`。

## Dependencies

依赖说明：

- Compound：主线工作流，负责想法、需求、计划、执行、审查和经验沉淀。
- Superpowers：工作纪律，负责计划优先、测试优先、系统调试和完成前检查。
- Gstack：交付支持，负责计划审查、QA、ship、canary、恢复和复盘。

这些依赖不是强制同时存在。`csg-workflow` 不自动安装它们。如果某个 Skill 不存在，它会说明缺什么，并给出手动替代步骤。

## Compatibility

兼容说明：

- Codex：使用 `AGENTS.md` 作为项目规则入口。
- Claude Code：使用 `CLAUDE.md` 作为项目规则入口。
- 两个规则文件都只追加 `csg-workflow` 自己的短规则块。
- 如果已有项目规则和 CSG 规则冲突，已有项目规则优先。

## Minimum Example

最小示例在 `examples/minimal-project/`。

它展示一个空项目如何拥有：

- `docs/workflow/state.md`
- `docs/workflow/decisions.md`
- `docs/workflow/log.md`

这个示例的目的不是演示完整开发流程，而是演示下一次对话如何从状态文件继续。

## Package Layout

```text
skills/csg-workflow/
  SKILL.md
  references/
  assets/templates/
  scripts/
examples/minimal-project/
tests/
```

## Validate

运行验证：

```bash
python3 skills/csg-workflow/scripts/validate_package.py
python3 -m unittest tests/test_csg_workflow_package.py
```

验证会检查 Skill 包结构、规则块安全、README 第一屏、最小示例和验收场景。

## License

许可证：MIT。详见 `LICENSE`。

## Current Project Docs

- 需求文档：`docs/brainstorms/2026-05-06-csg-workflow-requirements.md`
- 实施计划：`docs/plans/2026-05-06-001-feat-csg-workflow-skill-plan.md`
- CEO 审查：`docs/reviews/2026-05-06-csg-workflow-ceo-review.md`
- 开源落地评估：`docs/office-hours/2026-05-06-csg-workflow-open-source-review.md`
- 当前状态：`docs/workflow/state.md`
