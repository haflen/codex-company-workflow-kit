---
name: company-expert-routing
description: Use when a company workflow needs to decide whether an expert skill, multi-agent delivery, subagent review, official documentation, or current-agent expert lens should be used.
---

# 公司专家路由

按共享 `../../specs/global/assets/task-execution-policy.md` 的 READ-01 读取当前任务必需章节；已读未变的规则不重复加载。单点低风险修改在本技能完成局部验证即可结束；需要正式交付、打包或独立验收时保留对应阶段。

按 [工作流入口](../company-workflow-help/SKILL.md) 的“工作流与多 Agent 的选择”和“简短告知本次使用方式”核对模式、有效授权与告知。普通工作流按需使用专家skills不等于派发agent；明确选择单执行者时保留质量门禁，不静默升级。

## DELEGATE-01：结果复核与串行回退

派发先核对当前有效授权、真实工具和独立边界；路由建议不是授权。没有明确派发许可或缺能力时使用 serial，由主代理执行允许的工作，不安装代理、不新建用户聊天。只有可比较样例的通过率不降、协调成本及耗时确有收益，才采用并行；未实际对照则保留串行，不声称提速。

窄任务包记录实际 task_id、允许路径、禁止动作、验收、candidate_fingerprint、budget与输出位置。派发前在该任务说明中按已有契约写清不可变的字段名、类型和值（含不得扩展的状态值），以及允许修改的字段、正文和文件范围；约束必须随任务交给执行者，不能只放在协调者评分表中。若纠错需要改变固定字段，保留该字段并报告具体冲突，不自行扩展契约。共享契约、状态和集成由主代理单写；读审查默认不写文件。预算按已有约定，未知保持未知，不编造剩余额度。到限/取消后停止本任务实际子代理并核对停止，保存可用成果；失败只回收受影响项，在原范围串行处理，不无限重派。

采用前检查 result_id、实际候选指纹、变更范围和原始验证证据。缺证据的DONE、旧候选、越界动作、未知副作用或仅自报成功不作为完成；先调查实际结果，不能自动接受或重放。重复result_id不重复集成；候选漂移重新核对受影响证据，不能复用旧通过。模拟回复只能证明判定规则，不证明真的启动、取消或测量了子代理。

## 多 Agent 交付执行

用户已明确要求从业务资料/需求起步的多 agent 交付、实施或独立审查时，读取并执行 [完整操作说明](references/multi-agent-delivery.md)。沿用真实授权与当前业务 workflow，不增加审批阶段、启用口令、新 skill 或调度器。DELEGATE-01 的串行限制针对并发执行收益；执行者完成后由另一个代理独立审查可以串行交接，无性能对照不宣称提速。派发前核对原生能力并显式传入角色正文；只有实际调用和返回的身份才算已派发。按说明第1a节选择当前阶段的现有 workflow 和必要专家，传递来源原义、需求ID、反例及未决项；在既有 inputs/结果中保存准确技能路径/章节、真实读取指纹和规则→产物证据。主代理按工具轨迹或原始输出及实际产物核对，角色名或自报不能代替。缺少不可替代技能或必要审查时，该要求保持未满足；缺工具回退单执行者，不能冒称独立审查。取消代理不等于其命令或服务已停止，按说明核对真实运行身份和停止证据后才能重派或释放依赖。

## REVIEW-01：盲审输入与证据复用

仅在任务明确要求盲审或隐藏预设答案时，派发前核对实际可见输入，包括继承对话、历史摘要和记忆注入；新代理或不继承父对话不等于无污染。保存输入诊断及核对结果，审查者开始时再自检。发现历史答案、旧评分或无法确认输入隔离时，不把该轮计作盲审；在已有授权内改用已核对的干净上下文。运行环境支持时仅对该次调用关闭记忆，不修改全局配置或移除上级安全规则；无法核实时明确限制。普通审查不要求禁用记忆。答案与评分留在协调者侧，报告先冻结再对答案，不因本规则增加代理数或审查轮次。

按共享 EVIDENCE-01 先核对已有原始日志的候选/工具指纹、需求、环境适用性、完整性与原始输出；满足条件就复用，仅缺失、漂移或矛盾的部分补验。保留必要命令、工作目录、实际起止、退出码、stdout/stderr、关键输入/前后状态及来源指纹；当前访问优先复用宿主已有工具轨迹，不临时搭建全量文件访问记录器。沿用已核实的旧路径→当前路径映射，历史绝对路径只作元数据，不因此读取范围外目录；保留原时间，不冒称本次执行。盲审包可以包含同范围未评分的原始观察，不包含旧结论、答案或评分。旧日志不能替代必须刷新的外部检查；证据不足保持未验证。记录实际耗时、污染中止、样本补跑和采集/核对重跑，区分各自原因；不以缺日志换取提速，不从一次对照推导通用收益。

## 目的

集中管理 bundle 和专家选择，避免各工作流重复维护路由表。

## 与入口帮助的区别

