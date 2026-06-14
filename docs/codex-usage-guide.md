# Codex Usage Guide

这份文档说明公司用户如何在 Codex 里安装、初始化项目并完成一次完整功能交付。

## 1. 获取仓库

```bash
git clone https://github.com/<your-org>/codex-company-workflow-kit.git
cd codex-company-workflow-kit
```

## 2. 选择语言和安装方式

默认安装中文版本。英文版本使用 `--lang en` 或 PowerShell 的 `-Lang en`。

中文主包：

```text
outputs/company-codex-workflow-v2-zh/
```

英文主包：

```text
outputs/company-codex-workflow-v2/
```

### 全局安装

把公司 workflow 安装成 Codex 本机插件，之后任何项目都能唤起公司 skills。

macOS/Linux：

```bash
bash scripts/install.sh install-plugin --lang zh
```

Windows PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install.ps1 install-plugin -Lang zh
```

英文版本使用 `--lang en` 或 `-Lang en`。

全局插件安装后，公司 workflow skills 会以标准 Codex skill 形式提供，并包含 `agents/openai.yaml` UI 元数据。实际使用时有三种入口：

- 自然语言：例如“帮我判断现在该走哪个公司流程”。
- 显式 skill：例如 `$company-workflow-help`。
- Codex 客户端支持时的 skill picker / skill chips：显示名称、简介和默认提示来自每个 skill 下的 `agents/openai.yaml`。

这里不额外承诺自定义 `/company-...` slash 命令注册；如果当前 Codex 客户端只把 `/` 菜单用于内置命令，请使用自然语言或 `$skill` 入口。

### 项目安装

把公司规范和模板放进某个业务项目。

macOS/Linux：

```bash
bash scripts/install.sh bootstrap-project /path/to/project --lang zh
```

Windows PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install.ps1 bootstrap-project C:\path\to\project -Lang zh
```

### 组合安装

同时完成全局插件安装和项目初始化。

macOS/Linux：

```bash
bash scripts/install.sh all /path/to/project --lang zh
```

Windows PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install.ps1 all C:\path\to\project -Lang zh
```

npm 一键入口：

```bash
npx codex-company-workflow all /path/to/project --lang zh
```

默认不会覆盖已有文件。需要覆盖时显式加 `--force`。英文版本使用 `--lang en` 或 `-Lang en`。

### 只生成或刷新项目上下文索引

当项目已经安装过模板，只想重新生成 `INDEX.md` 草稿：

```bash
bash scripts/install.sh generate-index /path/to/project --lang zh
```

Windows PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install.ps1 generate-index C:\path\to\project -Lang zh
```

### 只更新已初始化项目里的模板

当公司 workflow kit 升级了 `specs/global/assets/` 里的模板，而业务项目已经初始化过时，不建议重新执行 `bootstrap-project --force`，因为那会替换整个 `specs/` 目录，可能影响项目里已有的需求、设计和任务文档。

推荐使用专门的模板更新命令。

macOS/Linux：

```bash
bash scripts/install.sh update-templates /path/to/project --lang zh
```

Windows PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install.ps1 update-templates C:\path\to\project -Lang zh
```

默认安全模式不会覆盖现有模板，而是生成：

```text
specs/global/assets.generated/
```

你可以让 Codex 对比：

```text
请对比 specs/global/assets 和 specs/global/assets.generated，说明模板有哪些变化，以及是否建议覆盖。
```

确认无问题后再覆盖：

```bash
bash scripts/install.sh update-templates /path/to/project --lang zh --force
```

PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install.ps1 update-templates C:\path\to\project -Lang zh -Force
```

### 卸载全局插件

如果只想从本机 Codex 里移除公司 workflow 插件：

macOS/Linux：

```bash
bash scripts/install.sh uninstall-plugin --lang zh
```

Windows PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install.ps1 uninstall-plugin -Lang zh
```

同时卸载中英文版本：

```bash
bash scripts/install.sh uninstall-plugin --all
```

PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install.ps1 uninstall-plugin -All
```

这会删除本机 marketplace 里的插件目录和插件记录，不会修改任何业务项目。

### 停用项目内工作流

如果某个业务项目不再使用公司 workflow：

```bash
bash scripts/install.sh deactivate-project /path/to/project
```

PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install.ps1 deactivate-project C:\path\to\project
```

默认只移除 `AGENTS.md` 里由 kit 管理的 marker 段落，并写入：

```text
.codex-workflow/deactivation-report.md
```

以下内容默认保留，因为它们可能已经成为项目资产：

- `specs/features/`
- `specs/global/INDEX.md`
- `specs/global/INDEX.generated.md`
- 已产生的需求、设计、任务和验证记录

如果确认要清理模板目录，再显式执行：

```bash
bash scripts/install.sh deactivate-project /path/to/project --force
```

PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install.ps1 deactivate-project C:\path\to\project -Force
```

`--force` 只清理可识别的模板目录：`specs/global/assets/` 和 `specs/global/assets.generated/`，不会删除 `specs/features/` 或 `INDEX.md`。

## 3. 确认项目上下文

打开业务项目里的：

