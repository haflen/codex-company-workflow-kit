---
name: company-implementation-runner
description: Use when company requirements, design, and task plan are confirmed and Codex should implement feature work or approved change requests.
---

# 公司实现执行器

## 目的

编排 Codex 实现工作，复用 Superpowers TDD 和验证纪律，不重复书写测试规则。

## 工作流

1. 确认需求、设计和任务计划存在，`/hotfix` 或 `/spike` 除外；如任务涉及 `business-rules.md`，必须读取规则文档。
2. 识别下一个任务及其验证方式。
3. 默认显式叠加 `superpowers:test-driven-development`；先定义最小失败案例或最小验证锚点，再写实现。
4. 实现依赖框架内部、类型、性能、并发、数据建模或 UI 质量时，使用 `company-expert-routing`。
5. 做范围内的最小改动。
6. 完成声明前执行对抗式审查，覆盖极端输入、异常状态、权限、并发、性能或 UI 渲染风险中与本任务相关的场景。
7. 完成声明前显式叠加 `superpowers:verification-before-completion`。
8. 自动判定验证等级 `V0/V1/V2/V3`，选择足够但不过度的验证证据。
9. 检查文档漂移：实现是否改变需求、业务规则、技术设计、API 契约、任务计划、项目入口或索引。
10. 运行验证；项目使用进度文档时，根据当前分支策略更新：集成分支可同步公共入口，业务分支写 `docs/public-doc-updates/<branch-or-feature>.md`。

## Superpowers 叠加

- 默认：`superpowers:test-driven-development` + `superpowers:verification-before-completion`。
- 有自动测试框架时：先写或定位失败测试，确认失败符合预期，再做最小实现。
- 没有自动测试框架时：先定义最小复现步骤、最小输入输出、最小页面路径、截图检查或手工验证清单。
- 只有纯文案、注释或无行为小改动时，可以不叠加 TDD，但仍必须叠加完成前验证，并说明原因。

## 验证等级

- `V0`：纯文档、注释、格式或无行为变更；检查 diff 和目标文件即可。
- `V1`：单点低风险小改动；执行聚焦命令、局部测试或最小手工路径。
- `V2`：默认功能实现；执行相关测试、类型/构建检查和必要的浏览器/手工验证。
- `V3`：生产、权限、安全、数据、性能、金额/指标公式、跨系统或 hotfix；执行回归、对抗场景和回滚/恢复说明。

不得为了省时间把 V2/V3 降级到 V1；也不要把 V0/V1 小改动强行全量验证。

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
- 验证等级：
- 验证证据：
- 文档漂移影响：
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

如果实现过程中发现操作逻辑、计算公式、字段口径、状态流转或异常处理缺失，不要自行猜测；停止实现并回到 `company-feature-requirements` 补齐 `business-rules.md`。

非集成分支不要把未合并结果直接写入 `说明文档.md` 的当前状态；如需记录公共入口变化，写公共文档影响补丁。

如果实现改变了文档承诺但未同步，完成报告必须写明 `文档漂移影响`，并说明是已补齐、需用户确认，还是待后续公共文档补丁处理。
