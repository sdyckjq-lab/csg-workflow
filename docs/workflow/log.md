# CSG Workflow 阶段记录

这个文件记录阶段过程。最新状态不要只看这里，要先读 `docs/workflow/state.md`。

## 2026-05-06

### 设计探索

- 研读了 Compound、Superpowers、Gstack 的相关 Skill。
- 产出中文主设计文档：`docs/ideation/2026-05-06-ai-project-workflow.zh.md`。

### 需求收敛

- 产出第一版需求文档：`docs/brainstorms/2026-05-06-csg-workflow-requirements.md`。
- 将项目名称从 `project-workflow` 改为 `csg-workflow`。

### Office Hours 评估

- 产出开源落地评估：`docs/office-hours/2026-05-06-csg-workflow-open-source-review.md`。
- 判断项目适合落地并开源，但应该以轻量 Skill 形态启动。
- 确定更好的上下文方案：短规则文件加分层状态文件。

### 下一步

- 使用 `ce-plan` 基于需求文档制定第一版实施计划。

### 规则文件冲突处理补充

- 明确 `AGENTS.md` 属于 Codex，`CLAUDE.md` 属于 Claude Code，通常由各自 `/init` 创建。
- 确定 `csg-workflow` 不覆盖已有规则文件，只追加或更新带标记的短规则块。
- 将规则模板改为 `BEGIN CSG-WORKFLOW RULES` / `END CSG-WORKFLOW RULES` 包裹的小段。

### CEO 审查

- 产出 CEO 审查文档：`docs/reviews/2026-05-06-csg-workflow-ceo-review.md`。
- 审查结论：方向成立，适合开源，但第一版范围过大。
- 已将需求文档收窄为第一版开源楔子：路由、交接、模板、示例。
- 已补充开源发布要求、缺插件降级路径和 README 第一屏要求。

### 实施计划

- 产出第一版实施计划：`docs/plans/2026-05-06-001-feat-csg-workflow-skill-plan.md`。
- 计划将实现拆为 7 个交付单元：Skill 包结构、阶段路由、Skill 选择、状态交接、规则文件安全追加、开源说明、场景验证。
- 自查确认计划覆盖 R1-R34、AE1-AE10、F1-F5。
- 审查后补强两点：验证脚本分阶段检查；规则文件 helper 默认预览，确认后才写入。

### 第一版实现

- 创建 Skill 包：`skills/csg-workflow/`。
- 创建引用文档：阶段路由、Skill 选择、缺插件处理、状态交接、项目规则处理。
- 创建模板：`AGENTS.md.block`、`CLAUDE.md.block`、`state.md`、`decisions.md`、`log.md`。
- 创建脚本：`validate_package.py`、`apply_rule_block.py`。
- 更新开源入口：`README.md`、`LICENSE`、`examples/minimal-project/`。
- 创建验证内容：`tests/pressure-scenarios/csg-workflow-v1.md`、`tests/test_csg_workflow_package.py`。
- 验证结果：包验证通过；7 个单元测试通过；规则块默认预览检查通过。

### 第一版审查修复

- 修复规则块脚本：如果结束标记出现在开始标记之前，现在会拒绝处理。
- 修复包验证脚本：现在会扫描 `skills/csg-workflow/` 下的 Python 文件。
- 新增两个测试覆盖上述问题。
- 验证结果：包验证通过；9 个单元测试通过；两个复现场景均通过。
