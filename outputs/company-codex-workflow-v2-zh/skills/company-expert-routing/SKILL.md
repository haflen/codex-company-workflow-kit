---
name: company-expert-routing
description: Use when a company workflow needs to decide whether an expert skill, subagent review, official documentation, or current-agent expert lens should be used.
---

# 公司专家路由

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
7. 如果支持多 agent 且问题复杂，派发聚焦专家审查。
8. 如果专家已随插件安装但当前会话不可见，记录到 `未调用但采用视角`，说明需要新开 Codex 线程刷新技能列表；不要要求用户逐个安装。
9. 对变化快的 API，优先当前官方文档或本地包文档。

## 阶段许可

专家路由不是实现授权。每次路由都必须输出 `阶段许可`：

- `允许实现`：需求、设计、任务计划和本轮范围都已确认，且没有新的范围变化。
- `只允许补文档`：用户要求补需求、设计、任务、字段映射、业务口径或公共文档影响，或者当前范围变化需要先沉淀文档。
- `需要先设计`：出现新增架构层、数据加工层、接口边界、表、外部系统、性能/权限/数据策略或技术路线取舍。
- `需要任务拆解`：方案已确认但新范围还没有任务、验证点和文档漂移检查。
- `需要用户确认`：补文档后产生新契约、字段映射、任务清单或范围变化，旧的实现授权不能继续沿用。
- `回到入口帮助`：用户只是在问现在该怎么做，尚未进入明确 workflow。

如果阶段许可不是 `允许实现`，必须输出 `实现授权状态：已失效，需要用户确认后再编码` 或说明为何本轮没有实现授权。

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

如果启用 `full-audit`，必须输出触发原因和 `Workflow Audit`。


## 人类优先输出

最终回复先使用：`一句话结论`、`这次完成了什么`、`需要你注意什么`、`你现在需要做什么`。用业务结果和用户影响表达，只给一个主要下一步；首次出现的内部术语必须解释。随后把 Superpowers、专家调用、命令、路径、哈希、验证证据和内部 workflow 字段放入 `技术审计附录`，不得把内部 workflow 字段逐项倾倒到人类摘要，也不得用审计字段代替人类摘要。

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
