# Codex Company Workflow Kit

公司项目使用的 Codex 工作流 starter kit，目标是让团队在 Codex 里稳定完成需求澄清、技术设计、任务拆解、实现验证、bugfix、hotfix、spike 和专家技能治理。

这不是为了把流程做重，而是为公司项目提供轻量护栏：

- 需求、设计、实现、验证可追溯。
- 旧项目能平滑接入，不覆盖已有规范。
- 强依赖专家 skills 随公司插件内置安装，用户不需要逐个对话安装。
- 专家 skills 通过 bundle 自动路由；安装和项目初始化会自动生成专家就绪和安全审查报告。
- 外部专家技能后续更新走 dry-run、diff、安全审查、用户确认和回滚记录。
- 项目上下文索引 `INDEX.md` 可以自动生成草稿，再由用户确认。
- 每轮执行会显式区分实际调用的 Superpowers/专家/插件能力，以及未调用但采用的专家视角。

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
- `EXPERT-READINESS.md`：安装期自动生成的专家依赖就绪和安全审查报告。
- `skills/`：公司工作流 skills。
- `skills/*/agents/openai.yaml`：Codex UI 技能列表/chips 使用的名称、简介和默认提示。
- `specs/global/assets/`：需求、设计、任务、hotfix、spike、技能升级报告模板。

## 能力调用透明度

公司 workflow 默认自动判定透明度级别，用户不需要自己选择：

- `light`：普通阶段内推进、小改动、低风险文档更新、简单入口推荐。
- `full-audit`：阶段交接、实现完成、bugfix 完成、hotfix、spike 结论、技能升级、安全审查、专家能力未真实调用、验证缺失，或涉及生产、数据、权限、架构、性能、安全风险。

## 第一性原理和对抗式审查

公司 workflow 内置两个质量检查，不需要用户每次手动补 prompt：

- `第一性原理检查`：复杂需求、技术设计、bugfix 根因、spike 结论前，回到底层事实、约束和最小成立条件，避免只修表层症状。
- `对抗式审查`：实现完成、bugfix 完成、hotfix、spike 结论、技能升级和安全审查前，从极端输入、异常状态、权限绕过、并发重试、未来时间、缓存假阳性和 UI 渲染压力等反例检查稳健性。

这些检查已经写入 `AGENTS.md`、核心 workflow skills 和项目模板。普通小改动可以跳过，但必须说明原因。

## 文档职责和编号命名空间

公司 workflow 还内置文档职责协议，避免把项目入口、spike 现场日志、正式 specs 和生命周期总结混成一条任务链：

- `说明文档.md` 或等价入口页只写项目入口、当前状态、最近重要事件和阅读路线，不承载 spike 流水任务。
- Spike 工作日志使用 spike 内部编号，例如 `SPK02-T001`。
- 正式任务使用 feature、版本或正式任务编号，例如 `FEAT-DT-T01`。
- `specs/global/INDEX.md` 维护文档职责地图、编号命名空间和更新触发条件。

如果旧项目出现同一个裸编号同时存在于入口文档和 spike 日志中，先修正文档职责地图和编号命名空间，再继续写入。

多分支并行时，公共入口文档按主线事实管理：

- `说明文档.md`、`specs/global/INDEX.md` 默认只在 main、develop、integration 或明确集成分支更新。
- feature、spike、hotfix 分支不把未合并内容写成项目“当前状态”。
- 分支影响公共入口、阅读路线、当前阶段或文档职责时，写 `docs/public-doc-updates/<branch-or-feature>.md`。
- 合并阶段统一把已合并事实同步到公共文档。

每轮输出会明确区分：

- `透明度模式`：本轮自动选择的 `light` 或 `full-audit`。
- `实际调用`：本轮真实触发或读取的 workflow、Superpowers、专家 skill、MCP、浏览器或 Codex 插件能力。
- `专家/插件能力`：本轮选择或依赖的专家、Superpowers、Codex 插件能力。
- `未调用但采用视角`：当前会话不可见、阶段不适合或风险不值得真实调用的能力。
- `第一性原理检查` 和 `对抗式审查`：本轮执行的底层事实检查、反例场景或跳过原因。
- `验证证据`：命令、检查结果、文件变更、截图、日志或人工检查证据。
- `未验证项` 和 `剩余风险`。

`full-audit` 会额外输出 `Workflow Audit`，说明阶段边界、Superpowers 声明、专家/插件真实调用、仅采用视角、验证证据和未验证项。这条规则已经写入插件 `AGENTS.md` 和所有 `company-*` workflow skill，不需要用户每次在对话里重复提醒。

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
- 补齐 `specs/global/assets/` 模板。
- 补齐项目根目录的 `BUNDLES.md` 和 `EXPERTS.lock.md`，用于专家技能组合和版本锁定。
- 生成 `.codex-workflow/EXPERT-READINESS.md` 和 `.codex-workflow/EXPERT-READINESS.json`。
- 自动扫描 README、manifest、测试目录、启动/构建/测试命令和常见源码入口。
- 生成 `specs/global/INDEX.md` 草稿，包含文档职责地图和编号命名空间。

如果旧项目已有 `INDEX.md`，默认保留原文件，并生成 `specs/global/INDEX.generated.md` 供确认。

如果项目中已有 `BUNDLES.md` 或 `EXPERTS.lock.md`，默认不会覆盖，而是生成 `BUNDLES.generated.md` 或 `EXPERTS.lock.generated.md` 供对比。确认后再使用 `--force` 覆盖。

只刷新项目上下文索引：

```bash
bash scripts/install.sh generate-index /path/to/company-project --lang zh
```

只检查专家依赖是否开箱可用：

```bash
bash scripts/install.sh expert-preflight /path/to/company-project --lang zh
```

只更新已初始化项目里的工作流模板：

```bash
bash scripts/install.sh update-templates /path/to/company-project --lang zh
```

这个命令也会检查并补齐 `BUNDLES.md` 和 `EXPERTS.lock.md`。默认不覆盖现有模板和专家依赖文件，而是生成：

```text
specs/global/assets.generated/
BUNDLES.generated.md
EXPERTS.lock.generated.md
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
检查这个项目的专家依赖是否就绪
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

强依赖专家已作为 vendored skills 随公司插件发布，保证开箱即用。后续不要静默拉取外部专家技能覆盖生产版本；外部技能更新必须走 dry-run、diff、安全审查、用户确认、覆盖更新、验证和回滚记录。
