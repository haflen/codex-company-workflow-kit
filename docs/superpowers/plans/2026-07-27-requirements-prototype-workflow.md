# 需求阶段原型工作流实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 新增中英文 `company-requirements-prototype` skill，让公司用户在需求阶段创建和迭代隔离的 HTML 原型，并在明确确认后转为需求基线，而不会自动进入技术设计或任务拆分。

**Architecture:** 新 skill 只负责需求可视化验证和原型产物生命周期；`company-workflow-help` 负责入口判断，`company-feature-requirements` 负责吸收原型反馈，`company-feature-design` 与 `company-spike-research` 负责边界熔断。草稿由 `.codex-workflow/prototypes/<feature>/draft/prototype.json` 记录来源，确认后复制到需求文档同级 `prototype/` 目录。

**Tech Stack:** Codex Agent Skills、Markdown 项目模板、YAML 菜单元数据、JSON 插件清单、Bash/Python 安装验证脚本、Git。

## Global Constraints

- 以 `docs/superpowers/specs/2026-07-27-requirements-prototype-workflow-design.md` 为唯一设计依据，不扩展到生产原型框架或真实 API 集成。
- 中英文插件语义一致，slash 入口统一为 `/company-requirements-prototype`。
- 需求原型是需求阶段验证分支，不是新的 SDLC 阶段。
- 原型确认不得自动触发技术设计或任务拆分；只有用户明确授权才进入下一阶段。
- 草稿只能位于 `.codex-workflow/prototypes/<feature>/draft/`，基线只能位于权威需求文档同级 `prototype/`。
- 不自动修改 `.gitignore`，不删除 `prototype.json` 无法证明归属的文件，不自动 commit 或 push。
- 接入真实 API、数据库、认证、生产数据、生产组件或性能验证时必须熔断并重新路由。
- 本机最终只安装中文版 `company-codex-workflow-v2-zh`。
- 不修改外部专家 skill 内容，不暂存无关的 `docs/company-internal-training.md`。

## File Map

- 新建中英文 `skills/company-requirements-prototype/`：需求原型行为协议与菜单入口。
- 修改中英文 `company-workflow-help`、`company-feature-requirements`、`company-feature-design`、`company-spike-research`、`company-delivery-closeout`：入口、反馈循环、授权边界、技术原型区分和临时产物收口。
- 修改中英文插件 `AGENTS.md` 与项目模板 `AGENTS.md`：项目级阶段边界。
- 修改中英文 `BUNDLES.md`：登记需求原型组合。
- 修改四份 `requirements-template.md`：加入按需出现的需求原型验证章节。
- 修改 README、快速开始、使用指南、常用提示语、技能树和 CHANGELOG：用户可发现性与发布说明。
- 修改四份插件 manifest：版本升级到 `0.2.26` 并补充能力描述。

---

### Task 1: 建立 RED 基线并新增中英文原型 skill

**Files:**
- Create: `outputs/company-codex-workflow-v2-zh/skills/company-requirements-prototype/SKILL.md`
- Create: `outputs/company-codex-workflow-v2-zh/skills/company-requirements-prototype/agents/openai.yaml`
- Create: `outputs/company-codex-workflow-v2/skills/company-requirements-prototype/SKILL.md`
- Create: `outputs/company-codex-workflow-v2/skills/company-requirements-prototype/agents/openai.yaml`

**Interfaces:**
- Consumes: 权威需求、业务规则、用户的原型验证目标、现有草稿清单和显式确认语义。
- Produces: 原型阶段状态、隔离草稿、`prototype.json`、浏览器验证证据、需求反馈、可选需求基线和结构化完成报告。

- [ ] **Step 1: 记录当前失败基线**

运行：

```bash
test -f outputs/company-codex-workflow-v2-zh/skills/company-requirements-prototype/SKILL.md
rg -n "先画 HTML 原型|company-requirements-prototype" \
  outputs/company-codex-workflow-v2-zh/skills/company-workflow-help/SKILL.md
```

Expected: 两项均失败；当前插件没有专用 skill，也没有需求原型入口。真实项目证据已显示旧流程会把原型确认误路由到技术设计和任务拆分。

- [ ] **Step 2: 创建中文版 skill**

Frontmatter 使用：

```yaml
---
name: company-requirements-prototype
description: Use when 公司项目仍处于需求阶段，需要创建、预览、修改或确认隔离的 HTML、页面或交互原型，以验证需求而不进入技术设计或生产实现时。
---
```

正文必须包含：适用/不适用判断、需求阶段授权、验证目标、`superpowers:brainstorming` 触发规则、专家路由、草稿清单、浏览器验证、反馈回流、基线转存、熔断条件、清理来源证明、停止条件和完整输出协议。

