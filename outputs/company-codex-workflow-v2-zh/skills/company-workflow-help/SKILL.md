---
name: company-workflow-help
description: Use when a company user is unsure which workflow to start, asks what to do next, wants a command phrase, or needs routing between onboarding, requirements, design, planning, implementation, bugfix, hotfix, spike, expert readiness, and skill updates.
---

# 公司工作流入口帮助

## 目的

帮助公司用户在不知道 skill 名称的情况下，判断当前应该进入哪条工作流。这里的 `/hotfix`、`/spike` 只是推荐说法，不是 Codex UI 里注册出来的真实 slash 命令。

## 路由判断

根据用户当前目标、项目状态和已有产物判断入口：

| 用户情况 | 复杂度 | 路由到 | Superpowers 叠加 | 推荐说法 |
| --- | --- | --- | --- | --- |
| 只想探讨想法，不写代码，不落正式文档 | L0 | `company-feature-requirements` 轻量模式 | `superpowers:brainstorming` | `轻量探讨：只聊方案，不写代码，不落正式文档。` |
| 文案、字段、小 UI、小配置等低风险小改动 | L1 | 轻量 planning 或 `company-implementation-runner` | 通常无；涉及行为时用 `superpowers:test-driven-development` | `小改动：轻量处理，给我验证结果。` |
| 想法或需求还不清楚 | L2 | `company-feature-requirements` | `superpowers:brainstorming` | `帮我梳理这个功能需求：...` |
| 需求和验收标准已确认 | L2 | `company-feature-design` | 复杂设计可用 `superpowers:brainstorming` 辅助方案比较 | `需求已确认，进入技术设计` |
| 技术方案已确认 | L2 | `company-feature-planning` | `superpowers:writing-plans` | `方案已确认，进入任务拆解` |
| 任务清单已确认 | L1/L2/L3 | `company-implementation-runner` | `superpowers:test-driven-development` + `superpowers:verification-before-completion` | `任务已确认，开始实现` |
| 现有行为不符合预期 | L1/L2 | `company-bugfix-runner` | `superpowers:systematic-debugging` | `开始 bugfix：...` |
| 紧急线上问题 | L3 | `company-bugfix-runner` hotfix 路径 | `superpowers:systematic-debugging` + `superpowers:verification-before-completion` | `热修复：...` 或 `开始 hotfix：...` |
| 需要技术可行性验证 | L1/L2 | `company-spike-research` | `superpowers:brainstorming` 用于实验方案，必要时 `superpowers:verification-before-completion` 检查证据 | `快速验证：...` 或 `开始 spike：...` |
| 需要更新专家技能 | L3 | `company-skill-upgrade-runner` | `superpowers:verification-before-completion` 用于完成前校验 | `检查专家技能更新` |
| 需要确认专家是否已安装、审查或可调用 | L1/L2 | `company-expert-readiness` | 无；这是安装和依赖诊断 | `检查这个项目的专家依赖是否就绪` |
| 想知道需要哪些专家组合 | L2/L3 | `company-expert-routing` | 按任务补充 `superpowers:brainstorming` / `superpowers:systematic-debugging` / `superpowers:test-driven-development` | `这个任务需要哪些专家组合？` |
| 旧项目需要接入或生成上下文草稿 | L2 | `company-legacy-project-onboarding` | `superpowers:brainstorming` 用于试点选择和迁移策略 | `请帮我把这个旧项目接入公司 Codex 工作流` |

## 复杂度分级

- L0：轻量探讨，只输出思路、选项、风险和下一步建议。
- L1：小改动，最小上下文、最小任务卡、最小验证。
- L2：标准交付，按需求、设计、任务、实现推进。
- L3：高风险变更，完整流程、专家路由、严格验证和用户确认。

## 输出格式

- 工作流层：`company-workflow-help`
- 复杂度级别：
- 推荐工作流：
- Superpowers 叠加：
- 执行策略：
- 原因：
- 推荐用户说法：
- 还需要用户补充：
- 需要检查的文件或产物：

## 约束

- 不要从模糊需求直接进入实现。
- 对文案、标签、单行配置等简单任务，不要强行套重流程。
- 如果用户正在某个阶段中，默认继续当前阶段，除非用户明确要求进入下一阶段。
- 如果多个入口都可能适用，优先选择能补齐最早缺失产物的入口。
- 每次推荐工作流时都必须显式说明 Superpowers 是否叠加；如果不叠加，说明原因是任务足够简单。
