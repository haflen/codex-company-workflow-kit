# Skill Tree

这份清单说明公司版当前已有 skills，以及它们在工作流里的位置。

## 总览

```text
基础工程能力
├── Superpowers: brainstorming
├── Superpowers: writing-plans
├── Superpowers: test-driven-development
├── Superpowers: systematic-debugging
├── Superpowers: requesting-code-review
├── Superpowers: verification-before-completion
├── Superpowers: finishing-a-development-branch
├── First Principles Check: 底层事实、约束、最小成立条件
├── Adversarial Review: 极端输入、异常状态、权限、并发、性能、渲染反例
└── Codex built-in: file edits, commands, browser checks, Git

入口帮助
└── company-workflow-help
    └── 决定进入哪条 workflow，并自动判定 light/full-audit

项目上下文
├── company-context-index
│   └── 读取文档职责地图、编号命名空间和当前任务路由
├── company-thread-handoff
│   └── 在长对话与新对话之间传递临时任务状态，并做风险分级接手验证
├── company-workflow-health-check
│   └── 诊断旧项目接入健康度、模板新旧、插件暴露和规则漂移
└── company-legacy-project-onboarding
    └── 旧项目接入时生成或修正文档职责地图

功能交付主链路
├── company-feature-requirements
│   └── 按需触发 business-rules.md，沉淀操作逻辑、计算口径和样例用例
├── company-feature-design
│   └── L2/L3 触发式方案对比，用户确认推荐方案后再进入任务拆解
├── company-feature-planning
├── company-implementation-runner
└── company-delivery-closeout

例外通道
├── company-bugfix-runner
└── company-spike-research

专家路由
├── company-expert-routing
│   └── 在已选 workflow 内选择 bundle、专家、Superpowers、MCP、浏览器或官方文档
└── company-expert-readiness

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
| `superpowers:requesting-code-review` | 审查最终待交付 diff 的规格一致性和代码风险 | delivery closeout |
| `superpowers:verification-before-completion` | 完成前验证证据 | implementation, bugfix |
| `superpowers:finishing-a-development-branch` | 检查业务分支收尾状态，不改变已选 commit/deliver 模式 | delivery closeout |
| First Principles Check | 回到底层事实、约束和最小成立条件 | requirements, design, bugfix, spike |
| Adversarial Review | 从极端、恶意、异常和边界场景验证稳健性 | planning, implementation, bugfix, hotfix, spike, skill governance |
| Phase Consistency Preflight | 实现或修复前检查入口、索引、版本 README、任务文档是否一致 | implementation, bugfix, hotfix, workflow health check |
| Scope Change Circuit Breaker | 发现新增架构层、数据加工层、接口边界或业务口径变化时，让旧实现授权失效并回到文档确认 | workflow help, expert routing, design, planning, implementation |
| Validation Levels `V0/V1/V2/V3` | 按风险自动选择验证成本，避免验证不足或全量过度验证 | planning, implementation, bugfix, hotfix |
| Controlled Continuous Implementation | 在已确认任务清单内批量推进，并在范围变化、验证失败或高风险点自动停下 | planning, implementation, workflow help |
| Codex Goal Tracking Recommendation | 对跨阶段、跨会话、高风险或连续执行任务建议建立目标，并提示目标不等于实现授权 | workflow help, implementation |
| Codex Plan Mode Recommendation | 对不确定路线、方案对比、旧项目接入或高风险任务建议先用计划模式判断，不改文件不编码 | workflow help |
| Subagents Recommendation | 对独立任务、独立失败域或高风险审查建议使用子 agent，说明能力状态，并要求显式请求和主 agent 复核 | workflow help, planning, implementation |
| Next-Step Guidance | 每轮完成后给出下一步建议和可复制口令 | all company workflows |
| Documentation Drift Check | 检查代码变更是否需要同步需求、业务规则、设计、任务或公共文档 | implementation, bugfix, hotfix |
| Chinese Code Logic Comments | 用中文解释跨语言代码里的业务规则、计算口径、数据映射和异常分支 | planning, implementation, bugfix, hotfix |
| Codex built-in tools | 文件编辑、命令执行、浏览器验证、Git | all implementation and verification work |

## Company Skills

| Skill | 中文职责 | When to Use |
| --- | --- | --- |
| `company-workflow-help` | 帮用户判断应该进入哪条工作流 | User is unsure where to start, asks what to do next, or needs a prompt phrase. |
| `company-context-index` | 建立或更新项目上下文索引 | Starting or resuming company work and needing project context routing. |
| `company-thread-handoff` | 选择继续、压缩、完整 fork 或分级交接，并校验目标对话理解 | Continuing, compacting, forking, or transferring a long conversation with verified receipt. |
| `company-workflow-health-check` | 检查项目工作流健康度、模板新旧、插件暴露和旧规则残留 | Project workflow adoption, templates, plugin exposure, or old rules need diagnosis. |
| `company-legacy-project-onboarding` | 旧项目接入、索引草稿确认、首个试点选择 | Introducing the workflow into an existing project or reviewing generated project context. |
| `company-feature-requirements` | 澄清需求、范围、验收标准 | Feature requirements, acceptance criteria, scope, or change-request requirements are needed. |
| `company-feature-design` | 产出技术设计、架构、API、数据流、测试策略 | Requirements are confirmed and design is needed before planning. |
| `company-feature-planning` | 把设计拆成可执行任务和验证点 | Requirements and design are confirmed and implementation tasks are needed. |
| `company-implementation-runner` | 按已确认任务执行实现和验证 | Requirements, design, and task plan are confirmed. |
| `company-delivery-closeout` | 规整里程碑成果、清理可证明临时产物、复验并按授权提交或推送 | A task batch, feature, milestone, or version phase is fully complete. |
| `company-bugfix-runner` | 区分 bug/变更，复现、修复、回归验证 | Behavior differs from requirements, tests, or documented expectations. |
| `company-spike-research` | 做限时技术预研和最小实验 | Feasibility, unfamiliar library, or architecture uncertainty needs reduction. |
| `company-expert-routing` | 自动选择专家组合、skill、subagent 或官方文档 | A workflow needs expert routing or current documentation strategy. |
| `company-expert-readiness` | 检查强依赖专家是否已内置安装、自动审查并在当前会话暴露 | A project needs expert dependency install, review, or exposure status. |
| `company-skill-upgrade-runner` | 完成技能更新 dry-run、diff、安全审查、确认后覆盖 | User wants to check, update, replace, or install workflow/expert skills. |
| `company-skill-security-review` | 审查第三方、开源、自进化 skill 的安全风险 | External or self-improved skills need review before trust. |
| `company-skill-maintenance` | 维护专家依赖、pin、bundle 影响面和回滚记录 | Updating, pinning, auditing, replacing, or reviewing trusted skills. |
| `company-skill-evolution-lab` | 记录 workflow 误触发/过重/过轻，并提出改进 | Workflow skills repeatedly misfire or need controlled improvement proposals. |

## Workflow Help vs Expert Routing

- `company-workflow-help` 是入口层：回答“我现在该走需求、设计、任务、实现、bugfix、spike、旧项目接入还是技能升级？”
- `company-expert-routing` 是执行层内的专家选择：回答“当前 workflow 里，需要前端、后端、测试、产品、业务、Superpowers、浏览器验证、MCP 或官方文档中的哪些组合？”
- 用户不需要主动判断 `light/full-audit`。入口和执行 workflow 会自动判定：普通推进用 `light`，阶段交接、完成报告、hotfix、spike 结论、技能升级、安全审查、专家能力未真实调用或验证缺失时用 `full-audit`。
- 用户也不需要手动输入“从第一性原理出发”或“做对抗式审查”。复杂设计、bugfix、spike 和完成前验证会自动触发；普通小改动可跳过但需要说明原因。
- `company-context-index` 和 `company-legacy-project-onboarding` 负责文档职责地图：入口页、spike 工作日志、正式 specs、生命周期总结不能共享裸任务编号。
- `company-thread-handoff` 先选择 `resume / compact / fork / handoff`；只有 handoff 才生成 `quick / standard / decision-rich` 胶囊。默认不落文件，目标对话必须完成语义校验；它不替代 `company-context-index`，也不产生实现授权。
- `business-rules.md` 不是每个需求都要写。只有指标公式、操作逻辑、状态流转、字段口径、异常数据、角色差异或复杂权限等场景触发；触发后由需求阶段创建，设计阶段映射，任务阶段转成验证点。
- 技术方案对比也不是每个设计都要做。L1 小改动可跳过并说明原因；L2/L3 大功能、核心模块、跨边界、数据模型、权限、安全、性能或业务规则设计必须比较 2-3 个方案，并等用户确认推荐方案后进入 planning。
- 验证等级不是用户手动选择。实现、bugfix 和 hotfix 自动判定 `V0/V1/V2/V3`，并在完成报告里输出验证证据、未验证项和剩余风险。
- 文档漂移检查是执行出口：如果实现改变了需求承诺、业务规则、API 契约、设计、任务或公共入口，必须补文档或标记待确认漂移。
- 中文代码逻辑备注是跨语言规则：Java、前端 TypeScript/Vue/React、Python、SQL 和脚本中，只要出现业务规则、公式阈值、字段映射、异常分支、兼容或性能策略等非显然逻辑，就必须补中文说明。
- 阶段一致性预检是执行入口：如果 `说明文档.md`、`INDEX.md`、当前 version/feature README 和任务文档互相矛盾，普通实现/bugfix 先暂停并修正文档路由；生产 hotfix 可先止血但必须记录补偿任务。
- 范围变化熔断是实现授权保护：如果实现中发现遗漏架构层、数据加工层、目标表、接口边界、业务口径或文档需要同步，旧的实现授权失效；workflow 只能先补文档和确认点，不能顺手继续编码。
- 连续执行模式是实现阶段的批量推进保护：只有任务清单确认且用户明确授权时启用；`V0/V1` 可连续，`V2` 小批量，`V3` 必须停下确认。
- 目标追踪建议是跨轮次总目标保护：L2/L3、跨会话、连续执行、旧项目接入和技能治理任务会建议建立 Codex 目标；目标存在不代表实现授权有效。
- Codex 计划模式建议是正式 workflow 前的路线保护：需求不清、方案分歧、旧项目接入、范围变化或 L3 高风险任务会建议先用计划模式判断路线；计划模式不改文件、不编码。
- Subagents 建议是复杂执行的上下文隔离保护：小任务默认不用；独立任务、独立失败域或高风险审查才建议使用。真实调用需要用户显式要求 spawn/delegate，且主 agent 必须复核子 agent 的 diff、验证证据和剩余风险。
- 下一步引导是所有完成报告的固定出口：必须给出 `下一步建议` 和 `推荐用户下一句`，避免用户不知道该继续、确认还是回退到文档阶段。
- 交付收口是实现后的独立出口：只有任务全部完成、明确延期或明确不做时才能进入；它负责最终成果盘点、来源化清理、审查、复验、精确暂存和授权范围内的 commit/push。

## Typical Flow

普通功能：

```text
company-workflow-help
-> company-context-index
-> company-feature-requirements
   -> optional superpowers:brainstorming
   -> optional business-rules.md when rules/calculation semantics are non-trivial
-> company-feature-design
   -> solution comparison for L2/L3 design triggers
-> company-feature-planning
   -> optional subagent split strategy for L2/L3 independent tasks or review
-> company-implementation-runner
   -> superpowers:test-driven-development when behavior is non-trivial
   -> superpowers:verification-before-completion before completion report
   -> optional controlled continuous mode after explicit user authorization
   -> optional subagents for independent implementation, investigation, or review
-> company-delivery-closeout
   -> superpowers:requesting-code-review for non-trivial final diffs
   -> superpowers:verification-before-completion on the final candidate
   -> superpowers:finishing-a-development-branch for branch-finalization checks
   -> optional local commit and ordinary business-branch push according to mode
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

旧项目健康检查：

```text
company-workflow-help
-> company-workflow-health-check
-> update-templates / bootstrap-project / reinstall plugin as recommended
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
