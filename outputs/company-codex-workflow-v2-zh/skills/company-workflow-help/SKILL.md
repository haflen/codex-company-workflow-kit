---
name: company-workflow-help
description: Use when a company user requests managed task delivery within stated boundaries, is unsure which workflow to start, asks what to do next, needs long-conversation continuity, or needs routing between onboarding, health check, requirements, design, planning, implementation, quality validation, bugfix, hotfix, spike, expert readiness, skill updates, professional document translation, and Chinese reports or review documents.
---

# 公司工作流入口帮助

按共享 `../../specs/global/assets/task-execution-policy.md` 的 READ-01 读取当前任务必需章节；已读未变的规则不重复加载。单点低风险修改在本技能完成局部验证即可结束；需要正式交付、打包或独立验收时保留对应阶段。

## 本地完成登记

已使用任务状态、终点为 `prepare`、无外部验收且任务为 `running` 的 `validation`/`delivery` 阶段，核对实际环境未变化后，使用 `scripts/complete_task.py`。它在同一次受 revision 保护的更新中登记 `delivery` 和 `completed`；仅为新增且未填写环境的证据继承现有环境，追加完成项和证据历史。显式环境不一致仍拒绝，不改写旧证据。

```sh
python3 <installed-plugin>/skills/company-workflow-help/scripts/complete_task.py \
  --project-root <project> --task-id <task> --expected-revision <current-revision> \
  --submission <submission.json>
```

提交 JSON 只包含本次新增的 `evidence`、`completed_items`，以及可选的 `current_task`、`next_step`；不要重复提交历史条目，也不要传 `phase`、`status` 或 `environment`。证据仍需原始日志、校验和、候选指纹及对应验收项。环境名称不会证明真实运行环境；无法确认一致时先补验，不靠改标签通过。

其他终点、外部验收或不满足上述前提时继续使用 `task_state.py` 原流程；拒绝后先 show/validate 核对真实原因，不自动删锁、刷新指纹或重跑业务操作。已完成任务不重复登记。

## 阶段连续性

按 READ-01 读取项目 `specs/global/assets/task-execution-policy.md` 的适用章节，缺失时使用 `../../specs/global/assets/task-execution-policy.md`；已读未变则复用。按 FLOW-01 至 FLOW-07 核对并实际进入已授权下一阶段；已有来源仍有效，不索要重复口令。保留本技能的质量、文档归属、权限及真实验收要求。

## 任务约定与已有授权

复用上文共享规则，需要记录时使用 `../../specs/global/assets/task-contract-template.md`。从真实请求提取目标、范围、验收、终点与授权来源，复用已确认信息；已有约定保持单一来源。只读或仅规划请求按其范围执行。已有授权覆盖的后续动作不要求重复口令；缺失决定只阻塞相关动作。

## 目的

帮助公司用户在不知道 skill 名称的情况下，判断当前应该进入哪条工作流。这里的 `/hotfix`、`/spike` 只是推荐说法，不是 Codex UI 里注册出来的真实 slash 命令。

## 与专家路由的区别

- `company-workflow-help` 决定“现在该走哪条 workflow”：健康检查、需求、设计、任务、实现、bugfix、hotfix、spike、旧项目接入、技能升级等。
- `company-expert-routing` 决定“进入某条 workflow 后，需要哪些专家、bundle、Superpowers、MCP、浏览器或官方文档”。
- `company-workflow-health-check` 诊断“这个项目的工作流接入是否健康”，例如旧项目仍有旧规则、模板缺失、插件装了但 skill 不生效。
- 用户不知道从哪里开始时，先用 `company-workflow-help`；进入明确 workflow 后，只有非平凡技术、业务、测试或风险判断才调用 `company-expert-routing`。
- 本 skill 不做详细专家选择，只判断是否需要进入专家路由。

## 路由判断

根据用户当前目标、项目状态和已有产物判断入口：