- [ ] **Step 3: 创建英文版 skill**

Frontmatter 使用：

```yaml
---
name: company-requirements-prototype
description: Use when a company project is still in requirements and needs an isolated HTML, page, or interaction prototype created, reviewed, revised, or confirmed to validate requirements without entering technical design or production implementation.
---
```

英文正文必须与中文版本保持相同的路径、状态、授权门、熔断条件和输出字段语义。

- [ ] **Step 4: 添加菜单元数据**

两个包均使用 `display_name: "/company-requirements-prototype"`。中文短描述为“在需求阶段创建和确认隔离原型”，英文短描述为“Validate requirements with an isolated prototype”。默认提示词必须显式说明仍处于需求阶段。

- [ ] **Step 5: 运行 GREEN 结构检查**

```bash
for lang in company-codex-workflow-v2-zh company-codex-workflow-v2; do
  skill="outputs/$lang/skills/company-requirements-prototype/SKILL.md"
  menu="outputs/$lang/skills/company-requirements-prototype/agents/openai.yaml"
  test "$(sed -n '2p' "$skill")" = "name: company-requirements-prototype"
  rg -q '\.codex-workflow/prototypes/<feature>/draft' "$skill"
  rg -q 'prototype.json' "$skill"
  rg -q 'SHA-256' "$skill"
  rg -q 'superpowers:brainstorming' "$skill"
  rg -q 'company-expert-routing' "$skill"
  rg -q '/company-requirements-prototype' "$menu"
done
```

Expected: 所有断言通过。

### Task 2: 接通入口、反馈循环和阶段熔断

**Files:**
- Modify: both `skills/company-workflow-help/SKILL.md`
- Modify: both `skills/company-feature-requirements/SKILL.md`
- Modify: both `skills/company-feature-design/SKILL.md`
- Modify: both `skills/company-spike-research/SKILL.md`
- Modify: both `skills/company-delivery-closeout/SKILL.md`

**Interfaces:**
- Consumes: 用户当前阶段、原型意图、原型确认、真实集成意图和清单内临时产物。
- Produces: 唯一正确的 workflow 路由、需求反馈回流、设计授权判断、技术 Spike 分流和收口分类。

- [ ] **Step 1: 在 workflow-help 中加入路由规则**

增加四个可观察分支：

```text
需求阶段创建/修改页面原型 -> company-requirements-prototype
原型反馈改变业务规则 -> company-feature-requirements -> company-requirements-prototype
原型确认 -> 转为需求基线并停止
原型确认且用户明确说进入技术设计 -> company-feature-design
```

明确禁止“页面设计已确认，进入任务拆解”这类自动跨阶段结论。

- [ ] **Step 2: 在 requirements 中加入原型验证循环**

允许隔离原型作为需求验证产物；生产源码仍禁止修改。需求变化先更新需求或 `business-rules.md`，再继续原型，不得自动创建技术设计或任务文档。

- [ ] **Step 3: 在 design 与 spike 中加入反向边界**

`company-feature-design` 必须检查显式设计授权，原型文件或原型确认本身不构成授权。`company-spike-research` 必须把页面/交互/文案验证路由回需求原型，只保留技术、性能或架构可行性原型。

- [ ] **Step 4: 在 delivery-closeout 中识别原型产物**

清单登记且活动/待确认的草稿归为 `retain-but-exclude`；已撤回、被替换或完成基线校验的来源草稿归为 `cleanup-candidate`；已确认基线归为 `include`；没有清单来源的原型归为 `blocking-unknown`。删除仍受现有 dry-run 和来源证明约束。

- [ ] **Step 5: 验证路由与禁令**

```bash
for lang in company-codex-workflow-v2-zh company-codex-workflow-v2; do
  root="outputs/$lang/skills"
  rg -q 'company-requirements-prototype' "$root/company-workflow-help/SKILL.md"
  rg -q 'company-requirements-prototype' "$root/company-feature-requirements/SKILL.md"
  rg -q 'prototype.json' "$root/company-delivery-closeout/SKILL.md"
  rg -q 'company-requirements-prototype' "$root/company-spike-research/SKILL.md"
done
```

Expected: 两种语言都具备入口、回流、熔断和收口分类。

### Task 3: 固化项目级规则、bundle 和模板

**Files:**
- Modify: `outputs/company-codex-workflow-v2{,-zh}/AGENTS.md`
- Modify: `outputs/company-codex-workflow-template{,-zh}/AGENTS.md`
- Modify: `outputs/company-codex-workflow-v2{,-zh}/BUNDLES.md`
- Modify: four `specs/global/assets/requirements-template.md` files

