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

1. 判断任务是否复杂到需要 bundle 或专家。
2. 阅读 `BUNDLES.md`，根据请求、spec、文件路径和技术栈选择最小匹配 bundle。
3. 使用专家 skill 前，检查 `EXPERTS.lock.md` 和 `.codex-workflow/EXPERT-READINESS.md`；强依赖专家应已随公司插件内置。
4. 在选中 bundle 内，只使用当前阶段需要的专家。
5. 如果专家在当前会话已暴露为 Codex skill，在触发条件匹配时直接使用。
6. 如果支持多 agent 且问题复杂，派发聚焦专家审查。
7. 如果专家已随插件安装但当前会话不可见，记录到 `未调用但采用视角`，说明需要新开 Codex 线程刷新技能列表；不要要求用户逐个安装。
8. 对变化快的 API，优先当前官方文档或本地包文档。

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

## 透明度分级判定

本 skill 必须自动选择透明度级别：

- `light`：默认模式。专家真实可调用、风险较低、专家只作为辅助校验时使用。
- `full-audit`：命中以下任一条件时自动启用：
  - 任一专家、Superpowers、MCP、浏览器或插件能力只是 `未调用但采用视角`。
  - `BUNDLES.md`、`EXPERTS.lock.md`、`EXPERT-READINESS.md` 三类依赖信息缺失或来源异常。
  - 安全审查、专家依赖更新、技能升级或自进化提案。
  - 官方文档无法确认变化快的 API。
  - 涉及生产、数据、权限、架构、性能或安全风险。
  - 用户要求审计、复核流程或确认是否真实调用。

如果启用 `full-audit`，必须输出触发原因和 `Workflow Audit`。

## 输出

- 工作流层：`company-expert-routing`
- 透明度模式：
- Superpowers 叠加：
- 实际调用：
- 专家/插件能力：
- 未调用但采用视角：
- 执行策略：
- 验证证据：
- 未验证项：
- 剩余风险：
- 选择的 bundle：
- 使用的专家：
- 原因：
- `EXPERTS.lock.md` 来源状态：
- `EXPERT-READINESS.md` 状态：
- 结果：
- 已检查的官方文档：
- Workflow Audit（仅 full-audit 时输出）：