| 用户情况 | 复杂度 | 路由到 | Superpowers 叠加 | 推荐说法 |
| --- | --- | --- | --- | --- |
| 只想探讨想法，不写代码，不落正式文档 | L0 | `company-feature-requirements` 轻量模式 | `superpowers:brainstorming` | `轻量探讨：只聊方案，不写代码，不落正式文档。` |
| 文案、字段、小 UI、小配置等低风险小改动 | L1 | 轻量 planning 或 `company-implementation-runner` | 通常无；涉及行为时用 `superpowers:test-driven-development` | `小改动：轻量处理，给我验证结果。` |
| 想法或需求还不清楚 | L2 | `company-feature-requirements` | `superpowers:brainstorming` | `帮我梳理这个功能需求：...` |
| 需求阶段需要先画、预览、修改或确认 HTML/页面/交互原型 | L1/L2 | `company-requirements-prototype` | 首次或实质性体验变化用 `superpowers:brainstorming`；非简单 UI 再用 `company-expert-routing` | `需求还没冻结，先做隔离 HTML 原型验证，不进入技术设计。` |
| 需要梳理操作逻辑、指标公式、计算口径、状态流转或异常处理 | L2/L3 | `company-feature-requirements` 并判定是否创建 `business-rules.md` | `superpowers:brainstorming`，必要时 `company-expert-routing` | `帮我梳理这个功能的业务规则和计算口径：...` |
| 已经进入实现，但发现遗漏架构层、数据加工层、表、接口边界、业务口径或文档需要同步 | L2/L3 | 触发范围变化熔断；回到 `company-feature-requirements` 或 `company-feature-design`，必要时再进 `company-feature-planning` | `superpowers:brainstorming`，并用 `company-expert-routing` 判断阶段许可 | `发现范围变化：先补文档和确认，不写代码。` |
| 需求和验收标准已确认 | L2 | `company-feature-design` | L2/L3 方案对比触发时使用 `superpowers:brainstorming` | `需求已确认，进入技术设计；如命中 L2/L3，请先做方案对比。` |
| 技术方案已确认 | L2 | `company-feature-planning` | `superpowers:writing-plans` | `方案已确认，进入任务拆解` |
| 任务清单已确认 | L1/L2/L3 | `company-implementation-runner` | `superpowers:test-driven-development` + `superpowers:verification-before-completion` | `任务已确认，开始实现` |
| 任务清单已确认，且用户希望少确认几次连续推进 | L1/L2 | `company-implementation-runner` 连续执行模式 | `superpowers:test-driven-development` + `superpowers:verification-before-completion` | `任务已确认，连续完成后续所有可执行任务；遇到缺失业务决定、权限或不可安全恢复的冲突再停。` |
| 实现任务已经完成，需要判断是否独立验收或执行交付门禁 | L1/L2/L3 | 自动判定；命中条件时进入 `company-quality-validation` | `superpowers:verification-before-completion`；测试策略使用 `testing-qa` | `实现已完成，请判断并执行独立质量验收。` |
| 任务批次、功能或里程碑已全部完成，需要规整成果、清理临时文件、提交或推送 | L2/L3 | `company-delivery-closeout` | `superpowers:requesting-code-review` + `superpowers:verification-before-completion` + `superpowers:finishing-a-development-branch` | `所有任务已完成，开始交付收口并推送业务分支。` |
| 现有行为不符合预期 | L1/L2 | `company-bugfix-runner` | `superpowers:systematic-debugging` | `开始 bugfix：...` |
| 紧急线上问题 | L3 | `company-bugfix-runner` hotfix 路径 | `superpowers:systematic-debugging` + `superpowers:verification-before-completion` | `热修复：...` 或 `开始 hotfix：...` |
| 需要技术可行性验证 | L1/L2 | `company-spike-research` | `superpowers:brainstorming` 用于实验方案，必要时 `superpowers:verification-before-completion` 检查证据 | `快速验证：...` 或 `开始 spike：...` |
| 需要更新专家技能 | L3 | `company-skill-upgrade-runner` | `superpowers:verification-before-completion` 用于完成前校验 | `检查专家技能更新` |
| 需要确认专家是否已安装、审查或可调用 | L1/L2 | `company-expert-readiness` | 无；这是安装和依赖诊断 | `检查这个项目的专家依赖是否就绪` |
| 想知道需要哪些专家组合 | L2/L3 | `company-expert-routing` | 按任务补充 `superpowers:brainstorming` / `superpowers:systematic-debugging` / `superpowers:test-driven-development` | `这个任务需要哪些专家组合？` |
| 旧项目需要接入或生成上下文草稿 | L2 | `company-legacy-project-onboarding` | `superpowers:brainstorming` 用于试点选择和迁移策略 | `请帮我把这个旧项目接入公司 Codex 工作流` |
| 旧项目已接入但想检查健康度、模板新旧、插件是否生效或为什么用起来不对 | L1/L2 | `company-workflow-health-check` | 通常无；需要设计修复方案时叠加 `superpowers:brainstorming` | `请检查这个项目的公司工作流健康度` |
| 只是稍后继续原任务，或当前对话太长但目标不变 | L1/L2 | `company-thread-handoff` 的 `resume/compact` 路由 | 无；优先使用 Codex 原生连续性 | `继续原任务` 或 `压缩当前任务后继续` |
| 开新任务且完整历史讨论不能丢 | L1/L2 | `company-thread-handoff` 的 `fork` 路由 | 无；使用 Codex 原生 fork | `完整继承历史并创建新任务` |
| 开干净的新任务，只保留决策、状态和下一步 | L1/L2/L3 | `company-thread-handoff` 的 `handoff` 路由 | 无；这里只做临时任务状态传递 | `生成标准交接并发送到新任务` |

