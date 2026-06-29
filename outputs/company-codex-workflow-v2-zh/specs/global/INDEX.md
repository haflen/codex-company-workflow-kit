# 项目上下文索引

每次使用公司工作流前先从这里开始。

## 项目快照

- 产品：
- 当前版本：
- 当前里程碑：
- 主要技术栈：
- 包管理器：
- 测试命令：
- 构建命令：
- 本地启动命令：
- 进度文档：`说明文档.md` 或等价文档

## 路由

- 当前功能 specs：
- 当前版本目录：
- 当前里程碑目录：
- API 契约：
- 测试位置：
- 主要源码入口：

## 文档职责地图

| 文档 | 职责 | 更新触发 | 编号命名空间 |
| --- | --- | --- | --- |
| `说明文档.md` 或等价入口页 | 项目入口、当前状态、最近重要事件、阅读路线 | 当前阶段、最近重要事件、阅读路线或关键状态变化 | 不使用 spike 任务号；使用日期型项目事件或最近变更 |
| `spike_*_工作日志.md` 或 spike 目录日志 | spike 现场流水、实验过程、临时结论 | spike 实验、观察、决策或临时任务变化 | `SPKxx-T001` 或 `Sxx-001` |
| `specs/versions/...` 或 `specs/features/...` | 正式需求、设计、任务计划、验收依据 | 需求、设计、任务、验收或正式变更被确认 | feature、版本或正式任务编号 |
| `docs/lifecycle/` | 生命周期阶段总结、里程碑回顾 | 版本阶段结束、里程碑变化或管理层摘要 | 日期或版本阶段编号 |

## 编号规则

- 不同层级文档不得共享裸 `任务 001` 这类编号。
- Spike 内部任务使用 spike 命名空间，例如 `SPK02-T183`。
- 正式任务使用 feature、版本或正式任务编号，例如 `FEAT-DT-T01`。
- 项目入口页记录“项目事件”或“最近变更”，不延续 spike 流水号。
- 发现编号冲突时，先修正文档职责地图，再继续写入。

## 工作流文档

| 需求 | 模板 |
| --- | --- |
| 功能需求 | `specs/global/assets/requirements-template.md` |
| 技术设计 | `specs/global/assets/design-template.md` |
| API 契约 | `specs/global/assets/api-contract-template.md` |
| 任务计划 | `specs/global/assets/tasks-template.md` |
| Spike 报告 | `specs/global/assets/spike-report-template.md` |
| Hotfix 报告 | `specs/global/assets/hotfix-report-template.md` |
| 变更请求 | `specs/global/assets/change-request-template.md` |
| 技能升级报告 | `specs/global/assets/skill-upgrade-report-template.md` |

## 当前风险

- 
