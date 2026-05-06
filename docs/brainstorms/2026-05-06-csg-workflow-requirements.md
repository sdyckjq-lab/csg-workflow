---
date: 2026-05-06
topic: csg-workflow-skill
language: zh-CN
source: docs/ideation/2026-05-06-ai-project-workflow.zh.md
---

# CSG Workflow Skill 需求文档

## Problem Frame

新手用户安装了 Compound、Superpowers、Gstack 等插件后，虽然拥有很多有用 Skill，但仍然不知道项目应该从哪里开始、每个阶段该调用哪个 Skill、哪些 Skill 是重复的、什么时候可以进入下一阶段，以及 compact、clear 或新开对话后该如何继续。

第一版要做的是一个名为 `csg-workflow` 的 workflow Skill。CSG 代表 Compound、Superpowers、Gstack。它不替代三套插件，而是把它们串成一条清晰、可执行、可恢复的项目路线。

它要帮助用户从想法走到需求、计划、实现、审查、QA、交付和经验沉淀，并通过轻量项目规则和分层状态文件，让后续对话能接得上。

---

## Actors

- A1. 新手用户：想从 0 到 1 做项目，但不熟悉各插件 Skill 的适用时机。
- A2. 熟练用户：知道部分 Skill，但希望有一套稳定路线减少选择成本。
- A3. `csg-workflow` Skill：负责识别阶段、推荐下一步、维护交接状态、提示通过标准。
- A4. 被编排的已有 Skill：Compound、Superpowers、Gstack 中被推荐或调用的能力。
- A5. 后续对话中的 AI：在 compact、clear 或新会话后，通过项目规则和状态文件恢复上下文。
- A6. 项目规则文件：`AGENTS.md` 和 `CLAUDE.md`，通常由 Codex 或 Claude Code 的 `/init` 创建，负责放置项目级规则。

---

## Key Flows

- F1. 新项目启动
  - **Trigger:** 用户在空项目或新项目里说想从 0 到 1 开始。
  - **Actors:** A1, A3, A6
  - **Steps:** Skill 先判断用户是否已有明确方向；如果没有方向，推荐想法探索；如果方向明确，进入需求梳理；同时创建或更新轻量项目状态。
  - **Outcome:** 用户知道当前阶段、下一步要做什么、该用哪个 Skill。
  - **Covered by:** R1, R2, R3, R6, R18, R20, R27

- F2. 阶段推进
  - **Trigger:** 用户完成了某个阶段，例如需求、计划、写代码或 QA。
  - **Actors:** A1, A3, A4
  - **Steps:** Skill 检查该阶段是否达到通过标准；如果通过，推荐下一阶段；如果不通过，指出应该回退到哪个阶段；最后更新状态文件或阶段记录。
  - **Outcome:** 项目按稳定路线推进，不靠用户记忆判断下一步。
  - **Covered by:** R9, R10, R11, R20, R23, R26

- F3. 上下文恢复
  - **Trigger:** 用户 compact、clear 或新开对话后继续项目。
  - **Actors:** A1, A3, A5, A6
  - **Steps:** 新对话先遵守 `AGENTS.md` 或 `CLAUDE.md` 的启动规则，再读取 `docs/workflow/state.md`，确认项目目标、当前文档、下一步行动和不要重复讨论的决定；然后按状态继续，而不是重新脑暴。
  - **Outcome:** 项目目标不丢，后续任务不会偏离前面已确认的方向。
  - **Covered by:** R18, R19, R20, R21, R22, R27, R30, R31, R32

- F4. 选择路线深度
  - **Trigger:** 用户项目规模不同，可能是小项目，也可能是正式开源项目或复杂产品。
  - **Actors:** A1, A2, A3
  - **Steps:** Skill 根据项目复杂度选择“新手小项目路线”或“复杂项目路线”；小项目减少审查和发布环节；复杂项目加入计划审查、QA、发布后检查和复盘。
  - **Outcome:** 新手不会被过多步骤吓住，复杂项目也不会缺少必要检查。
  - **Covered by:** R7, R14, R25

- F5. 经验沉淀
  - **Trigger:** 阶段结束、项目交付、或出现值得记住的错误。
  - **Actors:** A1, A3, A4
  - **Steps:** Skill 提醒用户使用 `ce-compound` 或相关经验记录能力，把错误、判断和经验沉淀下来；状态文件记录本次沉淀结果。
  - **Outcome:** 项目经验可复用，后续项目减少重复踩坑。
  - **Covered by:** R24, R26

