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
4. 复杂计划使用 `writing-plans` 风格的可执行拆解。
5. 任务边界不清、跨团队或依赖复杂技术栈细节时，使用 `company-expert-routing`。
6. 任务规划阶段结束后停止，除非用户给出实现交接口令。

## 产物

使用任务模板时按以下顺序查找：

1. 项目内：`specs/global/assets/tasks-template.md`。
2. 插件内置 fallback：相对当前 skill 目录读取 `../../specs/global/assets/tasks-template.md`。

## 好任务标准

- 足够小，可以在一次聚焦实现中完成。
- 有具体验证命令或手工检查。
- 不把无关重构混入功能交付。
