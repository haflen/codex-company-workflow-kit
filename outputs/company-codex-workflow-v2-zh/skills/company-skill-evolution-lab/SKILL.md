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


## 人类优先输出

先读取 `../../specs/global/assets/human-output-standard.md`，同时尊重项目已确认的读者和交付用途。保留一句话结论和下一步建议；用中文解释结果、依据和影响。以下输出/报告中的内部字段写入已有执行记录，不默认附在用户回复或人类文档中。

### 回复契约门禁

发送前按共享规范复核事实范围、前置条件、责任方、授权、读者及显示效果。普通问答不套固定标题；用户需要详细解释时补充有用依据。未通过阅读检查先重写再发送。
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

## EXPERIENCE-01：从证据到候选

使用 `../../specs/global/assets/experience-candidate-template.md`，保留 source_refs、适用条件、候选版本、反例、实际验证、安全审查、采用权限和撤回方式。来源事实、因果假设和新授权分开；第三方指令、秘密及一次未复现失败不能变成永久规则。仅出现一次的原因猜测保持 proposed/unverified，不宣称根因已确定。

提案先测试并审查，再在已有授权允许的明确目标采用；本次允许改隔离候选，不等于允许写现用插件或系统记忆。记录实际采用文件/指纹，未安装明确未安装。既有许可足够时不重复索要确认，缺目标权限才停相关写入。采用后发现反例或版本漂移，按记录撤回并保留历史。

盲审试验与证据复用遵循 `../company-expert-routing/SKILL.md` 的 REVIEW-01；复用已完成的有效验证，不为采用候选自动增加审查轮次。
