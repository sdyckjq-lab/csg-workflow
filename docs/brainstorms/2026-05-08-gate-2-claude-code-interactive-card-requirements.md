---
date: 2026-05-08
topic: gate-2-claude-code-interactive-card
language: zh-CN
---

# Gate 2 Claude Code Interactive Card 需求文档

## Summary

Gate 2 要把 `csg-workflow` 做成 Claude Code 内的交互式 Skill GPS：复用 Claude Code 的 `AskUserQuestion` 菜单能力，让用户用上下箭头选择、回车确认下一步。`csg-workflow` 只负责判断阶段、生成清晰选项、记录状态和交接 prompt，不自研 CLI、菜单或安装器。

---

## Problem Frame

Gate 1 已经建立了 Skill GPS 的核心协议：读取状态、判断阶段、生成一个 next-step card，并在确认前停止。但当前输出仍偏 Markdown 卡片，用户需要阅读较长文本后用文字回复 `yes/no/skip`。

Claude Code 已经提供了 `AskUserQuestion` 这种原生交互能力，可以直接渲染上下箭头选择和回车确认。Gate 2 的问题不是“实现一个新的终端菜单”，而是让 `csg-workflow` 正确使用这个已有能力，避免重复造轮子和扩大范围。

---

## Actors

- A1. 新手用户：希望看到少量可选下一步，而不是读完整流程说明或记住 Skill 名称。
- A2. `csg-workflow` Skill：判断阶段、生成下一步选项、调用 Claude Code 交互问题、更新交接状态。
- A3. Claude Code：提供 `AskUserQuestion` 菜单渲染、上下箭头选择和回车确认能力。
- A4. 后续 Skill：用户确认后被推荐或进入，例如 `ce-brainstorm`、`ce-plan`、`ce-work`、`qa-only`。
- A5. 后续会话中的 AI：通过 `docs/workflow/state.md` 恢复上一次已提议或执行中的 next-step card。

---

## Key Flows

- F1. 生成交互式下一步菜单
  - **Trigger:** 用户运行 `/csg-workflow` 或恢复项目时需要下一步推荐。
  - **Actors:** A1, A2, A3
  - **Steps:** Skill 读取项目规则和 `state.md`，完成 state-health preflight，判断当前阶段，生成一个默认推荐和少量可选动作，并用 `AskUserQuestion` 展示。
  - **Outcome:** 用户看到 Claude Code 原生选择菜单，而不是只看到 Markdown `yes/no/skip`。
  - **Covered by:** R1, R2, R3, R4, R5

- F2. 用户确认推荐下一步
  - **Trigger:** 用户在 `AskUserQuestion` 菜单里选择推荐动作。
  - **Actors:** A1, A2, A4, A5
  - **Steps:** Skill 将 card 状态写为执行中 checkpoint，保留当前阶段不提前推进，然后按推荐 Skill 进入下一步或输出可复制 prompt。
  - **Outcome:** 项目有可恢复的 active card；后续 Skill 不需要重新猜测当前阶段和任务目标。
  - **Covered by:** R6, R7, R8, R9

- F3. 用户选择调整、跳过或恢复
  - **Trigger:** 用户不接受推荐动作，或状态处于 recovery / conflict / repeat-confirmation 情况。
  - **Actors:** A1, A2, A3, A5
  - **Steps:** Skill 用 `AskUserQuestion` 提供调整、跳过、恢复、清除 checkpoint 等安全选项；不在用户未确认时调用后续 Skill 或推进阶段。
  - **Outcome:** 用户可以纠正路线或恢复状态，而不会被自动带到错误阶段。
  - **Covered by:** R10, R11, R12, R13

---

## Requirements

**Claude Code interaction**
- R1. Gate 2 必须复用 Claude Code 的 `AskUserQuestion` 作为交互菜单能力，不自研终端菜单、CLI 或箭头键 UI。
- R2. `csg-workflow` 在 Claude Code 中推荐下一步时，必须优先使用 `AskUserQuestion` 展示选择，而不是只输出 Markdown `yes/no/skip`。
- R3. 交互菜单必须只有少量选项，通常 2-4 个；第一个选项应是推荐动作，并在 label 中标明推荐。
- R4. 每个选项必须用新手能看懂的短标签和说明表达，不要求用户先知道 Skill 生态。
- R5. Markdown next-step card 可以作为详情或 fallback，但不应替代 Claude Code 交互菜单成为主体验。

**Routing and confirmation semantics**
- R6. 用户确认推荐动作后，Skill 必须更新 `docs/workflow/state.md`：记录 active card、当前 Skill、恢复动作，并保持 current_stage 不提前推进。
- R7. 阶段推进只能在预期产物存在、验证已记录，或用户确认等价完成后发生；不能因为菜单确认就推进阶段。
- R8. 确认后进入后续 Skill 时，必须保留足够上下文：用户目标、推荐 Skill、预期产物、不能做的事和恢复提示。
- R9. 如果后续 Skill 不可用，菜单应提供手动 fallback 或说明缺失，而不是假装 Skill 存在。

