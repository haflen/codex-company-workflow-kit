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

安装脚本会把插件源码放到 `~/plugins/<plugin-name>`，把 marketplace 索引写入 `~/.agents/plugins/marketplace.json`，并自动调用 Codex CLI 的 `plugin add` 刷新已安装缓存。输出中的 `version` 和 `installedPath` 是实际激活版本证据。如果找不到 Codex CLI，脚本会给出手工刷新命令；如果插件菜单能看到卡片但点击添加失败，优先检查插件是否误放到了 `~/.agents/plugins/plugins/<plugin-name>`。

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

安装公司插件也会安装强依赖专家 skills。用户不需要逐个安装 `frontend-design`、`frontend-developer`、`typescript-expert`、`testing-qa` 等专家；安装脚本会自动生成 `EXPERT-READINESS.md` 安全审查和就绪报告。安装器会刷新插件缓存，但已经打开的旧会话不会动态重载 skill 列表；安装完成后请新开 Codex 线程。

每轮公司 workflow 还会默认输出能力调用透明度信息，包括 `透明度模式`、`实际调用`、`专家/插件能力`、`未调用但采用视角`、`验证证据`、`未验证项` 和 `剩余风险`。透明度级别由 workflow 自动选择：

- `light`：普通阶段内推进、小改动、低风险文档更新、简单入口推荐。
- `full-audit`：阶段交接、实现完成、bugfix 完成、hotfix、spike 结论、技能升级、安全审查、专家能力未真实调用、验证缺失，或涉及生产、数据、权限、架构、性能、安全风险。

这用于区分“真实调用了 Superpowers/专家 skill/插件能力”和“只是按对应视角执行”，团队成员不需要每次额外提醒。

从 `0.2.22` 起，workflow 还会像反馈 Superpowers 一样反馈 Codex 计划模式和 subagents：

- `Codex 计划模式建议`：用于判断是否应先进入 Codex 计划模式做路线选择。计划模式只输出路线、风险、待确认问题和下一步口令，不改文件、不编码。
- `Subagents 建议`：用于判断是否值得把独立任务、独立失败域或独立审查交给子 agent。小任务默认不用，避免增加 token 和协调成本。
- `Subagent 能力状态`：用于说明当前是未检查、需要用户显式请求、需要本地 custom agents 配置，还是当前 App 主要展示活动。
- `Subagents 实际调用`：用于说明本轮是未调用、已调用，还是仅采用拆分视角。子 agent 结果必须由主 agent 复核后才能作为结论。

公司 workflow 还内置两类质量检查：

- `第一性原理检查`：复杂需求、设计、bugfix 根因和 spike 结论前，要求 Codex 回到底层事实、约束和最小成立条件。
- `对抗式审查`：实现完成、bugfix 完成、hotfix、spike 结论、技能升级和安全审查前，要求 Codex 从极端输入、异常状态、权限绕过、并发重试、未来时间、缓存假阳性和 UI 渲染压力等反例角度验证。

普通小改动可以跳过这些检查，但回复里必须说明跳过原因。

实现、bugfix 和 hotfix 完成时还会输出：

- `验证等级`：`V0` 纯文档、`V1` 小改动、`V2` 标准功能或普通 bugfix、`V3` 生产/权限/安全/数据/性能/公式/hotfix。
- `文档漂移影响`：判断是否需要同步 requirements、business-rules、design、api-contract、tasks、`说明文档.md`、`specs/global/INDEX.md` 或公共文档影响补丁。
- `代码备注检查`：判断 Java、前端 TypeScript/Vue/React、Python、SQL 或脚本中的业务规则、计算口径、数据映射、异常分支和非显然技术决策是否已有必要中文备注。

这两项用于控制验证成本：小任务不全量跑，大任务不低配验证。

在实现、bugfix 或 hotfix 前，workflow 还会执行阶段一致性预检：

- 读取入口页、`specs/global/INDEX.md`、当前 feature/version README、任务文档和相关 public-doc patch。
- 判断公共入口、索引和当前任务文档是否指向同一阶段。
- 如果发现入口页仍停在 spike/待办，但当前任务已经进入正式开发，Codex 会先说明冲突、本轮权威文档和修复建议。
- 普通实现和 bugfix 应先修正路由再动代码；生产 hotfix 可先止血，但完成报告必须记录补偿文档任务。

