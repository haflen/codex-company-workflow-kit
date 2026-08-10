---
name: company-context-index
description: Use when starting work in a company project, resuming an existing feature, or needing to update project context routing before requirements, design, implementation, bugfix, spike, or hotfix work.
---

# 公司上下文索引

## 目的

在进入需求、设计、实现、bugfix、spike 或 hotfix 前，建立最小必要项目上下文。

## 工作流

1. 阅读 `specs/global/INDEX.md`。
2. 确认 `INDEX.md` 是否包含文档职责地图：入口页、工作日志、正式 specs、业务规则与计算口径、生命周期文档、公共文档影响补丁、编号命名空间和更新触发条件。
3. 确认当前产品、版本、里程碑、技术栈、命令和入口文件。
4. 读取 `.codex-workflow/asset-boundaries.json`，记录文档根、工程根、工具/迁移根、配置确认状态和显式例外；同时检查 `asset-boundaries.generated.json`。配置缺失时建议运行 `generate-asset-boundaries`；候选存在时先审阅并 `accept-asset-boundaries` 或明确丢弃，不自行猜测新工程目录。
5. 只读取与当前任务相关的 spec、源文件和测试文件。
6. 判断当前分支是否为集成分支；非集成分支默认不直接更新 `说明文档.md` 或 `specs/global/INDEX.md` 的主线事实。
7. 如果索引过期，记录需要更新的字段；如果发现裸任务编号跨文档复用，先标记为文档职责风险。
8. 如果当前分支会影响公共入口、阅读路线、当前阶段或文档职责，建议写入 `docs/public-doc-updates/<branch-or-feature>.md`。
9. 输出本次任务的上下文摘要、应更新的文档和下一步建议。

## 输出

- 工作流层：`company-context-index`
- 透明度模式：
- Superpowers 叠加：无，原因：本阶段只做上下文路由和最小信息收集；如需迁移策略讨论，转入 `company-legacy-project-onboarding` 并叠加 `superpowers:brainstorming`。
- 实际调用：
- 专家/插件能力：
- 未调用但采用视角：
- 第一性原理检查：
- 对抗式审查：
- 执行策略：按需读取，不全量扫描。
- 验证证据：
- 未验证项：
- 剩余风险：
- 项目：
- 当前阶段：
- 文档职责地图：
- 当前分支公共文档策略：
- 公共文档影响补丁：
- 业务规则与计算口径：
- 编号命名空间：
- 相关 spec：
- 相关源码：
- 常用命令：
- 资产边界状态：缺失 / 草案待确认 / 已确认
- 文档根、工程根和显式例外：
- 当前不确定性：
- 建议更新的文档：
- 下一步：

## 约束

- 不要全量扫描文档。
- 不要在上下文阶段编辑实现代码。
- 缺失信息可以标记为待用户或项目负责人补充。
- 不要把 `说明文档.md`、spike 工作日志和正式 specs 视为同一条连续任务链。
- 非集成分支不要把分支局部状态写成公共文档的主线当前状态；改写为公共文档影响补丁。

## 文档质量门禁

创建或实质修改正式文档前，先读取项目内 `specs/global/assets/document-standard.md`；缺失时读取插件内置 `../../specs/global/assets/document-standard.md`。本 skill 负责检查 `DOC-G01`、`DOC-G04`、`DOC-G05`、`DOC-G06`、`DOC-G07`、`DOC-G08`、`DOC-G09`、`DOC-G10`、`DOC-G11`、`DOC-G12`。
