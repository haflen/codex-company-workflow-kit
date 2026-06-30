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
6. 完成声明前执行对抗式审查，覆盖极端输入、异常状态、权限、并发、性能或 UI 渲染风险中与本任务相关的场景。
7. 完成声明前显式叠加 `superpowers:verification-before-completion`。
8. 运行验证；项目使用进度文档时，根据当前分支策略更新：集成分支可同步公共入口，业务分支写 `docs/public-doc-updates/<branch-or-feature>.md`。

## Superpowers 叠加

- 默认：`superpowers:test-driven-development` + `superpowers:verification-before-completion`。
- 有自动测试框架时：先写或定位失败测试，确认失败符合预期，再做最小实现。
- 没有自动测试框架时：先定义最小复现步骤、最小输入输出、最小页面路径、截图检查或手工验证清单。
- 只有纯文案、注释或无行为小改动时，可以不叠加 TDD，但仍必须叠加完成前验证，并说明原因。

## 完成报告

- 工作流层：`company-implementation-runner`
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
- 最小失败案例或验证锚点：
- 对抗式审查结果：
- 完成任务：
- 变更文件：
- 公共文档影响：
- 验证：
- 进度文档更新：
- 剩余风险：

## 边界

不得实现未进入已确认任务计划的工作，除非用户明确批准扩展范围。

非集成分支不要把未合并结果直接写入 `说明文档.md` 的当前状态；如需记录公共入口变化，写公共文档影响补丁。
