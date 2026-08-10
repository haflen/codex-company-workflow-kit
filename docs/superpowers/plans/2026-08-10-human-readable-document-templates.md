# Human-Readable Company Document Templates Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将公司工作流的正式文档改造成面向跨角色评审者、内嵌 Mermaid、可追溯且可由 workflow skill 检查的人类友好型模板体系。

**Architecture:** 在中英文插件中增加一份共享文档标准和三类缺失模板，以现有模板为正式产物入口；项目 starter 保存同语言的同构副本。workflow skills 只引用稳定门禁 ID 并检查相关子集，`company-workflow-health-check` 负责全量诊断。Python 契约测试验证模板集合、标题顺序、图类型、编号、门禁映射和 starter 同步，现有安装器继续按目录复制，无需新增复制分支。

**Tech Stack:** Markdown、Mermaid、Codex `SKILL.md`、Python `unittest`、Bash/PowerShell 安装器、JSON plugin manifest、npm CLI wrapper。

## Global Constraints

- 第一优先读者是业务、产品、开发和测试组成的跨角色评审团队。
- 所有需求文档默认包含目标业务流程图。
- 所有技术设计默认包含总体架构图和核心调用时序图。
- 数据模型设计默认包含表关系图和数据形成时序图。
- 只有用户明确说明不需要时才允许图表豁免；AI 不得自行豁免。
- 图表统一使用 Markdown 内嵌 Mermaid，并在图前说明问题、图后说明关键结论。
- 使用 `work-item-id` 与 `F/BR/AC/D/API/T/TC-nnn` 建立跨文档追溯。
- 新建和实质更新的文档采用新标准；不得自动重写业务项目中的历史文档。
- 复用 L1/L2/L3 控制展开深度，不新增另一套复杂度评分。
- 暂不增加 pre-commit 或 CI 强制门禁。
- 中英文插件与同语言 starter 必须保持结构和能力对等。
- 不修改或提交现有未跟踪文件 `docs/company-internal-training.md`。

---

## File Structure

### Shared standards and templates

- Create: `outputs/company-codex-workflow-v2-zh/specs/global/assets/document-standard.md`
- Create: `outputs/company-codex-workflow-v2/specs/global/assets/document-standard.md`
- Create: `outputs/company-codex-workflow-v2{,-zh}/specs/global/assets/data-model-template.md`
- Create: `outputs/company-codex-workflow-v2{,-zh}/specs/global/assets/requirements-prototype-record-template.md`
- Create: `outputs/company-codex-workflow-v2{,-zh}/specs/global/assets/delivery-closeout-template.md`
- Modify: `requirements-template.md`, `design-template.md`, `business-rules-template.md`, `api-contract-template.md`, `tasks-template.md`, `spike-report-template.md`, `hotfix-report-template.md` under both plugin asset roots.
- Mirror the ten formal templates and `document-standard.md` into `outputs/company-codex-workflow-template{,-zh}/specs/global/assets/`.

### Workflow enforcement

- Modify: both plugin and both starter language variants of `AGENTS.md`.
- Modify: both language variants of `company-feature-requirements`, `company-feature-design`, `company-feature-planning`, `company-requirements-prototype`, `company-spike-research`, `company-bugfix-runner`, `company-context-index`, `company-delivery-closeout`, `company-implementation-runner`, and `company-workflow-health-check` skills.

### Routing and distribution

- Modify: `scripts/generate_index.py`.
- Modify: both plugin `specs/global/INDEX.md` files and both starter `specs/global/INDEX.md` files.
- Modify only if a failing integration test proves necessary: `scripts/install.sh` and `scripts/install.ps1`.

### Tests and release metadata

- Create: `tests/test_document_templates.py`.
- Modify: `scripts/install.sh`, `scripts/install.ps1`, and `package.json` verification commands to run the new test.
- Modify: `README.md`, `docs/company-quickstart.md`, `docs/codex-usage-guide.md`, and `CHANGELOG.md`.
- Modify: `package.json`, both `.codex-plugin/plugin.json` files, and both root `plugin.json` compatibility manifests; bump version from `0.2.27` to `0.2.28`.

---

### Task 1: Add Failing Document Contract Tests

**Files:**
- Create: `tests/test_document_templates.py`

**Interfaces:**
- Consumes: the four template roots and ten workflow skill paths already present in the repository.
- Produces: one `unittest` suite that later tasks use as the document contract.

- [ ] **Step 1: Create the template contract test**

Use this structure and exact formal template set:

