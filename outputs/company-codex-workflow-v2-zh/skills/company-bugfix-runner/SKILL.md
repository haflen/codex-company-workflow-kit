---
name: company-bugfix-runner
description: Use when company code behavior differs from requirements, design, acceptance criteria, tests, or documented expectations.
---

# 公司 Bugfix 执行器

## 目的

区分 bug 和需求变更，并完成复现、最小修复和回归验证。

## 工作流

1. 判断这是 bug 还是需求变更。
2. 如果是变更请求，路由回需求/变更规划。
3. 复现问题或收集最强证据。
4. 默认显式叠加 `superpowers:systematic-debugging`；先复现或收集证据，再定位根因。
5. 非平凡故障、技术栈相关失败或 hotfix 场景使用 `company-expert-routing`。
6. 做最小修复。
7. 增加或识别回归验证。
8. 完成声明前显式叠加 `superpowers:verification-before-completion`。
9. 记录根因、修复和验证。

## Superpowers 叠加

- 默认：`superpowers:systematic-debugging`。
- 高风险、回归或 hotfix：额外叠加 `superpowers:verification-before-completion`。
- 明确且低风险的小 bug：可以轻量使用 systematic-debugging，但仍必须说明复现/证据、最小修复和回归验证。

## 产物

紧急生产问题使用 hotfix 模板，按以下顺序查找：

1. 项目内：`specs/global/assets/hotfix-report-template.md`。
2. 插件内置 fallback：相对当前 skill 目录读取 `../../specs/global/assets/hotfix-report-template.md`。

普通 bug 更新功能说明或进度文档即可。

## 边界

不要把新功能行为打包进 bugfix。

## 输出格式

- 工作流层：`company-bugfix-runner`
- Superpowers 叠加：
- 实际调用：
- 专家/插件能力：
- 未调用但采用视角：
- 执行策略：
- 验证证据：
- 未验证项：
- 剩余风险：
- 复现或证据：
- 根因：
- 最小修复：
- 回归验证：
- 剩余风险：
