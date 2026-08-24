---
name: company-workflow-health-check
description: Use when a company project needs to diagnose workflow installation health, project bootstrap completeness, template freshness, plugin exposure, or why company workflow skills and templates are not working as expected.
---

# 公司工作流健康检查

## 目的

用只读方式判断一个公司项目是否已经正确接入 Codex 工作流，尤其适合旧项目、半初始化项目、模板缺失、插件升级后未同步、或用户反馈“明明装了但用起来不对”的场景。

## 与相邻技能的区别

- `company-workflow-help` 判断“当前该走哪条 workflow”。
- `company-expert-readiness` 判断“专家 skill 是否安装、审查、暴露和可调用”。
- `company-workflow-health-check` 判断“项目级工作流环境是否健康”：根文件、模板、索引、旧规则残留、版本漂移、诊断证据和修复命令。

## 工作流

1. 只读检查项目根目录，不修改业务代码或项目文档。
2. 检查根目录文件：`AGENTS.md`、`BUNDLES.md`、`EXPERTS.lock.md`。
3. 检查索引和模板：`specs/global/INDEX.md`、`specs/global/assets/`。
4. 检查关键模板是否存在：requirements、business-rules、design、api-contract、tasks、spike、hotfix、change-request、public-doc-update、quality-validation-report、skill-upgrade、workflow-health-report。
5. 检查 `.codex-workflow/asset-boundaries.json`、`asset-boundaries.generated.json`、本地校验器和确认状态；运行 changed 检查，用户要求全量审计时再运行 `audit-assets`。待审候选存在时标记为 `yellow`，新增/移动工程资产前必须采纳或明确丢弃。
6. 配置缺失为 `yellow`；已确认配置下出现阻断项为 `red`。草案状态本身不阻断试点，但复杂设计/实现前应确认工程根和例外。
7. 检查项目是否包含最新规则标记：Superpowers 可见叠加、第一性原理、对抗式审查、业务规则与计算口径、方案对比、多分支公共文档协议、阶段一致性预检、验证等级、触发式独立质量验收、文档漂移。
8. 检查是否存在旧规则或旧来源残留；如存在，标记为迁移风险，不自动删除。
9. 检查当前分支、公共文档边界和阶段一致性：入口页、`INDEX.md`、当前 version/feature README、任务文档是否指向同一阶段。
10. 发现入口页仍指向 spike/待办、但当前任务文档已进入正式实现时，标记为 `yellow` 或 `red`，并建议先修 public-doc patch 或入口路由。
11. 检查 `company-quality-validation` 是否暴露，AGENTS/BUNDLES 是否包含触发规则，项目是否有验收报告模板；需要验收但缺少结论或证据时标记为 `red`。
12. 对已存在的质量验收报告检查：是否位于权威任务文档同级或已登记路径，是否包含当前分支、HEAD、被验收路径、diff SHA-256、未跟踪文件哈希；候选指纹过期或条件通过缺少接受记录时标记为 `red`。
13. 如发现模板缺失或旧版本，给出安全修复命令；默认推荐 `update-templates`，不要直接覆盖用户文档。

## 目标终端检查

- 检查 INDEX 是否存在已确认的目标使用终端基线，以及需求、设计和任务是否一致继承。
- UI 项目缺少终端基线为 `yellow`；实现或测试包含未授权终端适配为 `red`。不得自行增加移动端适配作为修复手段。
- 健康检查只报告缺口和修复入口，不替用户确认产品支持范围。

## 健康等级

- `green`：核心文件、索引、模板和关键规则齐全；可以正常走 workflow。
- `yellow`：可工作，但存在模板缺失、旧规则残留、版本漂移或公共文档边界不清；建议先修复再进入复杂交付。
- `red`：缺少 `AGENTS.md`、`BUNDLES.md`、`EXPERTS.lock.md` 或 `specs/global/INDEX.md` 中任意关键入口；复杂任务不应继续。

## 修复建议规则

- 只缺模板：推荐 `bash scripts/install.sh update-templates <project-path> --lang zh`。
- 缺项目工作流入口：推荐 `bash scripts/install.sh bootstrap-project <project-path> --lang zh`。
- 插件缺失或技能不暴露：推荐先重新安装插件，再重启 Codex。
- 旧项目规则残留：推荐生成迁移清单，由用户确认后再整理，不自动删除。


## 人类优先输出

最终回复先使用：`一句话结论`、`这次完成了什么`、`需要你注意什么`、`你现在需要做什么`。用业务结果和用户影响表达，只给一个主要下一步；首次出现的内部术语必须解释。随后把 Superpowers、专家调用、命令、路径、哈希、验证证据和内部 workflow 字段放入 `技术审计附录`，不得把内部 workflow 字段逐项倾倒到人类摘要，也不得用审计字段代替人类摘要。


### 回复契约门禁

- 触发范围：本轮正式完成或阶段收尾、用户明确索要进度总结、阻塞结论或下一步方案，以及包含审计字段的成段回复。
- 1-2 句的工作中更新和普通问答始终不触发固定格式，即使提到当前结果、风险或下一步；但不得在轻量回复中附带完整审计明细。
- 用户要求“详细一点”时，只增加四段正文或 `技术审计附录` 的深度，不得删除、改名或调换四个标题。
- 审计字段只能出现在 `技术审计附录`，不得与四段人类摘要并列或抢在其前。
- 发送前检查四个标题是否齐全且顺序正确、风险是否翻译为实际影响、是否只有一个主要下一步；任一不满足时先重写再发送。

## 输出格式

- 工作流层：`company-workflow-health-check`
- 透明度模式：`full-audit`
- Superpowers 叠加：通常无；如果需要设计修复方案，可叠加 `superpowers:brainstorming`
- 实际调用：
- 专家/插件能力：
- 未调用但采用视角：
- 第一性原理检查：判断最小可用条件是什么
- 对抗式审查：旧项目、旧规则、半初始化、分支并行、插件未刷新等反例
- 健康等级：green / yellow / red
- 已检查文件：
- 缺失项：
- 版本或模板漂移：
- 公共文档边界：
- 阶段一致性预检：
- 独立质量验收接入与证据状态：
- 质量验收报告路径、候选指纹与条件接受记录：
- 本轮建议权威文档：
- 外部专家状态：
- 资产边界状态、检查范围和违规项：
- 建议修复命令：
- 不建议自动处理：
- 验证证据：
- 未验证项：
- 下一步建议：

## 边界

不要在健康检查中直接修复项目，除非用户明确要求“按建议修复”。

不要因为项目能运行就判定 workflow 健康；本技能判断的是 Codex 工作流接入状态，不是业务系统运行状态。

## 文档质量门禁

创建或实质修改正式文档前，先读取项目内 `specs/global/assets/document-standard.md`；缺失时读取插件内置 `../../specs/global/assets/document-standard.md`。本 skill 负责逐项检查 `DOC-G01`、`DOC-G02`、`DOC-G03`、`DOC-G04`、`DOC-G05`、`DOC-G06`、`DOC-G07`、`DOC-G08`、`DOC-G09`、`DOC-G10`、`DOC-G11`、`DOC-G12`。逐项诊断模板、正式文档和豁免记录，不使用行数或章节数作为替代标准。
