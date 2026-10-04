---
name: company-context-index
description: Use when starting work in a company project, resuming an existing feature, or needing to update project context routing before requirements, design, implementation, bugfix, spike, or hotfix work.
---

# 公司上下文索引

## 文档归属检查

先读取项目内 `specs/global/assets/document-ownership.md`；缺失时读取插件内置 `../../specs/global/assets/document-ownership.md`。确认已有任务、owner-path、record-path 和 release-target；优先复用原记录，归属不明时只询问关键归属。

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

## 目标终端检查

- 自动生成或刷新 INDEX 时必须包含目标使用终端基线，并让用户确认 PC Web、移动 Web、App、桌面客户端或大屏的支持状态。
- 自动推断不得把技术栈或现有 CSS 当成产品承诺；未确认终端保持待确认且视为不支持，不得自行增加移动端适配。
- 记录页面/代码/API 共用范围、最小视口、浏览器和输入方式；无 UI 项目可写“无直接终端差异”。


## 人类优先输出

先读取 `../../specs/global/assets/human-output-standard.md`，同时尊重项目已确认的读者和交付用途。保留一句话结论和下一步建议；用中文解释结果、依据和影响。以下输出/报告中的内部字段写入已有执行记录，不默认附在用户回复或人类文档中。

### 回复契约门禁

发送前按共享规范复核事实范围、前置条件、责任方、授权、读者及显示效果。普通问答不套固定标题；用户需要详细解释时补充有用依据。未通过阅读检查先重写再发送。
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
