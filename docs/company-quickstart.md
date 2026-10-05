# Company Quickstart

## 正式文档先读这里

初始化项目后，先阅读 `specs/global/assets/document-standard.md`。正式文档先说明结论和影响，再按读者用途组织适用的图表、规格与证据；标题和章节顺序可调整。

图表按文种和实际用途判定：技术设计保留架构图和时序图，操作指南与管理汇报按对应规则选择步骤、表格或图。已确认必需图和用户明确要求的图仍须用户明确豁免。已有 marker 的项目执行 `update-templates`；无 marker 的早期公司规则执行 `migrate-project`。两者都保留已确认索引和业务文档，候选模板写入 `.generated` 位置。

这份文档面向公司项目用户，也是内部培训的主入口。用户不需要记住所有 skill 名称，只需要知道在什么场景说什么。

如果你是第一次使用，建议先看：

- [Codex 使用完整说明](codex-usage-guide.md)
- [公司试点手册](pilot-playbook.md)
- [技能树清单](skill-tree.md)
- [技能升级 dry-run 工作流](skill-upgrade-dry-run.md)

## 第一次放进项目

安装后先确认 `specs/global/INDEX.md` 的 `目标使用终端基线`：产品支持 PC Web、移动 Web、App、桌面客户端还是大屏，是否共用页面/代码/API，以及最小视口、浏览器和输入方式。未确认的终端默认不支持；PC-only 项目不会自动产生移动端适配工作。

Workflow 回复保留一句话结论和下一步建议，用普通语言解释依据、影响、责任方和前置条件。人类文档独立可读；能力调用、执行策略和详细指纹进入已有内部记录，不默认附审计清单。中文回复使用中文标题和状态，必要的代码、路径及错误原文保持准确。

阶段收尾最后单独写 **下一步：**，明确由谁做什么、必要前提或“本任务已完成，你现在无需操作”。已有授权内继续执行；只请求确实缺少的信息或决定。普通问答和工作中更新不强制套用。

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

强依赖专家 skills 也随公司插件一起安装，例如 `frontend-developer`、`typescript-expert`、`frontend-design`、`testing-qa`。安装器会自动刷新 Codex 插件缓存，并输出实际激活版本；已打开的旧会话不会动态重载 skill 列表，所以安装或更新后仍需新开 Codex 线程。

公司 workflow 自动选择内部记录详略，保存真实调用、验证证据、未验证项和风险。试点时检查内部记录是否可追溯，同时单独检查用户回复是否清楚说明结论、依据、影响和下一步；不以审计字段出现在回复中作为通过标准。

从 `0.2.22` 起，入口和执行报告还会像反馈 Superpowers 一样反馈 Codex 计划模式和 subagents：

- `Codex 计划模式建议`：说明不需要、建议使用或强烈建议使用，以及原因和可复制提示词。计划模式只用于路线判断，不改文件、不编码。
- `Subagents 建议`：说明是否值得使用子 agent。小任务通常不需要；多任务、独立失败域或高风险审查才建议使用。
- `Subagent 能力状态`：说明当前是未检查、需要用户显式请求、需要本地 custom agents 配置，还是当前 App 主要展示活动。
- `Subagents 实际调用`：说明本轮是未调用、已调用，还是仅采用拆分视角。即使子 agent 返回完成，主 agent 仍要复核 diff、验证证据和剩余风险。

复杂需求、技术设计、修复、实验、实现完成和技能升级场景，还应在内部记录检查核心假设及相关异常、边界风险；面向用户说明会影响其决定的发现。

实现、bugfix 和 hotfix 完成时，还要检查是否包含 `验证等级`、`独立质量验收判定` 和 `文档漂移影响`。验证等级由 workflow 自动判定：`V0` 纯文档、`V1` 小改动、`V2` 标准功能或普通 bugfix、`V3` 生产/权限/安全/数据/性能/公式/hotfix。文档漂移用于判断是否需要同步需求、业务规则、设计、任务、`说明文档.md`、`INDEX.md` 或公共文档影响补丁。

