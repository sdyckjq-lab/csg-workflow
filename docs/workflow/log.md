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

## 2026-05-07

### Compact 路由修复

- 基于已合并的依赖检测和路由拦截改动，继续解决后半段恢复失效问题。
- 增加 post-compact route-only 规则和 in-progress checkpoint，要求恢复后先推荐下一步 Skill 并等待确认。
- 通过包验证、38 个单元测试、以及只读 Codex CLI 恢复试验。

### State-health 计划

- 产出计划：`docs/plans/2026-05-07-001-feat-state-health-recovery-plan.md`。
- 计划决定把 `state.md` 当作当前快照，不当作历史记录。
- 计划补充四项约束：主入口同步恢复规则、明显过期自动修不确定先问、真实恢复演练、`state.md` 最多 60 行。
- 本阶段将原本过长的 live `state.md` 压缩为当前快照，长历史保留在本日志和 `decisions.md`。

### State-health 实现

- 更新 `SKILL.md`、规则块模板和 `handoff-state.md`，恢复时先做 state-health preflight。
- 明确明显过期时先修 `state.md`，证据不确定时先问用户。
- 模板和最小示例新增完成态快照字段，`state.md` 上限设为 60 行。
- 新增 AE14 stale state recovery 和 AE15 completed state recovery 压力场景。
- 验证结果：包验证通过；41 个单元测试通过；stale state 和 completed checkpoint 两个只读恢复演练通过。

### State-health 审查修复

- 修复 review 发现的恢复路径缺口：活跃 checkpoint 恢复前必须对照 `log.md`，已完成任务不能继续恢复。
- 补强验证脚本和测试，避免压力场景、标题和 live `state.md` 校验出现假阳性。
- 压缩 live `state.md`，让它继续作为当前快照，而不是历史记录。
- 验证结果：包验证通过；45 个单元测试通过；diff 格式检查通过。
