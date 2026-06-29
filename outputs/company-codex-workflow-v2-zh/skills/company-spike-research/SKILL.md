---
name: company-spike-research
description: Use when company work needs a time-boxed technical feasibility experiment, unfamiliar library evaluation, prototype, or architecture uncertainty reduction before design.
---

# 公司 Spike 预研

## 目的

用受控、限时、最小实验降低技术不确定性。

## 工作流

1. 明确 spike 问题和时间盒。
2. 实验方案不唯一时，显式叠加 `superpowers:brainstorming`，比较 2-3 个最小实验路径。
3. 写出第一性原理假设：要证明什么、最小成立条件是什么、什么证据会推翻它。
4. 将实验代码隔离到 `spikes/`、`playground/` 或其他一次性路径。
5. 实验依赖非显然技术栈或 API 行为时，使用 `company-expert-routing`；优先 `company-spike` bundle 加一个技术栈专家。
6. 运行能回答问题的最小实验，并至少尝试一个反例或边界实验。
7. 完成前显式叠加 `superpowers:verification-before-completion`，检查证据是否足以回答 spike 问题。
8. 输出发现、建议和后续债务。

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
- 第一性原理假设：
- 最小实验：
- 反例或边界实验：
- 证据：
- 结论：
- 下一步：
