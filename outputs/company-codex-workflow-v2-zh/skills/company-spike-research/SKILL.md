---
name: company-spike-research
description: Use when company work needs a time-boxed technical feasibility experiment, unfamiliar library evaluation, technical prototype, performance evidence, or architecture uncertainty reduction before design.
---

# 公司 Spike 预研

## 文档归属检查

先读取项目内 `specs/global/assets/document-ownership.md`；缺失时读取插件内置 `../../specs/global/assets/document-ownership.md`。创建或更新阶段文档前，继承已确认归属并选择记录粒度；未验收任务续写原记录，小修复不自动新建根级 features 或完整文档包。必要的专项设计和验证不因记录精简而省略。

## 目的

用受控、限时、最小实验降低技术不确定性。

## 工作流

1. 先区分验证目的：技术、架构、性能或库可行性才是 spike；页面、交互、文案或模拟业务状态验证改用 `company-requirements-prototype`。然后明确 spike 问题和时间盒。
2. 实验方案不唯一时，显式叠加 `superpowers:brainstorming`，比较 2-3 个最小实验路径。
3. 写出第一性原理假设：要证明什么、最小成立条件是什么、什么证据会推翻它。
4. 确认 spike 编号命名空间，例如 `SPK02`；spike 内部任务使用 `SPK02-T001`，不使用裸 `任务 001`。
5. 将实验代码隔离到 `spikes/`、`playground/` 或其他一次性路径。
6. 实验依赖非显然技术栈或 API 行为时，使用 `company-expert-routing`；优先 `company-spike` bundle 加一个技术栈专家。
7. 运行能回答问题的最小实验，并至少尝试一个反例或边界实验。
8. 完成前显式叠加 `superpowers:verification-before-completion`，检查证据是否足以回答 spike 问题。
9. 输出发现、建议和后续债务；如果转正式开发，必须回到需求/设计/任务流程并建立新的正式任务编号。
10. 如果 spike 结论影响项目入口、阅读路线或当前阶段，非集成分支写公共文档影响补丁，不直接改 `说明文档.md`。

## Superpowers 叠加

- 默认：`superpowers:brainstorming` 用于设计最小实验。
- 完成前：`superpowers:verification-before-completion` 用于确认结论有证据。
- 如果 spike 问题已经非常明确，可以不叠加 brainstorming，但必须说明原因。

## 产物

使用 spike 模板时按以下顺序查找：

1. 项目内：`specs/global/assets/spike-report-template.md`。
2. 插件内置 fallback：相对当前 skill 目录读取 `../../specs/global/assets/spike-report-template.md`。

## 边界

Spike 代码默认不是生产代码，除非经过正常设计和实现流程转正。
需求阶段页面原型不属于本 skill，不得用 spike 绕过需求原型的确认和基线规则。
Spike 工作日志不是项目入口页；不要把 spike 内部任务号写入 `说明文档.md` 作为项目主线任务号。
Spike 分支未合并前，不要把 spike 临时结论写成公共文档的主线当前状态。


## 人类优先输出

先读取 `../../specs/global/assets/human-output-standard.md`，同时尊重项目已确认的读者和交付用途。保留一句话结论和下一步建议；用中文解释结果、依据和影响。以下输出/报告中的内部字段写入已有执行记录，不默认附在用户回复或人类文档中。

### 回复契约门禁

发送前按共享规范复核事实范围、前置条件、责任方、授权、读者及显示效果。普通问答不套固定标题；用户需要详细解释时补充有用依据。未通过阅读检查先重写再发送。
## 输出格式

- 工作流层：`company-spike-research`
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
- Spike 问题：
- Spike 编号命名空间：
- 第一性原理假设：
- 最小实验：
- 反例或边界实验：
- 证据：
- 结论：
- 转正式开发时的新编号建议：
- 公共文档影响：
- 下一步：

## 文档质量门禁

创建或实质修改正式文档前，先读取项目内 `specs/global/assets/document-standard.md`；缺失时读取插件内置 `../../specs/global/assets/document-standard.md`。本 skill 负责检查 `DOC-G01`、`DOC-G04`、`DOC-G05`、`DOC-G06`、`DOC-G07`、`DOC-G08`、`DOC-G09`、`DOC-G10`、`DOC-G11`、`DOC-G12`。