**Recovery and correction**
- R10. 当存在 active card 或状态冲突时，`csg-workflow` 必须优先展示恢复/清理菜单，而不是生成新的无关下一步。
- R11. 重复确认同一个 active card 时，应恢复或重新展示该 card，不重复追加日志，不推进阶段。
- R12. 用户选择跳过或调整路线时，Skill 不得调用推荐 Skill，不得写入执行中 checkpoint，除非用户明确选择保存调整后的 card。
- R13. 如果 `AskUserQuestion` 不可用，Skill 可以降级为 Markdown 选项和文字确认，但必须说明这是 fallback。

**Gate 1 simplification**
- R14. Gate 1 的 lifecycle、Skill catalog、router rules、state-health 仍保留，因为它们是判断下一步的核心。
- R15. Gate 1 中“renderer-neutral / future CLI / cli_menu / arrow-key menu”相关表述应降级为远期备注，不作为 Gate 2 的实施前提。
- R16. Gate 1 的 next-step card schema 应服务 Claude Code 交互和状态恢复；不应为了未来独立 CLI 增加额外字段或机器协议复杂度。
- R17. `state.md` 应保持当前快照，不为了潜在 CLI 解析变成复杂数据库或长机器配置。

---

## Acceptance Examples

- AE1. **Covers R1, R2, R3, R4, R5.** 给定用户运行 `/csg-workflow` 且状态健康，当 Skill 产出下一步时，应出现 Claude Code 原生选择菜单，推荐动作排第一；用户不需要手动输入 `yes/no/skip`。

- AE2. **Covers R6, R7, R8.** 给定用户确认推荐动作，当确认完成后，`state.md` 应记录 active card 和恢复动作，但 current_stage 不提前推进；后续 Skill 获得足够上下文继续。

- AE3. **Covers R9.** 给定推荐 Skill 缺失，当 Skill 展示菜单时，应提供手动 fallback 或缺失说明，不自动安装，也不假装可用。

- AE4. **Covers R10, R11.** 给定 `state.md` 已有 active card，当用户再次运行 `/csg-workflow`，应展示恢复/清理菜单，而不是新建重复 card 或推进阶段。

- AE5. **Covers R12.** 给定用户选择跳过或调整推荐动作，Skill 不应调用后续 Skill，也不应写入执行中 checkpoint，除非用户明确保存新 card。

- AE6. **Covers R14, R15, R16, R17.** 给定 Gate 1 文档仍包含未来 CLI 相关措辞，Gate 2 应把它们降级为远期备注或删除，不应为了未来 CLI 扩大当前实现。

---

## Success Criteria

- 用户运行 `/csg-workflow` 后，主要体验是 Claude Code 原生选择菜单，而不是长 Markdown 卡片加文字确认。
- 用户能用上下箭头选择、回车确认下一步。
- 确认后 `state.md` 可恢复，且不会提前推进阶段。
- Gate 2 不新增 CLI、installer、package generator、独立菜单 renderer 或 workflow executor。
- Gate 1 文档被精简到服务当前 Skill 交互，不再让未来 CLI 方向牵引当前范围。
- 后续 `ce-plan` 可以直接规划 AskUserQuestion 集成和文档精简，不需要处理自研 CLI。

---

## Scope Boundaries

- 不做 `csg start`。
- 不做自研终端箭头菜单。
- 不做 `csg package`、`csg install` 或 clean Skill package generator。
- 不做全局命令、PATH、npm/pip/binary 发布。
- 不做机器解析 Markdown 状态来驱动独立 CLI。
- 不做自动多 Skill 链或 workflow executor。
- 不为了未来 CLI 扩展 Gate 1 card schema。

---

## Key Decisions

- Gate 2 改为 Claude Code interactive card，而不是 Terminal Skill GPS CLI。
- 交互能力来自 Claude Code `AskUserQuestion`；`csg-workflow` 不重复实现菜单 UI。
- `csg-workflow` 的核心价值是阶段判断、选项生成、状态更新和 Skill 交接。
- Gate 1 不推翻，但要去掉或降级明显为未来 CLI 服务的复杂度。
- 当前错误方向的 `csg start` / `csg package` requirements 不再作为实施依据。

---

## Dependencies / Assumptions

- Claude Code 环境提供 `AskUserQuestion` 工具，并能渲染上下箭头选择和回车确认。
- Codex 或其他工具可能没有同等 UI；这些环境可以继续使用 Markdown fallback。
- `csg-workflow` 仍以 Skill 形式运行，不需要变成 plugin 或 CLI。
- Gate 1 的现有 navigator 文档和 validator 可以保留，但需要按新方向精简措辞。

---

## Outstanding Questions

### Resolve Before Planning

- 无。当前需求足够进入实施计划。

### Deferred to Planning

- [Affects R1, R2, R13][Technical] 在 Claude Code Skill 中调用 `AskUserQuestion` 的具体提示结构和 fallback 行为。
- [Affects R6, R7, R8][Technical] 用户确认后 `state.md` 的最小更新字段和日志追加规则。
- [Affects R15, R16, R17][Content] Gate 1 文档中哪些未来 CLI 表述应删除，哪些只需降级成远期备注。
