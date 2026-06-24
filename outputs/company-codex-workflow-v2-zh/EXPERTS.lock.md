# 专家技能依赖锁

本文件记录公司工作流信任的外部专家技能、来源、风险、bundle 影响面和回滚信息。

## 上游来源

- 仓库：`sickn33/antigravity-awesome-skills`
- URL：https://github.com/sickn33/antigravity-awesome-skills
- README 观察版本：`V12.3.0`
- README 观察规模：`1,527+` skills
- Codex 安装方式：强依赖专家已 vendored 到本公司插件 `skills/` 目录；不要求用户逐个运行外部安装命令。
- 代码许可：MIT
- 原始非代码内容许可：CC BY 4.0，除非上游有更具体声明
- 清单：`skills_index.json`
- 审查日期：2026-06-11

注意：README 和 package 元数据可能漂移。当前公司插件固定使用本仓库随包内置副本；后续更新必须走 `company-skill-maintenance` 和自动/人工复核。

## 策略

- 公司插件安装时必须自动校验所有强依赖专家 skill 是否随包存在。
- 不从 GitHub、npm、ClawHub 类 hub 或自进化结果自动更新。
- 安装期自动执行静态安全审查，生成 `EXPERT-READINESS.md` / `EXPERT-READINESS.json`。
- 新增、更新或自进化 skill 必须经过 `company-skill-security-review`。
- 使用 `company-skill-maintenance` 更新本文件并记录回滚。
- skill 含脚本、shell、网络、浏览器自动化或文件写入时，即使 manifest 标注 setup 为 none，也视为更高风险。

## 推荐安装和固定方式

公司用户无需手工安装专家 skill。公司插件安装和项目初始化会自动完成：

- 插件内置专家完整性检查。
- 静态安全审查和风险标注。
- 项目级 `.codex-workflow/EXPERT-READINESS.md` 就绪报告。
- Codex 当前会话刷新提示。

生产固定方式：

- Git tag：`sickn33/antigravity-awesome-skills@<release-tag>`
- Commit：`https://github.com/sickn33/antigravity-awesome-skills/tree/<commit>/<skill-path>`
- 公司内 vendored copy：复制已审查 skill 到公司受控 plugin，并在此记录来源 release / commit。

不要在生产中直接跟随 `main`，除非团队明确接受上游变动风险。

## 已锁定专家依赖

| Expert | AAS 路径 | 类别 | 风险 | 状态 | 说明 |
| --- | --- | --- | --- | --- | --- |
| `product-manager` | `skills/product-manager` | business | safe | Pilot 批准 | 用于 AC、用户故事、优先级。 |
| `business-analyst` | `skills/business-analyst` | business | safe | Pilot 批准 | 用于业务流程、指标、报表、状态流转。 |
| `ai-product` | `skills/ai-product` | ai-ml | safe | Pilot 批准 | 用于 LLM/RAG/prompt/agent workflow。 |
| `java-pro` | `skills/java-pro` | code | medium | 内置自动审查通过 | Java/Spring 主栈高价值。变化快 API 仍优先查官方文档。 |
| `python-pro` | `skills/python-pro` | code | medium | 内置自动审查通过 | 需结合项目运行时和依赖管理使用。 |
| `python-patterns` | `skills/python-patterns` | development | medium | 内置自动审查通过 | 架构指导较重，建议选择性使用。 |
| `django-pro` | `skills/django-pro` | framework | medium | 内置自动审查通过 | 仅 Django 项目使用。 |
| `frontend-developer` | `skills/frontend-developer` | front-end | medium | 内置自动审查通过 | React/Next 导向，Vue 项目使用时结合项目本地规范。 |
| `typescript-expert` | `skills/typescript-expert` | framework | medium | 内置自动审查通过 | 允许作为类型和模块边界专家调用；高风险迁移仍需 review。 |
| `frontend-design` | `skills/frontend-design` | front-end | medium | 内置自动审查通过 | 用于 UI 质量和视觉正确性；仍遵守公司/项目 UI 规范。 |
| `testing-qa` | `skills/testing-qa` | workflow-bundle | safe | Pilot 批准 | 用于 QA 策略和 gate。 |
| `webapp-testing` | `skills/webapp-testing` | test-automation | medium | 内置自动审查通过 | 用于浏览器/E2E 验证；含 helper script，运行前仍需遵守 sandbox/审批。 |
| `e2e-testing-patterns` | `skills/e2e-testing-patterns` | test-automation | safe | Pilot 批准 | 用于 E2E 策略。 |
| `systematic-debugging` | Superpowers 优先 | debugging | unknown | Prefer Superpowers | AAS 版本仅作 fallback。 |
| `test-driven-development` | Superpowers 优先 | testing | unknown | Prefer Superpowers | AAS 版本仅作 fallback。 |

## Bundle 影响面

| Expert | Bundles |
| --- | --- |
| `product-manager` | `company-core-delivery`, `company-frontend-delivery`, `company-ai-feature` |
| `business-analyst` | `company-core-delivery`, `company-backend-java`, `company-python-service`, `company-django-service` |
| `ai-product` | `company-ai-feature`, `company-spike` |
| `java-pro` | `company-backend-java`, `company-hotfix`, `company-spike` |
| `python-pro` | `company-python-service`, `company-django-service`, `company-ai-feature`, `company-hotfix`, `company-spike` |
| `frontend-developer` | `company-frontend-delivery`, `company-ai-feature`, `company-hotfix`, `company-spike` |
| `testing-qa` | 全部主要交付 bundle |
| `company-skill-upgrade-runner` | `company-skill-governance` |
| `company-skill-security-review` | `company-skill-governance` |
| `company-skill-maintenance` | `company-skill-governance` |
| `company-skill-evolution-lab` | `company-skill-governance` |

## 变更记录

| 日期 | 对象 | 变更 | 审查结果 | 回滚 |
| --- | --- | --- | --- | --- |
| 2026-06-24 | 全部强依赖专家 | 改为随公司插件 vendored 安装，并由安装脚本自动生成安全审查和就绪报告 | 开箱可用；后续更新仍走受控审查 | 回退本文件、移除 vendored expert skill 目录或使用上一版 starter kit |