## 复杂度分级

- L0：轻量探讨，只输出思路、选项、风险和下一步建议。
- L1：小改动，最小上下文、最小任务卡、最小验证。
- L2：标准交付，按需求、设计、任务、实现推进。
- L3：高风险变更，完整流程、专家路由、严格验证和用户确认。

## 需求原型路由

用户不需要自己判断原型属于哪个阶段。按目的和依赖边界自动处理：

- 页面、交互、文案和模拟业务状态验证：进入 `company-requirements-prototype`，保持需求阶段。
- 原型反馈改变目标、范围、验收标准或业务规则：先回 `company-feature-requirements` 更新权威文档，再继续原型。
- 用户只确认需求和原型：转为需求基线后停止，不进入技术设计或任务拆分。
- 用户确认需求和原型并明确说“进入技术设计”：转为基线后进入 `company-feature-design`，后续按 FLOW-01/02 核对。
- 真实 API、数据库、认证、生产数据/组件、后端、数据库结构、基础设施、性能或技术可行性：停止需求原型，改判 `company-spike-research` 或已授权的 `company-feature-design`。

“继续”按已有明确授权解释；没有整体授权时不能由原型确认推导出设计或实现权限。

## 对话交接路由

采用“主动唤起 + 风险时提醒”的混合模式。先判断用户要继续原任务、压缩当前上下文、完整继承历史，还是创建干净交接；不要把四种需求都转换成摘要。

命中以下任一情况时，提醒用户选择连续性方式，但不自动写文件或静默创建任务：

- 一个阶段已结束，但当前主任务仍有后续工作。
- 即将切换需求、设计、任务、实现或 bugfix 阶段。
- 对话出现状态遗忘、重复读取、范围混淆或授权漂移。
- 存在未提交改动、运行中服务或未完成验证。

默认推荐规则：目标不变只担心长度时用 `compact`；全部历史都重要时用 `fork`；新里程碑或希望减少 token 时用 `standard handoff`。产品边界、架构、业务规则、计算、数据、安全、多个被否方案或“不要重新讨论”时，自动升级为 `decision-rich`。

目标任务已存在时，不能事后注入完整历史；使用一个不可拆分的交接胶囊，并要求目标复述目标、决策、约束、状态、未完成事项和授权。传输状态显示为：`已生成 -> 已发送/待粘贴 -> 已读取 -> 语义校验通过/未通过`。

用户明确要求落盘时，只允许覆盖 `.codex/handoff/current.md`。交接不替代 `company-context-index`、正式需求/设计/任务文档或阶段确认，也不产生新的实现授权。

## 范围变化熔断判断

按 FLOW-06 比较已有范围与当前请求。只阻塞未授权新增范围或实际冲突，补具体差异并问缺失决定；保留原范围有效授权。关键词和常规文档同步不使授权失效。

## 验证等级路由

用户不需要判断验证等级。进入实现、bugfix 或 hotfix 后，由对应 workflow 自动判定 `V0/V1/V2/V3`：

- `V0`：纯文档或无行为变更。
- `V1`：低风险小改动。
- `V2`：标准功能或普通 bugfix。
- `V3`：生产、权限、安全、数据、性能、金额/指标公式、跨系统或 hotfix。

