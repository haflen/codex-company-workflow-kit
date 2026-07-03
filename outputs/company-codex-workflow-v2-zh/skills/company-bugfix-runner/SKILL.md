---
name: company-bugfix-runner
description: Use when company code behavior differs from requirements, design, acceptance criteria, tests, or documented expectations.
---

# 公司 Bugfix 执行器

## 目的

区分 bug 和需求变更，并完成复现、最小修复和回归验证。

## 工作流

1. 判断这是 bug 还是需求变更。
2. 如果是变更请求，路由回需求/变更规划；如果根因是业务规则、公式、口径或状态流转缺失，先补 `business-rules.md`，再决定是否修代码。
3. 执行阶段一致性预检：确认入口、索引、当前版本/功能文档和 bug 所属任务上下文是否一致。
4. 如果是生产 hotfix 且正在止血，可先记录预检冲突并继续最小恢复；普通 bugfix 发现阶段冲突时先暂停并修正文档路由。
5. 复现问题或收集最强证据。
6. 默认显式叠加 `superpowers:systematic-debugging`；先复现或收集证据，再定位根因。
7. 根因结论前执行第一性原理检查：事实链、最小复现条件、表层症状和底层原因的区别。
8. 非平凡故障、技术栈相关失败或 hotfix 场景使用 `company-expert-routing`。
9. 做最小修复。
10. 增加或识别回归验证，并执行与本缺陷相关的对抗式审查。
11. 检查中文代码逻辑备注：根因修复、异常分支、兼容策略、业务规则和回归防线必须有必要备注。
12. 自动判定验证等级 `V1/V2/V3`；纯文档纠错才可用 `V0`。
13. 检查文档漂移：bug 是否暴露需求、业务规则、设计、API 契约或任务计划缺口。
14. 完成声明前显式叠加 `superpowers:verification-before-completion`。
15. 记录根因、修复和验证；如果修复影响公共入口或当前状态，非集成分支写公共文档影响补丁。

## Superpowers 叠加

- 默认：`superpowers:systematic-debugging`。
- 高风险、回归或 hotfix：额外叠加 `superpowers:verification-before-completion`。
- 明确且低风险的小 bug：可以轻量使用 systematic-debugging，但仍必须说明复现/证据、最小修复和回归验证。

## 验证等级

- `V0`：仅修正文档、测试描述或无行为错别字。
- `V1`：低风险单点 bug，复现路径明确，影响范围小。
- `V2`：默认 bugfix，涉及用户可见行为、跨文件逻辑、接口、状态或数据。
- `V3`：生产、权限、安全、金额/指标计算、数据损坏、并发、性能、外部 API 或 hotfix。

如果根因是规则缺失或文档承诺错误，不要只修代码；必须输出 `文档漂移影响` 并路由回需求或变更请求。

## 中文代码逻辑备注

Bugfix 涉及 Java、前端 TypeScript/Vue/React、Python、SQL 或脚本时，都按同一标准检查中文备注：

- 根因修复改变业务判断、状态流转、字段映射、异常处理、兼容策略或阈值时，必须用中文说明原因和保护的场景。
- 不写“修复 bug”“判断为空”这类空泛备注。
- 如果正确行为无法从需求、设计或 `business-rules.md` 推导出来，先补规则，不用备注替代缺失需求。
- 回归防线如果依赖特殊输入、历史数据或边界条件，应在测试或代码旁说明业务意义。

## 阶段一致性预检

Bugfix 前检查最小上下文：

- 当前 bug 属于哪个 feature、version、hotfix 或线上事故。
- `说明文档.md`、`specs/global/INDEX.md` 是否把当前阶段或入口指向正确位置。
- 当前任务/版本文档是否能解释预期行为。
- 相关 public-doc patch 是否记录了分支对公共入口的影响。

普通 bugfix 发现入口或索引错误时，先修正文档路由再改代码。生产 hotfix 可先止血，但完成报告必须写明预检冲突和补偿文档任务。

## 产物

紧急生产问题使用 hotfix 模板，按以下顺序查找：

1. 项目内：`specs/global/assets/hotfix-report-template.md`。
2. 插件内置 fallback：相对当前 skill 目录读取 `../../specs/global/assets/hotfix-report-template.md`。

普通 bug 更新功能说明或分支内进度文档即可。非集成分支不要直接改公共入口页的主线当前状态；改写 `docs/public-doc-updates/<branch-or-feature>.md`。

## 边界

不要把新功能行为打包进 bugfix。

不要把“规则文档缺失”伪装成代码 bug。若现有代码无法从需求、设计或 `business-rules.md` 推导出正确行为，先补规则文档或变更请求。

## 输出格式

- 工作流层：`company-bugfix-runner`
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
- 复现或证据：
- 事实链和最小复现条件：
- 根因：
- 最小修复：
- 回归验证：
- 公共文档影响：
- 剩余风险：
