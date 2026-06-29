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
5. L2/L3 或业务规则复杂时，补充第一性原理检查：核心假设、不可破坏约束、最小成立条件。
6. 编写 Given-When-Then 验收标准，并至少列出关键反例或异常场景。
7. 需求阶段结束后停止，除非用户明确给出设计交接口令。

## Superpowers 叠加

- L0 轻量探讨：默认叠加 `superpowers:brainstorming`，只输出目标、方案选项、风险、待确认问题和下一步建议。
- L2 标准需求：默认叠加 `superpowers:brainstorming`，用于澄清意图、比较路径和收敛验收标准。
- 需求已经很明确时：可以不叠加，但输出必须写明 `Superpowers 叠加：无，原因：需求边界已明确`。

## 产物

使用需求模板时按以下顺序查找：

1. 项目内：`specs/global/assets/requirements-template.md`。
2. 插件内置 fallback：相对当前 skill 目录读取 `../../specs/global/assets/requirements-template.md`。

小需求可保存到 `specs/features/<feature>/requirements.md`。如果用户明确只想轻量探讨方案，不要强制落正式需求文档；可以只输出目标、方案选项、风险、待确认问题和下一步建议。

## 边界

需求工作不得修改实现代码，也不要规定过细的底层架构。

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
- 下一步建议：
