---
title: AI 编程项目 Workflow：三套 Skill 的融合方案
date: 2026-05-06
status: ideation
source_skill: ce-ideate
language: zh-CN
---

# AI 编程项目 Workflow：三套 Skill 的融合方案

## 2026-05-06 补充修正

项目名称改为 `csg-workflow`。CSG 代表 Compound、Superpowers、Gstack。

上下文交接方案也做了收敛：不要把所有内容都塞进 `state.md`。更好的方式是分层：

- `AGENTS.md` / `CLAUDE.md`：只放所有 agent 必须先遵守的短规则。
- `docs/workflow/state.md`：只放当前状态和下一步。
- `docs/workflow/decisions.md`：放长期决定。
- `docs/workflow/log.md`：放阶段记录。
- 详细流程、Skill 选择表和说明放在 `csg-workflow` Skill 文档里。

这样新 session 能稳定恢复，又不会每次读取太多无关内容。

## 一句话结论

这个项目第一版应该做成一个 **workflow Skill**，而不是 plugin。

它的核心价值不是再造一堆新能力，而是把你已经安装的 gstack、superpowers、compound 里的 Skill 串成一条新手能跟着走的项目路线：

想法 → 需求 → 计划 → 审查计划 → 写代码 → 审查代码 → QA 验收 → PR / 交付 → 发布后检查 → 经验沉淀

第一版最重要的能力是两件事：

- 告诉用户“当前阶段该用哪个 Skill”
- 每个阶段结束后，把项目状态写进固定文件，避免 compact、clear 或开新对话之后上下文断掉

plugin 可以以后再做。只有当你需要按钮、面板、同步状态、连接外部服务、自动看板时，plugin 才有必要。

## 这个项目要解决什么问题

很多新手安装了很多插件和 Skill，但真正开始做项目时还是会卡住：

- 不知道项目从哪里开始
- 不知道每个 Skill 到底什么时候用
- 不知道哪些 Skill 是重复的
- 不知道什么时候该停止脑暴，进入计划
- 不知道计划写完后要不要审查
- 不知道代码写完后该用哪个 review
- 不知道网页项目什么时候做 QA
- 不知道 ship 之前还缺什么
- compact、clear 或开新对话后，项目目标丢了
- 新对话里的 AI 不知道前面做过什么
- 做过的错误没有沉淀，下个项目还会再犯

所以这个项目不应该只是一个“Skill 清单”。

它应该是一个“项目导航器”：用户只需要说自己现在在哪个阶段，它就能告诉用户下一步该做什么、该调用哪个 Skill、通过什么标准才能进入下一步、如果不合格要退回哪里。

## 我实际参考了哪些内容

本方案基于本地 Skill 内容梳理，不是只看名字猜的。

本地 Skill 目录：

- gstack：`/Users/kangjiaqi/.gstack/repos/gstack/.agents/skills/`
- compound：`/Users/kangjiaqi/.codex/skills/compound-engineering/`
- superpowers：`/Users/kangjiaqi/.codex/plugins/cache/openai-curated/superpowers/82fd64bc/skills/`

外部参考：

