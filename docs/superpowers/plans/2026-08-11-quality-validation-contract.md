# Quality Validation Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the quality-validation-to-delivery-closeout contract with a durable report location, candidate identity, conditional-pass guardrails, canonical routes, and bounded evidence reuse.

**Architecture:** Keep Markdown as the only persisted contract. Required or mandatory validation writes a report beside the authoritative task document and binds it to validated paths using branch, HEAD, diff fingerprint, and untracked-file hashes. Delivery closeout recomputes the trigger, validates the report and fingerprint, and reuses fresh evidence unless validated paths drift.

**Tech Stack:** Markdown Codex skills and templates, Python `unittest` contract tests, shell/PowerShell installer verification, JSON plugin manifests.

## Global Constraints

- Release version is `0.2.30`.
- Maintain complete Chinese and English parity.
- Do not introduce a JSON sidecar, Git hook, CI gate, or mandatory report for `not required` validation.
- Keep quality validation read-only for production code.
- Preserve existing user files and unrelated repository changes.

---

### Task 1: Define Failing Contract Tests

**Files:**
- Modify: `tests/test_quality_validation_workflow.py`

**Interfaces:**
- Consumes: existing 0.2.29 quality workflow contract.
- Produces: executable assertions for report placement, candidate identity, transparency, routes, conditional-pass guardrails, closeout consumption, and 0.2.30 packaging.

- [ ] Add bilingual assertions for the compact transparency block and canonical workflow routes.
- [ ] Add assertions for report placement beside the authoritative task document and required persistence only for `required/mandatory`.
- [ ] Add assertions for branch, HEAD, validated paths, diff fingerprint, and untracked-file hashes.
- [ ] Add assertions for prohibited conditional-pass risks and explicit acceptance metadata.
- [ ] Add closeout assertions for missing/stale/blocked reports, fingerprint drift, evidence reuse, and no indiscriminate rerun.
- [ ] Change expected release version to `0.2.30`.
- [ ] Run `python3 tests/test_quality_validation_workflow.py` and verify failure is caused by missing 0.2.30 contract text.
- [ ] Commit with `test: define quality validation handoff contract`.

### Task 2: Implement Bilingual Skill and Template Contract

**Files:**
- Modify: `outputs/company-codex-workflow-v2-zh/skills/company-quality-validation/SKILL.md`
- Modify: `outputs/company-codex-workflow-v2/skills/company-quality-validation/SKILL.md`
- Modify: four `quality-validation-report-template.md` plugin/starter mirrors.
- Modify: bilingual `company-implementation-runner` and `company-bugfix-runner` skills only where report path/state output is required.

**Interfaces:**
- Consumes: failing tests from Task 1.
- Produces: one durable Markdown handoff contract and identical starter mirrors.

- [ ] Add persisted-report rules for `required/mandatory`, including canonical adjacent location and registered path.
- [ ] Add candidate identity and fingerprint rules.
- [ ] Add compact capability transparency fields to templates.
- [ ] Replace vague route labels with canonical workflow names and route reasons.
- [ ] Add hard conditional-pass prohibitions plus acceptance metadata.
- [ ] Add report path and candidate-state fields to implementation/bugfix completion output.
- [ ] Run focused quality workflow and document-template tests.
- [ ] Commit with `feat: bind quality reports to delivery candidates`.

### Task 3: Implement Closeout Consumption and Guidance

**Files:**
- Modify: bilingual `company-delivery-closeout` skills.
- Modify: bilingual `company-workflow-health-check` skills.
- Modify: `README.md`, `docs/company-quickstart.md`, `docs/codex-usage-guide.md`, and `docs/skill-tree.md`.

**Interfaces:**
- Consumes: report state and fingerprint from Task 2.
- Produces: deterministic closeout gate and user-facing explanation of evidence reuse.

- [ ] Add trigger recomputation, report discovery, status/acceptance validation, and candidate fingerprint comparison.
- [ ] Route validated-path drift back to `company-quality-validation` without recursive closeout.
- [ ] Clarify that quality validation and closeout call `verification-before-completion` for different artifacts.
- [ ] Add health diagnostics for missing report path, stale fingerprint, or absent acceptance record.
- [ ] Document report placement, optionality, status transition, and incremental revalidation.
- [ ] Run focused tests and `git diff --check`.
- [ ] Commit with `feat: enforce quality validation closeout gate`.

### Task 4: Release, Verify, Install, and Publish 0.2.30

**Files:**
- Modify: `package.json`.
- Modify: four plugin manifests.
- Modify: `CHANGELOG.md`.

**Interfaces:**
- Consumes: green contract implementation.
- Produces: validated and locally installed 0.2.30 release.

- [ ] Bump package and all manifests to `0.2.30`.
- [ ] Add a 0.2.30 changelog entry.
- [ ] Run `npm run verify` and both installer verification languages.
- [ ] Bootstrap a temporary project and verify the updated report template arrives.
- [ ] Fast-forward merge to `main` without staging `docs/company-internal-training.md`.
- [ ] Re-run `npm run verify` on merged `main`.
- [ ] Install the Chinese plugin locally and confirm `company-codex-workflow-v2-zh@personal` is enabled at `0.2.30`.
- [ ] Push `main` to `origin` and verify the remote commit.
