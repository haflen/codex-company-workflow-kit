---
name: company-implementation-runner
description: Use when company requirements, design, and task plan are confirmed and Codex should implement feature work or approved change requests.
---

# 公司实现执行器

## 目的

编排 Codex 实现工作，复用 Superpowers TDD 和验证纪律，不重复书写测试规则。

## 工作流

1. 确认需求、设计和任务计划存在，`/hotfix` 或 `/spike` 除外；如任务涉及 `business-rules.md`，必须读取规则文档。
2. 执行阶段一致性预检：检查 `说明文档.md`、`specs/global/INDEX.md`、当前 feature/version README、任务文档和相关 public-doc patch 是否一致。
3. 如果预检发现公共入口、索引、版本 README 或任务文档冲突，暂停实现；输出冲突、暂定权威文档和修复建议，等待用户确认或先修文档路由。
4. 识别下一个任务及其验证方式。
5. 默认显式叠加 `superpowers:test-driven-development`；先定义最小失败案例或最小验证锚点，再写实现。
6. 实现依赖框架内部、类型、性能、并发、数据建模或 UI 质量时，使用 `company-expert-routing`。
7. 做范围内的最小改动。
8. 完成声明前执行对抗式审查，覆盖极端输入、异常状态、权限、并发、性能或 UI 渲染风险中与本任务相关的场景。
9. 完成声明前显式叠加 `superpowers:verification-before-completion`。
10. 检查中文代码逻辑备注：业务规则、计算口径、数据映射、异常分支和非显然技术决策必须有必要备注。
11. 自动判定验证等级 `V0/V1/V2/V3`，选择足够但不过度的验证证据。
12. 检查文档漂移：实现是否改变需求、业务规则、技术设计、API 契约、任务计划、项目入口或索引。
13. 运行验证；项目使用进度文档时，根据当前分支策略更新：集成分支可同步公共入口，业务分支写 `docs/public-doc-updates/<branch-or-feature>.md`。

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

## 中文代码逻辑备注

实现涉及 Java、前端 TypeScript/Vue/React、Python、SQL 或脚本时，都按同一标准检查中文备注：

- 必须解释业务规则、状态分支、公式/阈值、精度、数据映射、fallback/隐藏/降级、兼容策略和非显然性能/并发/缓存处理。
- 不写语法翻译类废话备注。
- 阈值、公式或映射来源不清时，不用备注糊弄；回到需求、`business-rules.md` 或设计文档补齐。
- 如果逻辑改变，相关备注也必须同步改变。

## 阶段一致性预检

实现前只做轻量预检，不全量扫描文档。检查：

- 当前分支是否为 main/develop/integration 或业务分支。
- `说明文档.md` 当前阶段是否与任务文档一致。
- `specs/global/INDEX.md` 路由是否指向当前 feature/version。
- 当前 version/feature README 是否已确认进入实现阶段。
- 当前任务文档是否包含已确认任务、任务 ID 和验证点。
- 当前分支是否已有对应 `docs/public-doc-updates/` 补丁。

如果入口页仍写 spike/待办，而当前 version README 已进入正式开发，以当前任务文档作为暂定权威，但必须先修正公共入口影响记录；非集成分支优先写 public-doc patch。

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
- 阶段一致性预检：
- 本轮权威文档：
- 验证等级：
- 验证证据：
- 代码备注检查：
- 备注覆盖点：
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

如果实现包含复杂业务逻辑但没有必要中文备注，不得声称完成；必须补齐备注或说明为什么本次属于低风险自解释代码。