如果实现过程中发现遗漏了重要范围，例如 `data-preparation` 加工层、目标表、接口边界、调度链路、业务口径或字段映射，workflow 会触发范围变化熔断：

- 旧的实现授权失效，Codex 应输出 `实现授权状态：已失效，需要用户确认后再编码`。
- 本轮只允许补需求、设计、任务、字段映射或公共文档影响补丁。
- 补完文档后必须等用户确认新范围，再重新使用 `任务已确认，开始实现` 进入编码。

如果任务清单已经确认，并且你希望减少每个小任务后的确认，可以启用受控连续执行：

```text
任务已确认，连续完成后续所有可执行任务；遇到范围变化、V3 风险、验证失败或需要我确认时再停。
```

Codex 会自动判断是否适合连续执行。`V0/V1` 可以连续处理相关任务，`V2` 只处理 1-3 个强相关任务，`V3` 默认完成一个任务就停下。只要出现范围变化、验证失败、未确认业务规则、高权限命令、工作区冲突或本机资源异常，就必须停止并给出下一步口令。

每轮完成后，Codex 应输出：

- `下一步建议`：继续实现、回到需求/设计/任务确认、补验证、暂停或等待确认。
- `推荐用户下一句`：用户可以直接复制的下一句。

### Codex 目标追踪怎么配合

Codex 目标适合记录跨轮次最终成功标准，不适合替代公司 workflow 的阶段控制。

建议建立目标的场景：

- L2 标准功能，需要经过需求、设计、任务、实现和验证。
- 任务预计跨会话，或者用户启用了连续执行。
- 有多份文档、多模块、多验证点。

强烈建议建立目标的场景：

- L3 高风险任务。
- 旧项目接入公司 workflow。
- 技能升级、安全审查、专家依赖维护。
- hotfix 先止血，后续还要补测试、补文档、补复盘。

不建议建立目标的场景：

- L0 轻量探讨。
- L1 小文案、小 UI、小配置。
- 单轮能完成的小 bugfix 或一次性查询。

目标存在不等于可以直接写代码。需求没确认、设计没确认、任务没确认、触发范围变化熔断、命中 V3 停止条件或验证失败时，仍然必须停下。

推荐目标描述：

```text
完成 <功能名> 从需求确认、技术设计、任务拆解、实现、验证到文档同步的完整交付。
成功标准：需求/设计/任务已确认；代码实现完成；验证证据完整；文档漂移已处理；完成报告包含下一步建议。
```

### Codex 计划模式怎么配合

计划模式适合放在正式 workflow 前，用来判断路线，而不是替代公司流程。

适合使用：

- 需求还不清楚，不确定先需求、设计、spike 还是 bugfix。
- 较大功能需要先比较 2-3 个方案。
- 旧项目刚接入，需要判断第一步从哪里开始。
- 实现中触发范围变化，需要重新判断回到哪个阶段。
- 连续执行前，需要确认任务顺序、停止条件和风险等级。

不适合使用：

- 小文案、小 UI、小配置。
- 任务清单已经确认且路径清楚。
- hotfix 正在止血，先处理最小恢复路径。

推荐说法：

```text
请先用 Codex 计划模式判断这个任务应该进入哪条公司 workflow；不要改文件，不要写代码。请输出推荐流程、需要确认的问题、风险和下一步口令。
```

计划模式结束后，仍然要回到正式 workflow，例如 `company-feature-requirements`、`company-feature-design`、`company-feature-planning`、`company-implementation-runner`、`company-bugfix-runner` 或 `company-spike-research`。

### Subagents 怎么配合

Subagents 适合在路线和任务确认后使用，不适合拿来替代需求确认或实现授权。Codex 不会因为 workflow 建议就自动启动子代理；需要用户显式要求 `spawn agents`、`delegate in parallel`、`使用 subagents 并行审查` 或等价表达。

适合使用：

