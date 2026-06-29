---
name: company-context-index
description: Use when starting work in a company project, resuming an existing feature, or needing to update project context routing before requirements, design, implementation, bugfix, spike, or hotfix work.
---

# 公司上下文索引

## 目的

在进入需求、设计、实现、bugfix、spike 或 hotfix 前，建立最小必要项目上下文。

## 工作流

1. 阅读 `specs/global/INDEX.md`。
2. 确认 `INDEX.md` 是否包含文档职责地图：入口页、工作日志、正式 specs、生命周期文档、编号命名空间和更新触发条件。
3. 确认当前产品、版本、里程碑、技术栈、命令和入口文件。
4. 只读取与当前任务相关的 spec、源文件和测试文件。
5. 如果索引过期，记录需要更新的字段；如果发现裸任务编号跨文档复用，先标记为文档职责风险。
6. 输出本次任务的上下文摘要、应更新的文档和下一步建议。

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
- 编号命名空间：
- 相关 spec：
- 相关源码：
- 常用命令：
- 当前不确定性：
- 建议更新的文档：
- 下一步：

## 约束

- 不要全量扫描文档。
- 不要在上下文阶段编辑实现代码。
- 缺失信息可以标记为待用户或项目负责人补充。
- 不要把 `说明文档.md`、spike 工作日志和正式 specs 视为同一条连续任务链。
