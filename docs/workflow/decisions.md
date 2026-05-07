# CSG Workflow 决定记录

这个文件只记录长期决定。当前进度不要写在这里，当前进度写进 `docs/workflow/state.md`。

## 2026-05-06

- 第一版做成 Skill，不做 plugin。
- 项目名称改为 `csg-workflow`，CSG 代表 Compound、Superpowers、Gstack。
- Compound 做默认主线。
- Superpowers 做工作纪律。
- Gstack 做评审、QA、发布和上下文恢复。
- 第一版只推荐并引导下一步 Skill，等用户确认后再继续，不默认自动连续执行所有 Skill。
- 上下文方案采用分层设计：`AGENTS.md` / `CLAUDE.md` 放启动规则，`state.md` 放当前状态，`decisions.md` 放长期决定，`log.md` 放阶段记录。
- `AGENTS.md` 和 `CLAUDE.md` 不能写成长说明书，只放所有 agent 必须遵守的少量规则。
- 对已有 `AGENTS.md` / `CLAUDE.md` 只能追加或更新带标记的 `csg-workflow` 规则块，不能覆盖用户原有规则。
- 如果 `csg-workflow` 规则块和项目原规则冲突，默认项目原规则优先。
- 如果项目缺少规则文件，优先建议用户通过 Codex 或 Claude Code 的 `/init` 创建，再追加规则块。
- CEO 审查决定第一版必须收窄为“路由 + 交接 + 模板 + 示例”，完整从想法到发布的路线保留为长期愿景和阶段推荐。
- 开源第一版必须包含安装方式、依赖说明、兼容说明、缺插件降级、许可证和最小示例。
- 开源定位是轻量 workflow Skill，不是替代 Compound、Superpowers、Gstack 的新框架。
- 实施计划决定第一版包目录使用 `skills/csg-workflow/`，设计过程文档继续保留在 `docs/`。
- 实施计划决定 `SKILL.md` 只做短入口，阶段路由、Skill 选择、交接状态、规则文件和缺插件说明拆到 `references/`。
- 实施计划决定规则文件 helper 默认只预览，必须用户确认后才写入。
- 实施计划暂定开源许可证使用 MIT，发布前仍可按项目所有者选择调整。
- 第一版实现采用两个脚本：`validate_package.py` 做包结构和内容验证，`apply_rule_block.py` 做规则块预览和写入。
- 第一版测试采用 `unittest`，不引入额外依赖。

## 2026-05-07

- `state.md` 是当前恢复快照，不是历史记录；长历史必须放进 `docs/workflow/log.md`。
- 恢复时必须先做 state-health preflight，再相信 `state.md` 的下一步。
- 如果状态明显过期，可以先修复 `state.md` 再路由；如果证据不确定，必须先问用户。
- 活跃 checkpoint 不能直接恢复；必须先对照 `docs/workflow/log.md` 和最近验证，确认任务没有已经完成。
- `state.md` 目标 40 行以内，硬上限 60 行。

- 仓库根目录现在就是 Skill 根目录。`SKILL.md`、`references/`、`assets/`、`scripts/`、`agents/` 直接在仓库第一层。取代之前"包目录使用 `skills/csg-workflow/`"的决定。原因：用户 clone 整个仓库到 Skill 目录后 Claude Code 无法识别，因为 Skill 入口文件被嵌套了一层。

## 2026-05-07 Skill GPS Navigator Gate 1 决策

以下决策来自 CEO plan（Approach C, SELECTIVE EXPANSION 模式）：

- 产品定位：从路由推荐升级为 Skill GPS —— 每次给出一个 next-step card，包含当前阶段、推荐 Skill、可复制 prompt、预期产物、状态更新，用户只需确认。
- 实施方案选择 Approach C：`references/navigator/` 五文件重构。原因：唯一能修复产品层问题同时保持非执行 Skill 边界的路径。
- 每个生命周期阶段必须有规范化的 next-step card 示例。原因：示例让协议更难被误读，能更早暴露路由缺口。
- next-step card 使用轻量 fenced-block schema 校验（无外部依赖的简单解析器）。原因：规范化字段需要自动护栏，否则会悄悄漂移。
- 旧的 `references/stage-router.md`、`skill-selection.md`、`handoff-state.md` 转为薄兼容包装器，委托给 navigator 文档。原因：避免 split brain，保留旧入口和现有测试杠杆。
- 兼容包装器不能包含完整的生命周期表或 Skill 选择表（no-split-brain guard）。
- 解析器和校验器的错误必须有命名和可操作的修复提示。错误类别：missing_card_block, malformed_card_block, missing_field, missing_nested_key, invalid_stage, invalid_status, invalid_confidence, duplicate_card_id, wrapper_split_brain。
- Gate 1 必须有 prompt-injection 防护：用户提供的文本只能填充 `user_goal` 和 `prompt`，不能改变生命周期顺序、确认规则或安全边界。
- 重复确认同一个 active card 是安全的恢复操作：重新显示或恢复该 card，不追加重复日志，不推进阶段。
- Gate 1 必须有固定的手工验收清单，覆盖至少 6 个场景：模糊想法、已完成需求、缺 Skill、post-compact 恢复、prompt-injection 旁路、重复确认。
- 每个 card 必须包含短 `routing_trace`（2-4 条），解释阶段和 Skill 选择的推理链。
- Gate 1 验收标准不仅是文档和测试通过，还要求实际调用的 Skill 能产出一个 next-step card，遵循 Markdown 展示层级，并在确认前停下。
- 允许只读本地 Skill 可用性发现（读入口文件名、检查依赖状态），但不允许安装、修改外部 Skill 目录、扫描外部 Skill 内部实现、推断新路由、或自动运行发现的 Skill。
- recovery 是跨切面模式/card 类型，不是项目生命周期阶段。Recovery card 使用 `status: recovery_needed`，标识正在修复的阶段，修复后路由回该阶段或最早可信阶段。
- Gate 1 recovery 示例上限为 4 个：post-compact active-card recovery、old-state migration、repeat confirmation、conflicting evidence。其他降级状态类延后。
- 简化约束：每一条新增的规则、字段、状态更新和校验检查都必须减少初学者的选择负担。如果某个细节只是让内部系统更完整但不让用户的下一步更平静、安全、清晰，则延后到 Gate 2 或删除。
- Gate 1 不做 CLI、installer、arrow-key menu、renderer script、workflow executor、自动多 Skill 链、dashboard、database、包分发。
