# Codex Company Workflow Kit

公司项目使用的 Codex 工作流 starter kit，目标是让团队在 Codex 里稳定完成需求澄清、技术设计、任务拆解、实现验证、触发式独立质量验收、里程碑交付收口、bugfix、hotfix、spike 和专家技能治理。

这不是为了把流程做重，而是为公司项目提供轻量护栏：

- 需求、设计、实现、验证可追溯。
- 旧项目能平滑接入，不覆盖已有规范。
- 强依赖专家 skills 随公司插件内置安装，用户不需要逐个对话安装。
- 专家 skills 通过 bundle 自动路由；安装和项目初始化会自动生成专家就绪和安全审查报告。
- 外部专家技能后续更新走 dry-run、diff、安全审查、用户确认和回滚记录。
- 项目上下文索引 `INDEX.md` 可以自动生成草稿，再由用户确认。
- 正式文档先说明结论与影响，标题和顺序按读者用途调整；图表按文种及实际内容选择，使用 Mermaid 表达适用的工程图。
- 项目和功能都明确目标使用终端；未确认移动端时，不会自行增加响应式布局、触摸交互、移动端截图或移动 E2E。
- Workflow 回复保留一句话结论和下一步，解释依据及影响；内部审计另存，人类文档按读者用途编写。

阶段收尾最后单独写 **下一步：**，明确由谁做什么、必要前提或“本任务已完成，你现在无需操作”。已有授权内继续执行；只请求确实缺少的信息或决定。普通问答和工作中更新不强制套用。
- 需求阶段可用 `company-requirements-prototype` 创建隔离 HTML/页面/交互原型，确认后转为需求基线，不会自动进入技术设计或任务拆分。
- 长对话由 `company-thread-handoff` 自动建议继续、压缩、完整 fork 或分级交接；目标对话必须完成接收校验，不盲目继承旧状态或实现授权。
- 实现后由 workflow 自动判断是否进入 `company-quality-validation`；小改动不加流程，多任务/跨模块 V2、里程碑、V3 和 hotfix 补偿按风险进入独立验收。
- 所有任务完成后可用 `company-delivery-closeout` 规整代码、文档和临时产物，重新验证最终候选，并按授权本地提交或普通推送当前业务分支。
- 每轮执行在内部记录中区分实际调用的 Superpowers/专家/插件/subagents 能力，以及未调用但采用的专家或拆分视角；subagents 会额外说明能力状态和是否需要用户显式请求。

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
- `specs/global/assets/`：需求、业务规则、设计、任务、hotfix、spike、技能升级和工作流健康检查模板。

## 人类可读文档规范

- 入口：`specs/global/assets/document-standard.md`，定义 `DOC-G01` 到 `DOC-G12` 质量门禁。
- 按文种和实际用途判定图表要求；技术设计保留架构图和时序图，操作指南与管理汇报按对应规则选用步骤、表格或图。已确认必需图及用户明确要求的图，仍须用户明确豁免。
- 工程规格使用稳定的 `work-item-id`；验收报告关联任务和候选，操作指南与管理汇报按需引用已有任务、版本或来源。文档开头说明结论与影响，保留必要细节和证据；能力审计另存。
- 新文档完整执行规范；旧文档只在本次修改范围内渐进修复，不强制一次性重写历史资料。
- 已有 marker 的项目升级时运行 `update-templates`，它会刷新受管规则并生成索引、模板候选，不覆盖已确认的项目索引或业务文档。
- 没有 marker、仍使用旧版公司规则的项目运行 `migrate-project`。安装器会先备份 `AGENTS.md`，再切换为当前受管规则；直接运行 `update-templates` 只会生成 `AGENTS.generated.md`，不会把新旧规则叠加。

## 能力调用透明度

公司 workflow 默认自动判定透明度级别，用户不需要自己选择：

- `light`：普通阶段内推进、小改动、低风险文档更新、简单入口推荐。
- `full-audit`：阶段交接、实现完成、bugfix 完成、hotfix、spike 结论、技能升级、安全审查、专家能力未真实调用、验证缺失，或涉及生产、数据、权限、架构、性能、安全风险。

## 第一性原理和对抗式审查

公司 workflow 内置两个质量检查，不需要用户每次手动补 prompt：

