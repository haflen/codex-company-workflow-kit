---
name: company-feature-planning
description: Use when company requirements and technical design are confirmed and the work needs an implementation task plan with verification points.
---

# 公司功能任务拆解

## 目的

把已确认的需求和设计拆成可执行任务，并为每个任务标注验证点。

## 工作流

1. 确认需求和设计已可用；如果需求或设计链接了 `business-rules.md`，必须同时读取。
2. 如果设计阶段命中 L2/L3 方案对比条件，确认推荐方案已由用户确认；未确认时停止并回到 `company-feature-design`。
3. 跨边界工作确认 API 契约已存在。
4. 将工作拆成小任务，每个任务都包含验证方式和预估验证等级。
5. 任务新增或移动工程资产时，读取 `.codex-workflow/asset-boundaries.json`；每个任务写仓库相对完整路径、允许根目录和禁止根目录，不接受含糊的 `contracts/`、`scripts/` 等短路径。
6. 对计划路径运行 `.codex-workflow/bin/asset_boundaries.py check <project> --path <path>`；阻断项必须先回到设计修正，不能写成实现阶段注意事项。
7. 复杂计划显式叠加 `superpowers:writing-plans`，输出可执行计划和检查点。
8. 每个非平凡任务都包含最小失败案例或验证锚点，并至少包含一个对抗场景。
9. 如果存在 `business-rules.md`，把其中的样例用例、公式、状态流转和异常处理转成任务验证点；不得只写“按需求实现”。
10. 任务边界不清、跨团队或依赖复杂技术栈细节时，使用 `company-expert-routing`。
11. 如果任务合并后需要更新 `说明文档.md`、`specs/global/INDEX.md` 或阅读路线，增加“公共文档影响补丁”任务，而不是在业务分支直接改公共文档。
12. 如果任务可能改变需求、业务规则、技术设计、API 契约或项目入口，增加“文档漂移检查”任务。
13. 如果任务拆解来自实现阶段中的范围变化，必须写明旧实现授权已失效，新任务需要用户重新确认。
14. 标注连续执行资格：哪些任务可批量连续推进，哪些任务必须单独完成后停下确认。
15. 标注 subagent 拆分建议：哪些任务适合主 agent 串行执行，哪些适合子 agent 独立实现、独立排查或独立审查。
16. 任务规划阶段结束后停止，除非用户给出实现交接口令。

## Superpowers 叠加

- L1 小改动：通常不叠加，使用轻量任务卡；如涉及行为变化，则叠加 `superpowers:test-driven-development` 的最小失败案例思路。
- L2/L3 标准或复杂任务：默认叠加 `superpowers:writing-plans`。
- 每个任务必须包含验证点，为后续 `superpowers:test-driven-development` 和 `superpowers:verification-before-completion` 留出执行锚点。
- 业务规则文档中的样例用例优先转成自动测试；无法自动化时转成明确手工验证步骤。
- 任务验证等级按 `V0/V1/V2/V3` 预估；最终等级由实现或 bugfix 完成前确认。
- 只有任务边界、验证点和停止条件清楚时，才标记为可连续执行。
- 对 L2/L3 多任务计划，必须显式判断是否建议使用 Codex subagents；不建议时说明是因为任务耦合、文件冲突或收益不足。真实调用仍需要用户显式请求。

## 产物

使用任务模板时按以下顺序查找：

1. 项目内：`specs/global/assets/tasks-template.md`。
2. 插件内置 fallback：相对当前 skill 目录读取 `../../specs/global/assets/tasks-template.md`。

公共文档影响补丁模板按以下顺序查找：

1. 项目内：`specs/global/assets/public-doc-update-template.md`。
2. 插件内置 fallback：相对当前 skill 目录读取 `../../specs/global/assets/public-doc-update-template.md`。

## 好任务标准

- 足够小，可以在一次聚焦实现中完成。
- 有具体验证命令或手工检查。
- 不把无关重构混入功能交付。

## 连续执行资格

任务计划必须帮助后续实现器判断能否批量推进：

- `可连续`：`V0/V1` 或强相关 `V2`，范围清楚、验证点明确、失败不会扩大影响。
- `谨慎连续`：`V2` 且跨多个文件/页面/API，但仍在同一已确认任务链内；每 1-3 个任务后复核。
- `必须停下`：`V3`，或涉及生产、权限、安全、数据迁移、金额/指标公式、跨系统、未确认业务规则、范围变化、用户决策点。

连续执行任务仍必须逐项完成验证；不能因为“连续”而跳过 TDD、文档漂移检查或完成前验证。

## Subagent 拆分策略

任务计划必须帮助后续实现器判断是否值得使用 subagents：

- `不需要`：任务很小、边界单一、共享文件集中、主 agent 一次完成更省 token。
- `可用实现子 agent`：任务边界清楚，输入输出明确，只触碰少量文件，验证方式明确，和其他任务没有共享写入冲突。
- `可用排查子 agent`：多个测试失败、多个页面问题或多个模块问题彼此独立，适合按问题域并行定位。
- `可用审查子 agent`：L2/L3 或连续执行批次完成后，需要独立做规格一致性审查、代码质量审查、测试覆盖审查或安全风险审查。
- `禁止并行子 agent`：多个任务会编辑同一核心文件、共享数据库迁移、共享接口契约、同一状态模型或同一公共文档段落。
- `需要 custom agents`：建议使用公司 reviewer/test/security/explorer 角色，但项目尚未生成 `.codex/agents/`；提示执行 `bash scripts/install.sh install-agents <project-path> --lang zh`。

每个建议使用 subagent 的任务都要写清楚：

- 子 agent 角色：实现 / 排查 / 规格审查 / 代码质量审查 / 测试策略审查。
- 输入上下文：需求、设计、任务 ID、允许文件、禁止事项。
- 预期输出：变更摘要、验证证据、风险、是否阻塞。
- 合并策略：主 agent 复核 diff 和验证，不直接接受子 agent 的完成结论。

## 输出格式

- 工作流层：`company-feature-planning`
- 透明度模式：
- Superpowers 叠加：
- 实际调用：
- 专家/插件能力：
- 未调用但采用视角：
- 第一性原理检查：
- 对抗式审查：
- 执行策略：
- 验证证据：
- 未验证项：
- 剩余风险：
- 任务列表：
- 方案确认状态：
- 每个任务的最小失败案例或验证锚点：
- 每个任务的预估验证等级：
- 每个任务的连续执行资格：
- 必须停下确认的任务：
- Subagents 建议：不需要 / 建议使用 / 强烈建议使用
- Subagent 能力状态：未检查 / 需要用户显式请求 / 需要本地 custom agents 配置 / 当前 App 仅展示活动
- 每个任务的 subagent 策略：
- 禁止并行或必须主 agent 串行的任务：
- 子 agent 任务包草案：
- 每个任务的对抗场景：
- 业务规则验证覆盖：
- 文档漂移检查任务：
- 公共文档影响任务：
- 资产落点门禁：通过 / 阻断 / 不触发
- 实现交接口令：
- 实现授权状态：
