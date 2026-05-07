# 项目 Workflow 状态

## 当前阶段
安装布局修复：已完成扁平化迁移，验证中。

## 项目目标
让 `csg-workflow` 能被用户按文档安装后直接被 Claude Code 识别。

## 当前主要文档
`README.md`、`SKILL.md`、包验证脚本和安装说明。

## 下一步
运行全量验证和旧路径搜索，确认无残留问题后准备提交。

## 上一个任务
state-health recovery 已合并到 `main`。

## 执行中检查点
状态: in progress.
当前 Skill: ce-work.
当前任务: 执行安装布局修复计划。
恢复时下一步: 运行 validate_package.py 和全量测试，搜索旧路径残留。

## 阻塞问题
- None.

## 最近验证
- 47 个单元测试全部通过。

## 长期决定摘要
- `state.md` 是当前快照；长历史放 `log.md`。
- 恢复时明显过期可修复，不确定时先问用户。

## 不要重复讨论
- 不要重新讨论 plugin，也不要把完整 workflow 塞进规则块。

## 依赖状态
最后检查: 2026-05-07 before ship.
compound/superpowers/gstack: installed.