如果本次涉及 Java、前端 TypeScript/Vue/React、Python、SQL 或脚本里的非显然业务逻辑，还要检查是否包含 `代码备注检查` 和 `备注覆盖点`。AI 应补充中文逻辑备注，解释业务规则、计算口径、数据映射、异常分支、fallback/降级、兼容策略或性能/并发/缓存处理；不要写逐行翻译语法的废话备注。

启动实现、bugfix 或 hotfix 前，workflow 还会做阶段一致性预检。它会轻量读取入口页、`INDEX.md`、当前 feature/version README、任务文档和相关 public-doc patch，判断“当前到底处于哪个阶段”。如果发现入口页还写 spike/待办，而任务文档已经进入正式开发，Codex 应先暂停并给出冲突和修复建议，不应直接开始写代码。

如果在实现中发现“原任务漏了一个关键层”，例如新增 data-preparation、目标表、接口边界、字段映射或业务口径，旧的实现授权会失效。Codex 应先补文档并输出 `实现授权状态`，等你确认新范围后再继续编码。

## 需求阶段先做 HTML 原型

当需求还在梳理，但需要先看页面、交互、文案或模拟业务状态时，可以直接说：

```text
需求还没冻结，先根据当前内容做一个 HTML 原型验证页面和交互，不进入技术设计。
```

Codex 会进入 `company-requirements-prototype`。草稿与生产源码隔离，只使用模拟数据，并通过浏览器验证关键视口、交互和状态。继续修改时说：

```text
继续修改需求原型，保持需求阶段，不接真实接口。
```

确认后说：

```text
需求和原型均确认，转为需求基线；先不要进入技术设计。
```

此时只会把原型转存到需求文档同级 `prototype/` 并更新需求记录，不会自动生成技术方案或任务。需要进入技术设计时，再单独明确说“进入技术设计”。真实 API、数据库、认证、生产组件、后端或性能验证不属于需求原型，会自动停止并重新判断 Spike 或技术设计入口。

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

多分支并行时，业务分支默认不要直接改 `说明文档.md` 或 `specs/global/INDEX.md` 的主线当前状态。分支如果影响公共入口或阅读路线，先写 `docs/public-doc-updates/<branch-or-feature>.md`，等合并到集成分支时再统一更新公共文档。

涉及操作逻辑、指标公式、计算口径、状态流转、字段精度、异常数据或角色差异时，让 Codex 先判断是否需要 `business-rules.md`。小文案、小 UI、小配置等低风险改动不需要额外增加这份文档。

推荐说法：

```text
帮我梳理这个功能的业务规则和计算口径；如果只是小需求，不要强制创建 business-rules.md。
```

较大功能模块进入技术设计时，Codex 会自动判断是否需要方案对比。小改动不会强制对比；大功能、核心流程、跨边界、数据模型、权限、安全、性能或业务规则相关设计，会要求 2-3 个方案并让你确认推荐方案。

推荐说法：

```text
需求已确认，进入技术设计；如果这是 L2/L3 功能，请先做方案对比并给出推荐方案，等我确认后再拆任务。
```

如果项目运行工作流时提示找不到 `BUNDLES.md`、`EXPERTS.lock.md` 或 `specs/global/assets/` 模板，执行下面命令补齐：

```bash
bash scripts/install.sh update-templates /path/to/project --lang zh
```

已有文件默认不会被覆盖；脚本会生成 `.generated` 文件供对比确认。确认后使用 `--force` 覆盖时，旧模板会先备份到 `.codex-workflow/backups/assets.<timestamp>/`，同名受管模板会更新，项目独有文件保持不变。

如果 `AGENTS.md` 还是没有 `codex-workflow-kit:company` marker 的早期公司版本，改用：

```bash
bash scripts/install.sh migrate-project /path/to/project --lang zh
```

原 `AGENTS.md` 会保存到 `.codex-workflow/backups/`。当前规则写入受管 marker；`INDEX.md`、业务文档和源码保持原状。

如果安装器发现旧规则中还有项目本地附加内容，会保留原文件、生成 `AGENTS.generated.md` 并停止自动迁移。此时先让 Codex 对比并人工合并，不要使用 `--force`。

## 空项目或需求雏形

