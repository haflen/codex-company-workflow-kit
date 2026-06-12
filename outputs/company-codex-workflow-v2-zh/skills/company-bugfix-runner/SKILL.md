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
4. 根因不清、偶发、重复或回归风险高时，使用 `systematic-debugging`。
5. 非平凡故障、技术栈相关失败或 hotfix 场景使用 `company-expert-routing`。
6. 做最小修复。
7. 增加或识别回归验证。
8. 记录根因、修复和验证。

## 产物

紧急生产问题使用 `hotfix-report-template.md`。普通 bug 更新功能说明或进度文档。

## 边界

不要把新功能行为打包进 bugfix。