入口帮助只负责说明预计等级；最终等级由执行 workflow 在完成前确认。

## 连续执行路由

按 FLOW-01 至 FLOW-07 判断当前可执行步骤。明确目标与整体授权已经覆盖后续阶段时直接推进，不增加启用口令。必要需求、设计、任务和验收不能省略；实质决定缺失只阻塞依赖它的动作。V3 每项复核而非一律等待用户。

示例：`按已确认方案完成实现、验证和打包；仅在业务决定、范围或权限确有缺失时找我。` 示例不是必须照抄的口令。

## 交付收口路由

用户不需要判断何时进入收口。只有当前任务清单中的事项全部完成、明确延期或明确不做，并且不再有可执行实现任务时，才进入质量验收判定；无需独立验收，或验收为 `pass` / 用户明确接受且允许的 `conditional-pass` 后，才路由到 `company-delivery-closeout`。

- “整理本次成果”“清理临时文件并提交”“全部做完后提交”“收口并推送业务分支”等意图直接进入收口判断。
- 仍有可执行任务时，继续 `company-implementation-runner`；不得用收口静默关闭任务。
- `prepare` 只盘点、规整和验证；`commit` 增加本地提交；`deliver` 增加普通业务分支 push。
- 受保护分支、未知归属文件、验证失败、文档冲突或 staged 清单不一致时必须停止。

默认口令：`所有任务已完成，开始交付收口并推送业务分支。`

## 质量验收路由

用户不需要判断是否需要单独测试节点。实现或 bugfix 完成后自动按风险和交付范围判定：

- `V0/V1` 默认不单独验收；仍保留实现阶段的聚焦验证。
- 单任务 `V2` 默认不单独验收；但关键用户旅程、浏览器交互、API/数据库集成或明显回归面存在时进入 `company-quality-validation`。
- 多任务、跨模块、前后端联动、API/数据库集成的 `V2` 必须进入 `company-quality-validation`。
- 里程碑、发布候选、`V3` 与 hotfix 补偿验收必须进入 `company-quality-validation`。
- 验收 `blocked` 时进入 `company-bugfix-runner`，修复后回到同一验收范围；验收节点不得直接修改生产代码。
- `conditional-pass` 只有在风险不属于禁止条件且用户明确接受时才可进入收口；高风险 `V3` 不能用条件通过规避阻断。

## API 不可用与条件合入路由

当任务要求真实 API，但当前只能使用 Fixture/Mock 时，自动按以下状态判断：

- 前端候选已完成：`FIXTURE_READY`。
- 真实 API 联调或真实页面验收未完成：`API_PENDING`，质量验收保持阻断。
- 用户没有明确批准先合入：停在 `company-quality-validation` 或等待 API 恢复。
- 用户明确批准先合入指定普通业务分支：进入 `company-delivery-closeout` 的 `conditional-merge`，合入后为 `CONDITIONAL_MERGED`，原任务保持未完成。

**有条件合入不等于有条件通过。** 路由回答必须先用人话告诉客户“API 不可用，本次只先合并了分支，尚未完成真实联调和交付”，再给技术字段。不得证明真实数据、图表或业务计算正确。

推荐批准口令：`API 当前不可用；我批准将已验证的 Fixture 前端候选有条件合入 <目标业务分支>，不视为验收或交付，不发布不部署；API 恢复后继续 <补偿任务>。`

## Codex 计划模式建议

Codex 计划模式适合在正式 workflow 前做路线判断，不替代需求、设计、任务确认，也不授权实现。本 skill 只做建议，不自动进入计划模式。

计划模式建议分三档：

- `不需要`：L0/L1 小任务、路径已经清楚的实现、单点 bugfix、hotfix 止血、只问入口或只做一次性查询。
- `建议使用`：L2 标准功能但需求仍有歧义、需要比较 2-3 个方案、旧项目接入、范围变化后需要重新判断路线、连续执行前需要确认任务顺序和停止条件。
- `强烈建议使用`：L3 高风险任务、跨系统、数据、权限、安全、性能、金额/指标公式、生产事故复盘、大迁移或多人协作交付。

推荐计划模式提示词必须强调“不改文件、不编码、只判断路线”。例如：

