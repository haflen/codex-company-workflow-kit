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
2. 阅读 `EXPERTS.lock.md` 和 `BUNDLES.md`，了解当前 pin、审查状态和影响范围；优先项目根目录，其次插件内置 fallback `../../EXPERTS.lock.md` 和 `../../BUNDLES.md`。
3. 从 lock/bundle 得出精确目标清单，只检查被公司工作流引用的外部专家；不要全量 clone 或全量拉取大型 skill 仓库。
4. 优先使用 GitHub raw/API、sparse checkout 或单文件下载把候选版本放到临时审查位置；只有清单、目录结构或许可审查必须时才扩大拉取范围。
5. 对每个候选 skill 下载 `SKILL.md`，并只同步该 skill 目录内实际存在的 `references/`、`resources/`、`scripts/`、`LICENSE` 等配套文件。
6. 比对新旧版本：frontmatter、触发范围、正文、脚本、工具、网络、shell、浏览器自动化、文件写入、许可、来源、pin、setup 和风险。
7. 采纳外部 skill 内容时，默认保留本地 Codex 化 frontmatter，尤其是 `name` 和 `description: Use when...` 触发描述；只把上游风险、来源、版本、作者等信息写入 `upstream_*` 元数据。
8. 只有用户明确要求重置触发策略，且通过触发 sanity check，才允许覆盖本地 `description`。
9. 对候选版本运行 `company-skill-security-review`，并做对抗式审查：误触发、权限扩大、上下文膨胀、工具调用、脚本权限漂移、生成物污染和回滚失败。
10. 输出升级报告和建议。
11. 覆盖、安装或删除生产 skill 前，询问用户明确确认。
12. 用户批准后应用更新，更新 `EXPERTS.lock.md`，必要时更新 `BUNDLES.md`，记录回滚。
13. 验证插件并做触发规则 sanity check。

## 同步范围和本地保留规则

- 只同步 `EXPERTS.lock.md` 或本次用户明确点名的外部专家 skill。
- 不为了十几个专家 skill 拉取上千个 skill 的完整仓库；全量 clone 超时或浪费流量时，立即切换为 raw/API/sparse。
- 不覆盖本地工作流 skill，除非用户明确要求升级内部 workflow。
- 不覆盖本地 Codex 触发 `description`、命名约定、路由约束、Superpowers 叠加规则和公司安全护栏。
- 外部正文、示例、references、resources、scripts 可以同步，但必须保留本地 frontmatter 的触发语义。
- 如果上游新增脚本、脚本权限、网络访问、shell、浏览器自动化或凭证处理，必须在报告里单独列出，且脚本运行前仍需审批。
- 同步后清理安装/验证生成物，例如 `EXPERT-READINESS.md`、`EXPERT-READINESS.json`，不要把临时报告误提交为源文件。
- 如果 raw 下载导致脚本可执行位丢失，恢复原有可执行位或在报告中说明为什么改为普通文件。

## 决策规则

- 触发范围变宽、新增脚本、shell、网络访问、凭证处理或许可不清时，建议审查或拒绝。
- 候选正文可更新但本地触发描述会被覆盖时，默认拒绝直接覆盖，改为“保留本地 description + 合并上游正文”。
- 只更新示例或窄范围指导时，可建议 pilot approval。
- 高风险或 critical 风险 skill 即使 pilot 也需要明确批准。
- bundle 归属变化时，确认前说明受影响工作流。
- 没有精确 upstream commit 或 tag 时，不标记为生产批准。

## 确认门

覆盖前必须展示：

- 工作流层：`company-skill-upgrade-runner`
- 透明度模式：
- Superpowers 叠加：`superpowers:verification-before-completion`
- 实际调用：
- 专家/插件能力：
- 未调用但采用视角：
- 第一性原理检查：
- 对抗式审查：
- 执行策略：默认 dry-run，用户确认后才覆盖。
- 验证证据：
- 未验证项：
- 剩余风险：
- 待更新 skills：
- 来源和候选 pin：
- 受影响 bundle：
- 同步范围：
- 本地保留项：
- 关键差异：
- 安全审查结果：
- 建议：
- 回滚路径：
- 需要确认：

模糊表达如“看起来不错”“继续”“似乎可以”不算覆盖确认。

## 升级报告

复杂升级使用技能升级报告模板，按以下顺序查找：

1. 项目内：`specs/global/assets/skill-upgrade-report-template.md`。
2. 插件内置 fallback：相对当前 skill 目录读取 `../../specs/global/assets/skill-upgrade-report-template.md`。

小升级可在对话中报告，但必须包含目标、当前版本、候选版本、diff 摘要、风险、用户决策、文件变更和验证。
