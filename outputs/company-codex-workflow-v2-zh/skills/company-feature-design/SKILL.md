---
name: company-feature-design
description: Use when company feature requirements are confirmed and a technical design, architecture decision, API contract, data flow, or test strategy is needed before task planning.
---

# 公司功能技术设计

## 目的

在任务拆解前产出技术方案、契约、数据流、风险和测试策略。

## 工作流

1. 确认需求已存在，并包含验收标准。
2. 阅读项目上下文、现有模式和相关源文件。
3. 设计方向不唯一或架构取舍不清时，显式叠加 `superpowers:brainstorming` 做方案比较。
4. 对非平凡架构、框架、数据、UI 或测试决策使用 `company-expert-routing`，由它自动选择技术栈 bundle。
5. 输出设计、契约、风险说明和测试策略。
6. 涉及前后端或服务边界时，任务拆解前先产出 API 契约。
7. 设计阶段结束后停止，除非用户给出任务拆解交接口令。

## Superpowers 叠加

- 默认：方案存在不确定性时叠加 `superpowers:brainstorming`，用于比较 2-3 个设计路径。
- 高风险设计：叠加 `company-expert-routing` 后，可按专家结果继续使用 `superpowers:brainstorming` 收敛方案。
- 设计已经唯一且风险低时：可以不叠加，但输出必须写明原因。

## 产物

使用模板时按以下顺序查找：

1. 项目内：`specs/global/assets/design-template.md`；跨边界工作使用 `specs/global/assets/api-contract-template.md`。
2. 插件内置 fallback：相对当前 skill 目录读取 `../../specs/global/assets/design-template.md` 或 `../../specs/global/assets/api-contract-template.md`。

## 边界

设计工作不得编辑实现代码。

## 输出格式

- 工作流层：`company-feature-design`
- Superpowers 叠加：
- 实际调用：
- 专家/插件能力：
- 未调用但采用视角：
- 执行策略：
- 验证证据：
- 未验证项：
- 剩余风险：
- 推荐设计：
- 备选方案和取舍：
- 风险：
- 测试策略：
- 下一步：
