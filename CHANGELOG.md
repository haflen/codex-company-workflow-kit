# Changelog

## 0.2.18 - 2026-07-03

- Added Scope Change Circuit Breaker / 范围变化熔断 so old implementation authorization expires when new architecture layers, data-preparation layers, tables, API boundaries, field mappings, or business semantics appear mid-implementation.
- Required `company-workflow-help` and `company-expert-routing` to output phase permission and implementation authorization status before continuing into coding.
- Updated `company-implementation-runner` to stop before TDD/code edits when changed scope needs requirements, design, task planning, field mapping, or user confirmation first.
- Updated design, planning, templates, README, quickstart, usage guide, and skill tree docs to explain that documentation updates after a scope change must not automatically flow back into implementation.

## 0.2.17 - 2026-07-03

- Added cross-language Chinese code logic comment rules for Java, frontend TypeScript/Vue/React, Python, SQL, scripts, and generated configuration logic.
- Required comments for business rules, calculation semantics, data mappings, exceptional branches, fallback/degradation behavior, compatibility strategy, and non-obvious performance/concurrency/cache logic.
- Added `Code comment check` / `代码备注检查` and comment coverage fields to implementation and bugfix completion reports.
- Updated task templates, lightweight templates, and user docs so comment coverage is planned before implementation and checked before completion.

## 0.2.16 - 2026-07-03

- Added Phase Consistency Preflight before implementation, bugfix, and hotfix work.
- Required workflows to compare project entry docs, `specs/global/INDEX.md`, current feature/version README, task documents, and public-doc patches before coding.
- Updated workflow health checks to diagnose entry/index/task-document phase conflicts in legacy projects.
- Documented the authority order for public entry docs, routing indexes, branch-local task documents, and public-doc update patches.

## 0.2.15 - 2026-07-03

- Added `company-workflow-health-check` for read-only diagnosis of legacy or partially bootstrapped project workflow health.
- Added `workflow-health-report-template.md` and included it in project context indexes and generated INDEX drafts.
- Added automatic validation levels `V0/V1/V2/V3` so implementation, bugfix, and hotfix work can balance verification cost with risk.
- Added documentation-drift checks to implementation, bugfix, planning, task templates, docs, and lightweight templates.

## 0.2.14 - 2026-07-03

- Added trigger-based technical solution comparison for design-stage work.
- Required 2-3 option comparison and user confirmation for L2/L3 large modules, cross-boundary designs, data/security/performance work, business rules, or maintainability tradeoffs.
- Allowed L1 low-risk single-path changes to skip comparison with an explicit reason, and blocked task planning until triggered design comparisons are confirmed.

## 0.2.13 - 2026-07-03

- Added `business-rules-template.md` for operation logic, state transitions, calculation formulas, field semantics, exception handling, and example cases.
- Added trigger-based rules so small requirements do not create business-rules documents, while complex metrics, formulas, state, data semantics, or abnormal-data cases do.
- Updated requirements, design, planning, implementation, bugfix, context index, workflow help, AGENTS, generated INDEX output, and user docs to route business rules through requirements and convert examples into verification anchors.

## 0.2.12 - 2026-06-30

- Added a multi-branch public document protocol for company projects.
- Added `public-doc-update-template.md` so feature, spike, and hotfix branches can propose public document updates without directly rewriting `说明文档.md`.
- Updated AGENTS, INDEX templates, generated index output, context indexing, planning, implementation, bugfix, spike, and user docs to keep public docs as mainline facts.

## 0.2.11 - 2026-06-29

- Hardened skill upgrade governance to sync only referenced or explicitly named external experts instead of cloning large upstream catalogs.
- Added a preservation rule for local Codex `description: Use when...` frontmatter, routing constraints, Superpowers layering, and company guardrails during expert updates.
- Added upgrade hygiene rules for raw/API/sparse fetching, script permission drift, generated readiness artifacts, and runtime approval requirements.

## 0.2.10 - 2026-06-29

- Synced 13 vendored expert skills from `sickn33/antigravity-awesome-skills@e0ef87efd0ad5a18a23e21bb08406b3eaf563b35`.
- Preserved Codex-optimized `Use when...` trigger descriptions while updating upstream bodies, references, scripts, and metadata.
- Updated `EXPERTS.lock.md` to `V13.4.0` / `1,693+` observed upstream catalog state and recorded the exact vendored pin.
- Reclassified script-bearing experts: `typescript-expert` remains high risk and `webapp-testing` remains medium risk; both require runtime approval before script execution.

## 0.2.9 - 2026-06-29

- Added workflow document ownership rules for project entry pages, spike logs, formal specs, and lifecycle summaries.
- Added numbering namespace guidance to prevent bare task IDs from crossing document levels.
- Updated context indexing, legacy onboarding, spike workflow, INDEX generation, templates, and docs in zh/en packages.

## 0.2.8 - 2026-06-29

- Added built-in First Principles Check for complex requirements, design, bugfix root cause analysis, and spike conclusions.
- Added built-in Adversarial Review for implementation completion, bugfix completion, hotfix closure, spike conclusions, and skill governance.
- Updated company workflow skills, templates, expert routing, and docs in zh/en packages.
- Updated lightweight company templates with the same first-principles and adversarial-review guardrails.

## 0.2.0 - 2026-06-11

- Added company Codex workflow v2 starter kit.
- Added expert bundle routing through `BUNDLES.md`.
- Added expert dependency lock through `EXPERTS.lock.md`.
- Added user-confirmed skill upgrade workflow with dry-run, diff, security review, apply, validation, and rollback record.
- Added company user quickstart and dry-run upgrade guide.
- Added workflow help entry skill, common prompts, pilot playbook, Codex usage guide, and cross-platform install scripts.
- Added bilingual workflow help content and current company skill tree documentation.
- Added Superpowers integration documentation and mapped company workflow nodes to Superpowers engineering skills.
- Added Chinese localized template and v2 packages, plus zh/en installer language selection.
- Added automatic project context index draft generation and legacy project onboarding workflow.
