---
name: company-skill-upgrade-runner
description: Use when a user wants to check, update, upgrade, replace, or install company workflow skills or expert skills from an external source.
---

# 公司技能升级执行器

## 目的

为外部专家技能和内部工作流技能提供用户友好的升级流程。

## 用户触发

- `检查专家技能更新`
- `更新 java-pro`
- `把前端专家技能升级到最新稳定版`
- `从 antigravity-awesome-skills 同步这些专家`
- `对比新旧 skill 后让我确认是否覆盖`

## 默认 Dry Run

技能更新请求默认是 dry-run。可以自动检查更新、拉取候选版本到临时审查位置、比对版本并输出建议。

覆盖、删除、移动或安装生产技能必须在升级报告后得到用户明确确认。

## 工作流

1. 识别目标 skill、来源仓库或 hub、当前安装路径和目标位置。
2. 阅读 `EXPERTS.lock.md` 和 `BUNDLES.md`，了解当前 pin、审查状态和影响范围。
3. 将候选版本放到临时审查位置，不直接覆盖当前技能。
4. 比对新旧版本：frontmatter、触发范围、正文、脚本、工具、网络、shell、浏览器自动化、文件写入、许可、来源、pin、setup 和风险。
5. 对候选版本运行 `company-skill-security-review`。
6. 输出升级报告和建议。
7. 覆盖、安装或删除生产 skill 前，询问用户明确确认。
8. 用户批准后应用更新，更新 `EXPERTS.lock.md`，必要时更新 `BUNDLES.md`，记录回滚。
9. 验证插件并做触发规则 sanity check。

## 决策规则

- 触发范围变宽、新增脚本、shell、网络访问、凭证处理或许可不清时，建议审查或拒绝。
- 只更新示例或窄范围指导时，可建议 pilot approval。
- 高风险或 critical 风险 skill 即使 pilot 也需要明确批准。
- bundle 归属变化时，确认前说明受影响工作流。
- 没有精确 upstream commit 或 tag 时，不标记为生产批准。

## 确认门

覆盖前必须展示：

- 待更新 skills：
- 来源和候选 pin：
- 受影响 bundle：
- 关键差异：
- 安全审查结果：
- 建议：
- 回滚路径：
- 需要确认：

模糊表达如“看起来不错”“继续”“似乎可以”不算覆盖确认。

## 升级报告

复杂升级使用 `specs/global/assets/skill-upgrade-report-template.md`。小升级可在对话中报告，但必须包含目标、当前版本、候选版本、diff 摘要、风险、用户决策、文件变更和验证。