**Interfaces:**
- Consumes: 项目初始化模板和 plugin fallback 模板。
- Produces: 新旧项目一致的需求原型边界、专家组合和按需需求章节。

- [ ] **Step 1: 更新四份 AGENTS.md**

在阶段边界中加入：需求阶段允许修改隔离原型路径，禁止修改生产源码；模糊的“确认原型”只表示转需求基线；真实集成触发熔断。

- [ ] **Step 2: 增加 `company-requirements-prototyping` bundle**

两份 `BUNDLES.md` 记录：主 workflow 为 `company-requirements-prototype`，默认组合 `company-feature-requirements`、`frontend-design`、`webapp-testing`，复杂交互才增加 `frontend-developer`。

- [ ] **Step 3: 更新四份需求模板**

加入可选“需求原型验证”章节及八个字段，并明确“只有触发原型时保留本节，否则删除”。

- [ ] **Step 4: 验证四套模板一致性**

```bash
rg -l '需求原型验证' outputs/company-codex-workflow-v2-zh outputs/company-codex-workflow-template-zh | wc -l
rg -l 'Requirements Prototype Validation' outputs/company-codex-workflow-v2 outputs/company-codex-workflow-template | wc -l
```

Expected: 中文和英文各至少命中 plugin 与 template 的需求模板及项目规则。

### Task 4: 更新用户文档、版本和插件能力描述

**Files:**
- Modify: `README.md`
- Modify: `docs/company-quickstart.md`
- Modify: `docs/codex-usage-guide.md`
- Modify: `docs/common-prompts.md` if present; otherwise add the examples to quickstart only
- Modify: `docs/skill-tree.md`
- Modify: `CHANGELOG.md`
- Modify: `outputs/company-codex-workflow-v2{,-zh}/plugin.json`
- Modify: `outputs/company-codex-workflow-v2{,-zh}/.codex-plugin/plugin.json`

**Interfaces:**
- Consumes: 用户常见表达和插件菜单发现机制。
- Produces: 可复制提示词、技能树节点、发布记录和 Codex 可识别版本。

- [ ] **Step 1: 增加用户使用说明**

文档至少包含以下三个示例：

```text
需求还没冻结，先根据当前内容做一个 HTML 原型验证页面和交互，不进入技术设计。
继续修改需求原型，保持需求阶段，不接真实接口。
需求和原型均确认，转为需求基线；先不要进入技术设计。
```

- [ ] **Step 2: 更新技能树和 CHANGELOG**

技能树将 `company-requirements-prototype` 放在需求与技术设计之间的可选验证分支。CHANGELOG 新增 `0.2.26 - 2026-07-27`，记录原型路由、基线生命周期和阶段熔断。

- [ ] **Step 3: 升级四份 manifest**

版本统一从 `0.2.25` 改为 `0.2.26`；能力描述加入“需求阶段隔离原型验证和确认式需求基线”，不改变作者、仓库和专家依赖。

- [ ] **Step 4: 检查版本和技能发现**

```bash
test "$(rg -l '"'"'version"'"': "'"'0.2.26"'"'' outputs/company-codex-workflow-v2{,-zh}/{plugin.json,.codex-plugin/plugin.json} | wc -l | tr -d ' ')" = "4"
test "$(find outputs/company-codex-workflow-v2{,-zh}/skills/company-requirements-prototype -name SKILL.md | wc -l | tr -d ' ')" = "2"
```

Expected: 四份 manifest 和两份 skill 均命中。

### Task 5: 全量验证、本机安装和发布

**Files:** Source tree, generated plugin readiness reports, local Chinese plugin installation.

- [ ] **Step 1: 运行静态与插件验证**

```bash
npm run verify
bash scripts/install.sh verify --lang zh
bash scripts/install.sh verify --lang en
git diff --check
```

Expected: 全部通过。

- [ ] **Step 2: 运行七个行为场景断言**

逐项核对设计文档中的七个验证场景，至少检查：需求原型入口、原型修改保持需求阶段、业务规则反馈回流、真实接口熔断、转基线后停止、显式设计授权、非可视化小需求不创建原型。

- [ ] **Step 3: 安装中文版并核对 Codex 插件注册**

```bash
bash scripts/install.sh install-plugin --lang zh --force
/Applications/Codex.app/Contents/Resources/codex plugin list
```

Expected: `company-codex-workflow-v2-zh` 显示 `0.2.26`，英文版不在本次安装范围。

- [ ] **Step 4: 精确暂存、提交和推送**

仅暂存本计划列出的跟踪文件，明确排除 `docs/company-internal-training.md`。检查 `git diff --cached --name-status`、`git diff --cached --check` 和 `git diff --cached --stat` 后提交，再普通推送 `origin/main`。