- L2 多任务交付，任务边界清楚，且不会编辑同一核心文件。
- 多个测试失败、页面问题或模块问题彼此独立。
- L3 高风险任务需要独立做规格一致性审查、代码质量审查、测试覆盖审查或安全风险审查。
- 连续执行批次较大，需要降低主会话上下文负担。

不适合使用：

- 单文件小改。
- 多个任务都要改同一状态模型、同一数据库迁移、同一 API 契约或同一公共文档段落。
- 需求、设计或任务还没有确认。

用户通常不需要手动判断是否适合 subagents。`company-feature-planning` 会在任务模板中写出 `Subagent 策略`，`company-implementation-runner` 会在完成报告中输出 `Subagents 建议`、`Subagent 能力状态`、`Subagents 实际调用` 和 `子 agent 结果复核`。

Codex App 端没有单独的“子代理按钮”也正常；App 主要展示 subagent 活动。CLI 可以用 `/agent` 管理 agent thread。

如果需要稳定的公司角色，可以先生成项目级 custom agents：

```bash
bash scripts/install.sh install-agents /path/to/project --lang zh
```

生成位置：

```text
.codex/agents/company-explorer.toml
.codex/agents/company-reviewer.toml
.codex/agents/company-security-reviewer.toml
.codex/agents/company-test-reviewer.toml
```

默认不覆盖已有 `.codex/agents/`；需要覆盖时显式加 `--force`。

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

### 确认项目资产边界

项目初始化会自动安装本地校验器，并生成：

```text
.codex-workflow/bin/asset_boundaries.py
.codex-workflow/asset-boundaries.json
```

配置根据 manifest、构建和测试入口识别文档根、工程根、工具目录和原型目录。自动生成状态是 `generated-review-required`：明显违规立即阻断，尚未确认的工程根归属异常只警告。

空项目还没有 manifest 时，`engineeringRoots` 为空并不表示安装失败。不要确认空边界：先完成需求和技术设计，按确认方案创建第一批脚手架后执行 `generate-asset-boundaries --force`，再审阅并确认识别出的工程根。草案期间 `specs/`、`docs/` 下的明显错误落点仍会被阻断。

审阅配置无误后执行：

```bash
bash scripts/install.sh confirm-asset-boundaries /path/to/project --lang zh
```

上面的 `confirm` 只用于首次生成的正式草案。已有配置再次生成时会得到 `.codex-workflow/asset-boundaries.generated.json`；对比无误后使用：

```bash
bash scripts/install.sh accept-asset-boundaries /path/to/project --lang zh
```

该命令先校验候选，备份旧配置为 `asset-boundaries.backup.json`，再原子采纳并确认候选。

日常只检查本次新增和移动文件：

```bash
bash scripts/install.sh check-assets /path/to/project --lang zh
```

旧项目首次治理或用户明确要求全面审计时才运行：

```bash
bash scripts/install.sh audit-assets /path/to/project --lang zh
```

合法机器契约例外应编辑 `exceptions`，至少填写 `path`、`type: machine-contract`、`reason`、`owner` 和 `validation`。该例外只豁免机器契约规则，不会放行同目录的包管理文件、依赖树或可执行测试；不要通过扩大整个文档根权限来绕过单个例外。

当前版本尚未启用 pre-commit/CI 强制检查；团队试点稳定后，两者应复用同一校验器，先 warning、后 blocking。

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

当公司 workflow kit 升级了 `specs/global/assets/` 里的模板，而业务项目已经初始化过时，不建议重新执行 `bootstrap-project --force`，因为那可能影响项目里已有的需求、设计和任务文档。

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

这个命令也会检查项目根目录的专家依赖文件：

```text
BUNDLES.md
EXPERTS.lock.md
.codex-workflow/EXPERT-READINESS.md
```

如果文件不存在，会自动补齐；如果文件已存在，默认生成下面两个文件供对比确认，不直接覆盖：

```text
BUNDLES.generated.md
EXPERTS.lock.generated.md
```

你可以让 Codex 对比：

```text
请对比 specs/global/assets 和 specs/global/assets.generated，说明模板有哪些变化，以及是否建议覆盖。
```

