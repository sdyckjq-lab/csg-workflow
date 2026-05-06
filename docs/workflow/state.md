# 项目 Workflow 状态

## 当前阶段

阶段 5：第一版 `csg-workflow` Skill 已实现，并通过本地验证。

## 项目目标

创建一套名为 `csg-workflow` 的 AI 编程项目流程。CSG 代表 Compound、Superpowers、Gstack。它把三套插件里的有用 Skill 串成一条清楚、稳定、可继续的项目路线。

## 目标用户

已经安装了很多 Skill，但不知道每个 Skill 什么时候用、项目应该怎么推进、compact 或 clear 后怎么继续的新手用户。

## 已完成内容

- 研读了 gstack、compound、superpowers 的本地 Skill 内容。
- 对比了三套插件的强项、空缺和重复点。
- 设计了从想法、需求、计划、实现、审查、QA、交付到经验沉淀的融合流程。
- 确定第一版应该做成 Skill，而不是 plugin。
- 创建了英文设计原稿。
- 创建了中文主设计文档。
- 创建了第一版中文需求文档。
- 使用 office-hours 视角评估了落地和开源可行性。
- 将项目名称从 `project-workflow` 改为 `csg-workflow`。
- 将上下文方案调整为轻量规则文件加分层状态文件。
- 补充了 `AGENTS.md` / `CLAUDE.md` 已存在时的冲突处理策略。
- 完成 CEO 视角审查，并将第一版范围收窄为“路由 + 交接 + 模板 + 示例”。
- 创建了第一版实施计划，并完成计划自查。
- 创建了 `skills/csg-workflow/` Skill 包。
- 创建了阶段路由、Skill 选择、缺插件处理、状态交接、规则文件安全处理文档。
- 创建了 `AGENTS.md` / `CLAUDE.md` 规则块模板。
- 创建了 `state.md`、`decisions.md`、`log.md` 交接模板。
- 创建了规则块安全处理脚本和包验证脚本。
- 更新了 README、LICENSE 和最小示例。
- 创建了压力场景和单元测试。

## 当前主要文档

- 需求文档：`docs/brainstorms/2026-05-06-csg-workflow-requirements.md`
- 实施计划：`docs/plans/2026-05-06-001-feat-csg-workflow-skill-plan.md`
- CEO 审查：`docs/reviews/2026-05-06-csg-workflow-ceo-review.md`
- 开源落地评估：`docs/office-hours/2026-05-06-csg-workflow-open-source-review.md`
- 中文主设计文档：`docs/ideation/2026-05-06-ai-project-workflow.zh.md`
- 长期决定：`docs/workflow/decisions.md`
- 阶段记录：`docs/workflow/log.md`
- 规则模板：`docs/workflow/templates/AGENTS.md.template`、`docs/workflow/templates/CLAUDE.md.template`
- 英文原稿：`docs/ideation/2026-05-06-ai-project-workflow.md`

## 下一步

第一版已经实现。下一步可以试用 `skills/csg-workflow/`，或准备开源发布前的最后审查。

## 重要决定

- Compound 做默认主线。
- Superpowers 做工作纪律，重点用于先想清楚、测试、调试、审查和完成前验证。
- Gstack 做产品拷问、计划审查、QA、发布、上下文保存恢复和复盘。
- 项目必须使用本地状态文件和轻量项目规则，不能只依赖聊天记录。
- 第一版 Skill 名称改为 `csg-workflow`。
- 第一版只做开源楔子：路由、交接、模板、示例。
- 第一版只推荐并引导下一步 Skill，等用户确认后再继续，不默认自动连续执行所有 Skill。
- `AGENTS.md` 和 `CLAUDE.md` 只放少量强制启动规则，不放完整长流程。
- `state.md` 只放当前状态；长期决定进入 `decisions.md`；阶段记录进入 `log.md`。
- 对已有 `AGENTS.md` / `CLAUDE.md` 只能追加或更新带标记的 `csg-workflow` 规则块，不能覆盖用户原有规则。
- 如果 `csg-workflow` 规则块和项目原规则冲突，默认项目原规则优先。
- 第一版实现目录采用 `skills/csg-workflow/`，设计文档继续放在 `docs/`。
- 规则文件更新必须默认预览，只有用户确认后才写入。
- 包验证脚本是 `skills/csg-workflow/scripts/validate_package.py`。
- 规则块处理脚本是 `skills/csg-workflow/scripts/apply_rule_block.py`。

## 计划阶段已确定的问题

- `state.md`、`decisions.md`、`log.md` 的具体字段和默认文字。
- `AGENTS.md` 和 `CLAUDE.md` 的最短追加规则块模板。
- 已有 `AGENTS.md` / `CLAUDE.md` 中如何检测、追加和更新 `csg-workflow` 标记块。
- 开源安装方式、兼容说明、缺插件降级、最小示例和许可证。
- 哪些内容放在主 `SKILL.md`，哪些内容拆到参考文件。
- 用户确认进入下一阶段时，如何把上下文交给下一个 Skill。

这些问题已经在实施计划里拆到具体交付单元，下一步按计划实现即可。

## 已验证内容

- 确认项目最开始是空文件夹。
- 确认已创建的文件都存在。
- 检查过中文主设计文档，确认包含 plugin、Skill、交接、compact、clear、新手路线、复杂路线、必选、可选、状态文件等关键内容。
- 检查过需求文档，确认包含用户角色、关键流程、需求、验收例子、成功标准、范围边界、重要决定、假设和下一步。
- 确认需求文档没有需要先解决才能进入计划阶段的问题。
- 检查过 office-hours 评估，确认当前方向适合落地和开源，但需要按轻量规则文件加分层状态文件推进。
- 已创建 `decisions.md`、`log.md`、`AGENTS.md.template`、`CLAUDE.md.template` 作为下一步计划输入。
- 已补充规则文件冲突处理：不覆盖已有 `AGENTS.md` / `CLAUDE.md`，只追加或更新带标记的短规则块。
- 已完成 CEO 审查，确认方向适合继续，但第一版必须收窄为可安装、可试用、可恢复的最小 Skill。
- 已创建并自查实施计划，确认覆盖 R1-R34、AE1-AE10、F1-F5，未发现绝对路径或未填占位内容。
- 已运行 `python3 skills/csg-workflow/scripts/validate_package.py`，结果通过。
- 已运行 `python3 -m unittest tests/test_csg_workflow_package.py`，7 个测试通过。
- 已运行规则块预览检查，确认默认只预览不写入。
- 已检查 README、LICENSE、skills、examples、tests、workflow docs、plan docs，未发现绝对路径或未填标记内容。
- 已修复第一版审查发现的两个问题：反向规则标记会被拒绝；包验证会扫描 Python 脚本。
- 已重新运行包验证和测试，9 个测试通过。

## 不要重复讨论，除非有新情况

- 不要重新讨论第一版是否应该做成 plugin；目前决定是先做 Skill。
- 不要重新讨论三套插件谁做主线；目前决定是 Compound 主线、Superpowers 做纪律、Gstack 做交付和恢复。
- 不要把完整 workflow 塞进 `AGENTS.md` 或 `CLAUDE.md`。
- 不要覆盖用户已有 `AGENTS.md` 或 `CLAUDE.md`。
- 不要把 QA、ship、部署、canary 做成第一版自动化；第一版只推荐这些阶段。
- 不要重新从头设计项目目标；第一版已经实现，下一步应该试用、审查或准备发布。
