---
date: 2026-05-06
topic: csg-workflow-open-source-review
mode: Builder
status: APPROVED_WITH_CHANGES
source: docs/brainstorms/2026-05-06-csg-workflow-requirements.md
---

# CSG Workflow 开源落地评估

## 结论

`csg-workflow` 适合落地，也适合开源到 GitHub。

但它不能包装成“万能 AI 编程工作流”。那会太大，也不可信。更好的定位是：

> 一个面向 Codex / Claude Code 用户的轻量 workflow Skill，用来把 Compound、Superpowers、Gstack 串成稳定项目路线，并解决 compact、clear、新对话后的交接问题。

这个定位够窄，问题真实，开源用户也容易理解。

---

## Premises

1. 用户真实痛点不是“缺更多 Skill”，而是“Skill 太多，不知道怎么串起来”。
2. 真正阻塞项目连续性的不是计划写得不够长，而是阶段交接没有固定入口。
3. `state.md` 单文件可行，但不能无限膨胀。它应该是当前状态面板，不是项目数据库。
4. `AGENTS.md` 和 `CLAUDE.md` 是更强的启动入口，因为新 session 和新任务都会先读这些规则。
5. 这两个规则文件必须短。把完整 workflow 塞进去会浪费上下文，也会让用户不敢安装。
6. 这两个规则文件很可能已经存在，所以 `csg-workflow` 不能覆盖它们，只能追加或更新自己管理的小规则块。

这些前提成立，所以项目值得继续。

---

## Approaches Considered

### Approach A: 只改名，加一个 `state.md`

Summary: 把项目改名为 `csg-workflow`，仍然只依赖一个 `docs/workflow/state.md` 做上下文恢复。

Effort: S  
Risk: Medium

Pros:

- 改动最少，最快能进入实现。
- 新手容易理解，只有一个状态文件。
- 第一版很轻，不需要解释太多文件。

Cons:

- `state.md` 很快会变长，最后变成新的上下文垃圾桶。
- 长期决定、阶段记录、当前状态混在一起，新对话仍然可能读偏。
- 开源后不同用户会按自己的方式乱写，格式容易失控。

### Approach B: `csg-workflow` + 轻量规则文件 + 分层状态文件

Summary: 用 `AGENTS.md` / `CLAUDE.md` 放少量强制启动规则；用 `state.md` 放当前状态；用 `decisions.md` 放长期决定；用 `log.md` 放阶段记录。

Effort: M  
Risk: Low

Pros:

- 新 session 一开始就能知道先读哪里，解决恢复入口问题。
- `state.md` 保持短小，不会变成越来越长的历史文档。
- 开源后更容易解释：规则文件是入口，workflow 文档是说明，状态文件是当前进度。

Cons:

- 比单文件多两个文档，新手需要理解“状态”和“记录”的区别。
- 需要模板写得非常清楚，否则用户会把所有内容继续塞进 `state.md`。
- 计划阶段要明确每个文件什么时候更新。

### Approach C: 直接做 plugin 或可视化面板

Summary: 做成 plugin，提供界面、自动扫描 Skill、自动状态更新和项目看板。

Effort: XL  
Risk: High

Pros:

- 体验上更完整，更像产品。
- 后续可以支持多项目、多团队和自动检查。
- 如果用户量起来，plugin 形态更有扩展空间。

Cons:

- 第一版太重，会拖慢落地。
- 还没有真实用户反馈，不知道哪些自动化值得做。
- 容易从“解决新手流程问题”跑偏成“做一个项目管理系统”。

## Recommendation

选择 Approach B。

它比 A 稳，比 C 轻。最重要的是，它直接解决这个项目的核心痛点：新 session 怎么继续，下一阶段怎么接上，哪些决定不要反复推翻。

---

## Open Source Readiness

方向适合开源，但还不是今天就能发布。

发布到 GitHub 前至少需要：

- 一个能安装的 Skill 目录。
- 清楚的 README：说明 CSG 是 Compound、Superpowers、Gstack。
- 最小使用示例：从空项目启动，完成一次需求到计划的交接。
- `AGENTS.md` 和 `CLAUDE.md` 的短模板。
- `state.md`、`decisions.md`、`log.md` 的模板。
- 许可证。
- 兼容说明：依赖哪些外部 Skill，缺少某个插件时如何降级。

开源卖点应该是：

- 新手知道每一步该用哪个 Skill。
- compact、clear、新对话后不丢项目目标。
- 不替代三套插件，只负责把它们串起来。
- 规则文件很短，不浪费上下文。

---

## Better State Design

推荐状态方案：

```text
AGENTS.md / CLAUDE.md
  只放所有 agent 必须先读的短规则。

docs/workflow/state.md
  当前状态面板。只写现在在哪、下一步做什么、当前主要文档、是否阻塞。

docs/workflow/decisions.md
  长期决定。比如“第一版做 Skill，不做 plugin”。

docs/workflow/log.md
  阶段记录。每次完成阶段追加一条，不覆盖。

docs/brainstorms/、docs/plans/、docs/reviews/
  真正的详细产物。
```

`state.md` 的原则：

- 保持短。
- 经常更新。
- 只回答“现在怎么继续”。
- 不存完整历史。
- 不存长规则。

`AGENTS.md` / `CLAUDE.md` 的原则：

- 只放强制启动规则。
- 不放完整 Skill 路线表。
- 不放三套插件分析。
- 不放项目历史。
- 只指向 `docs/workflow/state.md` 和 `csg-workflow`。
- 已有文件不能覆盖，只能追加带标记的小规则块。
- 如果规则冲突，默认项目原规则优先。

推荐追加块格式：

```markdown
<!-- BEGIN CSG-WORKFLOW RULES -->
## CSG Workflow

本段由 `csg-workflow` 建议添加，只负责项目阶段交接。它不替代本文件里已有的项目规则。

如果本段和本文件其他规则冲突，优先遵守本文件其他项目规则，除非用户明确要求修改。

- 非简单任务开始前，先读 `docs/workflow/state.md`。
- 默认按 `state.md` 的下一步继续，除非用户明确改方向。
- 阶段结束后，更新 `docs/workflow/state.md`。
<!-- END CSG-WORKFLOW RULES -->
```

---

## Assignment

下一步进入 `ce-plan`。

计划阶段要优先定这四件事：

1. `csg-workflow` Skill 的目录结构。
2. `AGENTS.md` 和 `CLAUDE.md` 的最短追加规则块。
3. `state.md`、`decisions.md`、`log.md` 的模板和更新规则。
4. README 如何让陌生人 3 分钟内看懂并愿意试用。
