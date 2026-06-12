# 专家组合

Bundle 是工作流使用的小型专家组合，不是一套新的流程引擎。

工作流应自动选择最小匹配组合。用户仍可在对话中点名专家；显式用户请求优先于默认组合。

## 选择规则

1. 根据用户请求、当前 spec、文件路径和技术栈识别任务类型。
2. 只选择一个主 bundle。
3. 只有当前阶段明确需要时，才增加一个辅助专家。
4. 使用外部专家技能前检查 `EXPERTS.lock.md`。
5. 调试、TDD 和验证优先复用已安装的 Superpowers skills。

## Bundles

| Bundle | 使用场景 | 默认专家 | 可选专家 |
| --- | --- | --- | --- |
| `company-core-delivery` | 通用功能交付，涉及产品、流程和 QA | `product-manager`, `business-analyst`, `testing-qa` | `systematic-debugging`, `test-driven-development` |
| `company-backend-java` | Java/Spring 后端、事务、并发、API、持久化 | `business-analyst`, `java-pro`, `testing-qa` | `systematic-debugging`, `test-driven-development` |
| `company-python-service` | Python 服务、自动化、API、异步任务 | `business-analyst`, `python-pro`, `testing-qa` | `python-patterns`, `systematic-debugging` |
| `company-django-service` | Django、DRF、Celery、Channels、ORM 密集工作 | `business-analyst`, `django-pro`, `testing-qa` | `python-pro`, `webapp-testing` |
| `company-frontend-delivery` | 前端行为、React/Next/Vue、UI 状态、可访问性、浏览器验证 | `product-manager`, `frontend-developer`, `typescript-expert`, `testing-qa` | `frontend-design`, `webapp-testing` |
| `company-ai-feature` | LLM、RAG、prompt、agent workflow、AI 安全、Provider API 设计 | `product-manager`, `ai-product`, `testing-qa` | `python-pro`, `frontend-developer` |
| `company-hotfix` | 紧急生产缺陷或回滚敏感变更 | `systematic-debugging`, `testing-qa` | 匹配故障区域的技术栈专家 |
| `company-spike` | 限时可行性验证、不熟悉库、架构不确定性 | 匹配问题的技术栈专家 | `ai-product`, `webapp-testing`, `testing-qa` |
| `company-skill-governance` | 新增、更新、审查、升级或演进 workflow/expert skills | `company-skill-upgrade-runner`, `company-skill-maintenance`, `company-skill-security-review` | `company-skill-evolution-lab` |
| `company-workflow-entry` | 用户不知道应该从哪个工作流开始 | `company-workflow-help` | `company-expert-routing` |
| `company-legacy-onboarding` | 旧项目接入、项目上下文草稿生成、首次流程试点 | `company-legacy-project-onboarding`, `company-context-index` | `company-workflow-help`, 匹配项目技术栈的专家 |

## 阶段默认值

| 阶段 | Bundle 使用 |
| --- | --- |
| 需求 | 通常使用 `company-core-delivery`；AI 行为是产品本身时使用 `company-ai-feature`。 |
| 设计 | 选择承担主要架构风险的技术栈 bundle。 |
| 规划 | 延续设计阶段 bundle；验证策略不清楚时加入 `testing-qa`。 |
| 实现 | 只有实现选择依赖专家知识时才使用设计阶段 bundle。 |
| Bugfix | 紧急事故使用 `company-hotfix`，普通 bug 使用受影响技术栈 bundle。 |
| Spike | 使用 `company-spike`，输出保持简短并聚焦决策。 |
| 旧项目接入 | 使用 `company-legacy-onboarding`，先完成一个试点任务复盘，再扩大到完整 SDLC。 |
