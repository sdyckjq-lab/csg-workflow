---
title: AI Project Workflow From Skills
date: 2026-05-06
status: ideation
source_skill: ce-ideate
---

# AI Project Workflow From Skills

## One-Line Direction

Build this project first as a **workflow Skill**, not as a plugin. The first version should be a clear router and handoff system that tells a beginner what to do next, what to save before moving on, and which existing Skill to call at each stage. A plugin can come later if the project needs tools, UI, sync, analytics, or packaged connectors.

## What This Project Is Solving

Beginners install many useful Skills but still do not know:

- Where a project should start
- Which Skill belongs to which stage
- Which Skills overlap
- When to stop brainstorming and start planning
- When to run reviews
- How to recover after compacting or clearing context
- How to pass clean context from one conversation to the next
- How to turn repeated mistakes into future guidance

The core product should therefore be a **guided project workflow** with durable handoff files, not another large collection of unrelated Skills.

## Sources Read

Local Skill content was read from:

- `gstack`: `/Users/kangjiaqi/.gstack/repos/gstack/.agents/skills/`
- `compound`: `/Users/kangjiaqi/.codex/skills/compound-engineering/`
- `superpowers`: `/Users/kangjiaqi/.codex/plugins/cache/openai-curated/superpowers/82fd64bc/skills/`

External references used:

