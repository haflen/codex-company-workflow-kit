---
name: company-workflow-health-check
description: Use when a company project needs to diagnose workflow installation health, project bootstrap completeness, template freshness, plugin exposure, or why company workflow skills and templates are not working as expected.
---

# 公司工作流健康检查

## 目的

用只读方式判断一个公司项目是否已经正确接入 Codex 工作流，尤其适合旧项目、半初始化项目、模板缺失、插件升级后未同步、或用户反馈“明明装了但用起来不对”的场景。

## 与相邻技能的区别

- `company-workflow-help` 判断“当前该走哪条 workflow”。
- `company-expert-readiness` 判断“专家 skill 是否安装、审查、暴露和可调用”。
- `company-workflow-health-check` 判断“项目级工作流环境是否健康”：根文件、模板、索引、旧规则残留、版本漂移、诊断证据和修复命令。

## 工作流

1. 只读检查项目根目录，不修改业务代码或项目文档。
2. 检查根目录文件：`AGENTS.md`、`BUNDLES.md`、`EXPERTS.lock.md`。
3. 检查索引和模板：`specs/global/INDEX.md`、`specs/global/assets/`。
4. 检查关键模板是否存在：requirements、business-rules、design、api-contract、tasks、spike、hotfix、change-request、public-doc-update、skill-upgrade、workflow-health-report。
5. 检查项目是否包含最新规则标记：Superpowers 可见叠加、第一性原理、对抗式审查、业务规则与计算口径、方案对比、多分支公共文档协议、阶段一致性预检、验证等级、文档漂移。
6. 检查是否存在旧规则或旧来源残留；如存在，标记为迁移风险，不自动删除。
7. 检查当前分支、公共文档边界和阶段一致性：入口页、`INDEX.md`、当前 version/feature README、任务文档是否指向同一阶段。
8. 发现入口页仍指向 spike/待办、但当前任务文档已进入正式实现时，标记为 `yellow` 或 `red`，并建议先修 public-doc patch 或入口路由。
9. 如发现模板缺失或旧版本，给出安全修复命令；默认推荐 `update-templates`，不要直接覆盖用户文档。

## 健康等级

- `green`：核心文件、索引、模板和关键规则齐全；可以正常走 workflow。
- `yellow`：可工作，但存在模板缺失、旧规则残留、版本漂移或公共文档边界不清；建议先修复再进入复杂交付。
- `red`：缺少 `AGENTS.md`、`BUNDLES.md`、`EXPERTS.lock.md` 或 `specs/global/INDEX.md` 中任意关键入口；复杂任务不应继续。

## 修复建议规则

- 只缺模板：推荐 `bash scripts/install.sh update-templates <project-path> --lang zh`。
- 缺项目工作流入口：推荐 `bash scripts/install.sh bootstrap-project <project-path> --lang zh`。
- 插件缺失或技能不暴露：推荐先重新安装插件，再重启 Codex。
- 旧项目规则残留：推荐生成迁移清单，由用户确认后再整理，不自动删除。

## 输出格式

- 工作流层：`company-workflow-health-check`
- 透明度模式：`full-audit`
- Superpowers 叠加：通常无；如果需要设计修复方案，可叠加 `superpowers:brainstorming`
- 实际调用：
- 专家/插件能力：
- 未调用但采用视角：
- 第一性原理检查：判断最小可用条件是什么
- 对抗式审查：旧项目、旧规则、半初始化、分支并行、插件未刷新等反例
- 健康等级：green / yellow / red
- 已检查文件：
- 缺失项：
- 版本或模板漂移：
- 公共文档边界：
- 阶段一致性预检：
- 本轮建议权威文档：
- 外部专家状态：
- 建议修复命令：
- 不建议自动处理：
- 验证证据：
- 未验证项：
- 下一步建议：

## 边界

不要在健康检查中直接修复项目，除非用户明确要求“按建议修复”。

不要因为项目能运行就判定 workflow 健康；本技能判断的是 Codex 工作流接入状态，不是业务系统运行状态。
