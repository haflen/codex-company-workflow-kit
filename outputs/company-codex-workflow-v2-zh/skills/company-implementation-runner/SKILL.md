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
3. 默认显式叠加 `superpowers:test-driven-development`；先定义最小失败案例或最小验证锚点，再写实现。
4. 实现依赖框架内部、类型、性能、并发、数据建模或 UI 质量时，使用 `company-expert-routing`。
5. 做范围内的最小改动。
6. 完成声明前显式叠加 `superpowers:verification-before-completion`。
7. 运行验证；项目使用进度文档时同步更新。

## Superpowers 叠加

- 默认：`superpowers:test-driven-development` + `superpowers:verification-before-completion`。
- 有自动测试框架时：先写或定位失败测试，确认失败符合预期，再做最小实现。
- 没有自动测试框架时：先定义最小复现步骤、最小输入输出、最小页面路径、截图检查或手工验证清单。
- 只有纯文案、注释或无行为小改动时，可以不叠加 TDD，但仍必须叠加完成前验证，并说明原因。

## 完成报告

- 工作流层：`company-implementation-runner`
- Superpowers 叠加：
- 执行策略：
- 最小失败案例或验证锚点：
- 完成任务：
- 变更文件：
- 验证：
- 进度文档更新：
- 剩余风险：

## 边界

不得实现未进入已确认任务计划的工作，除非用户明确批准扩展范围。
