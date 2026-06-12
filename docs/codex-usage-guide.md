# Codex Usage Guide

这份文档说明公司用户如何在 Codex 里安装、初始化项目并完成一次完整功能交付。

## 1. 获取仓库

```bash
git clone https://github.com/haflen/codex-company-workflow-kit.git
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

## 4. 旧项目如何切换

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

完整说明见 [旧项目迁移指南](legacy-project-migration.md)。

## 5. 在 Codex 里使用

当前可用技能树见 [Skill Tree](skill-tree.md)。公司用户通常不需要记 skill 名称，先用入口帮助即可。

公司 workflow 会在合适节点复用 Superpowers 和 Codex 内置能力。完整说明见 [Superpowers Integration](superpowers-integration.md)。

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

## 6. 完整流程例子

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

## 7. 技能更新

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

## 8. Superpowers 怎么配合

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
