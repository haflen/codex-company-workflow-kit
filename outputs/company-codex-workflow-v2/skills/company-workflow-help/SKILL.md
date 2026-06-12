---
name: company-workflow-help
description: Use when a company user is unsure which workflow to start, asks what to do next, wants a command phrase, or needs routing between onboarding, requirements, design, planning, implementation, bugfix, hotfix, spike, and skill updates.
---

# Company Workflow Help / 公司工作流入口帮助

## Purpose / 目的

Help company users enter the right workflow without knowing skill names.

帮助公司用户在不知道 skill 名称的情况下，判断当前应该进入哪条工作流。

## Routing / 路由判断

Use the user's current goal, project state, and available artifacts:

根据用户当前目标、项目状态和已有产物判断入口：

| User Situation / 用户情况 | Route To / 路由到 | Suggested Phrase / 推荐说法 |
| --- | --- | --- |
| Idea or request is unclear / 想法或需求还不清楚 | `company-feature-requirements` | `帮我梳理这个功能需求：...` |
| Requirements and acceptance criteria are confirmed / 需求和验收标准已确认 | `company-feature-design` | `需求已确认，进入技术设计` |
| Design is confirmed / 技术方案已确认 | `company-feature-planning` | `方案已确认，进入任务拆解` |
| Tasks are confirmed / 任务清单已确认 | `company-implementation-runner` | `任务已确认，开始实现` |
| Existing behavior is wrong / 现有行为不符合预期 | `company-bugfix-runner` | `开始 bugfix：...` |
| Urgent production issue / 紧急线上问题 | `company-bugfix-runner` with hotfix path | `/hotfix ...` |
| Need feasibility research / 需要技术可行性验证 | `company-spike-research` | `/spike ...` |
| Need expert skill update / 需要更新专家技能 | `company-skill-upgrade-runner` | `检查专家技能更新` |
| Need expert routing explanation / 想知道需要哪些专家组合 | `company-expert-routing` | `这个任务需要哪些专家组合？` |
| Existing project needs adoption or context draft / 旧项目需要接入或生成上下文草稿 | `company-legacy-project-onboarding` | `请帮我把这个旧项目接入公司 Codex 工作流` |

## Output / 输出格式

- Recommended workflow / 推荐工作流:
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
