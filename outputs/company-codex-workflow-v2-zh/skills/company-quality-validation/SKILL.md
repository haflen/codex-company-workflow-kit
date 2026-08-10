---
name: company-quality-validation
description: Use when company implementation is complete and integrated acceptance, regression, milestone, release, V3, cross-module, cross-system, or post-hotfix quality evidence may be required before delivery closeout.
---

# 公司质量验收

## 目的

在实现完成后独立判断最终候选是否满足已确认需求并具备可交付证据。它补充 TDD，不重复开发过程测试。

## 自动触发判定

用户不需要选择，workflow 必须输出判定和依据。

| 场景 | 独立质量验收 |
| --- | --- |
| V0/V1 文档、注释、低风险单点改动 | 默认不触发；实现阶段证据足够时进入收口 |
| 单任务 V2 | 默认不触发；关键用户旅程、真实浏览器、API/数据库集成或明显回归面除外 |
| 多任务、跨模块、前后端/API/数据库联动的 V2 | 需要，完成后进入本 skill |
| 里程碑、版本交付或 V3 | 强制触发 |
| 普通 bugfix | 按回归影响面判定 |
| hotfix 止血后的补偿链路 | 强制触发 |

跳过不等于不测试。跳过独立阶段时仍保留实现或 bugfix workflow 的 TDD、回归和完成前验证证据。

## 最小上下文

只读取当前验收范围，不全量扫描文档：

1. 已确认需求、AC 和必要的 `business-rules.md`。
2. 当前设计、API/数据契约和任务完成状态。
3. 当前分支、最终候选 diff、测试入口、环境和数据说明。
4. 实现或 bugfix 完成报告中的验证证据与未验证项。

入口、任务或验收口径冲突时停止，回到需求、设计或任务规划；不得自行选择有利口径。

## 验收流程

1. 输出 `独立质量验收：不需要 / 需要 / 强制` 和触发依据。
2. 建立 `AC -> 场景 -> 证据 -> 结果` 追溯矩阵，不能用覆盖率替代 AC 追溯。
3. 按最高风险选择单元、集成、API、E2E、浏览器、权限、数据、性能或恢复验证；复用已有新鲜证据，避免无差别重跑。
4. 默认实际使用 `testing-qa`；Web 关键路径按需使用 `e2e-testing-patterns`、`webapp-testing`，复杂领域才进入 `company-expert-routing`。
5. **REQUIRED SUB-SKILL:** Use `superpowers:verification-before-completion`。只接受当前最终候选的新鲜证据。
6. 执行对抗式审查：至少覆盖与本次风险相关的异常、边界、权限、并发、数据、性能、兼容或渲染场景。
7. 输出唯一结论：`通过 / 有条件通过 / 阻断`。

## 结果路由

- `通过`：进入 `company-delivery-closeout`。
- `有条件通过`：列出未验证项、影响和到期条件；必须由用户显式接受。V3 的安全、权限、数据完整性、金额/公式、迁移或恢复风险不得有条件放行。
- `阻断`：实现缺陷进入 `company-bugfix-runner`；修复完成后重新执行原验收范围。
- 需求、业务规则或设计不明确：回到对应文档 workflow，不得伪装成代码 bug。

## 生产代码边界

本 skill 不得修改生产代码。允许生成验收报告、执行只读检查和运行已批准测试。缺失自动测试时记录补测任务；需要新增或修改测试代码时，回到规划/实现或 bugfix workflow 获得范围授权。

## 报告

模板查找顺序：

1. 项目内 `specs/global/assets/quality-validation-report-template.md`。
2. 插件 fallback `../../specs/global/assets/quality-validation-report-template.md`。

完成报告必须包含：

- 工作流层：`company-quality-validation`
- 透明度模式：`full-audit`
- 独立质量验收：不需要 / 需要 / 强制
- 判定依据：
- 验收范围与最终候选：
- Superpowers 叠加：
- 实际调用：
- 专家/插件能力：
- 未调用但采用视角：
- AC 追溯矩阵：
- 验证环境和数据：
- 验证证据：
- 对抗式审查：
- 验收结论：通过 / 有条件通过 / 阻断
- 缺陷与路由：
- 未验证项：
- 剩余风险：
- 交付收口就绪：就绪 / 未就绪
- 下一步建议：
- 推荐用户下一句：

## 文档质量门禁

创建或实质修改正式验收报告前，先读取项目内 `specs/global/assets/document-standard.md`；缺失时读取插件 fallback。检查 `DOC-G01`、`DOC-G04`、`DOC-G05`、`DOC-G06`、`DOC-G07`、`DOC-G08`、`DOC-G09`、`DOC-G10`、`DOC-G11`、`DOC-G12`。
