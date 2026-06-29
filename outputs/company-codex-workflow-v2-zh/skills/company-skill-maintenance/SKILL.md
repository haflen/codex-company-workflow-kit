---
name: company-skill-maintenance
description: Use when updating, pinning, auditing, replacing, or reviewing open-source or internal expert skills used by the company workflow.
---

# 公司技能维护

## 目的

把专家技能当作依赖管理：固定版本、审查、谨慎更新、可回滚。

## 工作流

1. 普通用户发起的更新请求，路由到 `company-skill-upgrade-runner`。
2. 阅读 `EXPERTS.lock.md`。
3. 识别要新增、更新、替换或移除的 skill。
4. 检查 `BUNDLES.md`，了解哪些工作流依赖该 skill。
5. 审查来源、许可、pin、变更文件和风险指令。
6. 采纳外部变更前运行 `company-skill-security-review`。
7. 比对新旧触发描述是否漂移；本地 Codex 化 `description: Use when...` 默认受保护。
8. 确认同步范围只覆盖被引用或被点名的外部专家 skill，不做全量仓库导入。
9. 审查后才更新 `EXPERTS.lock.md`。
10. 只有 bundle 归属或默认路由变化时才更新 `BUNDLES.md`。
11. 记录发布说明和回滚方式。

## 更新策略

- 公司默认：每月审查，或框架/运行时重大升级后立即审查。
- 安全或供应链问题：立即审查。
- 不自动合并外部 hub 更新。
- 新外部专家必须先有 lock entry 和审查。
- 外部专家更新默认保留本地触发 frontmatter、公司路由规则和 Superpowers 叠加规则。
- 大型上游仓库只做目标清单同步；优先 raw/API/sparse，避免全量拉取浪费时间和流量。
- 运行安装或验证生成的报告属于产物，除非明确设计为模板，否则不要提交。
- 脚本文件的可执行位、sandbox 风险和运行前审批要求必须作为依赖状态的一部分维护。

## 输出

- 工作流层：`company-skill-maintenance`
- 透明度模式：
- Superpowers 叠加：`superpowers:verification-before-completion`
- 实际调用：
- 专家/插件能力：
- 未调用但采用视角：
- 第一性原理检查：
- 对抗式审查：
- 执行策略：依赖审查、版本锁定、可回滚。
- 验证证据：
- 未验证项：
- 剩余风险：
- Skill：
- 来源和 pin：
- 许可：
- Diff 摘要：
- 同步范围：
- 本地保留项：
- 安全审查：
- 兼容性说明：
- 建议：
- 回滚：
