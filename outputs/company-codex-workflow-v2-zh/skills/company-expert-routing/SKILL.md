---
name: company-expert-routing
description: Use when a company workflow needs to decide whether an expert skill, subagent review, official documentation, or current-agent expert lens should be used.
---

# 公司专家路由

## 目的

集中管理 bundle 和专家选择，避免各工作流重复维护路由表。

## 路由方法

1. 判断任务是否复杂到需要 bundle 或专家。
2. 阅读 `BUNDLES.md`，根据请求、spec、文件路径和技术栈选择最小匹配 bundle。
3. 使用外部专家 skill 前，检查 `EXPERTS.lock.md` 的来源、pin、状态和审查说明。
4. 在选中 bundle 内，只使用当前阶段需要的专家。
5. 如果专家已安装为 Codex skill，在触发条件匹配时使用。
6. 如果支持多 agent 且问题复杂，派发聚焦专家审查。
7. 如果没有可用 skill 或 subagent，明确使用专家视角并说明没有单独专家可用。
8. 对变化快的 API，优先当前官方文档或本地包文档。

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
| 用户不知道从哪里开始或需要推荐说法 | `company-workflow-entry` |
| 旧项目接入、上下文索引草稿或首次流程试点 | `company-legacy-onboarding` |

多个 bundle 都匹配时，选择承担当前阶段最大风险的 bundle。只有必要时添加一个辅助专家。

## 专家映射

| 触发 | 专家 |
| --- | --- |
| 产品范围、用户故事、优先级、AC 质量 | `product-manager` |
| 业务流程、指标、报表、政策、审批、状态流转 | `business-analyst` |
| 开放想法有多个方向 | `brainstorming` |
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
| 旧项目接入或项目上下文草稿审查 | `company-legacy-project-onboarding` |
| 技能更新、比对、安全审查、确认和应用 | `company-skill-upgrade-runner` |
| 根因不清、 flaky 测试、回归、卡死 | `systematic-debugging` |
| 非平凡行为实现或易出错逻辑 | `test-driven-development` |

## 不路由

- 文案、标签、字段或单行配置等简单改动。
- 当前工作流已有足够本地证据。
- 没有具体不一致时，不用专家重新打开已确认需求。

## 输出

- 选择的 bundle：
- 使用的专家：
- 原因：
- `EXPERTS.lock.md` 来源状态：
- 结果：
- 已检查的官方文档：
