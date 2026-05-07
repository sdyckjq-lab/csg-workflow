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
