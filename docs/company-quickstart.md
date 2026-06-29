# Company Quickstart

这份文档面向公司项目用户，也是内部培训的主入口。用户不需要记住所有 skill 名称，只需要知道在什么场景说什么。

如果你是第一次使用，建议先看：

- [Codex 使用完整说明](codex-usage-guide.md)
- [公司试点手册](pilot-playbook.md)
- [技能树清单](skill-tree.md)
- [技能升级 dry-run 工作流](skill-upgrade-dry-run.md)

## 第一次放进项目

推荐使用一键脚本：

```bash
bash scripts/install.sh all /path/to/project --lang zh
```

Windows：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install.ps1 all C:\path\to\project -Lang zh
```

英文版本使用 `--lang en` 或 `-Lang en`。

注意：本仓库里写的 `/hotfix`、`/spike` 只是推荐输入法，不是 Codex UI 里自动注册的 slash 命令；在 Codex 里直接输入这些句子即可触发路由。

公司 workflow skills 已补齐 `agents/openai.yaml`，和常见开源 Codex skills 一样提供 UI 技能列表/chips 所需的名称、简介和默认提示。安装插件后，如果 Codex 客户端展示 skill picker 或 skill chips，应该能看到这些公司 workflow 入口；如果客户端只把 `/` 菜单用于内置命令，则请使用自然语言或 `$company-workflow-help` 触发。

强依赖专家 skills 也随公司插件一起安装，例如 `frontend-developer`、`typescript-expert`、`frontend-design`、`testing-qa`。安装或更新插件后，请新开 Codex 线程让当前会话刷新 skill 列表。

公司 workflow 每轮默认输出能力调用透明度信息。试点验收时，除了看需求、设计、任务和代码产物，还要检查回复是否包含 `透明度模式`、`实际调用`、`专家/插件能力`、`未调用但采用视角`、`验证证据`、`未验证项` 和 `剩余风险`。`透明度模式` 由 workflow 自动判定：普通推进用 `light`，阶段交接、完成报告、hotfix、spike 结论、技能升级、安全审查、专家能力未真实调用或验证缺失时用 `full-audit`。如果缺少这些字段，说明 workflow 没有完整执行透明度协议。

复杂需求、技术设计、bugfix、hotfix、spike、实现完成和技能升级场景，还要检查回复是否包含 `第一性原理检查` 和 `对抗式审查`。普通小改动可以跳过，但 Codex 必须说明跳过原因。

如果你想用 npm 一键入口，先把这个仓库发布成 npm 包，或者在本地 `npm link`，然后执行：

```bash
npx codex-company-workflow all /path/to/project --lang zh
```

这个 npm 命令只是包装层，实际执行的还是仓库里的 `scripts/install.sh` 和 `scripts/install.ps1`。

手工方式：

1. 把 `outputs/company-codex-workflow-v2-zh/AGENTS.md` 合并到目标项目根目录的 `AGENTS.md`。
2. 把 `outputs/company-codex-workflow-v2-zh/specs/global/assets/` 复制到目标项目的 `specs/global/assets/`。
3. 把 `outputs/company-codex-workflow-v2-zh/BUNDLES.md` 和 `outputs/company-codex-workflow-v2-zh/EXPERTS.lock.md` 复制到目标项目根目录。
4. 运行 `bash scripts/install.sh generate-index /path/to/project --lang zh` 生成 `specs/global/INDEX.md` 草稿。
5. 检查并确认产品名称、当前版本、里程碑、技术栈、启动/测试/构建命令、主要源码入口、文档职责地图和编号命名空间。
6. 根据公司实际技术栈调整 `BUNDLES.md`。
7. 检查 `.codex-workflow/EXPERT-READINESS.md`，确认强依赖专家已随插件内置、自动审查并可在新会话中暴露。

旧项目已有 `INDEX.md` 时，项目初始化默认不会覆盖。脚本会生成 `specs/global/INDEX.generated.md`，先由项目负责人确认，再决定是否替换原索引。

如果项目里已经有 `说明文档.md`、spike 工作日志、`docs/lifecycle/` 或多套历史日报，优先确认 `INDEX.md` 里的“文档职责地图”。入口页不延续 spike 任务号；spike 日志使用 `SPKxx-T001`；正式任务使用 feature、版本或正式任务编号。

如果项目运行工作流时提示找不到 `BUNDLES.md`、`EXPERTS.lock.md` 或 `specs/global/assets/` 模板，执行下面命令补齐：

```bash
bash scripts/install.sh update-templates /path/to/project --lang zh
```

已有文件默认不会被覆盖；脚本会生成 `.generated` 文件供对比确认。

## 空项目或需求雏形

如果项目还是空目录，或者还在需求梳理阶段，`bootstrap-project` 仍然适合先执行。它会先放入 `AGENTS.md` 和 `specs/`，让 Codex 有统一的需求沉淀位置。

这种阶段不要急着进入技术设计或实现。建议先说：

```text
我现在是项目发起人，这还是一个空项目，需求只有雏形。请帮我走公司需求澄清流程，先不要写代码。
```

然后让 Codex 产出或维护：

- 项目愿景和业务目标。
- 目标用户和核心场景。
- MVP 范围。
- 暂不做范围。
- 验收标准。
- 关键风险和待确认问题。

推荐把第一版需求放在：

```text
specs/features/project-kickoff/requirements.md
```

`specs/global/INDEX.md` 在空项目里会有很多“待用户确认”，这是正常的。先确认产品名、业务边界和当前阶段即可；技术栈、启动命令、测试命令可以等技术方案确定后再补。

## 旧项目接入

旧项目不要一上来强制套完整流程。推荐先把工作流作为旁路治理层接入，跑通后再逐步收敛到标准 SDLC。

推荐节奏：

```text
安装工作流
-> 自动生成 INDEX.md 草稿
-> 用户/项目负责人确认上下文
-> 选择一个小功能或 bugfix 试点
-> 复盘流程负担和产物质量
-> 再决定是否扩大到团队默认流程
```

推荐先说：

```text
请帮我把这个旧项目接入公司 Codex 工作流
```

Codex 应先检查已有 `AGENTS.md`、README、manifest、docs、测试目录和启动命令，再生成或审查 `INDEX.md` 草稿。旧项目已有规则优先保留，公司 workflow 只追加约束段落。

## 常用说法

```text
我现在该走哪个流程？背景是：<当前情况>
```

```text
帮我判断这个任务应该走需求、设计、实现、bugfix、hotfix 还是 spike：<任务描述>
```

```text
帮我梳理这个功能需求：<功能描述>
```

```text
请结合 Superpowers brainstorming 帮我梳理这个方案：<背景>
```

```text
请用 Superpowers systematic-debugging 排查这个问题：<问题描述>
```

```text
请帮我把这个旧项目接入公司 Codex 工作流
```

```text
请生成并检查这个项目的 INDEX.md 草稿
```

```text
我现在是项目发起人，这还是一个空项目，需求只有雏形。请帮我走公司需求澄清流程，先不要写代码。
```

```text
开始 bugfix：<现象、复现步骤、期望行为>
```

```text
/hotfix <事故描述>
```

```text
/spike <需要验证的技术问题>
```

## 连接 Superpowers

公司 workflow 不要求用户手动输入 `Superpowers` skill 名称。更自然的方式是直接说业务目标，让工作流在节点里自动结合对应能力。

用户通常只需要这样说：

```text
帮我梳理这个功能需求：...
开始 bugfix：...
任务已确认，开始实现
```

如果需要显式强调，也可以说：

```text
请结合 Superpowers brainstorming 帮我澄清这个方案
请用 Superpowers systematic-debugging 排查这个问题
请用 Superpowers test-driven-development 实现这个任务
```

如果当前 Codex 环境支持 `$superpowers:<skill>` 形式，也可以用：

```text
$superpowers:brainstorming
$superpowers:systematic-debugging
$superpowers:test-driven-development
```

## 更新、停用和卸载

更新已初始化项目里的模板：

```bash
bash scripts/install.sh update-templates /path/to/project --lang zh
```

默认只生成 `specs/global/assets.generated/` 供对比。确认后再覆盖：

```bash
bash scripts/install.sh update-templates /path/to/project --lang zh --force
```

停用项目内 workflow：

```bash
bash scripts/install.sh deactivate-project /path/to/project
```

默认保留项目资产，只移除 `AGENTS.md` 里的 workflow marker 段落。

卸载本机全局插件：

```bash
bash scripts/install.sh uninstall-plugin --lang zh
```

同时卸载中英文插件：

```bash
bash scripts/install.sh uninstall-plugin --all
```

## 培训时怎么讲

第一次内部培训可以直接按这个顺序讲：

1. 为什么需要这套 workflow。
2. 怎么安装到 Codex。
3. 空项目怎么从需求雏形开始。
4. 旧项目怎么接入。
5. 一个 feature、一个 bugfix、一个 spike 分别怎么走。
6. 怎么和 Superpowers 配合。
7. 模板更新、停用和卸载怎么做。

如果要给新人一页纸说明，直接复用本文件，不再单独维护另一份培训文档。

## 常见安装问题

### `/path/to/project` 可以直接复制吗？

不可以。`/path/to/project` 是占位符，要替换成真实项目路径。

错误示例：

```bash
bash scripts/install.sh bootstrap-project /path/to/company-trade-platform --lang zh
```

正确示例：

```bash
bash scripts/install.sh bootstrap-project /absolute/path/to/company-trade-platform --lang zh
```

### `bash: scripts/install.sh: No such file or directory` 是什么原因？

说明你当前目录不是 workflow kit 仓库。`scripts/install.sh` 在 `codex-company-workflow-kit` 里，不在业务项目里。

推荐方式：

```bash
cd /absolute/path/to/codex-company-workflow-kit
bash scripts/install.sh bootstrap-project /absolute/path/to/company-trade-platform --lang zh
```

如果已经在业务项目目录，也可以用绝对路径调用脚本：

```bash
bash /absolute/path/to/codex-company-workflow-kit/scripts/install.sh bootstrap-project /absolute/path/to/company-trade-platform --lang zh
```