- `第一性原理检查`：复杂需求、技术设计、bugfix 根因、spike 结论前，回到底层事实、约束和最小成立条件，避免只修表层症状。
- `对抗式审查`：实现完成、bugfix 完成、hotfix、spike 结论、技能升级和安全审查前，从极端输入、异常状态、权限绕过、并发重试、未来时间、缓存假阳性和 UI 渲染压力等反例检查稳健性。

这些检查已经写入 `AGENTS.md`、核心 workflow skills 和项目模板。普通小改动可以跳过，但必须说明原因。

## 三层质量体系

- 技术设计定义测试策略和可验证接口。
- `company-implementation-runner` 叠加 `superpowers:test-driven-development`，在编码过程中用最小失败案例提供快速反馈。
- 实现完成后自动判定是否进入 `company-quality-validation`，从 AC、关键旅程、集成、回归和交付风险角度做独立验收；该节点不修改生产代码。

`V0/V1` 默认跳过独立验收；单任务低风险 `V2` 默认跳过。多任务/跨模块/前后端或 API/数据库集成的 `V2` 需要验收；里程碑、发布候选、`V3` 和 hotfix 补偿强制验收。结果只有 `pass / conditional-pass / blocked`：阻断项进入 bugfix 后复验，通过后才进入交付收口。

需要或强制验收时，报告写在权威任务文档同级的 `quality-validation-report.md`，并记录当前分支、HEAD、被验收路径、diff SHA-256 和未跟踪文件哈希。交付收口会重新核对触发条件和候选指纹：指纹一致时复用验收证据，只补收口增量检查；被验收路径变化时回到质量验收。判定为不需要时不会额外创建报告。

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

业务规则与计算口径按需独立成文：

- 仅当功能涉及操作逻辑、状态流转、指标公式、字段口径、异常数据、角色差异、权限、批量行为、重复提交或冲突处理时，创建 `business-rules.md`。
- 小文案、小 UI、小配置等低风险改动不需要这份文档。
- 需求阶段负责判定是否需要；设计阶段只映射规则，不重新发明公式；任务拆解阶段把规则样例转成测试或手工验证。
- 实现或 bugfix 阶段发现规则缺失时，停止猜测，回到需求阶段补齐规则文档或变更请求。

需求原型也是按需分支：

- 需要先确认页面、交互、文案或模拟业务状态时，进入 `company-requirements-prototype`，仍保持需求阶段。
- 草稿位于 `.codex-workflow/prototypes/<feature>/draft/`，并由 `prototype.json` 记录归属和验证证据。
- 用户明确确认后，原型转存到权威需求同级 `prototype/`，并记录版本、验证范围和 SHA-256。
- 原型确认不会自动进入技术设计或任务拆分；真实 API、数据库、认证、生产组件或性能验证会停止原型并重新路由。

技术方案对比按复杂度触发：

- L1 小文案、小 UI、小配置或技术路径唯一的低风险改动，可以跳过方案对比，但必须说明原因。
- L2/L3 大功能、核心模块、跨边界、数据模型、权限、安全、性能、业务规则或长期维护取舍场景，必须比较 2-3 个方案。
- 方案对比必须给出推荐方案、备选方案、主要取舍、风险和用户确认点。
- 命中 L2/L3 方案对比后，用户未确认推荐方案前，不进入任务拆解。

验证等级和文档漂移按执行风险自动判定：

- `V0`：纯文档、注释、格式或无行为变更，只需要 diff 或目标文件复核。
- `V1`：低风险小改动，使用聚焦命令、局部测试或最小手工路径。
- `V2`：标准功能或普通 bugfix，使用相关测试、类型/构建检查和必要浏览器/手工验证。
- `V3`：生产、权限、安全、数据、性能、金额/指标公式、跨系统或 hotfix，需要回归、对抗场景和回滚/恢复说明。
- 实现、bugfix 和 hotfix 完成前会输出 `验证等级` 和 `文档漂移影响`；如果代码改变了需求承诺、业务规则、API 契约、设计或公共入口，必须补文档或标记待确认漂移。

中文代码逻辑备注按需强制：

- 适用于 Java、前端 TypeScript/Vue/React、Python、SQL、脚本和配置生成逻辑。
- 业务规则、状态分支、公式阈值、精度、数据映射、fallback/隐藏/降级、异常处理、兼容策略、性能/并发/缓存等非显然逻辑，必须补中文备注。
- 禁止写语法翻译式废话备注；阈值或公式来源不清时，回到需求或 `business-rules.md` 补齐。
- 实现、bugfix 和 hotfix 完成报告会输出 `代码备注检查` 和 `备注覆盖点`。