```python
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMAL_TEMPLATES = {
    "requirements-template.md",
    "design-template.md",
    "data-model-template.md",
    "business-rules-template.md",
    "api-contract-template.md",
    "tasks-template.md",
    "spike-report-template.md",
    "hotfix-report-template.md",
    "requirements-prototype-record-template.md",
    "delivery-closeout-template.md",
}
LANGUAGES = {
    "zh": {
        "plugin": ROOT / "outputs/company-codex-workflow-v2-zh",
        "starter": ROOT / "outputs/company-codex-workflow-template-zh",
        "conclusion": "## 先看结论",
        "change": "## 本次变化",
        "waiver": "图表豁免",
    },
    "en": {
        "plugin": ROOT / "outputs/company-codex-workflow-v2",
        "starter": ROOT / "outputs/company-codex-workflow-template",
        "conclusion": "## Decision Summary",
        "change": "## What Changed",
        "waiver": "Diagram Waiver",
    },
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class DocumentTemplateContractTests(unittest.TestCase):
    def test_formal_template_set_and_starter_mirror(self):
        for config in LANGUAGES.values():
            plugin_assets = config["plugin"] / "specs/global/assets"
            starter_assets = config["starter"] / "specs/global/assets"
            self.assertTrue((plugin_assets / "document-standard.md").is_file())
            self.assertTrue((starter_assets / "document-standard.md").is_file())
            for name in FORMAL_TEMPLATES:
                self.assertEqual(
                    read(plugin_assets / name),
                    read(starter_assets / name),
                    name,
                )

    def test_common_human_reading_contract(self):
        for config in LANGUAGES.values():
            assets = config["plugin"] / "specs/global/assets"
            for name in FORMAL_TEMPLATES:
                content = read(assets / name)
                self.assertIn("work-item-id", content, name)
                self.assertIn(config["conclusion"], content, name)
                self.assertIn(config["change"], content, name)
                self.assertIn(config["waiver"], content, name)
                self.assertIn("```mermaid", content, name)

    def test_required_diagram_types(self):
        for config in LANGUAGES.values():
            assets = config["plugin"] / "specs/global/assets"
            requirements = read(assets / "requirements-template.md")
            design = read(assets / "design-template.md")
            data_model = read(assets / "data-model-template.md")
            self.assertIn("flowchart", requirements)
            self.assertIn("flowchart", design)
            self.assertIn("sequenceDiagram", design)
            self.assertTrue("erDiagram" in data_model or "flowchart" in data_model)
            self.assertGreaterEqual(data_model.count("```mermaid"), 2)
```

- [ ] **Step 2: Add skill-gate and index assertions**

Add these constants before `DocumentTemplateContractTests`:

```python
SKILL_GATES = {
    "company-feature-requirements": {"DOC-G01", "DOC-G02", "DOC-G05", "DOC-G06", "DOC-G07", "DOC-G08", "DOC-G09", "DOC-G10", "DOC-G11", "DOC-G12"},
    "company-feature-design": {"DOC-G01", "DOC-G03", "DOC-G05", "DOC-G06", "DOC-G07", "DOC-G08", "DOC-G09", "DOC-G10", "DOC-G11", "DOC-G12"},
    "company-feature-planning": {"DOC-G01", "DOC-G04", "DOC-G05", "DOC-G06", "DOC-G07", "DOC-G08", "DOC-G09", "DOC-G10", "DOC-G11", "DOC-G12"},
    "company-requirements-prototype": {"DOC-G01", "DOC-G04", "DOC-G05", "DOC-G06", "DOC-G07", "DOC-G08", "DOC-G09", "DOC-G10", "DOC-G11", "DOC-G12"},
    "company-spike-research": {"DOC-G01", "DOC-G04", "DOC-G05", "DOC-G06", "DOC-G07", "DOC-G08", "DOC-G09", "DOC-G10", "DOC-G11", "DOC-G12"},
    "company-bugfix-runner": {"DOC-G01", "DOC-G04", "DOC-G05", "DOC-G06", "DOC-G07", "DOC-G08", "DOC-G09", "DOC-G10", "DOC-G11", "DOC-G12"},
    "company-context-index": {"DOC-G01", "DOC-G04", "DOC-G05", "DOC-G06", "DOC-G07", "DOC-G08", "DOC-G09", "DOC-G10", "DOC-G11", "DOC-G12"},
    "company-delivery-closeout": {"DOC-G01", "DOC-G04", "DOC-G05", "DOC-G06", "DOC-G07", "DOC-G08", "DOC-G09", "DOC-G10", "DOC-G11", "DOC-G12"},
    "company-implementation-runner": {"DOC-G06", "DOC-G07", "DOC-G08", "DOC-G09", "DOC-G10", "DOC-G11", "DOC-G12"},
    "company-workflow-health-check": {f"DOC-G{number:02d}" for number in range(1, 13)},
}
INDEX_ASSETS = {
    "document-standard.md",
    "data-model-template.md",
    "requirements-prototype-record-template.md",
    "delivery-closeout-template.md",
}
```

Add these methods inside `DocumentTemplateContractTests`:

```python
    def test_skill_gate_responsibilities(self):
        for config in LANGUAGES.values():
            for skill, gates in SKILL_GATES.items():
                content = read(config["plugin"] / "skills" / skill / "SKILL.md")
                for gate in gates:
                    self.assertIn(gate, content, f"{skill}: {gate}")

    def test_indexes_route_new_assets(self):
        for config in LANGUAGES.values():
            for root_name in ("plugin", "starter"):
                content = read(config[root_name] / "specs/global/INDEX.md")
                for asset in INDEX_ASSETS:
                    self.assertIn(asset, content, f"{root_name}: {asset}")
