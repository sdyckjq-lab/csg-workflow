---
date: 2026-05-06
topic: csg-workflow-ceo-review
mode: SCOPE_REDUCTION_FOR_V1
status: APPROVED_WITH_CHANGES
source: docs/brainstorms/2026-05-06-csg-workflow-requirements.md
---

# CSG Workflow CEO Review

## Verdict

这份需求值得继续做，也适合开源。

但第一版必须更窄。现在文档描述的是完整愿景，容易让实现阶段误以为要一次性覆盖从想法到发布的全部流程。第一版应该只证明一件事：

> 新手能从一个项目状态不清的目录开始，通过 `csg-workflow` 找到当前阶段、下一步 Skill、交接文件，并在新 session 里继续。

完整路线可以保留，但第一版的开源楔子必须是“路由 + 交接 + 模板 + 示例”。

---

## Premise Challenge

1. 真实问题成立。用户不是缺更多 Skill，而是不知道 Skill 怎么接成项目流程。
2. 需求文档的方向成立。`csg-workflow` 不替代三套插件，只做导航，这是对的。
3. 当前最大风险是第一版范围过大。完整路线可以写进文档，但不能都变成第一版必须实现的能力。
4. 开源落地还缺安装、兼容、缺插件降级、示例和许可要求。这些不是锦上添花，是陌生用户敢不敢试用的基础。
5. `AGENTS.md` / `CLAUDE.md` 的处理已经修正到正确方向：只追加标记块，不接管用户项目规则。

---

## Approaches Considered

### Approach A: 按当前完整愿景做第一版

- **Effort:** L
- **Risk:** High
- **Pros:** 愿景完整，看起来很有野心。
- **Cons:** 第一版难落地，容易变成一份很长的说明书，而不是一个能用的 Skill。

### Approach B: 第一版只做开源楔子

- **Effort:** M
- **Risk:** Low
- **Pros:** 能快速做出可安装、可试用、可验证的版本。
- **Cons:** 第一版不会自动覆盖完整从想法到 ship 的所有流程，需要明确说明哪些是路线图。

### Approach C: 直接做 plugin

- **Effort:** XL
- **Risk:** Very High
- **Pros:** 最终体验可能更完整。
- **Cons:** 现在没有用户反馈，直接做 plugin 会把问题做重，偏离“新手流程导航”的核心。

## Recommendation

选择 Approach B。

这是最像产品的路径：先让一个陌生用户装上、看懂、跑通一次，再决定是否扩展。

---

## Required Changes

### 1. 定义第一版楔子

第一版必须明确不是“全流程自动化”，而是：

- 判断当前阶段
- 推荐下一步 Skill
- 创建或更新交接文件
- 安全追加项目规则块
- 提供最小示例
- 支持新 session 恢复

### 2. 增加开源发布要求

需求文档必须写清：

- 安装方式
- 依赖哪些插件或 Skill
- 缺少某个插件时怎么降级
- README 第一屏怎么解释 CSG
- 许可证
- 示例项目

### 3. 增加缺插件降级路径

不能假设用户一定同时拥有 Compound、Superpowers、Gstack。

第一版至少要做到：

- 检测不到某个 Skill 时，不中断整个流程
- 告诉用户缺了什么
- 给出手动替代步骤
- 不自动安装外部插件

### 4. 强化新手第一步

用户第一次运行时，最重要的不是看完整路线图，而是知道：

- 我现在在哪一步
- 我下一步做什么
- 我要不要先写需求
- 我需要保存什么，避免下次断掉

### 5. 保留长期愿景，但不要压进第一版

QA、ship、发布后检查、经验沉淀都应该保留在路线图里，但第一版只需要能推荐这些阶段，不需要完整自动化这些阶段。

---

## What Already Exists

- 中文需求文档：`docs/brainstorms/2026-05-06-csg-workflow-requirements.md`
- 开源落地评估：`docs/office-hours/2026-05-06-csg-workflow-open-source-review.md`
- 当前状态文件：`docs/workflow/state.md`
- 长期决定记录：`docs/workflow/decisions.md`
- 阶段记录：`docs/workflow/log.md`
- 规则块模板：`docs/workflow/templates/AGENTS.md.template`、`docs/workflow/templates/CLAUDE.md.template`

---

## Dream State Delta

```text
当前状态
  需求文档已经能说明项目方向，但第一版边界还不够锋利。

本次审查后的状态
  第一版收窄为可安装、可试用、可恢复的 workflow Skill。

12 个月理想状态
  csg-workflow 成为新手启动 AI 编程项目时的默认入口。
  用户不需要理解所有 Skill，只需要知道自己当前在哪一步。
```

---

## NOT In Scope For V1

- 不做完整 plugin。
- 不做可视化项目面板。
- 不自动扫描并安装三套插件。
- 不自动执行完整从想法到发布的所有 Skill。
- 不接管用户已有 `AGENTS.md` / `CLAUDE.md`。
- 不把 QA、ship、部署、canary 做成第一版自动化。

---

## Failure Modes

| Failure mode | Impact | Required mitigation |
|---|---|---|
| 第一版范围太大 | 项目迟迟不能发布 | 明确 V1 只做路由、交接、模板、示例 |
| 用户缺少某个插件 | Skill 推荐后无法继续 | 提供缺插件提示和手动替代步骤 |
| 规则文件被覆盖 | 用户项目规则被破坏 | 只追加或更新标记块 |
| `state.md` 越写越长 | 新 session 仍然浪费上下文 | 长期决定和日志拆到独立文件 |
| README 解释不清 CSG | 开源用户看不懂项目 | 第一屏说明 CSG 含义和适用对象 |
| 示例缺失 | 用户不知道怎么开始 | 提供最小示例：空项目到需求/计划交接 |

---

## CEO Review Summary

```text
Mode selected        | SCOPE REDUCTION FOR V1
Verdict              | APPROVED WITH CHANGES
Core issue           | Vision is right, V1 scope needs sharper wedge
Critical changes     | V1 wedge, open-source requirements, missing-plugin fallback
UI scope             | None
Implementation ready | Yes, after requirements doc is patched
Next recommended     | ce-plan
```