如果项目还是空目录，或者还在需求梳理阶段，`bootstrap-project` 仍然适合先执行。它会先放入 `AGENTS.md` 和 `specs/`，让 Codex 有统一的需求沉淀位置。

初始化还会生成 `.codex-workflow/asset-boundaries.json`。它用于区分文档目录和真实工程目录，避免把包、测试、Fixture、Schema 或脚本写进 `specs/`。先让 Codex解释自动识别结果，确认无误后执行：

```bash
bash scripts/install.sh confirm-asset-boundaries /path/to/project --lang zh
```

空项目尚未确定技术栈且没有 manifest 时，`engineeringRoots` 为空是正常现象。此时保留 `generated-review-required`，先完成需求和技术设计；首次脚手架按已确认设计落地后，运行 `generate-asset-boundaries --force` 重新识别工程根，再审阅并确认。草案期间仍会阻断工程资产误入 `specs/` 或 `docs/`。

已有正式配置时，不使用 `confirm` 处理刷新结果。安装器会保留正式配置并生成 `asset-boundaries.generated.json`；审阅候选后执行：

```bash
bash scripts/install.sh accept-asset-boundaries /path/to/project --lang zh
```

该命令会备份旧配置、原子替换正式配置并标记为已确认。

日常无需全仓扫描；设计和实现会检查计划路径，交付前使用 `check-assets` 只检查本次新增和移动文件。

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
<已确认归属目录>/requirements.md
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

Codex 应先检查已有 `AGENTS.md`、README、manifest、docs、测试目录和启动命令，再生成或审查 `INDEX.md` 草稿。普通项目自定义规则保留并追加受管段落；早期无 marker 的整份公司规则先备份，再由 `migrate-project` 整体替换，避免新旧规则并存。

如果旧项目已经接入过，但你不确定当前是否健康，先说：

```text
请检查这个项目的公司工作流健康度
```

Codex 应进入 `company-workflow-health-check`，只读诊断根目录文件、模板、`INDEX.md`、旧规则残留、插件/专家暴露和建议修复命令。健康检查默认不改项目文件。

如果你是在任务开发前主动确认阶段状态，可以说：

```text
任务已确认，开始实现。但在写代码前，请先做阶段一致性预检。
```

新版 workflow 会自动做这件事；这句话只是显式提醒。

如果任务文档已经确认，并且你希望 Codex 一次推进多个可执行任务，可以说：

```text
任务已确认，连续完成后续所有可执行任务；遇到范围变化、V3 风险、验证失败或需要我确认时再停。
```

连续执行不是无条件自动驾驶。Codex 会按任务验证等级控制批量大小：`V0/V1` 可连续，`V2` 小批量，`V3` 单任务后停下确认。每轮完成后说明下一步建议和责任方；仅在确需用户补充信息、决定或授权时才交给用户处理。

如果这是跨阶段、跨会话或连续执行任务，Codex 还会给出 `目标追踪建议`：

- `不需要`：小任务、单轮任务、一次性查询。
- `建议建立`：标准功能、多文档、多验证点、需要跨会话继续。
- `强烈建议建立`：高风险任务、旧项目接入、技能升级、安全审查、hotfix 补偿链路。

目标只负责记录最终成功标准，不会跳过需求、设计、任务确认或范围变化熔断。

如果需求还不清楚、旧项目边界复杂、需要先比较方案或准备连续执行，可以先让 Codex 使用计划模式判断路线：

```text
请先用 Codex 计划模式判断这个任务应该进入哪条公司 workflow；不要改文件，不要写代码。请输出推荐流程、需要确认的问题、风险和下一步口令。
```

如果任务已经拆解完，Codex 会自动判断是否建议 subagents。但 Codex 只会在你显式要求时启动子代理；App 端没有独立子代理按钮也正常，CLI 才有 `/agent` 管理入口。

如果只是想让 Codex 判断，可以说：

```text
任务已确认，开始实现。请按公司 workflow 判断是否需要 subagents；如果不需要，请说明原因。
```

如果你确认要启用并行审查，可以说：