```

- [ ] **Step 3: Run the test and verify initial failure**

Run:

```bash
python3 tests/test_document_templates.py
```

Expected: FAIL because the shared standard and three new templates do not exist yet.

- [ ] **Step 4: Commit the failing contract test**

```bash
git add tests/test_document_templates.py
git commit -m "test: define human-readable document contracts"
```

---

### Task 2: Build the Shared Standard and Core Templates

**Files:**
- Create: both language variants of `document-standard.md` and `data-model-template.md`.
- Modify: both language variants of `requirements-template.md` and `design-template.md`.

**Interfaces:**
- Consumes: `DOC-G01` through `DOC-G12` and the ID rules in the approved design spec.
- Produces: the authoritative structure consumed by feature requirements and feature design workflows.

- [ ] **Step 1: Write `document-standard.md` in Chinese and English**

Include exact sections for scope, reading order, `work-item-id`, local ID formats, change baseline, Mermaid conventions, diagram waiver, `DOC-G01` through `DOC-G12`, L1/L2/L3 depth, and the workflow responsibility matrix. The English file must preserve the same IDs and semantics.

- [ ] **Step 2: Rewrite the requirements templates**

Use this heading order in Chinese and its semantic English equivalent:

```markdown
# 功能需求
## 元信息
## 先看结论
## 本次变化
## 建议阅读路径
## 用户、场景与价值
## 目标业务流程
## 操作步骤与系统反馈
## 页面与交互状态
## 范围与边界
## 业务规则与计算口径
## 验收标准
## 假设、待确认问题与已确认决策
## 需求原型与实物证据
## 追溯
## 图表豁免
## 人类可读性检查
## 人工确认与下一步
```

Embed a valid Mermaid `flowchart` with `F-001` style nodes and map `AC-001` to `F-001` in the acceptance table.

- [ ] **Step 3: Rewrite the design templates**

Include separate Mermaid `flowchart` and `sequenceDiagram` blocks, requirement/AC mapping, module boundaries, failures, data/state links, decision comparison, API contract links, quality attributes, asset placement, tests, release/recovery, waiver, gate result, and next-step confirmation.

- [ ] **Step 4: Create the data model templates**

Implement the complete order from the approved spec: conclusion, reading legend, object inventory, relationship diagram, formation sequence, read/write matrix, key relations, per-table design, page/API mapping, migration, acceptance, L1/L2/L3 depth, waiver, and gate result. Provide two Mermaid blocks and field tables that keep constraints separate from field definitions.

- [ ] **Step 5: Run focused tests**

```bash
python3 tests/test_document_templates.py
```

Expected: core structure assertions pass; failures remain for the other missing templates, starter mirrors, indexes, and skill gates.

- [ ] **Step 6: Commit the core templates**

```bash
git add outputs/company-codex-workflow-v2/specs/global/assets outputs/company-codex-workflow-v2-zh/specs/global/assets
git commit -m "feat: add human-first requirements design and data templates"
```

---

### Task 3: Upgrade the Remaining Formal Templates

**Files:**
- Modify: both language variants of `business-rules-template.md`, `api-contract-template.md`, `tasks-template.md`, `spike-report-template.md`, and `hotfix-report-template.md`.
- Create: both language variants of `requirements-prototype-record-template.md` and `delivery-closeout-template.md`.

**Interfaces:**
- Consumes: the shared metadata, change, waiver, trace, and gate sections from Task 2.
- Produces: the remaining type-specific formal documents listed in design section 7.

- [ ] **Step 1: Upgrade business rules and API contracts**

Business rules must include a Mermaid state or calculation flow, formula narrative, mathematical expression, source/unit/precision, missing-data behavior, worked example, and adversarial cases. API contracts must put a `sequenceDiagram` before request/response payloads and include authentication, validation, persistence, errors, compatibility, and realistic redacted examples.

- [ ] **Step 2: Upgrade tasks, spike, and hotfix templates**

Tasks use a dependency `flowchart` showing serial, parallel, confirmation, and release stops. Spike uses an uncertainty-to-evidence path. Hotfix uses a fault-to-recovery path and separates containment from permanent repair.

- [ ] **Step 3: Add prototype and closeout templates**

Prototype records use a page-state or interaction flow and preserve the requirements-stage boundary. Closeout uses an artifact or release flow and covers code, documents, scripts, migration, cleanup, verification, remaining risks, commit, and push evidence.

- [ ] **Step 4: Run focused tests**

```bash
python3 tests/test_document_templates.py
```

Expected: plugin template assertions pass; starter parity, index, and skill gate assertions still fail.

- [ ] **Step 5: Commit the formal template set**

```bash
git add outputs/company-codex-workflow-v2/specs/global/assets outputs/company-codex-workflow-v2-zh/specs/global/assets
git commit -m "feat: upgrade formal workflow document templates"
```

---

### Task 4: Enforce the Contract in AGENTS and Workflow Skills

**Files:**
- Modify: `outputs/company-codex-workflow-v2{,-zh}/AGENTS.md`.
- Modify: `outputs/company-codex-workflow-template{,-zh}/AGENTS.md`.
- Modify: the ten workflow skill pairs listed in File Structure.

**Interfaces:**
- Consumes: `document-standard.md` and stable `DOC-G01` through `DOC-G12` IDs.
- Produces: phase-specific generation and completion behavior without duplicating gate definitions.

- [ ] **Step 1: Add the human-readable document protocol to AGENTS**

State the shared reading order, mandatory diagram policy, explicit-user-only waiver, trace ID rules, authority rule, diagram size guidance, render evidence, historical-document compatibility, and no automatic phase crossing.

- [ ] **Step 2: Add gate references to requirements and design skills**

Requirements must cite `DOC-G01`, `DOC-G02`, and `DOC-G05` through `DOC-G12`, adding `DOC-G04` when it creates business rules. Design must cite `DOC-G01`, `DOC-G03`, and `DOC-G05` through `DOC-G12`, adding `DOC-G04` for data models and separate API contracts.

- [ ] **Step 3: Add type-specific gate references to planning, prototype, spike, bugfix, context, and closeout skills**

Use the exact responsibility matrix from design section 9.1. Each skill must read the project `document-standard.md` first, then plugin fallback `../../specs/global/assets/document-standard.md`.

- [ ] **Step 4: Limit implementation and health-check behavior**

Implementation checks only authoritative documents changed in the current run using `DOC-G06` through `DOC-G12`. Health check diagnoses all `DOC-G01` through `DOC-G12` and reports repairs without rewriting documents by default.

- [ ] **Step 5: Run skill gate tests**

```bash
python3 tests/test_document_templates.py
```

Expected: skill gate assertions pass; starter and index assertions remain.

- [ ] **Step 6: Commit workflow enforcement**

```bash
git add outputs/company-codex-workflow-v2/AGENTS.md outputs/company-codex-workflow-v2-zh/AGENTS.md outputs/company-codex-workflow-template/AGENTS.md outputs/company-codex-workflow-template-zh/AGENTS.md outputs/company-codex-workflow-v2/skills outputs/company-codex-workflow-v2-zh/skills
git commit -m "feat: enforce document readability gates in workflows"
```

---

### Task 5: Synchronize Starters, Indexes, and Project Installation

**Files:**
- Modify/Create: formal assets under both starter roots.
- Modify: four `specs/global/INDEX.md` files.
- Modify: `scripts/generate_index.py`.
- Modify only on proven failure: `scripts/install.sh`, `scripts/install.ps1`.

**Interfaces:**
- Consumes: completed plugin assets.
- Produces: project bootstrap and template upgrade candidates containing the same formal templates.

- [ ] **Step 1: Mirror each language's formal assets into its starter**

Copy the ten formal templates and `document-standard.md` from each plugin root to the matching starter root. Do not copy operational reports that are outside the approved formal-document scope.

- [ ] **Step 2: Update static indexes and index generation**

Add the document standard, data model, prototype record, and delivery closeout entries. Add a compact Mermaid navigation graph showing project entry, requirements, rules, design/data/API, tasks, implementation, verification, and closeout without duplicating milestone facts.

- [ ] **Step 3: Run the contract tests**

```bash
python3 tests/test_document_templates.py
```

Expected: all document contract tests pass.

- [ ] **Step 4: Exercise bootstrap and safe template update in temporary directories**

```bash
tmp_project="$(mktemp -d)"
bash scripts/install.sh bootstrap-project "$tmp_project" --lang zh
test -f "$tmp_project/specs/global/assets/data-model-template.md"
bash scripts/install.sh update-templates "$tmp_project" --lang zh
test -d "$tmp_project/specs/global/assets.generated"
```

Expected: bootstrap installs the new files; safe update preserves current assets and writes a review candidate. Change installer code only if this test fails because of installer behavior.

- [ ] **Step 5: Commit distribution changes**

```bash
git add outputs/company-codex-workflow-template outputs/company-codex-workflow-template-zh scripts/generate_index.py outputs/company-codex-workflow-v2/specs/global/INDEX.md outputs/company-codex-workflow-v2-zh/specs/global/INDEX.md
git commit -m "feat: distribute human-readable document templates"
```

---

### Task 6: Integrate Verification and Publish User Guidance

**Files:**
- Modify: `scripts/install.sh`, `scripts/install.ps1`, `package.json`, `README.md`, `docs/company-quickstart.md`, `docs/codex-usage-guide.md`, `CHANGELOG.md`.
- Modify: both plugin manifest pairs.

**Interfaces:**
- Consumes: passing tests and synchronized assets.
- Produces: version `0.2.28`, documented safe upgrade behavior, and one-command verification.

- [ ] **Step 1: Add the document test to verification commands**

`scripts/install.sh verify` must run:

```bash
python3 "$ROOT_DIR/tests/test_document_templates.py"
```

Add the equivalent command to PowerShell `Verify-Kit`. Update `package.json` so `npm run verify` performs Node syntax, shell syntax, asset-boundary tests, and document-template tests.

- [ ] **Step 2: Document creation and upgrade behavior**

Explain the human-first reading order, required Mermaid diagrams, explicit waiver, trace IDs, safe `assets.generated` comparison, old-document compatibility, and the difference between updating plugin templates and intentionally migrating an existing project document.

- [ ] **Step 3: Bump release metadata to `0.2.28`**

Update npm package version, Chinese and English `.codex-plugin/plugin.json`, root compatibility manifests, and changelog. Preserve plugin names and skill descriptions.

- [ ] **Step 4: Run package and installer verification**

```bash
npm run verify
bash scripts/install.sh verify --lang zh
bash scripts/install.sh verify --lang en
```

Expected: all checks pass; PowerShell syntax is checked when `pwsh` is available and otherwise reports a skip.

- [ ] **Step 5: Commit verification, docs, and release metadata**

```bash
git add scripts/install.sh scripts/install.ps1 package.json README.md docs/company-quickstart.md docs/codex-usage-guide.md CHANGELOG.md outputs/company-codex-workflow-v2/.codex-plugin/plugin.json outputs/company-codex-workflow-v2/plugin.json outputs/company-codex-workflow-v2-zh/.codex-plugin/plugin.json outputs/company-codex-workflow-v2-zh/plugin.json
git commit -m "chore: release human-readable workflow templates"
```

---

### Task 7: Final Verification, Local Install, and Release Check

**Files:**
- Verify all changed files.
- Do not stage: `docs/company-internal-training.md`.

**Interfaces:**
- Consumes: release candidate `0.2.28`.
- Produces: verified local Chinese plugin installation and a clean release commit set ready to push.

- [ ] **Step 1: Review scope and unrelated changes**

```bash
git status --short
git diff --check ec10c27..HEAD
git log --oneline -8
```

Expected: only planned tracked changes appear in commits; `docs/company-internal-training.md` remains untracked and unstaged.

- [ ] **Step 2: Run the complete verification suite**

```bash
python3 tests/test_asset_boundaries.py
python3 tests/test_document_templates.py
npm run verify
bash scripts/install.sh verify --lang zh
bash scripts/install.sh verify --lang en
```

Expected: every command exits successfully.

- [ ] **Step 3: Install the updated Chinese company plugin locally**

```bash
bash scripts/install.sh install-plugin --lang zh --force
```

Expected: Codex personal marketplace contains `company-codex-workflow-v2-zh` version `0.2.28`, including the new assets and updated skills.

- [ ] **Step 4: Verify the installed plugin and explain session refresh**

Run the repository's plugin listing/health command available in the environment, verify the installed manifest version, and state that already-open Codex tasks do not dynamically reload skills; validation requires a newly opened task after installation.

- [ ] **Step 5: Push only after local verification succeeds**

```bash
git push origin main
```

Expected: remote `main` contains the complete `0.2.28` release commits.
