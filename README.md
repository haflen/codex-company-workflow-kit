# Codex Company Workflow Kit

公司项目使用的 Codex 工作流 starter kit，目标是让团队在 Codex 里稳定完成需求澄清、技术设计、任务拆解、实现验证、bugfix、hotfix、spike 和专家技能治理。

这不是为了把流程做重，而是为公司项目提供轻量护栏：

- 需求、设计、实现、验证可追溯。
- 旧项目能平滑接入，不覆盖已有规范。
- 专家 skills 通过 bundle 自动路由，不要求用户手动点名。
- 外部专家技能更新走 dry-run、diff、安全审查、用户确认和回滚记录。
- 项目上下文索引 `INDEX.md` 可以自动生成草稿，再由用户确认。

## 当前主包

中文主包：

```text
outputs/company-codex-workflow-v2-zh/
```

英文主包：

```text
outputs/company-codex-workflow-v2/
```

轻量模板中文版：

```text
outputs/company-codex-workflow-template-zh/
```

轻量模板英文版：

```text
outputs/company-codex-workflow-template/
```

关键文件：

- `AGENTS.md`：公司项目硬约束和常用唤起语。
- `BUNDLES.md`：专家技能组合，工作流自动选择。
- `EXPERTS.lock.md`：外部专家技能依赖锁、来源、风险、bundle 影响面。
- `skills/`：公司工作流 skills。
- `skills/*/agents/openai.yaml`：Codex UI 技能列表/chips 使用的名称、简介和默认提示。
- `specs/global/assets/`：需求、设计、任务、hotfix、spike、技能升级报告模板。

## 安装

全局安装中文公司版插件：

```bash
bash scripts/install.sh install-plugin --lang zh
```

全局安装会把插件源码复制到 `~/plugins/<plugin-name>`，并把索引写入 `~/.agents/plugins/marketplace.json`。这是 Codex personal marketplace 的路径约定；不要手工改成 `~/.agents/plugins/plugins/<plugin-name>`。

初始化真实公司项目：

```bash
bash scripts/install.sh bootstrap-project /path/to/company-project --lang zh
```

`/path/to/company-project` 是占位符，需要替换成真实项目路径，例如：

```bash
bash scripts/install.sh bootstrap-project /absolute/path/to/company-trade-platform --lang zh
```

全局插件安装 + 项目初始化一起执行：

```bash
bash scripts/install.sh all /path/to/company-project --lang zh
```

英文版本使用 `--lang en`。

npm 一键入口：

```bash
npx codex-company-workflow all /path/to/company-project --lang zh
```

本地开发时也可以先执行 `npm link`，再直接用 `codex-company-workflow ...`。

默认不覆盖已有文件。需要覆盖时显式加 `--force`。

## 项目初始化会做什么

`bootstrap-project` 会把公司工作流初始化到某个具体项目里：

- 创建或合并 `AGENTS.md`。
- 复制 `specs/` 模板。
- 自动扫描 README、manifest、测试目录、启动/构建/测试命令和常见源码入口。
- 生成 `specs/global/INDEX.md` 草稿。

如果旧项目已有 `INDEX.md`，默认保留原文件，并生成 `specs/global/INDEX.generated.md` 供确认。

只刷新项目上下文索引：

```bash
bash scripts/install.sh generate-index /path/to/company-project --lang zh
```

只更新已初始化项目里的工作流模板：

```bash
bash scripts/install.sh update-templates /path/to/company-project --lang zh
```

默认不覆盖现有模板，而是生成：

```text
specs/global/assets.generated/
```

确认新旧模板差异后，再显式覆盖：

```bash
bash scripts/install.sh update-templates /path/to/company-project --lang zh --force
```

## 卸载和停用

卸载本机全局插件：

```bash
bash scripts/install.sh uninstall-plugin --lang zh
```

同时卸载中英文全局插件：

```bash
bash scripts/install.sh uninstall-plugin --all
```

停用某个项目里的公司工作流：

```bash
bash scripts/install.sh deactivate-project /path/to/company-project
```

默认只移除 `AGENTS.md` 里的公司 workflow marker 段落，并生成：

```text
.codex-workflow/deactivation-report.md
```

项目里的 `specs/features/`、`specs/global/INDEX.md` 和验证记录默认保留。需要同时清理模板目录时，显式执行：

```bash
bash scripts/install.sh deactivate-project /path/to/company-project --force
```

## 常用说法

```text
我现在该走哪个流程？背景是：<当前情况>
帮我梳理这个功能需求：<功能描述>
需求已确认，进入技术设计
方案已确认，进入任务拆解
任务已确认，开始实现
开始 bugfix：<问题描述>
/hotfix <线上事故>
/spike <技术问题>
请帮我把这个旧项目接入公司 Codex 工作流
请生成并检查这个项目的 INDEX.md 草稿
我现在是项目发起人，这还是一个空项目，需求只有雏形。请帮我走公司需求澄清流程，先不要写代码。
检查专家技能更新
对比并升级 java-pro，先不要覆盖
确认覆盖 java-pro
```

## 推荐阅读

1. [公司用户快速上手](docs/company-quickstart.md)
2. [Codex 使用完整说明](docs/codex-usage-guide.md)
3. [技能树清单](docs/skill-tree.md)
4. [公司试点手册](docs/pilot-playbook.md)
5. [技能升级 dry-run 工作流](docs/skill-upgrade-dry-run.md)

## Git 策略

建议版本节奏：

- `v0.2.x`：starter kit 文档和流程调整。
- `v0.3.x`：专家依赖、bundle、升级流程调整。
- `v1.0.0`：公司项目试点稳定后发布。

不要自动拉取外部专家技能到生产版本。外部技能更新必须走 dry-run、diff、安全审查、用户确认、覆盖更新、验证和回滚记录。
