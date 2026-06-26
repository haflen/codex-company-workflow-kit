---
name: company-workflow-help
description: Use when a company user is unsure which workflow to start, asks what to do next, wants a command phrase, or needs routing between onboarding, requirements, design, planning, implementation, bugfix, hotfix, spike, expert readiness, and skill updates.
---

# Company Workflow Help / 公司工作流入口帮助

## Purpose / 目的

Help company users enter the right workflow without knowing skill names. The `/hotfix` and `/spike` strings below are suggested prompt phrases, not real Codex slash commands.

帮助公司用户在不知道 skill 名称的情况下，判断当前应该进入哪条工作流。

## Routing / 路由判断

Use the user's current goal, project state, and available artifacts:

根据用户当前目标、项目状态和已有产物判断入口：

| User Situation / 用户情况 | Complexity / 复杂度 | Route To / 路由到 | Superpowers Layer / Superpowers 叠加 | Suggested Phrase / 推荐说法 |
| --- | --- | --- | --- | --- |
| Explore only; no code or formal docs / 只想探讨，不写代码，不落正式文档 | L0 | `company-feature-requirements` lightweight mode | `superpowers:brainstorming` | `Lightweight exploration: discuss options only; no code or formal document.` |
| Small copy, field, UI, or config change / 文案、字段、小 UI、小配置 | L1 | lightweight planning or `company-implementation-runner` | Usually none; behavior changes use `superpowers:test-driven-development` | `Small change: handle lightly and give verification evidence.` |
| Idea or request is unclear / 想法或需求还不清楚 | L2 | `company-feature-requirements` | `superpowers:brainstorming` | `帮我梳理这个功能需求：...` |
| Requirements and acceptance criteria are confirmed / 需求和验收标准已确认 | L2 | `company-feature-design` | `superpowers:brainstorming` when options need comparison | `需求已确认，进入技术设计` |
| Design is confirmed / 技术方案已确认 | L2 | `company-feature-planning` | `superpowers:writing-plans` | `方案已确认，进入任务拆解` |
| Tasks are confirmed / 任务清单已确认 | L1/L2/L3 | `company-implementation-runner` | `superpowers:test-driven-development` + `superpowers:verification-before-completion` | `任务已确认，开始实现` |
| Existing behavior is wrong / 现有行为不符合预期 | L1/L2 | `company-bugfix-runner` | `superpowers:systematic-debugging` | `开始 bugfix：...` |
| Urgent production issue / 紧急线上问题 | L3 | `company-bugfix-runner` with hotfix path | `superpowers:systematic-debugging` + `superpowers:verification-before-completion` | `start hotfix: ...` |
| Need feasibility research / 需要技术可行性验证 | L1/L2 | `company-spike-research` | `superpowers:brainstorming`; optionally `superpowers:verification-before-completion` | `start spike: ...` |
| Need expert skill update / 需要更新专家技能 | L3 | `company-skill-upgrade-runner` | `superpowers:verification-before-completion` | `检查专家技能更新` |
| Need to confirm experts are installed, reviewed, or callable / 需要确认专家是否已安装、审查或可调用 | L1/L2 | `company-expert-readiness` | none; installation and dependency diagnosis | `检查这个项目的专家依赖是否就绪` |
| Need expert routing explanation / 想知道需要哪些专家组合 | L2/L3 | `company-expert-routing` | Depends on task: brainstorming / systematic-debugging / test-driven-development | `这个任务需要哪些专家组合？` |
| Existing project needs adoption or context draft / 旧项目需要接入或生成上下文草稿 | L2 | `company-legacy-project-onboarding` | `superpowers:brainstorming` | `请帮我把这个旧项目接入公司 Codex 工作流` |

## Complexity Levels / 复杂度分级

- L0: lightweight exploration; no formal document.
- L1: small change; minimal context and minimal verification.
- L2: standard delivery through requirements, design, planning, and implementation.
- L3: high-risk change with full workflow, expert routing, strict verification, and user confirmation.

## Output / 输出格式

- Workflow layer / 工作流层: `company-workflow-help`
- Recommended workflow / 推荐工作流:
- Complexity level / 复杂度级别:
- Superpowers layer / Superpowers 叠加:
- Actual calls:
- Expert/plugin capabilities:
- Not called, lens only:
- Execution strategy / 执行策略:
- Verification evidence:
- Unverified items:
- Remaining risk:
- Why / 原因:
- Suggested user phrase / 推荐用户说法:
- Required input from user / 还需要用户补充:
- Files or artifacts to check / 需要检查的文件或产物:

## Guardrails / 约束

- Do not start implementation from a vague request.
- 不要从模糊需求直接进入实现。
- Do not force a heavy workflow for trivial copy, labels, or single-line config changes.
- 对文案、标签、单行配置等简单任务，不要强行套重流程。
- If the user is in the middle of a phase, continue that phase unless they clearly ask to advance.
- 如果用户正在某个阶段中，默认继续当前阶段，除非用户明确要求进入下一阶段。
- If multiple routes fit, pick the route that resolves the earliest missing artifact.
- 如果多个入口都可能适用，优先选择能补齐最早缺失产物的入口。
- Every routing answer must explicitly state whether a Superpowers layer is used; if not, state that the task is simple enough to skip it.
- 每次推荐工作流时都必须显式说明 Superpowers 是否叠加；如果不叠加，说明原因是任务足够简单。