```text
请先用 Codex 计划模式判断这个任务应该进入哪条公司 workflow；不要改文件，不要写代码。请输出推荐流程、需要确认的问题、风险和下一步处理建议。
```

边界：

- 计划模式输出只是路线建议；正式产物仍要进入 `company-feature-requirements`、`company-feature-design`、`company-feature-planning` 或对应 workflow。
- 计划模式不能替代用户对需求、方案、任务或实现范围的确认。
- 计划模式不能覆盖范围变化熔断、阶段一致性预检、V3 验证要求与实际权限门禁和验证要求。

## Subagents 使用建议

Subagents 适合隔离上下文、独立审查或处理互不影响的问题域，不是默认执行方式。本 skill 只做建议，真正执行需要当前 Codex 环境支持，并且用户显式请求 `spawn agents`、`delegate in parallel`、`使用 subagents 并行审查` 或等价表达。

Subagents 建议分三档：

- `不需要`：L0/L1 小任务、单文件小改、纯文档/注释、小 UI 文案、小配置、单一路径 bugfix。
- `建议使用`：L2 多任务交付，任务之间边界清楚；多个独立失败域；需要单独做规格一致性审查、代码质量审查或测试策略审查。
- `强烈建议使用`：L3 高风险任务、跨模块/跨系统、数据/权限/安全/性能、复杂旧项目接入、技能升级安全审查、多个团队边界或连续执行批次较大。

使用原则：

- 主 agent 负责阶段判断、授权、任务分派、汇总和最终验证。
- 子 agent 只拿到窄任务包：目标、边界、允许文件、禁止事项、验证方式和预期输出。
- 不要让多个子 agent 同时编辑同一文件或同一共享状态。
- 子 agent 输出不能直接等于完成；主 agent 必须复核 diff、验证证据和剩余风险。
- Codex App 端主要展示 subagent 活动，不要求用户寻找独立子代理入口；CLI 可用 `/agent` 管理 agent thread。
- 如需稳定公司角色，建议先执行 `bash scripts/install.sh install-agents <project-path> --lang zh`，生成 `.codex/agents/company-*.toml`。

## Codex 目标追踪建议

Codex 目标适合做跨轮次目标容器，不替代公司 workflow 的阶段判断和实现授权。本 skill 只做建议，不自动创建目标。

目标追踪建议分三档：

- `不需要`：L0 轻量探讨、L1 小文案/小 UI/小配置、单轮能完成的小 bugfix、只问入口或只做一次性查询。
- `建议建立`：L2 标准功能、跨需求/设计/任务/实现多阶段、预计跨会话、需要连续执行、涉及多份文档或多个验证点。
- `强烈建议建立`：L3 高风险任务、旧项目接入、技能升级/安全审查/专家依赖维护、hotfix 止血后还有补测试/补文档/复盘、多人协作或跨系统交付。

推荐目标描述必须写最终成功标准，不写当前操作步骤。例如：

```text
完成 <功能名> 从需求确认、技术设计、任务拆解、实现、验证到文档同步的完整交付。
成功标准：需求/设计/任务已确认；代码实现完成；验证证据完整；文档漂移已处理；完成报告包含下一步建议。
```

边界：

- 目标存在不代表可以直接编码；阶段一致性预检、范围变化熔断、V3 验证要求与实际权限门禁和用户确认仍然优先。
- 目标只记录“最终要完成什么”，不要把每个 workflow 步骤都塞进目标。
- 不要为了小任务建议建立目标。

## 透明度分级判定

用户不需要判断使用哪种透明度级别；本 skill 必须自动选择：

- `light`：默认模式。适合普通阶段内推进、小改动、低风险文档更新、简单入口推荐。
- `full-audit`：命中以下任一条件时自动启用：
  - 阶段交接：需求到设计、设计到任务、任务到实现。
  - 实现完成、bugfix 完成、hotfix 任意阶段、spike 结论输出。
  - 技能升级、安全审查、专家依赖异常或自进化提案。
  - 当前会话缺少应有 Superpowers、专家 skill、MCP、浏览器或插件能力。
  - 出现“仅采用专家视角，没有真实调用”的情况。
  - 验证失败、验证缺失、无法运行测试。
  - 涉及生产、数据、权限、架构、性能或安全风险。
  - 用户要求审计、复核流程或确认是否合规。

