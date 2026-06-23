---
name: company-spike-research
description: Use when company work needs a time-boxed technical feasibility experiment, unfamiliar library evaluation, prototype, or architecture uncertainty reduction before design.
---

# 公司 Spike 预研

## 目的

用受控、限时、最小实验降低技术不确定性。

## 工作流

1. 明确 spike 问题和时间盒。
2. 将实验代码隔离到 `spikes/`、`playground/` 或其他一次性路径。
3. 实验依赖非显然技术栈或 API 行为时，使用 `company-expert-routing`；优先 `company-spike` bundle 加一个技术栈专家。
4. 运行能回答问题的最小实验。
5. 输出发现、建议和后续债务。

## 产物

使用 spike 模板时按以下顺序查找：

1. 项目内：`specs/global/assets/spike-report-template.md`。
2. 插件内置 fallback：相对当前 skill 目录读取 `../../specs/global/assets/spike-report-template.md`。

## 边界

Spike 代码默认不是生产代码，除非经过正常设计和实现流程转正。
