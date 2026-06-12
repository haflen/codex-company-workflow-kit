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
4. 如果想法有多个方向，或用户仍在探索，使用 `brainstorming`。
5. 编写 Given-When-Then 验收标准。
6. 需求阶段结束后停止，除非用户明确给出设计交接口令。

## 产物

使用 `specs/global/assets/requirements-template.md`。小需求可保存到 `specs/features/<feature>/requirements.md`。

## 边界

需求工作不得修改实现代码，也不要规定过细的底层架构。