- `company-workflow-help` 负责判断用户当前应该进入哪条 workflow。
- `company-expert-routing` 只在 workflow 已经明确后使用，负责选择最小必要 bundle、专家 skill、Superpowers、MCP、浏览器能力或官方文档。
- 如果用户只是问“现在该怎么做”，先回到 `company-workflow-help`。
- 如果当前任务已经进入需求、设计、任务、实现、bugfix、hotfix、spike 或技能治理阶段，并且存在非平凡判断，再使用本 skill。

## 路由方法

1. 先判断阶段许可：允许实现、只允许补文档、需要先设计、需要任务拆解、需要用户确认，还是需要回到 `company-workflow-help`。
2. 判断任务是否复杂到需要 bundle 或专家。
3. 阅读 `BUNDLES.md`，根据请求、spec、文件路径和技术栈选择最小匹配 bundle。
4. 使用专家 skill 前，检查 `EXPERTS.lock.md` 和 `.codex-workflow/EXPERT-READINESS.md`；强依赖专家应已随公司插件内置。
5. 在选中 bundle 内，只使用当前阶段需要的专家。
6. 如果专家在当前会话已暴露为 Codex skill，在触发条件匹配时直接使用。
7. 如果支持多 agent 且问题复杂，按 DELEGATE-01 核对实际权限、范围和收益，再决定是否派发聚焦审查。
8. 如果专家已随插件安装但当前会话不可见，记录到 `未调用但采用视角`，说明需要新开 Codex 线程刷新技能列表；不要要求用户逐个安装。
9. 对变化快的 API，优先当前官方文档或本地包文档。

## 阶段许可

专家路由不是实现授权。每次路由都必须在内部执行记录保存 `阶段许可`：

- `允许实现`：需求、设计、任务计划和本轮范围都已确认，且没有新的范围变化。
- `只允许补文档`：用户要求补需求、设计、任务、字段映射、业务口径或公共文档影响，或者当前范围变化需要先沉淀文档。
- `需要先设计`：出现新增架构层、数据加工层、接口边界、表、外部系统、性能/权限/数据策略或技术路线取舍。
- `需要任务拆解`：方案已确认但新范围还没有任务、验证点和文档漂移检查。
- `需要用户确认`：出现既有授权和材料未覆盖的新业务规则、实质架构取舍、契约冲突或范围变化；只阻塞依赖缺失决定的动作。按已确认原义整理文档或任务本身不使旧授权失效。
- `回到入口帮助`：用户只是在问现在该怎么做，尚未进入明确 workflow。

如果当前阶段尚不允许实现，记录具体未满足前置条件或授权范围；不把“先做需求/设计”一律写成整体授权失效。沿 FLOW-01/02 补齐已授权的阶段，前置条件满足就继续；真实缺失决定或权限才请求用户。仅讨论/仅需求到约定终点停止。

命中范围变化熔断时，不得把专家选择结果当作编码许可；专家只能帮助补齐需求、设计、任务或确认点。

## 文件查找顺序

优先使用业务项目内的专家依赖文件；找不到时使用插件内置版本，不要直接放弃专家路由。

1. 项目根目录：`BUNDLES.md`、`EXPERTS.lock.md`。
2. 项目规范目录：`specs/global/BUNDLES.md`、`specs/global/EXPERTS.lock.md`。
3. 插件内置 fallback：相对当前 skill 目录读取 `../../BUNDLES.md`、`../../EXPERTS.lock.md`、`../../EXPERT-READINESS.md`。

如果三个位置都不可用，才说明无法读取专家依赖文件，并退化为当前 agent 的专家视角。

## 自动 Bundle 选择

| 信号 | Bundle |
| --- | --- |
| 通用产品/流程/QA 功能 | `company-core-delivery` |
| 中文周会、汇报、方案与评审成稿或精简（不含单句润色） | `company-document-writing` |
| Java、Spring、JVM、事务、持久化 | `company-backend-java` |
| Python 服务、自动化、异步任务 | `company-python-service` |
| Django、DRF、Celery、ORM | `company-django-service` |
| React、Next、Vue、TypeScript UI、浏览器行为 | `company-frontend-delivery` |
| LLM、RAG、prompt、agent workflow、AI Provider API | `company-ai-feature` |
| 紧急生产问题或回滚敏感缺陷 | `company-hotfix` |
| 可行性实验或不熟悉技术选择 | `company-spike` |
| 技能更新、专家依赖更新、自进化提案 | `company-skill-governance` |
| 用户不知道从哪里开始、需要推荐说法或专家就绪检查 | `company-workflow-entry` |
| 旧项目接入、上下文索引草稿或首次流程试点 | `company-legacy-onboarding` |

多个 bundle 都匹配时，选择承担当前阶段最大风险的 bundle。只有必要时添加一个辅助专家。

## 专家映射

