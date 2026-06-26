# 公司 Codex 工作流

本项目使用轻量 SDLC。目标是让需求、设计、实现和验证可追溯，同时不拖慢简单工作。

## 上下文优先

- 规划或编辑前，先阅读 `specs/global/INDEX.md`。
- 如果存在 `说明文档.md` 或等价进度文档，读取当前进展和项目状态。
- 只读取当前版本、里程碑、功能文档和相关源码。
- 除非任务是审计或迁移，不要扫描所有 Markdown 文件。

## 阶段边界

- 需求阶段产出目标、范围、验收标准和边界条件，不编辑实现代码。
- 设计阶段产出架构、契约、数据流、风险和测试策略，不编辑实现代码。
- 规划阶段产出可执行任务和验证点，不编辑实现代码。
- 实现阶段只在需求、设计和任务确认后开始，`/spike` 和 `/hotfix` 除外。
- 模糊的“继续”表示继续当前阶段，不表示进入下一阶段。

## Superpowers 可见叠加

- 每个 workflow 输出都必须显式包含 `工作流层`、`Superpowers 叠加` 和 `执行策略`。
- 每个 workflow 开头都必须显式包含 `实际调用`、`专家/插件能力` 和 `未调用但采用视角`，不能只写“专家视角”而不说明是否真实调用 skill。
- 每个 workflow 结尾都必须显式包含 `验证证据`、`未验证项` 和 `剩余风险`。如果本阶段不需要验证，必须说明原因。
- 如果某个 Superpowers、专家 skill、MCP、浏览器或其他 Codex 插件能力没有在当前会话真实暴露或真实调用，必须写入 `未调用但采用视角`，并说明原因。
- 需求探索默认叠加 `superpowers:brainstorming`。
- 复杂任务拆解默认叠加 `superpowers:writing-plans`。
- 实现阶段默认叠加 `superpowers:test-driven-development` 和 `superpowers:verification-before-completion`。
- Bugfix 默认叠加 `superpowers:systematic-debugging`，完成前叠加 `superpowers:verification-before-completion`。
- 如果某个简单任务不叠加 Superpowers，必须明确说明原因。

## 能力调用透明度

所有公司 workflow 默认使用以下透明度协议，除非用户明确要求极简输出：

开头：

- `工作流层：`
- `实际调用：` 写真实触发或读取的 workflow、Superpowers、专家 skill、MCP、浏览器能力。
- `专家/插件能力：` 写本轮需要或已选择的专家、Superpowers、Codex 插件能力。
- `未调用但采用视角：` 写当前会话不可见、阶段不适合或风险不值得真实调用的能力。
- `执行策略：`

结尾：

- `验证证据：` 写命令、检查结果、文件变更、截图、日志或人工检查证据。
- `未验证项：` 写未能验证或本阶段无需验证的内容。
- `剩余风险：`

不能用“已按专家视角执行”替代真实调用说明；必须区分 `已真实调用` 与 `仅采用视角`。

## 交接口令

- `需求已确认，进入技术设计`
- `方案已确认，进入任务拆解`
- `任务已确认，开始实现`
- `开始 bugfix`
- `/spike <技术问题>`
- `/hotfix <事故>`
- `检查技能更新`
- `更新 <skill-name> 技能`
- `对比并升级 <skill-name>`

## 专家使用

普通工作不要求用户手动点名专家。工作流应从 `BUNDLES.md` 选择最小匹配组合，再在当前阶段需要时使用对应专家。

如果用户明确点名专家，在不违反安全和项目约束的前提下优先遵循。

第三方 API 或框架行为可能变化时，优先使用官方最新文档。没有 Context7 类 MCP 时，说明限制并使用官方文档或本地包文档。

使用 `company-expert-routing` 作为专家选择入口。使用 `BUNDLES.md` 管理专家组合，使用 `EXPERTS.lock.md` 检查外部专家技能的来源、pin、许可和审查状态。优先读取项目根目录文件；如果项目内缺失，读取插件内置 fallback，不要直接放弃专家路由。

使用模板时优先读取项目内 `specs/global/assets/`；如果项目模板缺失，读取插件内置 fallback，并提醒用户执行 `bootstrap-project` 或 `update-templates` 补齐项目模板。

不要自动更新外部专家技能。采用 `company-skill-upgrade-runner` 获取候选版本、比对新旧内容、安全审查、输出建议，并等待用户明确确认后再覆盖。

自进化默认只产出提案。使用 `company-skill-evolution-lab` 记录重复问题并提出受控改进，不允许 skill 直接自改生产版本。

## 验证

- 功能工作在有测试框架时需要测试。
- Bug 修复在改代码前需要复现或清晰证据链。
- 完成报告必须包含准确验证命令或手工检查。
- 无法自动验证时，提供聚焦的手工检查清单。

## 文档

- 公司项目应维护 `说明文档.md` 或等价进度文档。
- 版本化 specs 可使用 `specs/versions/<version>/<milestone>/`。
- 小变更可使用 `specs/features/<feature>/` 下的紧凑 spec。
- 公共 API 和复杂逻辑需要注释；常规函数不需要样板注释。
