# Company Quality Validation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a risk-triggered company quality-validation workflow between implementation and delivery closeout without duplicating TDD or burdening low-risk work.

**Architecture:** A bilingual `company-quality-validation` skill owns integrated acceptance and release-quality evidence. Existing workflow entry, planning, implementation, bugfix, closeout, bundles, project rules, templates, indexes, and docs route through it only when deterministic risk triggers apply.

**Tech Stack:** Markdown skills and templates, YAML Codex skill interface metadata, Python `unittest`, Shell and PowerShell installers, JSON plugin manifests.

## Global Constraints

- Release version is `0.2.29`.
- V0/V1 remain outside independent quality validation by default.
- Multi-task or cross-boundary V2, milestone/release delivery, V3, and post-hotfix compensation trigger validation.
- Quality validation does not modify production code; defects route to bugfix and unclear semantics route to requirements/design.
- Every workflow response states the validation decision, reason, actual capabilities, evidence, unverified items, risk, and next workflow.
- English and Chinese plugin/starter assets remain structurally equivalent.

---

### Task 1: Define Regression Contracts

**Files:**
- Create: `tests/test_quality_validation_workflow.py`
- Modify: `tests/test_document_templates.py`

**Interfaces:**
- Consumes: current bilingual plugin and starter layout.
- Produces: executable contracts for skill discovery, trigger routing, report structure, starter mirrors, indexes, and release wiring.

- [ ] Write tests that require both language skills and `agents/openai.yaml` files.
- [ ] Require V0/V1 skip, cross-boundary V2 trigger, milestone/V3 mandatory trigger, bugfix return, and closeout gate language.
- [ ] Add `quality-validation-report-template.md` and `company-quality-validation` document-gate coverage.
- [ ] Run `python3 tests/test_quality_validation_workflow.py` and the focused document tests; confirm failure because assets do not exist.
- [ ] Commit the red contracts.

### Task 2: Add Bilingual Skill and Report Template

**Files:**
- Create: `outputs/company-codex-workflow-v2{,-zh}/skills/company-quality-validation/SKILL.md`
- Create: `outputs/company-codex-workflow-v2{,-zh}/skills/company-quality-validation/agents/openai.yaml`
- Create: `outputs/company-codex-workflow-v2{,-zh}/specs/global/assets/quality-validation-report-template.md`
- Create: `outputs/company-codex-workflow-template{,-zh}/specs/global/assets/quality-validation-report-template.md`

**Interfaces:**
- Consumes: validation levels, approved ACs, business rules, designs, tasks, final candidate, `testing-qa`, and Superpowers verification.
- Produces: `pass / conditional-pass / blocked`, trace matrix, evidence, defect route, and closeout readiness.

- [ ] Implement concise trigger-only frontmatter descriptions and English slash-style display names.
- [ ] Encode scope, trigger matrix, minimum-context reading, evidence, no-production-code boundary, and rerun loop.
- [ ] Create decision-first Mermaid report templates and mirror plugin bytes into starters.
- [ ] Run focused tests and commit the skill and template.

### Task 3: Connect the Workflow Graph

**Files:**
- Modify: bilingual `AGENTS.md`, `BUNDLES.md`, and `specs/global/INDEX.md` in plugin and starter packages.
- Modify: bilingual `company-workflow-help`, `company-feature-planning`, `company-implementation-runner`, `company-bugfix-runner`, `company-delivery-closeout`, and `company-workflow-health-check` skills.
- Modify: `scripts/generate_index.py`.

**Interfaces:**
- Consumes: Task 2 skill name and report path.
- Produces: automatic route selection and guarded transitions across implementation, defect repair, validation, and closeout.

- [ ] Add the quality bundle/stage and project guardrails.
- [ ] Add planning fields for predicted validation need and acceptance scope.
- [ ] Route implementation completion to validation when triggered and otherwise to closeout.
- [ ] Route quality defects through bugfix and require revalidation; make closeout reject missing mandatory evidence.
- [ ] Add index and generated-index navigation, run routing tests, and commit.

### Task 4: Release, Documentation, and Installation Verification

**Files:**
- Modify: `package.json`, `scripts/install.sh`, `scripts/install.ps1`.
- Modify: four plugin manifests under `outputs/company-codex-workflow-v2{,-zh}`.
- Modify: `README.md`, `CHANGELOG.md`, `docs/company-quickstart.md`, `docs/codex-usage-guide.md`, `docs/skill-tree.md`.

**Interfaces:**
- Consumes: completed workflow assets and tests.
- Produces: release `0.2.29`, packaged verification, user guidance, and installed Chinese plugin.

- [ ] Add the new regression suite to npm, Shell, and PowerShell verification.
- [ ] Bump package and manifests to `0.2.29` and document automatic trigger rules.
- [ ] Run `npm run verify`, bilingual installer verify, temporary bootstrap/update checks, and manifest parity checks.
- [ ] Install the Chinese plugin locally, verify Codex reports it enabled, merge to `main`, push GitHub, and preserve unrelated user files.
