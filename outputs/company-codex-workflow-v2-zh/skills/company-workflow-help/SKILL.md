---
name: company-workflow-help
description: Use when a company user is unsure which workflow to start, asks what to do next, wants a command phrase, or needs routing between onboarding, requirements, design, planning, implementation, bugfix, hotfix, spike, and skill updates.
---

# 公司工作流入口帮助

## 目的

帮助公司用户在不知道 skill 名称的情况下，判断当前应该进入哪条工作流。

## 路由判断

根据用户当前目标、项目状态和已有产物判断入口：

| 用户情况 | 路由到 | 推荐说法 |
| --- | --- | --- |
| 想法或需求还不清楚 | `company-feature-requirements` | `帮我梳理这个功能需求：...` |
| 需求和验收标准已确认 | `company-feature-design` | `需求已确认，进入技术设计` |
| 技术方案已确认 | `company-feature-planning` | `方案已确认，进入任务拆解` |
| 任务清单已确认 | `company-implementation-runner` | `任务已确认，开始实现` |
| 现有行为不符合预期 | `company-bugfix-runner` | `开始 bugfix：...` |
| 紧急线上问题 | `company-bugfix-runner` hotfix 路径 | `/hotfix ...` |
| 需要技术可行性验证 | `company-spike-research` | `/spike ...` |
| 需要更新专家技能 | `company-skill-upgrade-runner` | `检查专家技能更新` |
| 想知道需要哪些专家组合 | `company-expert-routing` | `这个任务需要哪些专家组合？` |
| 旧项目需要接入或生成上下文草稿 | `company-legacy-project-onboarding` | `请帮我把这个旧项目接入公司 Codex 工作流` |

## 输出格式

- 推荐工作流：
- 原因：
- 推荐用户说法：
- 还需要用户补充：
- 需要检查的文件或产物：

## 约束

- 不要从模糊需求直接进入实现。
- 对文案、标签、单行配置等简单任务，不要强行套重流程。
- 如果用户正在某个阶段中，默认继续当前阶段，除非用户明确要求进入下一阶段。
- 如果多个入口都可能适用，优先选择能补齐最早缺失产物的入口。
