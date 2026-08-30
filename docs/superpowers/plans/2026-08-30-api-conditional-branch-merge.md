# API Conditional Branch Merge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Allow explicitly approved conditional merges into ordinary business branches while preserving API-pending, blocked-validation, and not-delivered status.

**Architecture:** Add a separate integration disposition beside the existing quality result instead of weakening `pass / conditional-pass / blocked`. Persist the state in bilingual project rules, workflow skills, and mirrored templates; enforce the contract with repository tests.

**Tech Stack:** Markdown Codex skills and templates, Python `unittest`, JSON plugin manifests, npm verification wrapper.

**Spec:** `docs/superpowers/specs/2026-08-30-api-conditional-branch-merge-design.md`

## Global Constraints

- Fixture and Mock remain frontend-development aids only.
- Required real API evidence missing means quality validation remains blocked.
- Conditional merge requires explicit approval and targets only an ordinary business branch.
- Conditional merge never means acceptance, delivery, release, deployment, or data correctness.
- Chinese and English outputs must stay behaviorally equivalent.

---

### Task 1: Contract Regression Tests

**Files:**
- Modify: `tests/test_quality_validation_workflow.py`

**Interfaces:**
- Consumes: bilingual plugin and starter distributions.
- Produces: failing checks for state separation, customer warning, approval metadata, and mirrored templates.

- [ ] Add assertions for `FIXTURE_READY`, `API_PENDING`, `CONDITIONAL_MERGED`, and the plain-language warning.
- [ ] Run `python3 tests/test_quality_validation_workflow.py` and confirm failure because the contract is absent.

### Task 2: Workflow and Project Rules

**Files:**
- Modify: `outputs/company-codex-workflow-v2{,-zh}/AGENTS.md`
- Modify: `outputs/company-codex-workflow-template{,-zh}/AGENTS.md`
- Modify: `outputs/company-codex-workflow-v2{,-zh}/skills/company-{implementation-runner,quality-validation,delivery-closeout,workflow-help}/SKILL.md`

**Interfaces:**
- Consumes: the approved state model.
- Produces: routing and execution rules for implementation, validation, and conditional merge.

- [ ] Add the project-wide Fixture/API boundary.
- [ ] Add implementation state transitions and mandatory API follow-up.
- [ ] Keep validation blocked when required API evidence is missing.
- [ ] Add an explicitly authorized conditional merge mode with protected-branch and deployment guards.
- [ ] Route API-unavailable work through the new decision.

### Task 3: Persistent Templates

**Files:**
- Modify: bilingual plugin and starter `tasks-template.md`
- Modify: bilingual plugin and starter `quality-validation-report-template.md`
- Modify: bilingual plugin and starter `delivery-closeout-template.md`

**Interfaces:**
- Consumes: workflow state and approval metadata.
- Produces: durable records that a new conversation can verify.

- [ ] Add data-source, real-API, Fixture-isolation, and compensation-task fields.
- [ ] Add conditional-merge approval and customer-warning fields.
- [ ] Ensure plugin and starter copies are byte-identical per language.

### Task 4: Release and Verification

**Files:**
- Modify: `package.json`
- Modify: bilingual plugin manifests
- Modify: `CHANGELOG.md`
- Modify: `docs/codex-usage-guide.md`

**Interfaces:**
- Consumes: verified workflow and templates.
- Produces: release `0.2.34` and locally installable plugin output.

- [ ] Bump all package and plugin versions to `0.2.34`.
- [ ] Document the conditional-merge boundary and customer notice.
- [ ] Run the focused test, `npm run verify`, and `git diff --check`.
- [ ] Install the Chinese plugin locally and verify the exposed version.
