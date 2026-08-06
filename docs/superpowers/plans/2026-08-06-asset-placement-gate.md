# Asset Placement Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a lightweight, automatic asset-placement gate that prevents executable, test, dependency, and build assets from being created under documentation roots.

**Architecture:** A standard-library Python validator owns project boundary discovery and changed/planned-path checks. Bootstrap installs the validator and generates a reviewable project config; company workflow skills consume the same config at design, planning, implementation, health-check, and closeout stages. Future pre-commit and CI enforcement reuse the validator but remain deferred.

**Tech Stack:** Python 3 standard library, Bash, PowerShell, Markdown Codex skills, `unittest`.

## Global Constraints

- Do not create a new user-facing workflow skill.
- Existing project boundary configs are preserved; updates produce a generated review candidate unless forced.
- Changed-path checks must avoid full repository scans.
- Documentation roots may declare explicit machine-contract exceptions.
- Pre-commit and CI enforcement remain deferred in this release.

---

### Task 1: Asset boundary validator

**Files:**
- Create: `scripts/asset_boundaries.py`
- Create: `tests/test_asset_boundaries.py`

**Interfaces:**
- Produces: `generate`, `confirm`, and `check` CLI commands.
- Produces: `.codex-workflow/asset-boundaries.json` schema version 1.

- [x] Write failing tests for build manifests, dependency trees, executable tests, machine contracts under docs, explicit exceptions, draft/confirmed configs, and changed-only checks.
- [x] Run the tests and confirm failure because the validator does not exist.
- [x] Implement the minimum validator needed by the tests.
- [x] Run focused tests and confirm they pass.

### Task 2: Installer integration

**Files:**
- Modify: `scripts/install.sh`
- Modify: `scripts/install.ps1`
- Modify: `bin/codex-company-workflow.js`

**Interfaces:**
- Produces: `generate-asset-boundaries`, `confirm-asset-boundaries`, `check-assets`, and `audit-assets` commands.
- Bootstrap and template updates install `.codex-workflow/bin/asset_boundaries.py`.

- [x] Add temporary-project installer tests to the verification path.
- [x] Integrate safe generation and review-candidate behavior.
- [x] Add syntax and command verification.

### Task 3: Workflow and template gates

**Files:**
- Modify: zh/en `AGENTS.md` files.
- Modify: zh/en design, task, and workflow-health templates.
- Modify: zh/en design, planning, implementation, bugfix, health-check, context-index, legacy-onboarding, and closeout skills.

**Interfaces:**
- Consumes: `.codex-workflow/asset-boundaries.json` and local validator.
- Produces: design ownership tables, allowed/forbidden task roots, pre-edit hard stops, and changed-file closeout checks.

- [x] Add static regression tests for every required workflow node.
- [x] Confirm tests fail against the current skills.
- [x] Add concise bilingual rules without changing expert source skills.
- [x] Run static regression tests.

### Task 4: Documentation and release

**Files:**
- Modify: `README.md`, quickstart, usage guide, skill tree, changelog, and plugin manifests.

**Interfaces:**
- Documents: automatic generation, review/confirmation, changed-file checks, full audits, and deferred pre-commit/CI rollout.

- [x] Update bilingual user guidance and examples.
- [x] Bump company plugin versions.
- [x] Run full verification, temporary bootstrap/update tests, and plugin validation.
- [x] Install the Chinese company plugin locally, commit, and push `main`.
