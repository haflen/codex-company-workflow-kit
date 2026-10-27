# 专家技能依赖锁

本文件记录公司工作流信任的外部专家技能、来源、风险、bundle 影响面和回滚信息。

## 上游来源

- 仓库：`sickn33/antigravity-awesome-skills`
- URL：https://github.com/sickn33/antigravity-awesome-skills
- README 观察版本：`V20.0.0`
- README 观察规模：`2,750+` skills
- Codex 安装方式：强依赖专家已 vendored 到本公司插件 `skills/` 目录；不要求用户逐个运行外部安装命令。
- 代码许可：MIT
- 原始非代码内容许可：CC BY 4.0，除非上游有更具体声明
- 清单：`skills_index.json`
- 当前 vendored pin：`6d4ea18320984083107f07ff69587fa355ee94c0`
- 候选 commit 日期：2026-10-24 (v20.0.0)
- 审查日期：2026-10-26

注意：README 和 package 元数据可能漂移。当前公司插件固定使用本仓库随包内置副本；后续更新必须走 `company-skill-maintenance` 和自动/人工复核。


The default pin applies to all 13 AAS experts. product-manager is authorized for noncommercial use only; see its LICENSE/PROVENANCE and the dated adoption record.

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

The table below records prior baseline decisions. The dated adoption record below governs current pins and the product-manager noncommercial restriction; historical approval labels do not override that scope.


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
| `typescript-expert` | `skills/typescript-expert` | framework | high | 内置审查通过，脚本运行前审批 | 上游标记 critical；包含诊断脚本且使用 shell 执行固定命令，作为类型和模块边界专家使用。 |
| `frontend-design` | `skills/frontend-design` | front-end | medium | 内置自动审查通过 | 用于 UI 质量和视觉正确性；仍遵守公司/项目 UI 规范。 |
| `testing-qa` | `skills/testing-qa` | workflow-bundle | safe | Pilot 批准 | 用于 QA 策略和 gate。 |
| `webapp-testing` | `skills/webapp-testing` | test-automation | medium | 内置审查通过，脚本运行前审批 | Helper script 含命令白名单、禁 shell 元字符和项目目录限制；运行前仍需遵守 sandbox/审批。 |
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
| 2026-06-29 | 13 个 vendored 专家 | 同步上游 `sickn33/antigravity-awesome-skills@e0ef87efd0ad`；保留 Codex 化触发 description，更新正文和配套资源 | 通过静态审查；纯 Markdown 为 safe/medium，`typescript-expert`/`webapp-testing` 脚本运行前审批 | 回退本次 commit 或恢复上一版 vendored `skills/<expert>` 目录 |

## professional-translation — company-maintained adaptation

This expert is not from the AAS catalog above. Local path: `skills/professional-translation`. Reference: `Tasdax123/claude-fidelity-translator`, commit `c9f0651b007b547bdfae103235a4567fa1acd75e`, MIT; reviewed 2026-10-11. Only the scoped Codex Markdown protocol is included, with upstream license and PROVENANCE.md; no upstream scripts, model/API dependency or automatic parallel execution. Risk: low for this reviewed artifact. Required bundled expert; missing skill blocks installation. Version follows the company plugin.

### 2026-10-14 local incremental-path revision

professional-translation: company-authored conditional Markdown incremental path, full workflow retained for missing/unreliable baselines, complex or conflicting edits, full-review requests and DOCX/PDF/image/layout work. Mechanism reference dsh-translate-docs at reviewed commit prefix d74326738864; no code import or new runtime. See skill PROVENANCE.md and CW-AUTO-20261007/T-041–T-043. Existing upstream pin/license and bundle membership unchanged. Local package version 0.2.39-rc.3.

## company-document-writing — company-authored writing capability

Required bundled expert for `company-document-writing`, package 0.2.39-rc.9. Internal isolated candidate 0.7; no upstream repository or external runtime. SKILL.md SHA256 `3f6c12205b056783ed8826d5a01e7ca3d81e0234f4aebe039fed7e5f50c5f793`. Pure Markdown guidance and examples, plus Codex display metadata; low execution risk. Limited writing validation does not guarantee reader acceptance. See `skills/company-document-writing/PROVENANCE.md`.

## 2026-10-26 approved local upgrade

- Package: 0.2.39-rc.15. All 13 AAS experts use v20.0.0 at `6d4ea18320984083107f07ff69587fa355ee94c0`.
- User approved the reviewed 12-expert update and readiness correction, source adoption and Chinese plugin installation/loading verification. No commit, push or publication.
- User additionally approved product-manager for noncommercial use only after the license conflict was explained. Effective license CC BY-NC-SA 4.0; original LICENSE at initial commit `bedf44d06159e37d99e4f11c591761c7f70e96ec` is bundled, with provenance. The catalog's MIT label is not accepted as commercial permission.
- Source overrides in the readiness script record the product-manager license/scope separately. Personal workflow and Superpowers remain unchanged.
- Upstream risk labels are preserved separately from review/adoption authority. Existing two Python helpers updated; no new runtime or executable dependency. Scripts remain subject to source review, actual task authorization and sandbox rules.
- Local triggers, names, bundles and company safeguards preserved; TypeScript handoff/fallback examples adapted to available tools and to preserve failed checks.
- Prior baseline: e0ef87efd0ad5a18a23e21bb08406b3eaf563b35. Exact changes, tests, before/after hashes and rollback originals are under Workflow/执行记录/全技能审查升级-20261026/正式应用.
- Static readiness is not security approval. Installation and actual loading are confirmed only by separately recorded runtime evidence.