实现前阶段一致性预检用于避免旧项目入口和真实任务状态不一致：

- 在 `任务已确认，开始实现`、bugfix 或 hotfix 前，workflow 会轻量检查 `说明文档.md`、`specs/global/INDEX.md`、当前 feature/version README、任务文档和相关 `docs/public-doc-updates/`。
- 如果入口页仍停在 spike/待办，但当前任务文档已进入正式开发，workflow 会先暂停并说明冲突、本轮权威文档和修复建议。
- 非集成分支默认不直接改公共入口；优先写 public-doc update patch，等合并阶段再升格到 `说明文档.md` 和 `INDEX.md`。

范围变化熔断用于避免长会话里复用旧的实现授权：

- 如果实现中发现遗漏架构层、数据加工层、表、接口边界、业务口径、字段映射或文档需要同步更新，旧的 `任务已确认，开始实现` 授权立即失效。
- workflow 会先输出 `阶段许可` 和 `实现授权状态`；非 `允许实现` 时，只能补需求、设计、任务、字段映射或 public-doc patch。
- 补完文档后必须等用户确认新范围，再重新进入实现；专家路由只能辅助判断，不能替代用户确认。

受控连续执行用于减少重复确认，但只在已确认任务清单内生效：

- 用户明确说“连续完成后续所有任务”“批量推进”或等价表达时，`company-implementation-runner` 才会启用。
- `V0/V1` 可连续处理相关任务；`V2` 每批只处理 1-3 个强相关任务；`V3` 默认单任务后停下确认。
- 每个任务完成后都会重新检查范围变化、验证失败、V3 风险、用户确认点、工作区冲突、高权限命令和本机资源异常。
- 推荐口令：`任务已确认，连续完成后续所有可执行任务；遇到范围变化、V3 风险、验证失败或需要我确认时再停。`

Codex 目标追踪用于跨轮次任务，不替代公司 workflow：

- L0/L1 小任务默认不建议建立目标。
- L2 标准功能、跨阶段、跨会话、多文档、多验证点或连续执行任务，workflow 会建议建立目标。
- L3 高风险任务、旧项目接入、技能升级/安全审查、专家依赖维护、hotfix 后补偿链路，workflow 会强烈建议建立目标。
- 目标描述只写最终成功标准；目标存在不代表实现授权有效，阶段预检、范围熔断、V3 停止条件和用户确认仍然优先。

Codex 计划模式用于正式 workflow 前的路线判断，不替代公司 workflow：

- L0/L1 小任务、路径清楚的单点实现或单点 bugfix 默认不建议使用计划模式。
- L2 需求有歧义、需要方案对比、旧项目接入、范围变化后重新判断路线、连续执行前确认任务顺序时，workflow 会建议使用计划模式。
- L3 高风险、跨系统、数据、权限、安全、性能、金额/指标公式、大迁移或多人协作交付时，workflow 会强烈建议使用计划模式。
- 计划模式只做路线、风险、待确认问题和下一步口令判断；不能改文件、不能编码、不能替代用户确认。

Subagents 用于独立任务、独立排查和独立审查，不是默认执行方式，也不是 App 端的独立按钮入口：

- L0/L1 小任务默认不用，避免增加 token 和协调成本。
- L2 多任务且边界清楚，或多个独立失败域，workflow 会建议使用 subagents。
- L3 高风险、跨模块/跨系统、数据/权限/安全/性能或较大连续执行批次，workflow 会强烈建议至少使用独立审查子 agent。
- Codex 只在用户显式要求 `spawn agents`、`delegate in parallel`、`使用 subagents 并行审查` 或等价表达时启动子代理；workflow 建议本身不等于真实调用。
- Codex CLI 可用 `/agent` 管理 agent thread；Codex App 侧主要展示 subagent 活动，不要求用户寻找单独的子代理按钮。
- 如需稳定公司角色，可以在项目中执行 `bash scripts/install.sh install-agents /path/to/company-project --lang zh` 生成 `.codex/agents/`。
- 主 agent 始终负责阶段许可、实现授权、任务分派、diff 复核、验证证据和最终结论；子 agent 输出不能直接等于完成。

每次完成报告都必须给出下一步引导：