```text
请使用 subagents 并行审查：一个检查测试缺口，一个检查代码质量，一个检查安全风险。等待全部完成后汇总。
```

如果需要稳定公司角色，先在项目里执行：

```bash
bash scripts/install.sh install-agents /path/to/project --lang zh
```

这会生成项目级 `.codex/agents/company-*.toml`。默认不覆盖已有 agents；确认后可加 `--force`。

## 长对话续接

先按实际需求选择一句：

```text
继续原任务。
压缩当前任务后继续。
完整继承历史并创建新任务。
生成标准交接并发送到新任务。
```

目标不变只担心长度时用 compact；完整历史都重要时用 fork；需要干净上下文和较低 token 时用 handoff。交接分为 `quick / standard / decision-rich`，用户不需要手动判级。

默认不新增项目文档。确实需要文件时，明确要求覆盖 `.codex/handoff/current.md`。目标对话会核对项目事实并复述目标、决策、约束、状态、未完成事项和授权；语义校验通过后才继续高风险动作。`company-thread-handoff` 管临时任务状态，`company-context-index` 管项目长期上下文。

## 里程碑交付收口

实现 workflow 负责逐任务编码和验证；所有任务做完后先自动判定是否进入 `company-quality-validation`。`V0/V1` 和低风险单任务 `V2` 默认不增加节点；多任务/跨模块/前后端/API/数据库 `V2`、里程碑、发布候选、`V3` 和 hotfix 补偿进入独立验收。

命中时可直接说：

```text
实现已完成，请判断并执行独立质量验收。
```

验收只输出 `pass / conditional-pass / blocked`，不修改生产代码。`blocked` 转 bugfix 并按原范围复验；通过或用户明确接受允许的条件通过后，再使用 `company-delivery-closeout` 规整本次成果。

判定为 `需要/强制` 时，Codex 会把 `quality-validation-report.md` 放在权威任务文档同级，并记录当前分支、HEAD、被验收路径、diff SHA-256 与未跟踪文件哈希。判定为不需要时不新增报告。交付收口核对候选指纹，未漂移则复用证据；行为相关路径变化才重新验收。

默认的一次性交付口令：

```text
所有任务已完成，开始交付收口并推送业务分支。
```

该口令授权盘点代码、测试、文档、配置和资产，按来源清理临时文件，复验最终候选，创建一次本地 commit，并普通 push 当前业务分支。它不授权强制推送、rebase、amend、合并、发布、部署或删除未知文件。

只想先检查、不提交时说 `开始交付收口`；只需本地提交时说 `收口并提交`。受保护分支、未知文件、未完成任务、验证失败、文档冲突或 staged 清单不一致会自动停止。

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

```text
所有任务已完成，开始交付收口并推送业务分支。
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

## 连接 Codex 计划模式和 Subagents

计划模式、subagents、Superpowers 和公司 workflow 的分工不同：

```text
Codex 计划模式 -> 正式 workflow 前判断路线，不改文件
company-workflow-help -> 判断进入哪条公司流程
company-feature-planning -> 拆任务，并标注连续执行和 subagent 策略
company-implementation-runner -> 执行、验证、反馈 subagent 能力状态和是否真实调用
Superpowers -> 提供 brainstorming、TDD、debugging、verification 等工程纪律
```

正常使用时，你不需要记这些内部机制。看输出里有没有 `Codex 计划模式建议`、`Subagents 建议`、`Subagent 能力状态`、`Subagents 实际调用`、`Superpowers 叠加` 和 `实际调用`，就能判断 workflow 是否把链路打通。

## 更新、停用和卸载

更新已初始化项目里的模板：

```bash
bash scripts/install.sh update-templates /path/to/project --lang zh
```

默认只生成 `specs/global/assets.generated/` 供对比。确认后再覆盖：

同时会刷新 `AGENTS.md` 中带 marker 的公司规则，并生成 `specs/global/INDEX.generated.md` 供确认；项目自己的规则、已确认索引和业务文档不会被覆盖。

早期无 marker 的公司规则不要用 `--force` 硬覆盖，使用：

```bash
bash scripts/install.sh migrate-project /path/to/project --lang zh
```

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
