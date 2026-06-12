# Skill Tree

这份清单说明公司版当前已有 skills，以及它们在工作流里的位置。

## 总览

```text
基础工程能力
├── Superpowers: brainstorming
├── Superpowers: writing-plans
├── Superpowers: test-driven-development
├── Superpowers: systematic-debugging
├── Superpowers: verification-before-completion
└── Codex built-in: file edits, commands, browser checks, Git

入口帮助
└── company-workflow-help

项目上下文
├── company-context-index
└── company-legacy-project-onboarding

功能交付主链路
├── company-feature-requirements
├── company-feature-design
├── company-feature-planning
└── company-implementation-runner

例外通道
├── company-bugfix-runner
└── company-spike-research

专家路由
└── company-expert-routing

技能治理
├── company-skill-upgrade-runner
├── company-skill-security-review
├── company-skill-maintenance
└── company-skill-evolution-lab

```

## Skills

## Foundation Layer

这些能力不由本仓库维护，但公司 workflow 会在合适节点复用它们。

| Capability | 中文职责 | Used By |
| --- | --- | --- |
| `superpowers:brainstorming` | 开放问题澄清、方案分歧收敛 | requirements, design, workflow help |
| `superpowers:writing-plans` | 复杂任务计划和可执行拆解 | planning |
| `superpowers:test-driven-development` | 非平凡实现的测试先行纪律 | implementation |
| `superpowers:systematic-debugging` | 复现、定位、验证根因 | bugfix, hotfix |
| `superpowers:verification-before-completion` | 完成前验证证据 | implementation, bugfix |
| Codex built-in tools | 文件编辑、命令执行、浏览器验证、Git | all implementation and verification work |

## Company Skills

| Skill | 中文职责 | When to Use |
| --- | --- | --- |
| `company-workflow-help` | 帮用户判断应该进入哪条工作流 | User is unsure where to start, asks what to do next, or needs a prompt phrase. |
| `company-context-index` | 建立或更新项目上下文索引 | Starting or resuming company work and needing project context routing. |
| `company-legacy-project-onboarding` | 旧项目接入、索引草稿确认、首个试点选择 | Introducing the workflow into an existing project or reviewing generated project context. |
| `company-feature-requirements` | 澄清需求、范围、验收标准 | Feature requirements, acceptance criteria, scope, or change-request requirements are needed. |
| `company-feature-design` | 产出技术设计、架构、API、数据流、测试策略 | Requirements are confirmed and design is needed before planning. |
| `company-feature-planning` | 把设计拆成可执行任务和验证点 | Requirements and design are confirmed and implementation tasks are needed. |
| `company-implementation-runner` | 按已确认任务执行实现和验证 | Requirements, design, and task plan are confirmed. |
| `company-bugfix-runner` | 区分 bug/变更，复现、修复、回归验证 | Behavior differs from requirements, tests, or documented expectations. |
| `company-spike-research` | 做限时技术预研和最小实验 | Feasibility, unfamiliar library, or architecture uncertainty needs reduction. |
| `company-expert-routing` | 自动选择专家组合、skill、subagent 或官方文档 | A workflow needs expert routing or current documentation strategy. |
| `company-skill-upgrade-runner` | 完成技能更新 dry-run、diff、安全审查、确认后覆盖 | User wants to check, update, replace, or install workflow/expert skills. |
| `company-skill-security-review` | 审查第三方、开源、自进化 skill 的安全风险 | External or self-improved skills need review before trust. |
| `company-skill-maintenance` | 维护专家依赖、pin、bundle 影响面和回滚记录 | Updating, pinning, auditing, replacing, or reviewing trusted skills. |
| `company-skill-evolution-lab` | 记录 workflow 误触发/过重/过轻，并提出改进 | Workflow skills repeatedly misfire or need controlled improvement proposals. |

## Typical Flow

普通功能：

```text
company-workflow-help
-> company-context-index
-> company-feature-requirements
   -> optional superpowers:brainstorming
-> company-feature-design
-> company-feature-planning
-> company-implementation-runner
   -> superpowers:test-driven-development when behavior is non-trivial
   -> superpowers:verification-before-completion before completion report
```

Bugfix：

```text
company-workflow-help
-> company-context-index
-> company-bugfix-runner
   -> superpowers:systematic-debugging when root cause is unclear
```

技能升级：

```text
company-workflow-help
-> company-skill-upgrade-runner
-> company-skill-security-review
-> company-skill-maintenance
```

旧项目接入：

```text
company-workflow-help
-> company-legacy-project-onboarding
-> company-context-index
-> first pilot feature, bugfix, or spike
```

## Expert Bundles

专家组合不直接塞进主流程。主流程通过 `company-expert-routing` 读取 `BUNDLES.md`，按任务类型自动选择最小组合。

常见组合：

| Bundle | 用途 |
| --- | --- |
| `company-core-delivery` | 通用功能交付 |
| `company-backend-java` | Java/Spring 后端 |
| `company-python-service` | Python 服务或自动化 |
| `company-django-service` | Django/DRF/Celery |
| `company-frontend-delivery` | 前端交互、UI、浏览器验证 |
| `company-ai-feature` | LLM/RAG/prompt/agent |
| `company-hotfix` | 紧急生产缺陷 |
| `company-spike` | 技术预研 |
| `company-skill-governance` | 技能升级、安全审查、自进化 |
| `company-workflow-entry` | 用户不知道该从哪里开始 |
| `company-legacy-onboarding` | 旧项目接入和上下文草稿确认 |