- **下一步：** 作为最后一个独立段落，给出一个主要动作、责任方和前提；约定范围完成则明确无需操作。
- 需要用户处理时写明具体缺失信息、决定或权限；已有授权范围内继续执行。

内部执行记录会明确区分：

- `透明度模式`：本轮自动选择的 `light` 或 `full-audit`。
- `实际调用`：本轮真实触发或读取的 workflow、Superpowers、专家 skill、MCP、浏览器或 Codex 插件能力。
- `专家/插件能力`：本轮选择或依赖的专家、Superpowers、Codex 插件能力。
- `未调用但采用视角`：当前会话不可见、阶段不适合或风险不值得真实调用的能力。
- `Codex 计划模式建议`：是否建议使用计划模式、原因、提示词和计划完成后的正式 workflow。
- `Subagents 建议`、`Subagent 能力状态` 和 `Subagents 实际调用`：是否建议使用子 agent，当前是否需要显式请求或 custom agents，是否真实调用，还是仅采用拆分视角。
- `第一性原理检查` 和 `对抗式审查`：本轮执行的底层事实检查、反例场景或跳过原因。
- `验证证据`：命令、检查结果、文件变更、截图、日志或人工检查证据。
- `未验证项` 和 `剩余风险`。

`full-audit` 会在内部记录额外保存 `Workflow Audit`，说明阶段边界、Superpowers 声明、专家/插件真实调用、仅采用视角、验证证据和未验证项。这条规则已经写入插件 `AGENTS.md` 和所有 `company-*` workflow skill，不需要用户每次在对话里重复提醒。

## 安装

全局安装中文公司版插件：

```bash
bash scripts/install.sh install-plugin --lang zh
```

全局安装会把插件源码复制到 `~/plugins/<plugin-name>`，把索引写入 `~/.agents/plugins/marketplace.json`，并自动执行 `codex plugin add <plugin-name>@personal` 刷新 Codex 安装缓存。安装器会依次查找 `CODEX_CLI`、PATH、`~/.local/bin/codex` 和 macOS 的 ChatGPT/Codex App 内置 CLI；找不到时会明确给出手工刷新命令。这是 Codex personal marketplace 的路径约定；不要手工改成 `~/.agents/plugins/plugins/<plugin-name>`。

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
- 安装 `.codex-workflow/bin/asset_boundaries.py`，并生成 `.codex-workflow/asset-boundaries.json` 资产边界草案。
- 自动扫描 README、manifest、测试目录、启动/构建/测试命令和常见源码入口。
- 生成 `specs/global/INDEX.md` 草稿，包含文档职责地图和编号命名空间。

如果旧项目已有 `INDEX.md`，默认保留原文件，并生成 `specs/global/INDEX.generated.md` 供确认。

如果项目中已有 `BUNDLES.md` 或 `EXPERTS.lock.md`，默认不会覆盖，而是生成 `BUNDLES.generated.md` 或 `EXPERTS.lock.generated.md` 供对比。确认后再使用 `--force` 覆盖。

### 资产落点门禁

安装器会根据项目 manifest、构建和测试入口推断文档根、工程根、工具目录和原型目录。新项目直接生成草案；旧项目已有配置时保留原文件，并生成 `.codex-workflow/asset-boundaries.generated.json` 供比较。

空项目尚无 manifest 时，工程根为空是正常草案状态：先完成需求和技术设计，首次脚手架落地后再用 `generate-asset-boundaries --force` 刷新、审阅并确认。草案期间明显误入 `specs/` 或 `docs/` 的工程资产仍会被阻断。

```bash
# 重新生成边界草案
bash scripts/install.sh generate-asset-boundaries /path/to/company-project --lang zh

# 首次生成的正式草案，用户审阅无误后确认
bash scripts/install.sh confirm-asset-boundaries /path/to/company-project --lang zh

# 已有配置刷新后，审阅 generated 候选并安全采纳
bash scripts/install.sh accept-asset-boundaries /path/to/company-project --lang zh

# 只检查本次新增和移动文件
bash scripts/install.sh check-assets /path/to/company-project --lang zh

# 旧项目全量审计，按需运行
bash scripts/install.sh audit-assets /path/to/company-project --lang zh
```

设计、任务规划、实现、bugfix、健康检查和交付收口会自动读取同一配置。`specs/` 和 `docs/` 默认只承载文档；包管理文件、依赖树、可执行测试和机器契约不得借“可执行规格”名义落入文档目录。合法 OpenAPI/Schema 例外必须使用 `type: machine-contract`，并声明路径、所有者、原因和验证方式；它只豁免机器契约规则，不能放行包、依赖或可执行测试。