如果推荐入口触发 `full-audit`，必须说明触发原因。

## 目标终端路由

- UI、交互或客户端请求在进入设计、实现前，先检查 `specs/global/INDEX.md` 和当前需求是否确认目标使用终端。
- 终端范围缺失时路由到 `company-feature-requirements`；不得把通用前端建议当成移动端需求，不得自行增加移动端适配。
- 用户在实现中临时新增终端或改变共用策略时，判定为范围变化并使旧实现授权失效。

## 人类优先输出

先读取 `../../specs/global/assets/human-output-standard.md`，同时尊重项目已确认的读者和交付用途。保留一句话结论和下一步建议；用中文解释结果、依据和影响。以下输出/报告中的内部字段写入已有执行记录，不默认附在用户回复或人类文档中。

### 回复契约门禁

发送前按共享规范复核事实范围、前置条件、责任方、授权、读者及显示效果。普通问答不套固定标题；用户需要详细解释时补充有用依据。未通过阅读检查先重写再发送。
## 输出格式

- 工作流层：`company-workflow-help`
- 透明度模式：
- 复杂度级别：
- 推荐工作流：
- Superpowers 叠加：
- 实际调用：
- 专家/插件能力：
- 未调用但采用视角：
- 第一性原理检查：
- 对抗式审查：
- 执行策略：
- 验证证据：
- 未验证项：
- 剩余风险：
- 原因：
- 阶段许可：
- 实现授权状态：
- 推荐用户说法：
- 对话交接建议：不需要 / 建议生成
- 交接建议原因：
- 推荐交接口令：
- 是否建议连续执行：
- 连续执行推荐口令：
- Codex 计划模式建议：不需要 / 建议使用 / 强烈建议使用
- 计划模式建议原因：
- 计划模式提示词：
- 计划完成后的正式 workflow：
- Subagents 建议：不需要 / 建议使用 / 强烈建议使用
- Subagents 建议原因：
- Subagent 能力状态：未检查 / 当前会话可用 / 需要用户显式请求 / 需要本地 custom agents 配置 / 当前 App 仅展示活动
- 推荐 subagent 用法：
- Subagents 实际调用：未调用 / 已调用 / 仅采用拆分视角
- Subagents 未调用原因：
- 目标追踪建议：不需要 / 建议建立 / 强烈建议建立
- 建议原因：
- 推荐目标描述：
- 还需要用户补充：
- 需要检查的文件或产物：
- Workflow Audit（仅 full-audit 时输出）：

## 约束

- 不要从模糊需求直接进入实现。
- 对文案、标签、单行配置等简单任务，不要强行套重流程。
- 如果用户正在某个阶段中，默认继续当前阶段，除非用户明确要求进入下一阶段。
- 如果多个入口都可能适用，优先选择能补齐最早缺失产物的入口。
- 每次推荐工作流时都必须显式说明 Superpowers 是否叠加；如果不叠加，说明原因是任务足够简单。
- 不要在入口帮助阶段展开详细专家清单；只判断是否需要进入 `company-expert-routing`。
- 命中范围变化熔断时，不得推荐继续实现；先推荐补文档、设计或任务确认。

## 等待与接续

按共享 WAIT-01 探测当时可用的原生等待能力，核对真实机制ID、原任务、当前候选、取消状态和授权。无有效机制时明确 manual_resume；本回合等待不等于已建后台续做。重复或旧事件不重做动作；无变化不通知，取消后不重启。

## 文档翻译入口

“把客户手册翻译成英文”“检查中英文是否一致”等请求直接使用 `professional-translation`，按已知源文、语言和交付目标执行，缺必要信息才问。不要求用户记住技能名，也不要求先走软件需求、设计和实现阶段。原文件默认保留，交付文字审校不冒充版面或线上功能验收。

## 汇报与评审写作入口

“写周会汇报”“整理成能发给同事的说明”“把方案写得便于评审”等请求，直接使用 `company-document-writing`，沿用已有读者、材料、用途和授权完成成稿、内部核稿及必要显示检查。已知信息不重复询问，不要求用户点技能或审批提纲。内部检查发现表达问题，在原范围修好后交付，不把普通修订作为用户下一步。仅改一句文案在当前任务完成；翻译仍走 `professional-translation`。这项能力不授予业务实现、发消息或发布权限。
