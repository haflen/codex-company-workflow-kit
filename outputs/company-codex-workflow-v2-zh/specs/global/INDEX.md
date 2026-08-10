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

## 资产落点门禁

- 配置文件：`.codex-workflow/asset-boundaries.json`
- 确认状态：待确认
- 工程资产根目录：待确认
- 需求、设计和任务计划应写明预期产物的完整仓库相对路径；实现前检查计划落点，交付前检查实际变更文件。
- 自动生成配置后，项目负责人确认工程根目录和例外；未确认前不得把推断结果当成正式项目约束。

## 文档职责地图

| 文档 | 职责 | 更新触发 | 编号命名空间 |
| --- | --- | --- | --- |
| `说明文档.md` 或等价入口页 | 项目入口、当前状态、最近重要事件、阅读路线 | 当前阶段、最近重要事件、阅读路线或关键状态变化 | 不使用 spike 任务号；使用日期型项目事件或最近变更 |
| `spike_*_工作日志.md` 或 spike 目录日志 | spike 现场流水、实验过程、临时结论 | spike 实验、观察、决策或临时任务变化 | `SPKxx-T001` 或 `Sxx-001` |
| `specs/versions/...` 或 `specs/features/...` | 正式需求、设计、任务计划、验收依据 | 需求、设计、任务、验收或正式变更被确认 | feature、版本或正式任务编号 |
| `business-rules.md` 或 `*_业务规则与计算口径.md` | 操作逻辑、状态流转、指标公式、字段口径、异常处理和样例用例 | 需求命中复杂业务规则、计算口径或状态流转触发条件 | feature、版本或正式任务编号 |
| `docs/lifecycle/` | 生命周期阶段总结、里程碑回顾 | 版本阶段结束、里程碑变化或管理层摘要 | 日期或版本阶段编号 |
| `docs/public-doc-updates/` | 多分支并行时的公共文档影响补丁 | 分支影响入口页、当前状态、阅读路线、文档职责或编号规则，但尚未合并主线 | 分支名、feature ID 或 PR ID |

## 多分支公共文档协议

- 公共文档代表主线事实；feature、spike、hotfix 分支默认只读 `说明文档.md` 和本索引。
- 分支未合并前，不把分支局部进展写成项目“当前状态”。
- 分支需要改变公共入口或索引时，先写 `docs/public-doc-updates/<branch-or-feature>.md`。
- 集成阶段再统一把已合并事实写入 `说明文档.md` 和本索引。
- 如果多个分支影响同一公共段落，公共段落只在集成分支统一重写。

## 编号规则

- 不同层级文档不得共享裸 `任务 001` 这类编号。
- Spike 内部任务使用 spike 命名空间，例如 `SPK02-T183`。
- 正式任务使用 feature、版本或正式任务编号，例如 `FEAT-DT-T01`。
- 项目入口页记录“项目事件”或“最近变更”，不延续 spike 流水号。
- 发现编号冲突时，先修正文档职责地图，再继续写入。

## 工作流文档

```mermaid
flowchart LR
    A["先读 document-standard"] --> B["选择文档类型模板"]
    B --> C["先写结论和图"]
    C --> D["补关键表格和细节"]
    D --> E["按 DOC-G01~G12 自检"]
```

| 需求 | 模板 |
| --- | --- |
| 正式文档阅读与质量规范 | `specs/global/assets/document-standard.md` |
| 功能需求 | `specs/global/assets/requirements-template.md` |
| 数据模型与表结构 | `specs/global/assets/data-model-template.md` |
| 业务规则与计算口径 | `specs/global/assets/business-rules-template.md` |
| 技术设计 | `specs/global/assets/design-template.md` |
| API 契约 | `specs/global/assets/api-contract-template.md` |
| 任务计划 | `specs/global/assets/tasks-template.md` |
| Spike 报告 | `specs/global/assets/spike-report-template.md` |
| Hotfix 报告 | `specs/global/assets/hotfix-report-template.md` |
| 需求原型确认记录 | `specs/global/assets/requirements-prototype-record-template.md` |
| 交付收口报告 | `specs/global/assets/delivery-closeout-template.md` |
| 变更请求 | `specs/global/assets/change-request-template.md` |
| 公共文档影响补丁 | `specs/global/assets/public-doc-update-template.md` |
| 技能升级报告 | `specs/global/assets/skill-upgrade-report-template.md` |
| 工作流健康检查报告 | `specs/global/assets/workflow-health-report-template.md` |

## 当前风险

- 资产落点配置尚未确认。
