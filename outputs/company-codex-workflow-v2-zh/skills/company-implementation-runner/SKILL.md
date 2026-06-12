---
name: company-implementation-runner
description: Use when company requirements, design, and task plan are confirmed and Codex should implement feature work or approved change requests.
---

# 公司实现执行器

## 目的

编排 Codex 实现工作，复用 Superpowers TDD 和验证纪律，不重复书写测试规则。

## 工作流

1. 确认需求、设计和任务计划存在，`/hotfix` 或 `/spike` 除外。
2. 识别下一个任务及其验证方式。
3. 非平凡行为变更或易出错逻辑使用 `test-driven-development`。
4. 实现依赖框架内部、类型、性能、并发、数据建模或 UI 质量时，使用 `company-expert-routing`。
5. 做范围内的最小改动。
6. 完成声明前使用验证纪律。
7. 运行验证；项目使用进度文档时同步更新。

## 完成报告

- 完成任务：
- 变更文件：
- 验证：
- 进度文档更新：
- 剩余风险：

## 边界

不得实现未进入已确认任务计划的工作，除非用户明确批准扩展范围。

