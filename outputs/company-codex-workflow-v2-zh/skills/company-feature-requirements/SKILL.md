---
name: company-feature-requirements
description: Use when a company project needs feature requirements, acceptance criteria, scope clarification, or change-request requirements before technical design or implementation.
---

# 公司功能需求澄清

## 目的

产出可进入技术设计的目标、范围、验收标准和边界条件。

## 工作流

1. 使用 `company-context-index` 建立上下文。
2. 澄清目标、用户、范围内、范围外、依赖和风险。
3. 需求复杂时使用 `company-expert-routing`，由它从 `BUNDLES.md` 自动选择组合。
4. 如果想法有多个方向，或用户仍在探索，显式使用 `superpowers:brainstorming`。
5. 判断是否需要独立业务规则文档。只有命中触发条件时才创建或更新 `business-rules.md`，小需求不要强制增加文档。
6. L2/L3 或业务规则复杂时，补充第一性原理检查：核心假设、不可破坏约束、最小成立条件。
7. 编写 Given-When-Then 验收标准，并至少列出关键反例或异常场景。
8. 用户希望在需求阶段验证页面、交互、文案或模拟状态时，路由到 `company-requirements-prototype`；原型反馈改变需求时，先更新权威需求或 `business-rules.md`，再继续原型。
9. 需求阶段结束后停止。原型确认只允许转为需求基线；除非用户明确给出设计交接口令，否则不得进入技术设计，更不得创建任务。

## Superpowers 叠加

- L0 轻量探讨：默认叠加 `superpowers:brainstorming`，只输出目标、方案选项、风险、待确认问题和下一步建议。
- L2 标准需求：默认叠加 `superpowers:brainstorming`，用于澄清意图、比较路径和收敛验收标准。
- 需求已经很明确时：可以不叠加，但输出必须写明 `Superpowers 叠加：无，原因：需求边界已明确`。

## 产物

使用需求模板时按以下顺序查找：

1. 项目内：`specs/global/assets/requirements-template.md`。
2. 插件内置 fallback：相对当前 skill 目录读取 `../../specs/global/assets/requirements-template.md`。

业务规则模板按以下顺序查找：

1. 项目内：`specs/global/assets/business-rules-template.md`。
2. 插件内置 fallback：相对当前 skill 目录读取 `../../specs/global/assets/business-rules-template.md`。

小需求可保存到 `specs/features/<feature>/requirements.md`。如果用户明确只想轻量探讨方案，不要强制落正式需求文档；可以只输出目标、方案选项、风险、待确认问题和下一步建议。

## 业务规则文档触发条件

命中以下任一条件时，需求阶段必须生成或更新 `business-rules.md`，并在需求文档中链接它：

- 指标、金额、评分、排序、权重、汇总、折算、预测、分摊或任何公式。
- 状态机、审批流、任务流、角色差异、权限规则或操作分支。
- 字段来源、单位、精度、舍入、映射、口径、数据字典或跨系统数据一致性。
- 缺失数据、异常值、边界值、批量处理、重复提交、并发操作或冲突处理。
- 用户提到“公式、口径、逻辑、规则、计算、操作流程、状态变化、指标释义”。

如果都不命中，输出写明：`业务规则文档：不需要，原因：...`。

## 边界

需求工作不得修改生产实现代码，也不要规定过细的底层架构。只有 `company-requirements-prototype` 可以在 `.codex-workflow/prototypes/<feature>/draft/` 修改隔离、模拟数据的需求原型；生产源码仍禁止修改。

## 目标终端门禁

- UI、交互或客户端功能必须先读取 `specs/global/INDEX.md` 的目标使用终端基线，并确认本功能是继承还是例外。
- 需求至少明确支持终端、是否共用页面/代码/API、最小视口、浏览器、输入方式，以及是否需要响应式、触摸和移动端验证。
- 未确认的终端视为不支持；不得自行增加移动端适配、移动断点、触摸交互、移动截图或移动 E2E。
- 仅后端、任务或接口功能可以写“无直接终端差异”，不要为了填模板制造多端要求。

## 人类优先输出

最终回复先给人类摘要，再给技术审计附录：

1. 一句话结论：用业务语言说明需求是否清楚。
2. 这次完成了什么：只列已澄清的目标、范围和决策。
3. 需要你注意什么：把待确认事项及其影响说清楚。
4. 你现在需要做什么：只给一个主要下一步和一句简短回复。

随后使用 `技术审计附录` 承载下面的内部字段。首次出现的缩写和等级必须解释；不得把内部 workflow 字段逐项倾倒到人类摘要。

## 输出格式

- 工作流层：`company-feature-requirements`
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
- 需求结论：
- 方案选项：
- 风险和待确认问题：
- 核心假设和反例场景：
- 业务规则文档判定：
- 业务规则文档：
- 下一步建议：

## 文档质量门禁

创建或实质修改正式文档前，先读取项目内 `specs/global/assets/document-standard.md`；缺失时读取插件内置 `../../specs/global/assets/document-standard.md`。本 skill 负责检查 `DOC-G01`、`DOC-G02`、`DOC-G05`、`DOC-G06`、`DOC-G07`、`DOC-G08`、`DOC-G09`、`DOC-G10`、`DOC-G11`、`DOC-G12`。命中复杂业务规则时同时执行 `DOC-G04`。