本版本不自动安装 Git hook，也不启用 CI 阻断。后续团队推广时，pre-commit 和 CI 直接复用 `asset_boundaries.py check --changed`，先 warning、后 blocking，并对存量问题建立基线。

只刷新项目上下文索引：

```bash
bash scripts/install.sh generate-index /path/to/company-project --lang zh
```

只检查专家依赖是否开箱可用：

```bash
bash scripts/install.sh expert-preflight /path/to/company-project --lang zh
```

可选安装项目级 custom agents：

```bash
bash scripts/install.sh install-agents /path/to/company-project --lang zh
```

这会生成：

```text
.codex/agents/company-explorer.toml
.codex/agents/company-reviewer.toml
.codex/agents/company-security-reviewer.toml
.codex/agents/company-test-reviewer.toml
```

默认不覆盖已有 `.codex/agents/`；需要覆盖时加 `--force`。

在旧项目或试点项目中检查工作流接入健康度，可以在 Codex 里说：

```text
请检查这个项目的公司工作流健康度
```

Codex 会进入 `company-workflow-health-check`，只读检查 `AGENTS.md`、`BUNDLES.md`、`EXPERTS.lock.md`、`specs/global/INDEX.md`、模板新旧、规则漂移、插件/专家暴露和建议修复命令。

只更新已初始化项目里的工作流模板：

```bash
bash scripts/install.sh update-templates /path/to/company-project --lang zh
```

这个命令也会检查并补齐 `BUNDLES.md` 和 `EXPERTS.lock.md`。默认不覆盖现有模板和专家依赖文件，而是生成：

```text
specs/global/INDEX.generated.md
specs/global/assets.generated/
BUNDLES.generated.md
EXPERTS.lock.generated.md
```

`AGENTS.md` 中带 `codex-workflow-kit:company` marker 的受管段落会直接更新，marker 外的项目规则保持不变；已确认的 `specs/global/INDEX.md` 始终保留，新增字段只写入 `INDEX.generated.md` 等待用户确认。

如果项目的 `AGENTS.md` 是早期版本且没有 marker，使用安全迁移命令：

```bash
bash scripts/install.sh migrate-project /path/to/company-project --lang zh
```

该命令先把原文件保存到 `.codex-workflow/backups/`，再写入当前受管规则。现有 `INDEX.md`、业务文档、源码和模板目录都不会直接覆盖；新版本分别写入 `.generated` 文件或目录供确认。

如果旧 `AGENTS.md` 含有无法确认来源的本地附加规则，迁移会在备份和生成 `AGENTS.generated.md` 后停止，不会删除这些规则。`migrate-project` 不接受 `--force`。

npm 全局安装或 `npx` 用户也可执行：

```bash
npx codex-company-workflow migrate-project /path/to/company-project --lang zh
```

确认新旧模板差异后，再显式覆盖。覆盖前会把现有模板完整备份到 `.codex-workflow/backups/assets.<timestamp>/`；只覆盖同名受管模板，项目独有文件保持不变：

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

长对话切换先按实际需要选择：

```text
继续原任务。
压缩当前任务后继续。
完整继承历史并创建新任务。
生成标准交接并发送到新任务。
```

只担心上下文太长时优先压缩；全部历史不能丢时使用 fork；进入新里程碑或希望降低 token 时使用标准交接。涉及产品边界、架构、业务规则、计算、数据、安全或多个被否方案时，自动升级为 `decision-rich`。

交接默认只在回复中输出。需要本地文件时明确说“并覆盖 `.codex/handoff/current.md`”。新对话可说：

```text
读取 .codex/handoff/current.md，验证当前状态后继续任务。
```

`company-thread-handoff` 只传递当前主任务的临时状态；`company-context-index` 仍负责项目长期导航。目标对话会复述目标、关键决策、约束、状态、未完成事项和授权，确认语义一致后再继续。

```text
我现在该走哪个流程？背景是：<当前情况>
帮我梳理这个功能需求：<功能描述>
需求已确认，进入技术设计
方案已确认，进入任务拆解
任务已确认，开始实现
实现已完成，请判断并执行独立质量验收。
所有任务已完成，开始交付收口并推送业务分支。
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