---

## Visual Overview

```mermaid
flowchart LR
    A["AGENTS.md / CLAUDE.md 启动规则"] --> B["读取 state.md"]
    B --> C["判断当前阶段"]
    C --> D["推荐下一步 Skill"]
    D --> E["执行当前阶段"]
    E --> F["验证结果"]
    F --> G["更新 state.md"]
    G --> H["必要时写入 decisions.md / log.md"]
    H --> I["下一阶段或新对话继续"]
```

---

## Requirements

**第一版开源楔子**

- R1. 第一版必须收窄为“路由 + 交接 + 模板 + 示例”，不做完整全流程自动化。
- R2. 第一版必须能让用户从一个新项目或已有项目开始，判断当前阶段、推荐下一步 Skill，并创建或更新必要交接文件。
- R3. 第一版必须提供一个最小可跑通示例：从空项目启动，生成状态文件，进入需求或计划阶段。
- R4. 第一版必须明确哪些能力只是路线图中的阶段推荐，不属于第一版自动化范围。
- R5. 第一版必须包含开源发布基础内容：安装方式、依赖说明、兼容说明、许可证、最小示例、README 第一屏说明。

**阶段识别与路线引导**

- R6. Skill 必须能判断用户当前处于哪个项目阶段：入口判断、想法探索、需求梳理、制定计划、审查计划、写代码、代码审查、QA 验收、PR / 交付、发布后检查、经验沉淀。
- R7. Skill 必须提供两条路线：新手小项目路线和复杂项目路线，并能说明当前为什么适合其中一条。
- R8. Skill 必须在每个阶段给出默认推荐 Skill、可选 Skill，以及不建议当前使用的 Skill。
- R9. Skill 必须用简单语言解释“为什么这个阶段该用这个 Skill”，不能只列名字。
- R10. Skill 必须为每个阶段提供通过标准；未达到标准时，必须说明应该回退到哪个阶段。
- R11. Skill 必须把完整项目路线固定为：想法 → 需求 → 计划 → 审查计划 → 写代码 → 审查代码 → QA 验收 → PR / 交付 → 发布后检查 → 经验沉淀；小项目可以跳过部分复杂环节，但不能跳过状态交接和完成前验证。

**Skill 选择与重复处理**

- R12. Skill 必须明确 Compound、Superpowers、Gstack 的定位：Compound 做主线，Superpowers 做工作纪律，Gstack 做评审、QA、发布和上下文恢复。
- R13. Skill 必须提供重复 Skill 的选择规则，例如脑暴类、计划类、代码审查类、QA 类、经验沉淀类分别怎么选。
- R14. Skill 必须把 Skill 分成三类：必选、按情况可选、复杂项目再用。
- R15. Skill 不应默认自动执行所有下一步 Skill；第一版应先推荐下一步，并在用户确认后再进入对应 Skill。
- R16. 如果用户缺少某个推荐 Skill，`csg-workflow` 必须说明缺少什么，并给出手动替代步骤，不能让流程直接中断。
- R17. 第一版不能自动安装 Compound、Superpowers、Gstack，只能说明依赖和安装建议。

**上下文交接**

- R18. Skill 必须在项目内使用 `docs/workflow/state.md` 作为恢复入口，但不能把所有历史、规则、长说明都塞进这个文件。
- R19. `state.md` 必须保持短小，只记录当前阶段、项目目标、当前主要文档、下一步行动、阻塞问题、最近验证结果、不要重复讨论的事项。
- R20. 每个阶段结束时，Skill 必须提醒并更新 `state.md`；如果状态文件缺失或明显过期，不能直接推进到下一阶段。
- R21. 新对话继续项目时，Skill 必须先读取项目规则文件和 `state.md`，再决定下一步；除非状态文件明确要求回退，否则不能重新设计已完成阶段。
- R22. 长期决定必须写入 `docs/workflow/decisions.md`，阶段过程记录必须写入 `docs/workflow/log.md`；`state.md` 只保留“现在该怎么继续”。

**验证与交付**

- R23. Skill 必须要求每个阶段有实际验证记录；写代码、QA、交付阶段尤其不能只凭描述判断完成。
- R24. Skill 必须在项目阶段结束或交付后推荐经验沉淀，默认优先使用 `ce-compound`。
- R25. Skill 的输出必须面向新手，解释要直白，避免把用户带进过多工具细节；高级路径可以单独展开。
- R26. Skill 必须能生成或维护阶段报告，让后续 `ce-plan`、`ce-work`、`ce-code-review` 等 Skill 能接上，不需要重新猜测产品目标。