| 触发 | 专家 |
| --- | --- |
| 产品范围、用户故事、优先级、AC 质量 | `product-manager` |
| 中文周会、汇报、方案与评审成稿或精简（不含单句润色） | `company-document-writing` |
| 业务流程、指标、报表、政策、审批、状态流转 | `business-analyst` |
| 开放想法有多个方向 | `superpowers:brainstorming` |
| LLM、RAG、prompt、agent workflow、AI 安全、Provider API | `ai-product` |
| Java/Spring 后端、事务、并发、JVM 行为 | `java-pro` |
| Python 运行时、异步、工具链、API | `python-pro` 或 `python-patterns` |
| Django、DRF、Celery、Channels、ORM | `django-pro` |
| React、Next、Vue、前端状态、可访问性 | `frontend-developer` |
| TypeScript 类型、模块边界、monorepo | `typescript-expert` |
| 视觉质量、设计系统、响应式或视觉回归 | `frontend-design` |
| 测试策略、QA gate、回归覆盖 | `testing-qa` |
| 浏览器自动化或 E2E 验证 | `webapp-testing` |
| 对抗式审查、极端输入、异常状态、上线前反例验证 | `testing-qa`，涉及浏览器时加 `webapp-testing` |
| 第一性原理架构推导、跨边界方案或根因事实链 | 当前技术栈专家 + `testing-qa` |
| 用户需要工作流入口指导 | `company-workflow-help` |
| 用户需要确认专家依赖是否已安装、审查或暴露 | `company-expert-readiness` |
| 旧项目接入或项目上下文草稿审查 | `company-legacy-project-onboarding` |
| 技能更新、比对、安全审查、确认和应用 | `company-skill-upgrade-runner` |
| 根因不清、 flaky 测试、回归、卡死 | `superpowers:systematic-debugging` |
| 非平凡行为实现或易出错逻辑 | `superpowers:test-driven-development` |

## 不路由

- 文案、标签、字段或单行配置等简单改动。
- 当前工作流已有足够本地证据。
- 没有具体不一致时，不用专家重新打开已确认需求。
- 专家建议必须服从 INDEX 和当前需求已确认的目标使用终端；专家原文中的通用响应式、移动端或设备覆盖建议不构成产品需求，未确认前不得自行增加移动端适配或执行相关建议。

## 透明度分级判定

本 skill 必须自动选择透明度级别：

- `light`：默认模式。专家真实可调用、风险较低、专家只作为辅助校验时使用。
- `full-audit`：命中以下任一条件时自动启用：
  - 任一专家、Superpowers、MCP、浏览器或插件能力只是 `未调用但采用视角`。
  - `BUNDLES.md`、`EXPERTS.lock.md`、`EXPERT-READINESS.md` 三类依赖信息缺失或来源异常。
  - 安全审查、专家依赖更新、技能升级或自进化提案。
  - 官方文档无法确认变化快的 API。
  - 第一性原理检查发现核心假设未验证，或对抗式审查发现未覆盖的高风险反例。
  - 涉及生产、数据、权限、架构、性能或安全风险。
  - 用户要求审计、复核流程或确认是否真实调用。

如果启用 `full-audit`，必须在内部执行记录中保存触发原因和 `Workflow Audit`；用户明确索要时再提供审计内容。


## 人类优先输出

先读取 `../../specs/global/assets/human-output-standard.md`，同时尊重项目已确认的读者和交付用途。保留一句话结论和下一步建议；用中文解释结果、依据和影响。以下输出/报告中的内部字段写入已有执行记录，不默认附在用户回复或人类文档中。

### 回复契约门禁

发送前按共享规范复核事实范围、前置条件、责任方、授权、读者及显示效果。普通问答不套固定标题；用户需要详细解释时补充有用依据。未通过阅读检查先重写再发送。
## 输出

- 工作流层：`company-expert-routing`
- 透明度模式：
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
- 阶段许可：
- 实现授权状态：
- 选择的 bundle：
- 使用的专家：
- 原因：
- `EXPERTS.lock.md` 来源状态：
- `EXPERT-READINESS.md` 状态：
- 结果：
- 已检查的官方文档：
- Workflow Audit（仅 full-audit 时输出）：

## 文档翻译补充路由

客户手册、技术或业务文档的翻译、双语审校使用 `company-document-translation` / `professional-translation`；短句不强制进入。旧项目 BUNDLES/EXPERTS 已存在但缺少此新增条目时，读取插件内置条目补充，不把旧表缺项解释为技能不存在，也不覆盖项目定制。项目明确禁用或限制优先。此路由仅处理文档，不授予业务代码变更或发布权限。

## 汇报与评审补充路由

中文周会、汇报、方案与评审成稿或精简使用 `company-document-writing`。单句文案不强制路由；业务事实沿用已核实材料，只有口径确有疑义时增加 `business-analyst`。项目旧BUNDLES/EXPERTS缺新增条目时读取插件内置条目，保留项目明确限制与定制。内部写作核对和修订由执行者完成，不新增审批表或用户阶段口令。此路由不授予业务修改、发送或发布权限。
