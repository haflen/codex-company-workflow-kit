---
name: company-skill-evolution-lab
description: Use when company workflow skills repeatedly misfire, feel too heavy or too weak, miss expert routing, or need controlled self-improvement proposals.
---

# 公司技能演进实验室

## 目的

把自改进纳入工作流，但不允许技能未经审查直接改写自己。

## 原则

自改进先产出提案。正式 skill 只有在审查、安全检查和回归用例之后才变更。

## 触发

- 同一 skill 以同样方式误触发三次。
- 用户反复反馈流程太重、太轻或缺步骤。
- 专家路由失败或选错专家。
- 框架/API 变化导致指导过期。
- 重复手工 workaround 应沉淀为工作流知识。

## 工作流

1. 用具体例子记录摩擦或失败。
2. 判断问题来自触发文本、工作流正文、专家路由、模板形态还是缺失依赖。
3. 如果问题是专家选择，先提议修改 `BUNDLES.md` 或 `company-expert-routing`。
4. 起草改进提案，不直接改生产版本。
5. 从第一性原理说明旧规则为什么失败：触发条件、阶段边界、上下文假设或验证锚点哪个不成立。
6. 增加或更新能捕捉旧问题的回归用例，并做对抗式审查，确认新规则不会过度触发。
7. 如果提案改变权限、工具、外部技能、脚本或专家依赖，运行 `company-skill-security-review`。
8. 建议接受、修改或拒绝。

## 提案输出

- 工作流层：`company-skill-evolution-lab`
- 透明度模式：
- Superpowers 叠加：`superpowers:brainstorming` 用于比较改进路径；完成前使用 `superpowers:verification-before-completion` 检查提案完整性。
- 实际调用：
- 专家/插件能力：
- 未调用但采用视角：
- 第一性原理检查：
- 对抗式审查：
- 执行策略：只产出提案，不直接改生产 skill。
- 验证证据：
- 未验证项：
- 剩余风险：
- 受影响 skill：
- 失败模式：
- 证据：
- 建议变更：
- 回归用例：
- 安全影响：
- 回滚：