**项目规则文件**

- R27. Skill 必须提供轻量 `AGENTS.md` 和 `CLAUDE.md` 模板，让 Codex、Claude Code 等 agent 在新 session 或新任务里都能先读到强制规则。
- R28. `AGENTS.md` 和 `CLAUDE.md` 只能放少量硬规则：先读状态文件、按状态继续、阶段结束更新状态、不要重复推翻已确认决定、详细流程去读 Skill 文档。
- R29. `AGENTS.md` 和 `CLAUDE.md` 不能放完整 workflow、长 Skill 选择表、长解释或历史记录，避免每次启动浪费上下文。
- R30. Skill 不能覆盖用户已有的 `AGENTS.md` 或 `CLAUDE.md`。如果文件已经存在，只能追加或更新 `csg-workflow` 自己管理的短规则块。
- R31. `csg-workflow` 规则块必须带明确的开始和结束标记，重复运行时只能替换这两个标记之间的内容，不能改动其他内容。
- R32. 如果已有项目规则和 `csg-workflow` 规则冲突，默认以已有项目规则为准，除非用户明确要求修改原规则。
- R33. 如果缺少 `AGENTS.md` 或 `CLAUDE.md`，Skill 应优先建议用户用 Codex 或 Claude Code 的 `/init` 创建，再追加 `csg-workflow` 规则块；只有用户确认后，才可以创建最小文件。
- R34. `AGENTS.md` 和 `CLAUDE.md` 的规则块可以内容相近，但必须分别面向 Codex 和 Claude Code，不假设两个工具读取同一个文件。

---

## Acceptance Examples

- AE1. **Covers R6, R8, R9, R15.** 给定用户只有一个模糊项目想法，当用户启动 `csg-workflow`，Skill 应判断这是想法或需求阶段，并推荐先走 `ce-ideate` 或 `ce-brainstorm`，同时说明为什么不应该直接写代码。

- AE2. **Covers R10, R11, R20, R23.** 给定用户说“代码写完了”，但没有提供运行或检查结果，当 Skill 判断阶段是否完成时，必须要求补充验证，而不是直接进入交付阶段。

- AE3. **Covers R12, R13, R14, R16.** 给定用户不知道代码审查该用 `ce-code-review`、`gstack review` 还是 Superpowers 的 review，Skill 应说明默认先用 `ce-code-review`，合并或发布前再用 `gstack review`，Superpowers 主要用于强化完成前审查习惯。

- AE4. **Covers R18, R19, R20, R21, R27.** 给定用户 clear 后新开对话继续项目，当 Skill 启动时，应先读取项目规则文件和 `docs/workflow/state.md`，根据其中的下一步继续，而不是重新讨论项目是否应该做成 Skill。

- AE5. **Covers R7, R14, R25.** 给定用户做一个很小的个人脚本，Skill 应推荐新手小项目路线，只保留需求、计划、执行、验证、审查和状态更新，不默认加入发布、canary、复杂 plan review。

- AE6. **Covers R24, R26.** 给定项目完成了一个阶段并发现过错误，Skill 应提醒用 `ce-compound` 沉淀经验，并把沉淀结果写回状态文件或阶段记录，供后续阶段参考。

- AE7. **Covers R27, R28, R29, R30, R31, R32.** 给定项目已有 `AGENTS.md` 和 `CLAUDE.md`，Skill 只能追加或更新带标记的 `csg-workflow` 短规则块，不能把完整说明书写进去，也不能覆盖用户已有规则。

- AE8. **Covers R33, R34.** 给定项目没有 `AGENTS.md`，但用户正在 Codex 中工作，Skill 应建议用户先用 Codex 的 `/init` 创建规则文件，或在用户确认后创建最小 `AGENTS.md`，不能静默创建长规则文件。

- AE9. **Covers R1, R4, R16, R17.** 给定用户缺少 Gstack，但已经安装 Compound，Skill 应继续给出 Compound 主线步骤，并说明 Gstack 相关 QA / ship 能力需要用户安装后才可使用。

- AE10. **Covers R3, R5.** 给定陌生用户第一次打开 GitHub 仓库，README 第一屏应解释 CSG 的含义、适用对象、安装方式、最小示例和第一版边界。