- [OpenAI Academy: Plugins and skills](https://openai.com/academy/codex-plugins-and-skills/)
- [Agent Skills specification](https://agentskills.io/specification)
- [Agent Skills overview](https://agentskills.io/home)

## 三套插件的整体判断

### Compound：最适合做项目主线

Compound 最像一条完整的软件项目流水线。

它覆盖的阶段比较完整：

- 想法探索：`ce-ideate`
- 需求梳理：`ce-brainstorm`
- 制定计划：`ce-plan`
- 写代码：`ce-work`
- 调试：`ce-debug`
- 文档 / 计划审查：`ce-doc-review`
- 代码审查：`ce-code-review`
- PR 描述和创建：`ce-pr-description`、`ce-commit-push-pr`
- 处理 PR 反馈：`ce-resolve-pr-feedback`
- 浏览器测试：`ce-test-browser`
- 经验沉淀：`ce-compound`、`ce-compound-refresh`
- 查找过去会话：`ce-sessions`、`ce-session-inventory`、`ce-session-extract`

它的强项：

- 有比较清楚的顺序：想法 → 需求 → 计划 → 执行 → 审查 → 沉淀
- 很重视文档产物，比如 brainstorm、plan、solution
- 适合把需求、计划、代码、测试结果连起来
- 审查能力比较强，不只是泛泛说“代码看起来可以”
- `ce-compound` 很适合做你说的“知识复利”

它的弱点：

- 对新手来说入口太多，不知道先用哪个
- 有些流程比较重，小项目可能感觉麻烦
- 有些 Skill 假设用户已经知道怎么组织项目
- 它自己没有把“三套插件如何融合”这件事讲清楚

在融合 workflow 里的定位：

Compound 应该当主线。

默认路径建议是：

`ce-ideate` → `ce-brainstorm` → `ce-plan` → `ce-work` → `ce-code-review` → `ce-compound`

### Superpowers：最适合当工作纪律

Superpowers 不像完整项目管理工具，它更像一套工作规矩。

它强调：

- 不要一上来就写代码，先想清楚：`brainstorming`
- 写计划再执行：`writing-plans`
- 按计划执行：`executing-plans`
- 需要隔离开发时用工作区：`using-git-worktrees`
- 能测试先测试：`test-driven-development`
- 调试不要乱猜，先找原因：`systematic-debugging`
- 做完之前先审查：`requesting-code-review`
- 收到 review 不要盲改：`receiving-code-review`
- 说完成前必须验证：`verification-before-completion`
- 收尾开发分支：`finishing-a-development-branch`
- 创建新 Skill：`writing-skills`

它的强项：

- 规则清楚，适合训练新手习惯
- 能防止几个常见问题：不做计划、跳过测试、没验证就说完成、调试靠猜、review 反馈照单全收
- 很适合放在关键节点当“检查线”

它的弱点：

- 单独使用时，不够像完整项目路线
- 对小项目可能显得过于严格
- 对 compact / clear 后的交接没有直接给出完整方案
- 计划格式可能太细，新手容易被吓住

在融合 workflow 里的定位：

Superpowers 不做主线，而是做“质量规则”。

也就是说：

- 进入写代码前，用它提醒必须先有计划
- 改行为逻辑时，用它提醒先测关键行为
- 调试时，用它提醒先找根因
- 结束前，用它提醒必须实际验证

### Gstack：最适合做评审、QA、发布和上下文恢复

Gstack 是三者里最像“交付工具箱”的一套。

它覆盖的范围很广：

- 早期产品拷问：`office-hours`
- 创始人 / CEO 视角审查：`plan-ceo-review`
- 工程计划审查：`plan-eng-review`
- 设计计划审查：`plan-design-review`
- 开发者体验审查：`plan-devex-review`
- 自动计划审查：`autoplan`
- 合并前代码审查：`review`
- 网页 QA 和修复：`qa`、`qa-only`
- 浏览器探索：`browse`
- 收尾发布：`ship`
- 合并、部署、验证：`land-and-deploy`
- 上线后观察：`canary`
- 发布后文档：`document-release`
- 上下文保存和恢复：`context-save`、`context-restore`
- 项目经验记录：`learn`
- 复盘：`retro`
- 安全边界：`guard`、`careful`、`freeze`、`unfreeze`

它的强项：

- 后半段非常强：QA、review、ship、deploy、canary、文档
- `context-save` 和 `context-restore` 对上下文断裂问题很有价值
- plan review 分得细，适合复杂项目
- 比较有“真实发布”的意识，不只是写完代码

它的弱点：

- Skill 太多，新手更容易不知道该选哪个
- 有些 Skill 很重，不适合小项目一开始就全用
- review 类 Skill 和 Compound 有重叠
- 如果没有统一入口，会变成“工具很多，但路线不清楚”

在融合 workflow 里的定位：

Gstack 适合做三件事：

- 早期拷问项目是否值得做
- 中后期做计划审查、QA、发布
- 在上下文快满或要开新对话时做保存和恢复

## 阶段能力对照表

| 阶段 | 默认推荐 | 可选替代 | 说明 |
|---|---|---|---|
| 想法探索 | `ce-ideate` | `office-hours`、`superpowers:brainstorming` | 不确定做什么时，先用 `ce-ideate`；想判断值不值得做时，用 `office-hours` |
| 需求梳理 | `ce-brainstorm` | `superpowers:brainstorming`、`office-hours` | `ce-brainstorm` 的结果更适合接到 `ce-plan` |
| 制定计划 | `ce-plan` | `superpowers:writing-plans` | `ce-plan` 更适合作为默认；Superpowers 更严格 |
| 审查计划 | `ce-doc-review` | `plan-eng-review`、`plan-ceo-review`、`plan-design-review`、`plan-devex-review`、`autoplan` | 默认用 Compound；复杂项目再加 Gstack 的专项 review |
| 写代码 | `ce-work` | `superpowers:executing-plans`、`subagent-driven-development` | 默认用 `ce-work`；复杂任务可引入更严格的执行规则 |
| 调试 | `ce-debug` | `systematic-debugging`、`investigate` | 默认用 `ce-debug`；Superpowers 的原则用于避免乱猜 |
| 代码审查 | `ce-code-review` | `gstack review`、`requesting-code-review` | 写完后先用 `ce-code-review`；合并前可再用 `gstack review` |
| PR 反馈 | `ce-resolve-pr-feedback` | `receiving-code-review`、GitHub 相关 Skill | 处理具体评论时，用 `ce-resolve-pr-feedback` |
| 浏览器 QA | `gstack qa` | `qa-only`、`ce-test-browser` | 网页项目优先用 `gstack qa`，因为它不只是看，还会修 |
| PR / 交付 | `ce-commit-push-pr` | `gstack ship`、`finishing-a-development-branch` | 普通 PR 用 Compound；正式发布用 Gstack |
| 发布后检查 | `land-and-deploy`、`canary`、`document-release` | `ce-demo-reel` | 主要是 Gstack 的强项 |
| 经验沉淀 | `ce-compound` | `learn`、`retro` | `ce-compound` 是主力；`learn` 和 `retro` 可补充 |
| 上下文交接 | 本项目自己的 `state.md` | `context-save`、`context-restore`、`ce-sessions` | 交接文件必须成为强制动作 |

## 推荐融合 workflow

### 阶段 0：项目入口判断

目标：

- 先判断这个项目是什么类型
- 不要一开始就乱调用 Skill
- 选出适合的小项目路线或复杂项目路线

这个阶段应该做什么：

- 写清楚项目目标
- 写清楚目标用户
- 写清楚第一版要交付什么
- 判断现在是“想法不清楚”还是“已经知道要做什么”

建议 Skill：

- 必选：这个 workflow Skill 自己
- 可选：`ce-ideate`
- 可选：`office-hours`

为什么：

- 如果用户连方向都不确定，直接 plan 没意义
- 如果用户已经知道要做什么，就不需要长时间脑暴
- `office-hours` 适合判断这个东西有没有价值

通过标准：

- 项目目标能用一句话说清楚
- 目标用户明确
- 第一版成果明确
- 下一阶段明确

如果不理想：

- 目标不清楚，回到 `ce-ideate`
- 价值不清楚，回到 `office-hours`
- 用户不清楚，重新做需求梳理

交接要保存：

- 当前项目一句话目标
- 目标用户
- 当前阶段
- 下一步要做什么

保存到：

- `docs/workflow/state.md`

### 阶段 1：想法探索

目标：

- 从多个可能方向里选出最值得做的方向
- 避免第一反应就开干

这个阶段应该做什么：

- 列出可能的项目方向
- 比较每个方向的价值和难度
- 选出一个主方向
- 明确哪些方向暂时不做

建议 Skill：

- 必选：如果方向不清楚，用 `ce-ideate`
- 可选：`office-hours`
- 可选：`superpowers:brainstorming`

为什么：

- `ce-ideate` 适合从多个方向里筛选
- `office-hours` 适合用更尖锐的问题判断想法是否站得住
- Superpowers 的 brainstorming 适合避免太早收敛

通过标准：

- 已选出一个主方向
- 能解释为什么选它
- 明确暂时不做哪些方向
- 知道下一步要写需求

如果不理想：

- 如果方向太散，继续 `ce-ideate`
- 如果价值不清楚，去 `office-hours`
- 如果想法太大，拆小第一版

交接要保存：

- 选中的方向
- 被放弃的方向
- 选择理由
- 第一版范围

### 阶段 2：需求梳理

目标：

- 把“想做什么”变成“第一版具体做什么”
- 让后面的计划能直接接上

这个阶段应该做什么：

- 写清楚用户是谁
- 写清楚用户要完成什么事
- 写清楚第一版必须有什么
- 写清楚暂时不做什么
- 写清楚验收标准

建议 Skill：

- 必选：`ce-brainstorm`
- 可选：`office-hours`
- 可选：`superpowers:brainstorming`

为什么：

- `ce-brainstorm` 适合把想法变成需求文档
- 需求文档能直接交给 `ce-plan`
- 这个阶段做清楚，后面才不会偏题

通过标准：

- 有一份需求文档
- 第一版范围明确
- 必做和不做都明确
- 有可检查的验收标准

如果不理想：

- 如果需求太散，回到想法探索
- 如果范围太大，缩小第一版
- 如果用户场景不清楚，继续需求梳理

交接要保存：

- 需求文档路径
- 第一版范围
- 不做清单
- 验收标准

### 阶段 3：制定计划

目标：

- 把需求变成可执行步骤
- 明确先做什么、后做什么
- 降低写代码时跑偏的概率

这个阶段应该做什么：

- 读需求文档
- 拆成阶段任务
- 标出风险点
- 标出需要验证的地方
- 写出完成顺序

建议 Skill：

- 必选：`ce-plan`
- 可选：`superpowers:writing-plans`

为什么：

- `ce-plan` 比较适合作为默认计划工具
- Superpowers 的计划更严格，适合复杂任务或高风险任务

通过标准：

- 有一份计划文档
- 每个任务都有明确目标
- 知道哪些文件或模块会被改
- 知道怎么验证
- 下一步能直接开始执行

如果不理想：

- 如果计划缺需求，回到需求梳理
- 如果计划太大，拆成更小版本
- 如果风险不清楚，进入计划审查

交接要保存：

- 计划文档路径
- 当前要执行的任务
- 风险点
- 验证方式

### 阶段 4：审查计划

目标：

- 在写代码前发现问题
- 避免做错方向、做太大、或漏掉关键风险

这个阶段应该做什么：

- 检查计划是否符合目标
- 检查范围是否过大
- 检查是否有安全、设计、体验、工程风险
- 确认计划是否能执行

建议 Skill：

- 小项目必选：可以跳过正式审查，但至少让 workflow 自己检查一次
- 中等项目推荐：`ce-doc-review`
- 产品方向风险大：`plan-ceo-review`
- 工程风险大：`plan-eng-review`
- 视觉和交互风险大：`plan-design-review`
- 面向开发者的工具：`plan-devex-review`
- 不确定该用哪个：`autoplan`

为什么：

- `ce-doc-review` 适合作为默认计划审查
- Gstack 的专项 review 适合复杂项目，从不同角度挑问题
- 计划阶段修问题比写完代码后返工便宜

通过标准：

- 计划没有明显目标偏差
- 第一版范围可控
- 关键风险都有处理方式
- 可以进入写代码阶段

如果不理想：

- 范围太大，回到制定计划
- 目标不对，回到需求梳理
- 想法本身不成立，回到想法探索

交接要保存：

- 审查结论
- 必须修改的问题
- 已接受的风险
- 修改后的计划路径

### 阶段 5：写代码

目标：

- 按计划完成第一版，不临时发散

这个阶段应该做什么：

- 先读计划和状态文件
- 只做当前阶段范围内的事
- 边做边验证
- 遇到 bug 先找原因，不乱改

建议 Skill：

- 必选：`ce-work`
- 可选：`superpowers:executing-plans`
- 可选：`superpowers:test-driven-development`
- 调试时：`ce-debug` 或 `superpowers:systematic-debugging`

为什么：

- `ce-work` 适合按计划执行
- Superpowers 适合提醒不要跳过测试和验证
- 调试时要先确认原因，再改代码

通过标准：

- 当前计划任务已完成
- 自己实际跑过或检查过
- 没有明显破坏原有功能
- 状态文件已更新

如果不理想：

- 如果实现发现计划有问题，回到制定计划
- 如果需求不清楚，回到需求梳理
- 如果 bug 找不到原因，进入调试流程

交接要保存：

- 完成了什么
- 改了哪些范围
- 怎么验证的
- 还剩什么

### 阶段 6：审查代码

目标：

- 在交付前找出明显 bug、遗漏和风险

这个阶段应该做什么：

- 对照计划检查代码
- 检查是否实现了需求
- 检查测试和验证是否足够
- 修复审查发现的问题

建议 Skill：

- 默认：`ce-code-review`
- 合并前再查：`gstack review`
- 接收 review 反馈时：`superpowers:receiving-code-review`

为什么：

- `ce-code-review` 适合做实现后的完整审查
- `gstack review` 适合作为合并前最后一道门
- Superpowers 能提醒不要盲目接受所有评论，要判断反馈是否真的成立

通过标准：

- 高风险问题已修
- 重要问题已修
- 剩余问题有明确说明
- 重新验证通过

如果不理想：

- 代码问题多，回到写代码
- 计划和代码不一致，回到计划
- 需求理解错了，回到需求梳理

交接要保存：

- 审查结果
- 修了哪些问题
- 哪些问题决定暂不处理
- 验证结果

### 阶段 7：QA / 浏览器验收

目标：

- 从用户视角确认项目真的能用
- 尤其适合网页、工具、交互页面

这个阶段应该做什么：

- 打开页面或运行项目
- 走一遍主要流程
- 检查移动端和桌面端
- 检查空状态、错误状态、加载状态
- 修掉看到的问题

建议 Skill：

- 网页项目默认：`gstack qa`
- 只想检查不想改：`qa-only`
- 轻量浏览器测试：`ce-test-browser`
- 手动探索：`browse`

为什么：

- 很多问题只有打开页面才看得出来
- `gstack qa` 比较适合边测边修
- `qa-only` 适合只要报告、不想自动修改时

通过标准：

- 主流程能跑通
- 页面没有明显错位
- 交互能正常工作
- 关键异常情况有处理
- 验收结果已写入状态文件

如果不理想：

- 页面问题多，回到写代码
- 需求不符合用户目标，回到需求梳理
- 计划漏掉关键流程，回到制定计划

交接要保存：

- 测了哪些页面
- 走了哪些流程
- 发现并修了什么
- 剩余风险

### 阶段 8：PR / 交付准备

目标：

- 把完成的工作整理成可以给别人看的交付物

这个阶段应该做什么：

- 整理变更说明
- 确认验证结果
- 创建 PR 或准备交付
- 写清楚使用方式和限制

建议 Skill：

- 普通 PR：`ce-commit-push-pr`
- 只写 PR 描述：`ce-pr-description`
- 完整收尾：`gstack ship`
- 分支收尾：`superpowers:finishing-a-development-branch`

为什么：

- Compound 适合正常 PR 路径
- Gstack 的 `ship` 更适合正式发布前的大检查
- Superpowers 适合确保完成前没有漏掉基本事项

通过标准：

- 变更说明清楚
- 验证结果清楚
- 交付物可访问
- 没有未解释的风险

如果不理想：

- 验证不完整，回到 QA
- 审查没做，回到代码审查
- 需求没满足，回到写代码或需求梳理

交接要保存：

- PR 地址或交付路径
- 变更摘要
- 验证结果
- 已知限制

### 阶段 9：发布、上线后检查

目标：

- 如果项目真的发布了，要确认发布后没有出问题

这个阶段应该做什么：

- 合并或发布
- 验证线上结果
- 观察错误和异常
- 更新文档

建议 Skill：

- 合并和部署：`land-and-deploy`
- 上线后观察：`canary`
- 发布后文档：`document-release`

为什么：

- 写完不等于发布成功
- 发布后要确认用户看到的是正确结果
- 文档要跟着更新，否则下次又会断上下文

通过标准：

- 发布完成
- 线上验证通过
- 没有明显异常
- 文档更新完成

如果不理想：

- 发布失败，回到发布准备或写代码
- 线上异常，进入调试流程
- 文档缺失，补文档

交接要保存：

- 发布结果
- 线上验证结果
- 发现的问题
- 文档更新记录

### 阶段 10：经验沉淀

目标：

- 把这次项目里踩过的坑变成以后能复用的经验

这个阶段应该做什么：

- 回顾本阶段哪里出过错
- 找出真实原因
- 写成以后能提醒 AI 的经验
- 更新状态文件

建议 Skill：

- 必选：`ce-compound`
- 可选：`learn`
- 可选：`retro`

为什么：

- `ce-compound` 是 Compound 最有价值的能力之一
- 它能从过去的 session 和错误里提炼经验
- 这正好解决你说的“知识复利”问题

通过标准：

- 有明确经验记录
- 经验能指导下次项目
- 状态文件更新为下一阶段或完成

如果不理想：

- 如果没有真实问题，就只记录完成摘要
- 如果问题没想清楚，继续复盘
- 如果项目还没完成，回到对应阶段

交接要保存：

- 本次经验
- 下次避免什么
- 下一步是否继续迭代

## 上下文交接机制

这是整个项目最关键的设计。

不能只靠聊天记录保存项目上下文。因为聊天会变长，会 compact，也可能 clear。

所以每个项目都必须有一个固定的状态文件：

`docs/workflow/state.md`

这个文件不是普通备忘录，而是“下一次对话的入口”。

新对话开始时，AI 应该先读它，再决定下一步做什么。

### 状态文件应该包含什么

建议固定包含这些内容：

```markdown
# Workflow State

## Current Stage
当前处于哪个阶段。

## Project Goal
项目一句话目标。

## Target User
目标用户是谁。

## Current Decision
当前已经确定的关键方向。

## Completed So Far
已经完成了什么。

## Active Artifact
当前最重要的文件或文档。

## Next Action
下一步应该做什么。

## Do Not Reopen Unless
哪些问题不要反复讨论，除非出现新证据。

## Important Decisions
已经做过的重要决定。

## Open Questions
还没解决的问题。

## Verification So Far
已经验证过什么。

## Lessons / Risks To Remember
要记住的风险和经验。
```

### 每个阶段结束时必须做什么

每个阶段结束时，都要更新：

- 当前阶段
- 已完成内容
- 下一步
- 当前主要文档
- 验证结果
- 不要重复讨论的决定

### compact / clear 之后怎么继续

新对话只需要这样开始：

> 先读 `docs/workflow/state.md`，然后按里面的 Next Action 继续。

如果要更稳，还可以再加：

> 不要重新设计已经完成的阶段，除非 state.md 里写着需要回退。

这样可以避免新对话又从头脑暴、重新 plan、重复推翻已经确认的方向。

### 什么时候用 gstack 的 context-save / context-restore

建议规则：

- 小项目：只用 `docs/workflow/state.md`
- 中等项目：每个大阶段结束后，同时用 `context-save`
- 复杂项目：新对话开始时用 `context-restore`，再读 `state.md`

这个项目自己的状态文件应该是主入口。Gstack 的 context 工具可以作为加强版，不应该替代状态文件。

## 新手小项目路线

新手不要一上来就把所有 Skill 用满。

推荐最短路线：

1. 项目入口判断
2. `ce-brainstorm`
3. `ce-plan`
4. `ce-work`
5. 实际验证
6. `ce-code-review`
7. 如果是网页，用 `gstack qa`
8. 更新 `state.md`
9. `ce-compound`

新手小项目里，可以暂时跳过：

- `plan-ceo-review`
- `plan-design-review`
- `plan-devex-review`
- `autoplan`
- `land-and-deploy`
- `canary`
- `retro`

除非项目已经变复杂，或者真的要公开发布。

新手最需要遵守的是：

- 不要没需求就 plan
- 不要没 plan 就写代码
- 不要没验证就说完成
- 不要 clear 后靠记忆继续
- 每阶段结束都更新 `state.md`

## 复杂项目路线

复杂项目建议完整一点：

1. `ce-ideate`
2. `office-hours`
3. `ce-brainstorm`
4. `ce-plan`
5. `ce-doc-review`
6. 根据风险追加：
   - 产品风险：`plan-ceo-review`
   - 工程风险：`plan-eng-review`
   - 设计风险：`plan-design-review`
   - 开发者体验风险：`plan-devex-review`
7. `ce-work`
8. 行为变更时用 `test-driven-development`
9. 遇到 bug 用 `ce-debug` 或 `systematic-debugging`
10. `ce-code-review`
11. `gstack review`
12. 网页项目用 `gstack qa`
13. `ce-commit-push-pr`
14. 需要发布时用 `gstack ship`
15. 发布后用 `land-and-deploy`、`canary`、`document-release`
16. 最后用 `ce-compound`、`learn`、`retro`

复杂项目还应该强制：

- 每个阶段结束更新 `state.md`
- 上下文快满前做 `context-save`
- 新对话开始做 `context-restore`
- 所有重要决定写进文档，不只留在聊天里

## 必选、可选和复杂项目专用 Skill

### 第一版 workflow 必选

这些应该是默认主线：

- `ce-brainstorm`
- `ce-plan`
- `ce-work`
- `ce-code-review`
- `ce-compound`
- `docs/workflow/state.md`

如果用户还没有方向，再加：

- `ce-ideate`

如果是网页项目，再加：

- `gstack qa`

### 推荐可选

这些适合根据情况使用：

- `office-hours`
- `ce-doc-review`
- `ce-debug`
- `ce-test-browser`
- `ce-pr-description`
- `ce-commit-push-pr`
- `context-save`
- `context-restore`

### 复杂项目再用

这些不要默认塞给新手：

- `plan-ceo-review`
- `plan-eng-review`
- `plan-design-review`
- `plan-devex-review`
- `autoplan`
- `subagent-driven-development`
- `using-git-worktrees`
- `land-and-deploy`
- `canary`
- `document-release`
- `retro`

## 重复 Skill 怎么选

### 脑暴类重复

可选项：

- `ce-ideate`
- `ce-brainstorm`
- `superpowers:brainstorming`
- `office-hours`

选择规则：

- 不知道做什么：用 `ce-ideate`
- 已经有方向，要变成需求：用 `ce-brainstorm`
- 想法可能不值得做：用 `office-hours`
- 想避免太快收敛：用 `superpowers:brainstorming`

### 计划类重复

可选项：

- `ce-plan`
- `superpowers:writing-plans`
- `autoplan`

选择规则：

- 默认用 `ce-plan`
- 想要非常细的执行步骤，用 `superpowers:writing-plans`
- 不知道该找哪些角度审查计划，用 `autoplan`

### 代码审查类重复

可选项：

- `ce-code-review`
- `gstack review`
- `requesting-code-review`

选择规则：

- 写完代码后默认用 `ce-code-review`
- 合并前或发布前用 `gstack review`
- 想强化“完成前必须审查”的习惯，用 `requesting-code-review`

### QA 类重复

可选项：

- `gstack qa`
- `qa-only`
- `ce-test-browser`
- `browse`

选择规则：

- 网页项目默认用 `gstack qa`
- 只想要报告，不想自动修，用 `qa-only`
- 轻量检查用 `ce-test-browser`
- 人工探索页面用 `browse`

### 经验沉淀类重复

可选项：

- `ce-compound`
- `learn`
- `retro`

选择规则：

- 想沉淀可复用经验，用 `ce-compound`
- 想记录项目内学习，用 `learn`
- 想做阶段复盘，用 `retro`

## 为什么第一版应该做成 Skill

第一版做成 Skill 的理由：

- 你的核心问题是“怎么做项目”，不是“缺一个工具按钮”
- Skill 更轻，适合开源给新手安装
- Skill 能直接规定流程、交接文件和阶段标准
- Skill 更容易和现有 gstack、superpowers、compound 配合
- 初期不需要维护复杂界面和额外服务

第一版 Skill 应该做什么：

- 识别用户当前项目阶段
- 推荐下一步 Skill
- 提醒用户更新 `state.md`
- 告诉用户当前阶段的通过标准
- 告诉用户如果结果不好应该回退到哪里
- 给新手小项目和复杂项目两条路线

### 什么时候再做 plugin

当你需要这些能力时，再考虑 plugin：

- 可视化项目阶段面板
- 自动读取所有 Skill 并生成路线
- 自动检查 `state.md` 是否过期
- 自动生成阶段报告
- 多项目管理
- 和 GitHub、Slack、Notion、Linear 等工具打通
- 团队共享 workflow 状态

所以建议路线是：

V1：Skill  
V2：Skill 加少量辅助脚本  
V3：如果真的需要界面和连接能力，再做 plugin

## 建议项目结构

建议这个开源项目以后长这样：

```text
ai-project-workflow/
  README.md
  skills/
    ai-project-workflow/
      SKILL.md
      templates/
        state.md
        intake.md
        stage-report.md
        handoff.md
      references/
        skill-selection-matrix.md
        beginner-path.md
        complex-path.md
        plugin-comparison.md
  examples/
    small-web-app/
      docs/workflow/state.md
    cli-tool/
      docs/workflow/state.md
  docs/
    design/
      project-workflow.zh.md
      project-workflow.en.md
```

第一版最重要的是 `SKILL.md` 和 `templates/state.md`。

不需要一开始就做复杂结构。

## 最值得做的 5 个产品点

### 1. Workflow Router Skill

这是最核心的东西。

它负责问：

- 你现在是在想法阶段、计划阶段、写代码阶段，还是验收阶段？
- 你有没有需求文档？
- 你有没有计划文档？
- 你有没有验证过？
- 你是不是刚 compact / clear？

然后它告诉用户下一步该用哪个 Skill。

### 2. Project State Contract

也就是 `docs/workflow/state.md`。

它解决上下文断裂。

每个阶段结束都必须更新它。

新对话必须先读它。

### 3. Beginner / Advanced Lanes

同一套 workflow 应该有两条路线：

- 新手小项目路线：少而稳
- 复杂项目路线：完整审查、QA、发布、复盘

这样不会让新手被一堆 Skill 吓住，也不会限制高级用户。

### 4. Stage Exit Gates

每个阶段都要有“通过标准”。

例如：

- 需求阶段：第一版范围明确
- 计划阶段：知道怎么验证
- 写代码阶段：实际跑过
- QA 阶段：主流程走通
- ship 阶段：交付说明清楚

没有通过标准，就不要进入下一阶段。

### 5. Skill Selection Matrix

也就是“Skill 选择表”。

它解决新手最常见的问题：

> 这些 Skill 都看起来有用，我到底该用哪个？

这个表应该清楚告诉用户：

- 当前阶段默认用哪个
- 什么情况下换另一个
- 哪些是小项目可以跳过的
- 哪些是复杂项目才需要的

## 不建议做的方向

### 不建议第一版就做 plugin

plugin 会让项目一开始变重。

你现在最需要的是路线清楚，而不是界面复杂。

### 不建议做一个超大万能 Skill

不要重新实现 gstack、superpowers、compound 的所有能力。

这个项目应该做“导航器”，不是做“替代品”。

### 不建议只选一个插件

三个插件各有强项：

- Compound 适合主线
- Superpowers 适合工作纪律
- Gstack 适合评审、QA、发布和上下文恢复

只用一个会浪费已有能力。

### 不建议默认用 `autoplan`

`autoplan` 适合复杂计划审查，但不适合作为新手默认入口。

新手更需要清楚路线，而不是一开始就进入重型审查。

## 推荐下一步

下一步不是马上写代码。

建议先用 `ce-brainstorm`，把这份设计收敛成正式需求文档。

目标是明确：

- 第一版 Skill 叫什么
- 它解决哪个最小问题
- 它要问用户哪些问题
- 它要生成哪些文件
- 它什么时候推荐哪个 Skill
- 它如何强制更新 `state.md`
- 新手路径和复杂路径如何呈现

完成 `ce-brainstorm` 后，再进入 `ce-plan`。

## 当前版本的最终判断

这套 workflow 的最优形态是：

第一层：一个新手能直接用的 Skill  
第二层：固定的项目状态文件  
第三层：按阶段调用已有 gstack、superpowers、compound Skill  
第四层：阶段结束后沉淀经验  
第五层：未来需要时再升级成 plugin

也就是说，这个项目的真正价值不是“发明新的开发方法”，而是把已有好工具串成一条不会断、不会乱、适合新手跟着走的路线。
