# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在本仓库中工作时提供指引。

## 项目简介

CSG Workflow（`csg-workflow`）是一个轻量级 Skill，用于 AI 编程工具（Codex、Claude Code）。它帮用户判断项目当前阶段、推荐下一步该用哪个 Skill、保存交接状态、支持对话恢复后继续。

CSG 代表 Compound（主线流程）、Superpowers（工作纪律）、Gstack（交付支持）。

第一版只做：路由、交接文件、模板、示例。不做 plugin、不做看板、不自动执行完整流程。

## 常用命令

```bash
# 验证包结构和内容
python3 skills/csg-workflow/scripts/validate_package.py

# 运行全部测试
python3 -m unittest tests/test_csg_workflow_package.py

# 预览规则块变更（只看不写）
python3 skills/csg-workflow/scripts/apply_rule_block.py --target <文件路径> --template <模板路径>

# 写入规则块变更（需要 --write 才会真的改文件）
python3 skills/csg-workflow/scripts/apply_rule_block.py --target <文件路径> --template <模板路径> --write
```

## 架构

Skill 包在 `skills/csg-workflow/`：

- **`SKILL.md`** — 入口文件，包含安全规则。内容短，细节委托给 references。
- **`references/`** — 阶段路由（stage-router）、Skill 选择（skill-selection）、交接状态（handoff-state）、项目规则处理（project-rules）、缺 Skill 降级（missing-skills）。这些是运行时的决策文档。
- **`assets/templates/`** — 规则块模板（`AGENTS.md.block`、`CLAUDE.md.block`）和交接文件模板（`state.md`、`decisions.md`、`log.md`）。
- **`scripts/`** — `validate_package.py`（检查结构、内容、禁止模式）和 `apply_rule_block.py`（预览/写入规则块）。
- **`agents/openai.yaml`** — Codex agent 定义。

交接状态使用 `docs/workflow/` 下的三个文件：
- `state.md` — 当前阶段、下一步、已验证内容
- `decisions.md` — 长期决定（含日期和原因）
- `log.md` — 阶段记录（只追加）

设计和规划文档在 `docs/`（brainstorms、plans、reviews、office-hours、ideation）。

## 关键规则

- `AGENTS.md`/`CLAUDE.md` 中的规则块由 `<!-- BEGIN CSG-WORKFLOW RULES -->` 和 `<!-- END CSG-WORKFLOW RULES -->` 包裹。只能修改标记之间的内容。
- `apply_rule_block.py` 默认只预览不写入，必须加 `--write` 才会实际修改文件。
- 发布文件中禁止出现：绝对本地路径（`/Users/...`）、file URI、editor URI、TODO/TBD 标记、未完成的中文标记（待补/待定）。验证脚本会扫描 `skills/` 下所有 `.md`、`.yaml`、`.py` 文件。
- 已有的项目规则优先于 CSG 规则，除非用户明确要求覆盖。
- 第一版不自动安装依赖、不自动执行 Skill、不覆盖用户已有的规则文件。
- 测试只用 `unittest`，不引入额外依赖。

## Git 与项目管理

- 修改代码时优先新建分支工作，不直接在 main 上改。
- 阶段性进度要用 commit 保存，保持提交边界清晰。
- 未经用户同意，不要合并到 main，不要推送。

## 隐私与脱敏

- 推送到 GitHub 或任何公开平台时，作者名统一使用 `Kiro`，不要出现真实姓名。
- 提交内容中不要包含本地绝对路径（如 `/Users/xxx/`），统一使用相对路径。
- 提交前用 `python3 skills/csg-workflow/scripts/validate_package.py` 检查是否有泄露。
