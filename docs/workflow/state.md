# 项目 Workflow 状态

## 当前阶段
阶段 5 后续：state-health recovery 已完成，准备合并到 `main`。

## 项目目标
让 `csg-workflow` 在 compact、clear 或新会话后，能用短快照恢复当前阶段并继续推荐正确 Skill。

## 当前主要文档
`SKILL.md`、`handoff-state.md`、pressure scenarios。

## 下一步
合并完成后等待下一个任务。

## 上一个任务
已实现 state-health recovery，并完成 review、验证和发布准备。

## 执行中检查点
状态: idle.
当前 Skill: None.
当前任务: None.
恢复时下一步: Wait for the next user request after merge.

## 阻塞问题
- None.

## 最近验证
- 包验证通过；45 个单元测试通过；diff 格式检查通过。
- Read-only recovery trials passed for stale state and completed checkpoint cases.

## 长期决定摘要
- `state.md` 是当前快照；长历史放 `log.md`。
- 恢复时明显过期可修复，不确定时先问用户。

## 不要重复讨论
- 不要重新讨论 plugin，也不要把完整 workflow 塞进规则块。

## 依赖状态
最后检查: 2026-05-07 before ship.
compound/superpowers/gstack: installed.
