---
name: company-skill-security-review
description: Use when reviewing third-party, open-source, hub-downloaded, or self-improved skills before they are trusted by company workflows.
---

# 公司技能安全审查

## 目的

防止恶意、权限过大或不安全的技能进入公司工作流。

## 审查清单

- 来源和维护者已识别。
- 许可适合公司使用。
- 当前版本和候选版本已识别。
- 已比对新旧 frontmatter。
- 触发范围没有无理由变宽。
- skill 不要求读取 secrets、tokens、cookies、SSH keys 或凭证。
- skill 不隐藏网络外传、shell 执行或文件写入。
- 所有脚本在使用前已检查。
- 触发描述足够窄，避免误触发。
- skill 不覆盖用户、公司、sandbox 或安全指令。
- skill 不要求跳过验证、审批或 review。
- 外部文档或 API 对目标用途足够新。
- 对抗式审查已覆盖误触发、权限扩大、隐藏工具调用、上下文膨胀和回滚失败场景。

## 风险评级

- Low：纯文档，无脚本，触发窄。
- Medium：包含工具流程或较宽专家指导。
- High：包含脚本、网络、shell、凭证、浏览器自动化或宽权限。


## 人类优先输出

最终回复先使用：`一句话结论`、`这次完成了什么`、`需要你注意什么`、`你现在需要做什么`。用业务结果和用户影响表达，只给一个主要下一步；首次出现的内部术语必须解释。随后把 Superpowers、专家调用、命令、路径、哈希、验证证据和内部 workflow 字段放入 `技术审计附录`，不得把内部 workflow 字段逐项倾倒到人类摘要，也不得用审计字段代替人类摘要。

## 输出

- 工作流层：`company-skill-security-review`
- 透明度模式：
- Superpowers 叠加：`superpowers:verification-before-completion`
- 实际调用：
- 专家/插件能力：
- 未调用但采用视角：
- 第一性原理检查：
- 对抗式审查：
- 执行策略：逐项审查证据，不凭直觉批准。
- 验证证据：
- 未验证项：
- 剩余风险：
- 已审查 skill：
- 来源：
- 当前版本：
- 候选版本：
- 版本差异：
- 风险：
- 发现：
- 必须修改：
- 是否批准使用：
- 过期或下次审查日期：