```text
specs/global/INDEX.md
```

安装脚本会自动生成草稿，并标注“待用户确认”。项目负责人至少检查：

- Product
- Current version
- Current milestone
- Primary stack
- Test command
- Build command
- Local run command
- Main source entrypoints

旧项目已有 `INDEX.md` 时，默认不会覆盖。脚本会生成 `specs/global/INDEX.generated.md`，你可以让 Codex 对比两个文件，然后确认是否替换。

## 4. 空项目如何开始

如果这是一个从 0 到 1 的空项目，或者需求还只是雏形，初始化后的第一步不是写代码，而是建立第一份需求上下文。

推荐在业务项目里说：

```text
我现在是项目发起人，这还是一个空项目，需求只有雏形。请帮我走公司需求澄清流程，先不要写代码。
```

Codex 应进入 `company-feature-requirements`，优先帮你澄清：

- 项目目标和业务边界。
- 目标用户、核心场景和主要流程。
- MVP 范围和暂不做范围。
- 验收标准。
- 风险、依赖和待确认问题。

建议产物路径：

```text
specs/features/project-kickoff/requirements.md
```

此时 `INDEX.md` 里的技术栈、启动命令、测试命令可以先保持“待用户确认”。等技术方案确定后，再进入设计阶段补齐。

## 5. 旧项目如何切换

旧项目不要一次性切换成完整新流程。推荐按下面节奏：

```text
项目安装
-> 自动生成 INDEX 草稿
-> 项目负责人确认上下文
-> 选择一个小功能、bugfix 或 spike 试点
-> 复盘流程成本和验证质量
-> 再扩大到团队默认流程
```

在 Codex 里可以直接说：

```text
请帮我把这个旧项目接入公司 Codex 工作流
```

Codex 应进入 `company-legacy-project-onboarding`，先检查已有 `AGENTS.md`、README、manifest、docs、测试目录和启动命令，再生成或审查 `INDEX.md` 草稿。旧项目已有规则优先保留，公司 workflow 只追加约束段落。

不建议旧项目一开始就要求所有历史需求补齐 specs。更稳的做法是：从接入后的第一个新功能或第一个 bugfix 开始沉淀需求、设计、任务和验证证据。

完整说明见 [公司用户快速上手](company-quickstart.md)。

## 6. 在 Codex 里使用

当前可用技能树见 [Skill Tree](skill-tree.md)。公司用户通常不需要记 skill 名称，先用入口帮助即可。

公司 workflow 会在合适节点复用 Superpowers 和 Codex 内置能力。完整说明见 [公司用户快速上手](company-quickstart.md)。

如果不知道入口，说：

```text
我现在该走哪个流程？背景是：我们要做一个客户列表导出功能
```

做新功能：

```text
帮我梳理这个功能需求：客户列表支持按筛选条件导出 CSV
```

确认需求后：

```text
需求已确认，进入技术设计
```

确认设计后：

```text
方案已确认，进入任务拆解
```

确认任务后：

```text
任务已确认，开始实现
```

## 7. 完整流程例子

目标：客户列表支持按当前筛选条件导出 CSV。

1. 用户说：

```text
帮我梳理这个功能需求：客户列表支持按当前筛选条件导出 CSV
```

2. Codex 输出目标、范围、验收标准和边界条件。

3. 用户确认：

```text
需求已确认，进入技术设计
```

4. Codex 自动选择合适 bundle。若这是前端加后端接口，通常会偏向 `company-frontend-delivery` 和后端相关专家。

5. 用户确认方案：

```text
方案已确认，进入任务拆解
```

6. Codex 输出任务和验证点。

7. 用户确认实现：

```text
任务已确认，开始实现
```

8. Codex 按任务做 scoped edits，运行测试或给出手工验证。

   如果实现涉及非平凡行为，Codex 应在这个阶段使用 Superpowers TDD；完成前应给出验证证据。用户通常不需要手动输入 `/Superpowers /test-driven-development`。

9. 用户要求收尾：

```text
请给我本次变更总结、验证证据和剩余风险
```

## 8. 技能更新

默认 dry-run：

```text
检查专家技能更新
```

或：

```text
对比并升级 java-pro，先不要覆盖
```

Codex 会先输出新旧版本比对、安全审查和建议。只有你明确说：

```text
确认覆盖 java-pro
```

才允许覆盖生产 skill。

## 9. Superpowers 怎么配合

日常推荐说业务目标，而不是手动拼 skill 名称：

```text
帮我梳理这个功能需求：...
开始 bugfix：...
任务已确认，开始实现
```

公司 workflow 会自动在合适节点使用：

- `superpowers:brainstorming`
- `superpowers:test-driven-development`
- `superpowers:systematic-debugging`
- `superpowers:verification-before-completion`

高级用户可以显式要求：

```text
请结合 Superpowers brainstorming 帮我梳理这个方案
请用 Superpowers systematic-debugging 排查这个问题
请用 Superpowers test-driven-development 实现这个任务
```

如果当前 Codex 环境支持 `$superpowers:<skill>` 显式引用，也可以使用 `$superpowers:brainstorming` 这类形式。