- [OpenAI Academy: Plugins and skills](https://openai.com/academy/codex-plugins-and-skills/)
- [Agent Skills specification](https://agentskills.io/specification)
- [Agent Skills overview](https://agentskills.io/home)

## Plugin-Level Analysis

### Compound

Compound is the strongest backbone for an end-to-end software project workflow.

What it covers well:

- Idea discovery: `ce-ideate`
- Requirements shaping: `ce-brainstorm`
- Planning: `ce-plan`
- Execution: `ce-work`
- Debugging: `ce-debug`
- Requirements/plan review: `ce-doc-review`
- Code review: `ce-code-review`
- PR description and PR creation: `ce-pr-description`, `ce-commit-push-pr`
- PR feedback resolution: `ce-resolve-pr-feedback`
- Browser testing: `ce-test-browser`
- Knowledge compounding: `ce-compound`, `ce-compound-refresh`
- Session history and previous attempts: `ce-sessions`, `ce-session-inventory`, `ce-session-extract`

Strengths:

- Clear sequence: ideate -> brainstorm -> plan -> work -> review -> ship-like handoff
- Strong durable artifacts: `docs/brainstorms/`, `docs/plans/`, `docs/solutions/`
- Strong traceability: requirements IDs, implementation units, test scenarios, plan-to-diff checks
- Strong review model: role-based document review and code review
- Strong knowledge loop through `ce-compound`

Weaknesses:

- It is powerful but not beginner-simple.
- It assumes the user can choose between many related Skills.
- It can be heavy for small projects.
- Some workflows expect subagents or rich tooling, so a beginner needs a simpler front door.

Best use in the fused workflow:

- Make Compound the default spine.
- Use `ce-brainstorm`, `ce-plan`, `ce-work`, `ce-code-review`, and `ce-compound` as the core path.

### Superpowers

Superpowers is less of a full product pipeline and more of a strict working discipline.

What it covers well:

- Always design before implementation: `brainstorming`
- Write implementation plans: `writing-plans`
- Execute plans: `executing-plans`
- Work in isolated branches/worktrees: `using-git-worktrees`
- Test-first implementation: `test-driven-development`
- Root-cause debugging: `systematic-debugging`
- Review before completion: `requesting-code-review`, `receiving-code-review`
- Verify before claiming done: `verification-before-completion`
- Finish a development branch: `finishing-a-development-branch`
- Create new Skills: `writing-skills`

Strengths:

- Very clear rules.
- Excellent for preventing common beginner mistakes: skipping planning, skipping tests, claiming done too early, accepting review feedback blindly, debugging by guessing.
- Strong teaching value because the principles are easy to understand.

Weaknesses:

- It is stricter than many small projects need.
- It lacks a full product-stage map by itself.
- It does not solve cross-session handoff as directly as gstack and compound.
- Its plan format is very detailed and can become too much for small projects.

Best use in the fused workflow:

- Use it as the "quality discipline layer".
- Pull in its rules at key gates: design first, TDD when behavior changes, root-cause before fixes, verify before completion.

### Gstack

Gstack is the broadest operational toolkit.

What it covers well:

- Early idea/product pressure test: `office-hours`
- Ambition and scope review: `plan-ceo-review`
- Engineering plan review: `plan-eng-review`
- Design plan review: `plan-design-review`
- Developer-experience plan review: `plan-devex-review`
- Full auto plan review: `autoplan`
- Pre-landing code review: `review`
- Web QA and fix loop: `qa`, `qa-only`
- Browser exploration: `browse`
- Ship workflow: `ship`
- Merge/deploy/verify: `land-and-deploy`
- Production monitoring: `canary`
- Documentation after ship: `document-release`
- Context handoff: `context-save`, `context-restore`
- Project learnings: `learn`
- Retrospective: `retro`
- Safety boundaries: `guard`, `careful`, `freeze`, `unfreeze`

Strengths:

- Strongest at late-stage delivery: QA, review, ship, deploy, canary, docs.
- Strongest built-in answer to context loss through `context-save` and `context-restore`.
- Strong plan review variants for product, engineering, design, and DX.
- Good for open-source project maturity because it thinks about docs, releases, retros, and operational safety.

Weaknesses:

- Very large surface area.
- Many Skills include long generated preambles, which can be overwhelming to study directly.
- Some commands are opinionated and heavy for a beginner's first small project.
- Several review Skills overlap with Compound review Skills.

Best use in the fused workflow:

- Use gstack for pressure-testing, late-stage QA/release, and context handoff.
- Do not make gstack the beginner's first default for every stage.

## Stage Mapping

| Stage | Best Default | Good Alternatives | Notes |
|---|---|---|---|
| Idea discovery | `ce-ideate` | `office-hours`, `superpowers:brainstorming` | Use `ce-ideate` when asking "what are the best directions?" Use `office-hours` when judging whether something is worth building. |
| Requirements | `ce-brainstorm` | `superpowers:brainstorming`, `office-hours` | `ce-brainstorm` produces a requirements doc that feeds `ce-plan`. |
| Plan | `ce-plan` | `superpowers:writing-plans` | `ce-plan` is more portable and right-sized; Superpowers plan is stricter and more step-by-step. |
| Plan review | `ce-doc-review` | `plan-eng-review`, `plan-ceo-review`, `plan-design-review`, `plan-devex-review`, `autoplan` | Use Compound for default doc review. Use gstack review variants when the plan has product/design/DX risk. |
| Implementation | `ce-work` | `superpowers:executing-plans`, `subagent-driven-development` | `ce-work` is the best general executor. Superpowers is stricter when plan tasks are independent and test-first. |
| Debugging | `ce-debug` | `systematic-debugging`, `investigate` | Use `ce-debug` for integrated diagnose-and-fix; use Superpowers principle as a guardrail. |
| Code review | `ce-code-review` | `gstack review`, `requesting-code-review` | Use `ce-code-review` before PR. Use `gstack review` as pre-landing or ship gate. |
| PR feedback | `ce-resolve-pr-feedback` | `receiving-code-review`, GitHub Skills | `receiving-code-review` is a discipline; `ce-resolve-pr-feedback` is the action workflow. |
| Browser QA | `gstack qa` | `qa-only`, `ce-test-browser`, `ce-test-browser` plus manual checks | For web apps, gstack QA is stronger because it tests and fixes. |
| Ship / PR | `ce-commit-push-pr` for normal PR, `gstack ship` for full release gate | `finishing-a-development-branch` | `gstack ship` is heavier and more automated. |
| Deploy / post-ship | `land-and-deploy`, `canary`, `document-release` | `ce-demo-reel`, `ce-pr-description` | Mostly gstack territory. |
| Knowledge compounding | `ce-compound` | `gstack learn`, `retro` | `ce-compound` creates durable docs; gstack tracks project learnings and retros. |
| Context handoff | workflow's own handoff file | `context-save`, `context-restore`, `ce-sessions` | This project should make handoff mandatory at every stage boundary. |

## Recommended Fused Workflow

### Stage 0: Project Intake

Goal:

- Decide what kind of project this is.
- Pick the workflow lane before invoking many Skills.

Use:

- Required: workflow router itself
- Optional: `ce-ideate` if the user has many possible directions
- Optional: `office-hours` if the question is "is this worth building?"

Exit gate:

- Project goal is one sentence.
- Target user is named.
- First deliverable is clear.
- The next stage is chosen.

If weak:

- Go to `ce-ideate` or `office-hours`.

Handoff file:

- `docs/workflow/state.md`

### Stage 1: Ideation

Goal:

- Generate and rank possible project directions.
- Avoid locking into the first idea too early.

Use:

- Required when direction is unclear: `ce-ideate`
- Optional: `office-hours`
- Optional: `superpowers:brainstorming` if the user already has one idea and wants to shape it

Exit gate:

- One idea is selected.
- Rejected ideas are recorded with reasons.
- The selected idea has a clear "why now" and "who for".

If weak:

- Stay in ideation.
- If all ideas are too vague, run `office-hours`.

Handoff file:

- `docs/ideation/<date>-<topic>.md`

### Stage 2: Requirements

Goal:

- Turn the selected idea into a durable description of what to build.

Use:

- Required: `ce-brainstorm`
- Optional: `office-hours` before requirements if the product/user is still fuzzy
- Optional: `superpowers:brainstorming` for stricter design-before-code discipline

Exit gate:

- Problem statement is clear.
- Scope boundaries are explicit.
- Success criteria are concrete.
- Open questions are split into "must answer before planning" and "can defer".

If weak:

- Return to Stage 1 if the idea is wrong.
- Stay in Stage 2 if only requirements are incomplete.

Handoff file:

- `docs/brainstorms/<topic>-requirements.md`

### Stage 3: Planning

Goal:

- Decide how to build the requirements without writing code yet.

Use:

- Required: `ce-plan`
- Optional: `superpowers:writing-plans` when you want very explicit task-by-task TDD instructions
- Optional for developer-facing tools: `plan-devex-review`

Exit gate:

- Plan has implementation units.
- Files or areas to change are named.
- Tests are named.
- Risks and dependencies are clear.
- The plan has enough detail that the next conversation can execute it.

If weak:

- Return to Stage 2 if behavior is unclear.
- Stay in Stage 3 if implementation details are weak.

Handoff file:

- `docs/plans/<date>-<topic>-plan.md`

### Stage 4: Plan Review

Goal:

- Catch wrong scope, missing edge cases, weak tests, product risk, design risk, and feasibility gaps before implementation.

Use:

- Required for non-trivial projects: `ce-doc-review`
- Optional product ambition review: `plan-ceo-review`
- Optional engineering review: `plan-eng-review`
- Optional UI review: `plan-design-review`
- Optional developer-tool review: `plan-devex-review`
- Optional all-in-one heavy review: `autoplan`

Exit gate:

- Review findings are resolved, accepted, or explicitly deferred.
- Plan contains a "not in scope" section.
- Remaining risks are known.

If weak:

- Return to Stage 3 to revise the plan.
- Return to Stage 2 if review reveals the wrong product problem.

Handoff file:

- Updated plan plus `docs/workflow/state.md`

### Stage 5: Implementation

Goal:

- Build the plan completely, with tests and incremental verification.

Use:

- Required: `ce-work`
- Optional: `superpowers:test-driven-development` when changing behavior
- Optional: `superpowers:using-git-worktrees` before starting feature work
- Optional: `superpowers:subagent-driven-development` when the plan has independent tasks
- Optional: `ce-debug` for bugs or failing tests

Exit gate:

- All implementation units are done.
- Tests relevant to the changed area pass.
- New behavior has tests.
- No unfinished "almost done" work remains.

If weak:

- Return to Stage 3 if the plan is wrong.
- Return to Stage 5 investigation/debugging if implementation is failing.

Handoff file:

- `docs/workflow/state.md`, updated after each major unit or before compact/clear.

### Stage 6: Code Review

Goal:

- Find code risks before PR or release.

Use:

- Required for non-trivial changes: `ce-code-review`
- Optional: `gstack review` as pre-landing check
- Optional discipline: `superpowers:requesting-code-review`

Exit gate:

- Critical and high-confidence findings are fixed.
- False positives are documented.
- Remaining risks are explicit.

If weak:

- Return to Stage 5 to fix.
- Return to Stage 3 if review reveals plan-level flaw.

Handoff file:

- `docs/workflow/state.md` plus review result summary.

### Stage 7: Browser QA / Acceptance

Goal:

- Verify the user-facing product actually works, especially for web projects.

Use:

- Required for web apps: `gstack qa` or `qa-only`
- Optional: `ce-test-browser`
- Optional: `ce-polish-beta` for browser-based polishing

Exit gate:

- Main flows were opened and tested.
- Console errors, empty states, and key interactions were checked.
- Bugs found during QA were fixed and re-tested.

If weak:

- Return to Stage 5 for fixes.
- Return to Stage 3 if QA reveals missing design/requirements.

Handoff file:

- `docs/workflow/qa-report.md` or `.gstack/qa-reports/` summary.

### Stage 8: Ship / PR

Goal:

- Package the work for review or delivery.

Use:

- Simple/default: `ce-commit-push-pr`
- Heavy/full release gate: `gstack ship`
- Optional PR description: `ce-pr-description`
- Optional visual proof: `ce-demo-reel`
- Optional branch finish: `superpowers:finishing-a-development-branch`

Exit gate:

- Commit exists.
- PR exists, or local delivery is complete.
- PR description explains value and verification.
- Tests/reviews/QA status is included.

If weak:

- Return to Stage 6 or 7.

Handoff file:

- `docs/workflow/state.md` with PR link and verification status.

### Stage 9: Land, Deploy, and Monitor

Goal:

- Merge safely and verify production.

Use:

- Optional: `land-and-deploy`
- Optional: `canary`
- Optional: `document-release`

Exit gate:

- PR merged or intentionally left open.
- Deployment status known.
- Production smoke check or canary completed if applicable.
- Docs match what shipped.

If weak:

- Return to Stage 7 for QA.
- Return to Stage 5 for fixes.

Handoff file:

- `docs/workflow/release-summary.md`

### Stage 10: Compound Knowledge

Goal:

- Turn mistakes, fixes, and hard-won lessons into reusable memory.

Use:

- Required after meaningful bug/fix/review lesson: `ce-compound`
- Optional: `ce-compound-refresh`
- Optional: `gstack learn`
- Optional: `gstack retro`

Exit gate:

- At least one reusable lesson is saved when the project produced one.
- Future sessions can search and reuse it.

If weak:

- Do not force a lesson for trivial work.
- If there was a real mistake or repeated pattern, capture it.

Handoff file:

- `docs/solutions/...`

## The Context Handoff System

The main missing layer across the existing plugins is a single beginner-friendly handoff contract.

This project should add one durable state file:

`docs/workflow/state.md`

This file should be updated at every stage boundary and before any compact/clear.

Recommended structure:

```markdown
# Project Workflow State

## Current Stage
Stage 3: Planning

## Project Goal
...

## Target User
...

## Current Decision
...

## Completed So Far
- Stage 1 ideation: done, selected ...
- Stage 2 requirements: done, file ...

## Active Artifact
docs/plans/...

## Next Action
Run ce-doc-review on ...

## Do Not Reopen Unless
- Product goal changes
- Requirements are contradicted
- QA shows missing behavior

## Important Decisions
- ...

## Open Questions
- Blocking:
- Deferred:

## Verification So Far
- ...

## Lessons / Risks To Remember
- ...
```

Why this matters:

- `compact` can preserve some summary, but it is not a stable project memory.
- `/clear` loses conversation state entirely.
- A new conversation can read `docs/workflow/state.md` and immediately know what has happened and what to do next.
- This also makes the future open-source project understandable to beginners.

Use gstack's `context-save` and `context-restore` as optional personal backup, but do not rely on them as the only handoff layer. A project-local state file is easier to share in an open-source repo.

## Beginner Path

For a small beginner project, use this shorter route:

1. `ce-brainstorm`
2. `ce-plan`
3. `ce-work`
4. `ce-code-review`
5. `gstack qa` if it is a web app
6. `ce-commit-push-pr`
7. `ce-compound` if something reusable was learned

Mandatory handoff:

- Update `docs/workflow/state.md` after each stage.

Skip by default:

- `autoplan`
- `plan-ceo-review`
- `plan-devex-review`
- `land-and-deploy`
- `canary`
- `retro`

Use only when needed.

## Complex Project Path

For a larger project:

1. `ce-ideate`
2. `office-hours`
3. `ce-brainstorm`
4. `ce-plan`
5. `ce-doc-review`
6. Add review variants based on risk:
   - Product risk: `plan-ceo-review`
   - Engineering risk: `plan-eng-review`
   - UI risk: `plan-design-review`
   - Developer-tool risk: `plan-devex-review`
7. `ce-work`
8. `ce-code-review`
9. `gstack review`
10. `gstack qa`
11. `ce-commit-push-pr` or `gstack ship`
12. `land-and-deploy`
13. `canary`
14. `document-release`
15. `ce-compound`
16. `retro`

Mandatory handoff:

- Update `docs/workflow/state.md` before every stage change and before context reset.

## What Should Be Required vs Optional

Required for almost every real project:

- Requirements: `ce-brainstorm`
- Plan: `ce-plan`
- Work: `ce-work`
- Review: `ce-code-review`
- Handoff: `docs/workflow/state.md`
- Verification: relevant tests or QA

Required only when applicable:

- `gstack qa` for web apps
- `ce-debug` for bugs
- `ce-compound` when a reusable learning exists
- `plan-design-review` for meaningful UI
- `plan-devex-review` for developer-facing tools

Optional / advanced:

- `ce-ideate` when choosing among many ideas
- `office-hours` for product viability and founder-style pressure testing
- `autoplan` for heavy all-in review
- `land-and-deploy`, `canary`, `document-release` for real release workflows
- `retro` for periodic process review

## Overlaps and How To Choose

### Brainstorming Overlap

- `ce-ideate`: many possible ideas; rank survivors.
- `ce-brainstorm`: one chosen idea; define requirements.
- `superpowers:brainstorming`: strict design-before-code process.
- `office-hours`: pressure test whether the idea is worth building.

Default:

- Start with `ce-brainstorm` if the idea exists.
- Use `ce-ideate` only before that if the direction is not chosen.
- Use `office-hours` when product value is uncertain.

### Planning Overlap

- `ce-plan`: best default.
- `superpowers:writing-plans`: stricter, more step-by-step, better when handing tasks to subagents or enforcing TDD.

Default:

- Use `ce-plan`.
- Use Superpowers planning only when the project needs extremely explicit task execution.

### Review Overlap

- `ce-doc-review`: review requirements or plans.
- `plan-eng-review`: deeper engineering plan review.
- `plan-ceo-review`: ambition/product/scope review.
- `plan-design-review`: UI plan review with visuals.
- `plan-devex-review`: developer experience review.
- `ce-code-review`: code review before PR.
- `gstack review`: pre-landing PR review.

Default:

- Plan doc: `ce-doc-review`
- Code before PR: `ce-code-review`
- Pre-landing/release: `gstack review`

### QA Overlap

- `gstack qa`: test and fix web app issues.
- `gstack qa-only`: report only.
- `ce-test-browser`: browser test affected pages.

Default:

- Web app ready for acceptance: `gstack qa`
- Want report only: `qa-only`
- Need narrower route-based browser testing: `ce-test-browser`

### Knowledge Overlap

- `ce-compound`: write durable solution docs in `docs/solutions/`.
- `gstack learn`: search/manage gstack's project learnings.
- `retro`: periodic engineering reflection.

Default:

- Use `ce-compound` after real mistakes, fixes, or reusable patterns.
- Use `gstack learn` to inspect accumulated gstack memories.
- Use `retro` weekly or after a project milestone.

## Product Shape Recommendation

### V1: A Single Skill

Build one Skill first:

`project-workflow`

It should do three things:

1. Read `docs/workflow/state.md` if it exists.
2. Detect the current stage.
3. Recommend or invoke the next Skill with a short explanation and a required handoff update.

It should include:

- A stage map
- Beginner path
- Complex path
- Handoff file template
- Stage exit gates
- Skill selection rules
- Recovery instructions for compact/clear
- A "where am I?" command

Why Skill first:

- OpenAI says Skills are for following a process, while plugins are for connecting tools or sources of information.
- Agent Skills are lightweight and portable: a folder with `SKILL.md`, optional scripts, references, and assets.
- This project is currently mostly process design, not external tool integration.
- New users can inspect and edit a Skill more easily than a plugin.
- A Skill can later grow into a plugin if needed.

### V2: Optional Scripts

Add scripts only after the workflow proves useful:

- `scripts/status.sh`: show current stage and active artifacts
- `scripts/init-workflow.sh`: create `docs/workflow/state.md`
- `scripts/advance-stage.sh`: update state safely
- `scripts/validate-state.sh`: check required fields before moving on

### V3: Plugin Later

Move to plugin form only if you need:

- UI for stage navigation
- Cross-repo workflow dashboard
- Integration with GitHub, Slack, Google Drive, or task trackers
- Automatic state syncing
- MCP tools
- Analytics across projects
- A packaged install experience with multiple Skills and tools

In that case, the plugin should bundle:

- `project-workflow` Skill
- Handoff templates
- Validation scripts
- Optional MCP/tooling for reading PRs, issues, and docs

## Suggested Project Structure

```text
workflow/
├── README.md
├── skills/
│   └── project-workflow/
│       ├── SKILL.md
│       ├── references/
│       │   ├── stage-map.md
│       │   ├── handoff-template.md
│       │   └── skill-selection.md
│       └── scripts/
│           ├── init-workflow.sh
│           ├── status.sh
│           └── validate-state.sh
├── docs/
│   ├── workflow/
│   │   ├── state-template.md
│   │   └── stage-gates.md
│   └── examples/
│       ├── beginner-web-app.md
│       └── complex-saas-project.md
└── tests/
    └── pressure-scenarios/
        ├── clear-after-plan.md
        ├── resume-after-qa.md
        └── wrong-skill-selection.md
```

## Strongest Candidate Ideas

### 1. Workflow Router Skill

What it does:

- Reads current state.
- Tells the user exactly what stage they are in.
- Calls or recommends the right next Skill.
- Forces a handoff update at every boundary.

Why it survives:

- Directly solves the beginner problem.
- Low implementation complexity.
- Works as a Skill first.
- Can later become a plugin.

Risk:

- If it only lists Skills, it becomes a static cheat sheet. It must actively enforce stage gates and handoff.

### 2. Project State Contract

What it does:

- Defines `docs/workflow/state.md` as the stable cross-session memory.
- Makes every stage update it.

Why it survives:

- This solves the biggest pain: context loss after compact/clear.
- It is independent of which plugin executes the next stage.

Risk:

- If too verbose, agents will not keep it updated. It needs a short required section and optional detail sections.

### 3. Beginner / Advanced Lanes

What it does:

- Gives users two routes:
  - Beginner: fewer Skills, fewer reviews, clear defaults
  - Advanced: more reviews, QA, deploy, canary, retro

Why it survives:

- Prevents beginners from drowning in all available Skills.
- Still gives power users a full pipeline.

Risk:

- If the lanes are too rigid, the workflow will feel bureaucratic. It should allow one-line stage overrides.

### 4. Stage Exit Gates

What it does:

- Defines "done enough to move on" for every stage.

Why it survives:

- Prevents the common mistake of moving from fuzzy idea to coding too early.
- Also prevents review/QA from becoming optional hand-waving.

Risk:

- Needs to stay short and practical.

### 5. Skill Selection Matrix

What it does:

- Explains overlaps and when to choose which Skill.

Why it survives:

- Directly solves beginner confusion.
- Makes the project useful even before automation.

Risk:

- Can go stale as plugins change. Keep it in `references/skill-selection.md` and version it.

## Ideas Rejected

### Rejected: Build a Plugin First

Reason:

- Current problem is process clarity, not tool connection.
- Plugin form adds packaging and tool complexity before proving the workflow.

### Rejected: Create a Brand-New All-In-One Mega Skill That Reimplements Everything

Reason:

- The existing Skills are already strong.
- The project should route and coordinate them, not duplicate them.

### Rejected: Use Only One Plugin

Reason:

- Compound has the best spine, but gstack handles context/release/QA better, and Superpowers has clearer discipline rules.

### Rejected: Make `autoplan` the Default

Reason:

- It is too heavy for beginners and small projects.
- Better as an advanced lane tool.

## Recommended Next Step

Move from ideation to requirements:

Run `ce-brainstorm` on this chosen direction:

> Build a beginner-friendly AI project workflow Skill that routes users through idea, requirements, plan, review, implementation, QA, ship, and knowledge capture, with a durable handoff file that survives compact/clear.

The requirements stage should decide:

- Exact Skill name
- Exact stage list
- Exact handoff file format
- Whether the Skill auto-invokes next Skills or only recommends them
- How strict stage gates should be
- How much content belongs in `SKILL.md` vs `references/`