---

## Success Criteria

- 新手用户能根据 Skill 的引导知道自己当前在哪个阶段、下一步该做什么、该用哪个 Skill。
- 用户在 compact、clear 或新开对话后，能通过项目规则文件和 `docs/workflow/state.md` 顺利继续，不需要重新解释整个项目。
- 需求、计划、实现、审查、QA、交付之间能顺畅衔接，后续 Skill 不需要重新发明项目目标和范围。
- 小项目不会被复杂流程拖慢，复杂项目也不会漏掉计划审查、QA、发布和经验沉淀。
- 第一版交付后，用户可以把它整理成开源 Skill，分享给其他新手安装使用。
- 开源仓库的 README 能让陌生用户在 3 分钟内看懂：这不是替代三套插件，而是把三套插件串成稳定项目路线。

---

## Scope Boundaries

### Deferred for later

- 自动扫描用户本机所有已安装 Skill，并动态生成完整能力图谱。
- 提供可视化项目阶段面板。
- 自动检测状态文件是否过期并主动提醒。
- 自动创建 GitHub PR、同步 Notion、同步 Linear 或 Slack。
- 多项目管理和团队共享状态。
- 把 workflow 升级成 plugin。
- 为每个 Skill 写完整教程或案例库。
- 自动安装 Compound、Superpowers、Gstack。

### Outside this product's identity

- 不做 Compound、Superpowers、Gstack 的替代品。
- 不重新实现已有 Skill 的完整能力。
- 不把所有项目都强制套进同一套重流程。
- 不做纯项目管理工具或任务看板。
- 不做只给高级用户看的复杂方法论文。
- 不把 `AGENTS.md` 或 `CLAUDE.md` 变成大型说明书。
- 不接管用户已有项目规则的所有权。
- 不自动重写 `/init` 已经生成的规则文件。

---

## Key Decisions

- 第一版名称改为 `csg-workflow`：CSG 分别代表 Compound、Superpowers、Gstack，能直接表达项目来源。
- 第一版形态选择 Skill，不选择 plugin：当前核心问题是流程和交接，不是界面和外部连接。
- Compound 作为默认主线：它覆盖从想法、需求、计划、执行、审查到经验沉淀的完整路径。
- Superpowers 作为工作纪律：它最适合防止跳过计划、测试、调试原则和完成前验证。
- Gstack 用于评审、QA、发布和上下文恢复：它在项目后半段和交付阶段最强。
- 第一版默认“推荐并引导”，不默认自动连续调用所有 Skill：这样更适合新手，也更容易控制范围。
- 上下文方案采用分层设计：`AGENTS.md` / `CLAUDE.md` 放硬规则，`state.md` 放当前状态，`decisions.md` 放长期决定，`log.md` 放阶段记录。
- `AGENTS.md` / `CLAUDE.md` 采用“追加标记块”策略，不覆盖用户已有规则；已有项目规则默认优先。

---

## Dependencies / Assumptions

- 用户已经安装或可访问 Compound、Superpowers、Gstack 中的相关 Skill。
- 第一版主要面向 Codex、Claude Code 等 agent 编程环境。
- Codex 项目通常使用 `AGENTS.md`；Claude Code 项目通常使用 `CLAUDE.md`；两者通常由各自的 `/init` 创建。
- 本项目当前是从空文件夹开始，第一版重点是先产出可用 Skill，而不是完整插件生态。
- 状态文件和阶段记录必须随项目一起保存，不能只存在聊天记录里。
- 未来开源时，文档应优先保证中文用户能读懂，再补充英文版本。

---

## Outstanding Questions

### Resolve Before Planning

- 无。当前需求已经足够进入计划阶段。

### Deferred to Planning

- [Affects R18, R19, R22][Technical] `state.md`、`decisions.md`、`log.md` 的具体模板字段和更新规则。
- [Affects R8, R12, R13, R14][Technical] Skill 选择规则是写在主 `SKILL.md`，还是拆到单独参考文件。
- [Affects R15][Technical] 用户确认后如何把上下文传给下一个 Skill。
- [Affects R27, R28, R29, R30, R31, R32, R33, R34][Content] `AGENTS.md` 和 `CLAUDE.md` 的最短追加规则块模板。
- [Affects R5, R25][Content] 中文主文档和英文开源文档如何保持一致。

---

## Next Steps

-> /ce-plan for structured implementation planning.