如果专家依赖文件也生成了 `.generated` 版本，可以继续让 Codex 对比：

```text
请对比 BUNDLES.md 和 BUNDLES.generated.md、EXPERTS.lock.md 和 EXPERTS.lock.generated.md，说明专家组合和版本锁有哪些变化。
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
- Document ownership map
- Numbering namespaces

旧项目已有 `INDEX.md` 时，默认不会覆盖。脚本会生成 `specs/global/INDEX.generated.md`，你可以让 Codex 对比两个文件，然后确认是否替换。

如果旧项目里存在 `说明文档.md`、spike 工作日志、生命周期总结或历史日报，先确认文档职责：

- 入口页只写当前状态、最近重要事件和阅读路线。
- Spike 工作日志只写现场流水，使用 `SPKxx-T001` 这类编号。
- 正式 specs 使用 feature、版本或正式任务编号。
- 生命周期文档只写阶段总结。

同一个裸编号出现在不同层级文档时，先让 Codex 修正 `INDEX.md` 的文档职责地图和编号命名空间，再继续推进需求、设计或实现。

多分支并行时，不要让每个业务分支直接改 `说明文档.md` 的“当前状态”。推荐做法：

- 业务分支只更新自己的 `specs/features/...`、`specs/versions/...`、spike 日志或工作日志。
- 如果该分支合并后需要改变公共入口、阅读路线、最近重要事件或文档职责，创建 `docs/public-doc-updates/<branch-or-feature>.md`。
- 集成分支或主线合并阶段，再统一把这些补丁整理进 `说明文档.md` 和 `specs/global/INDEX.md`。

可直接对 Codex 说：

```text
这个分支会影响说明文档，请生成公共文档影响补丁，不要直接改说明文档。
```

## 业务规则与计算口径

当功能包含公式、指标、排序、权重、状态流转、审批/任务流、字段来源、单位、精度、缺失数据、异常值、批量处理、重复提交或并发冲突时，需求阶段应先判断是否需要独立的 `business-rules.md`。

这份文档不是每个需求都要写。它只用于复杂业务规则，避免公式和操作规则散落在聊天记录、技术设计或实现代码里。

推荐说法：

```text
帮我梳理这个功能的业务规则和计算口径：包括操作逻辑、状态流转、公式、字段口径、异常处理和样例用例。
```

后续阶段的处理方式：

- 设计阶段读取 `business-rules.md`，把规则映射到模块、接口、数据结构和测试策略。
- 任务拆解阶段把样例用例转成自动测试或明确手工验证步骤。
- 实现或 bugfix 阶段如果发现规则缺失，不要猜测，回到需求阶段补齐规则文档或变更请求。

## 技术方案对比

技术设计阶段不是所有任务都要做方案对比。公司工作流采用触发式强制：

- L1 小文案、小 UI、小配置、低风险且技术路径唯一的改动，可以跳过方案对比，但需要说明原因。
- L2/L3 大功能、核心模块、核心流程、跨前后端/服务边界、数据模型、权限、安全、性能、缓存、并发、外部 API、业务规则或长期维护取舍场景，必须比较 2-3 个方案。

方案对比应包含：

- 推荐方案。
- 备选方案。
- 每个方案适合什么情况。
- 主要代价、风险和长期影响。
- 需要用户确认的问题。

可直接对 Codex 说：

```text
需求已确认，进入技术设计；如果命中 L2/L3 方案对比条件，请先比较 2-3 个方案，并等我确认推荐方案后再进入任务拆解。
```

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

如果旧项目已经接入过，但仍使用旧规则、模板可能过期，或你不确定插件是否生效，先说：

```text
请检查这个项目的公司工作流健康度
```

Codex 应进入 `company-workflow-health-check`，只读检查 `AGENTS.md`、`BUNDLES.md`、`EXPERTS.lock.md`、`specs/global/INDEX.md`、模板新旧、规则漂移、插件/专家暴露和建议修复命令。健康检查默认不改项目文件。

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

如果需求阶段需要先确认页面或交互，不必进入技术设计：

```text
需求还没冻结，先根据当前内容做一个 HTML 原型验证页面和交互，不进入技术设计。
继续修改需求原型，保持需求阶段，不接真实接口。
```

确认原型后只转为需求基线：

```text
需求和原型均确认，转为需求基线；先不要进入技术设计。
```

Codex 会使用 `company-requirements-prototype` 管理隔离草稿、浏览器证据和需求基线。原型确认不是技术设计授权，也不会生成任务清单。

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

所有任务完成后：

```text
所有任务已完成，开始交付收口并推送业务分支。
```

Codex 会进入 `company-delivery-closeout`：先检查业务分支和任务状态，再逐文件分类代码、测试、文档、配置、资产、临时产物和未知文件；随后规整权威文档、dry-run 清理、审查最终 diff、重新验证，并只精确暂存确认文件。正常通过后创建一次本地 commit，并使用普通 push 推送当前业务分支。

三种模式：

- `开始交付收口` -> `prepare`，不 commit、不 push。
- `收口并提交` -> `commit`，只创建本地 commit。
- `收口并推送业务分支` -> `deliver`，本地 commit 后普通 push。

该流程不会自动 force、rebase、amend、合并、发布或部署。受保护分支、任务未完成、未知文件、验证/审查失败、文档冲突、敏感或异常大文件、staged 清单不一致、远端领先或普通 push 被拒绝时都会停止并给出恢复入口。

### 长对话切换到新对话

当前任务还没结束时，按你需要的连续性选择：

```text
继续原任务。
压缩当前任务后继续。
完整继承历史并创建新任务。
生成标准交接并发送到新任务。
```

只因长度问题优先 compact；全部历史不能丢时使用 fork；希望新任务更干净、减少 token 时使用 handoff。handoff 自动选择 `quick / standard / decision-rich`，以当前主任务为核心，区分已验证事实、历史判断、待确认事项、被否方案和未授权旁支。

只有需要本地续接文件时才说：

```text
生成当前任务交接摘要，并覆盖 .codex/handoff/current.md。
```

新对话中说：

```text
读取 .codex/handoff/current.md，验证当前状态后继续任务。
```

目标对话会先核对路径、分支、工作区、关键文件、未完成任务和实现授权，再复述目标、关键决策、约束、状态、未完成事项和授权。传输状态按“已生成、已发送或待粘贴、已读取、语义校验”反馈。低风险差异说明后继续，中风险差异重新验证，高风险差异停止确认。交接不替代 `INDEX.md`、正式需求/设计/任务文档，也不自动授权编码。

## 7. 完整流程例子

目标：客户列表支持按当前筛选条件导出 CSV。

1. 用户说：

```text
帮我梳理这个功能需求：客户列表支持按当前筛选条件导出 CSV
```

2. Codex 输出目标、范围、验收标准和边界条件。

   如果本功能需要先验证页面、交互或文案，用户可在此插入可选原型循环：

```text
需求还没冻结，先做隔离 HTML 原型验证，不进入技术设计。
```

   原型反馈先回写需求；用户说“需求和原型均确认，转为需求基线”后，Codex 转存基线并停止。非可视化需求可直接跳过这一步。

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

   如果实现涉及非平凡行为，Codex 应在这个阶段使用 Superpowers TDD；写代码前应先通过阶段一致性预检，完成前应给出验证等级、验证证据和文档漂移影响。用户通常不需要手动输入 `/Superpowers /test-driven-development`。

9. 全部任务完成后，用户要求正式收口：

```text
所有任务已完成，开始交付收口并推送业务分支。
```

10. Codex 使用 `company-delivery-closeout` 盘点导出功能的代码、测试、需求/设计/任务文档和临时 CSV；未知文件会阻止删除和提交。

11. Codex 对最终待提交 diff 使用 `superpowers:requesting-code-review`，用 `superpowers:verification-before-completion` 重跑验证，并用 `superpowers:finishing-a-development-branch` 检查分支状态。通过后只暂存确认文件，创建本地 commit 并普通 push 当前业务分支。

12. 最终报告列出验证命令、删除和保留文件、commit SHA、分支、远端、push 结果、剩余风险和下一步建议。

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
