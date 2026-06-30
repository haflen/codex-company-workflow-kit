---
name: company-feature-planning
description: Use when company requirements and technical design are confirmed and the work needs an implementation task plan with verification points.
---

# 公司功能任务拆解

## 目的

把已确认的需求和设计拆成可执行任务，并为每个任务标注验证点。

## 工作流

1. 确认需求和设计已可用。
2. 跨边界工作确认 API 契约已存在。
3. 将工作拆成小任务，每个任务都包含验证方式。
4. 复杂计划显式叠加 `superpowers:writing-plans`，输出可执行计划和检查点。
5. 每个非平凡任务都包含最小失败案例或验证锚点，并至少包含一个对抗场景。
6. 任务边界不清、跨团队或依赖复杂技术栈细节时，使用 `company-expert-routing`。
7. 如果任务合并后需要更新 `说明文档.md`、`specs/global/INDEX.md` 或阅读路线，增加“公共文档影响补丁”任务，而不是在业务分支直接改公共文档。
8. 任务规划阶段结束后停止，除非用户给出实现交接口令。

## Superpowers 叠加

- L1 小改动：通常不叠加，使用轻量任务卡；如涉及行为变化，则叠加 `superpowers:test-driven-development` 的最小失败案例思路。
- L2/L3 标准或复杂任务：默认叠加 `superpowers:writing-plans`。
- 每个任务必须包含验证点，为后续 `superpowers:test-driven-development` 和 `superpowers:verification-before-completion` 留出执行锚点。

## 产物

使用任务模板时按以下顺序查找：

1. 项目内：`specs/global/assets/tasks-template.md`。
2. 插件内置 fallback：相对当前 skill 目录读取 `../../specs/global/assets/tasks-template.md`。

公共文档影响补丁模板按以下顺序查找：

1. 项目内：`specs/global/assets/public-doc-update-template.md`。
2. 插件内置 fallback：相对当前 skill 目录读取 `../../specs/global/assets/public-doc-update-template.md`。

## 好任务标准

- 足够小，可以在一次聚焦实现中完成。
- 有具体验证命令或手工检查。
- 不把无关重构混入功能交付。

## 输出格式

- 工作流层：`company-feature-planning`
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
- 任务列表：
- 每个任务的最小失败案例或验证锚点：
- 每个任务的对抗场景：
- 公共文档影响任务：
- 实现交接口令：
