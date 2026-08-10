# Changelog

## 0.2.29 - 2026-08-11

- Added bilingual `company-quality-validation` skills and `/company-quality-validation` UI entries for risk-triggered independent delivery acceptance.
- Added bilingual quality-validation report templates with AC-to-scenario-to-evidence traceability and mirrored them into project starter kits.
- Connected workflow help, planning, implementation, bugfix, health checks, AGENTS, expert bundles, indexes, and delivery closeout to one automatic trigger matrix.
- Kept `V0/V1` and low-risk single-task `V2` lightweight while requiring validation for multi-task/cross-module/integration `V2`, milestones, release candidates, `V3`, and post-hotfix compensation.
- Added explicit `pass / conditional-pass / blocked` outcomes; blocked work returns to bugfix and must re-run the original validation scope before closeout.
- Added packaged regression coverage, install-time verification, and user guidance for the three-layer quality model: design strategy, implementation TDD, and independent acceptance.

## 0.2.28 - 2026-08-10

- Added one bilingual human-readable document standard with explicit `DOC-G01` through `DOC-G12` gates, stable `work-item-id` traceability, and user-only diagram waivers.
- Reworked formal requirements, design, data-model, business-rule, API-contract, task, prototype-approval, spike, hotfix, and delivery-closeout templates around decision-first reading and type-specific Mermaid diagrams.
- Added a fixed data-table design structure covering conclusions, domain relationships, write/read sequence, table responsibilities, field dictionaries, constraints, versioning, migration, examples, and validation.
- Connected AGENTS, ten workflow skill pairs, project indexes, generated indexes, starter kits, installers, and package verification to the same document contract.
- Kept legacy-project adoption low-friction: template updates stage candidates under `specs/global/assets.generated/` and never rewrite completed project documents automatically.

## 0.2.27 - 2026-08-06

- Added a bilingual asset placement gate that separates documentation roots from build, runtime, test, dependency, migration, and machine-contract assets.
- Added automatic `.codex-workflow/asset-boundaries.json` generation from project manifests, safe review candidates for existing configs, and explicit user confirmation.
- Added changed-file and full-audit commands with deterministic blocking for package manifests, dependency trees, executable tests, and undeclared machine contracts under documentation roots.
- Added safe generated-config acceptance with validation, backup, atomic replacement, and preservation of local exceptions.
- Scoped machine-contract exceptions to `AB004`, expanded OpenAPI/Swagger/AsyncAPI and common project-marker detection, and made non-Git diagnostics actionable.
- Synchronized npm packaging with plugin `0.2.27` and included the regression suite used by packaged `verify`/`all` commands.
- Connected context indexing, legacy onboarding, design, planning, implementation, bugfix, workflow health checks, delivery closeout, AGENTS rules, and templates to the same boundary configuration.
- Kept pre-commit and CI enforcement deferred while exposing a reusable validator for a later warning-to-blocking rollout.

## 0.2.26 - 2026-07-27

- Added bilingual `company-requirements-prototype` skills for isolated HTML, page, interaction, copy, and mock-state validation during requirements.
- Added a manifest-backed draft lifecycle under `.codex-workflow/prototypes/<feature>/draft/` and explicit promotion to a versioned requirements baseline beside authoritative requirements.
- Prevented prototype confirmation from automatically entering technical design or task planning; ambiguous confirmation and continuation now remain in the requirements stage.
- Added circuit breakers for real APIs, databases, authentication, production components, backend/schema/infrastructure, performance, and technical feasibility requests.
- Connected workflow help, requirements, design, spike, delivery closeout, project guardrails, expert bundles, templates, user guidance, and plugin manifests.

## 0.2.25 - 2026-07-27

- Replaced summary-only conversation handoff with outcome-first `resume`, `compact`, `fork`, and clean `handoff` routing.
- Added `quick`, `standard`, and `decision-rich` capsules, including rejected decisions and reopening conditions for complex company work.
- Added explicit transfer lifecycle and semantic receipt checks so target tasks restate goals, decisions, constraints, state, pending work, and authorization.
- Added accurate historical-knowledge boundaries and fallback behavior when native Codex task controls are unavailable.
- Updated bilingual skills, project guardrails, user guidance, manifests, and local installation metadata.

## 0.2.24 - 2026-07-16

- Added bilingual `company-delivery-closeout` skills with `prepare`, `commit`, and `deliver` modes for completed task batches, features, milestones, and version phases.
- Added per-file artifact classification, provenance-based cleanup dry-runs, protected-branch and unknown-file stops, exact staging, final-candidate verification, and ordinary business-branch push boundaries.
- Connected workflow help and implementation completion reports so users are automatically guided from the final task into delivery closeout.
- Added explicit Superpowers composition for final diff review, verification before completion, and branch-finalization checks without changing the selected closeout mode.
- Updated manifests, AGENTS guardrails, quickstart, usage guide, skill tree, and examples for the `0.2.24` company packages.

## 0.2.23 - 2026-07-13

- Added bilingual `company-thread-handoff` skills for compact long-conversation export and risk-based resume verification.
- Added `quick` and `full` handoff levels, verified-fact separation, unauthorized side-topic handling, and implementation-authorization checks.
- Added mixed routing: users can invoke handoff directly, while workflow help only recommends it at phase, context-drift, dirty-worktree, running-service, or incomplete-verification boundaries.
- Kept chat-only output as the default; optional file output only overwrites `.codex/handoff/current.md` and never creates routine project documentation.

## 0.2.22 - 2026-07-08

- Corrected subagents from an assumed default workflow capability to a conditional Codex capability requiring explicit user spawn/delegate instructions.
- Added `Subagent capability status` fields to workflow help, planning, implementation, AGENTS, templates, and user docs.
- Added optional project-scoped custom agent templates under `.codex/agents/` for company explorer, reviewer, security reviewer, and test reviewer roles.
- Added `install-agents <project-path>` to macOS/Linux and PowerShell installers so teams can opt into custom agents without forcing them into every project.
- Clarified that Codex App surfaces subagent activity but users do not need to find a separate subagent button; CLI users can manage agent threads with `/agent`.

## 0.2.21 - 2026-07-08

- Added Codex Plan Mode Recommendation for unclear routing, L2/L3 solution comparison, legacy onboarding, scope-change route reset, continuous implementation preflight, and high-risk work.
- Added Subagents Recommendation for independent tasks, independent failure domains, independent review, and high-risk continuous batches.
- Required workflow help, planning, implementation, AGENTS, templates, and docs to report Plan Mode and subagents status alongside Superpowers capability tracing.
- Added task-template fields for subagent strategy, subagent split plan, prohibited parallel work, and main-agent review.
- Clarified that Plan Mode never edits files or authorizes implementation, and subagent results must be reviewed by the main agent before completion claims.

## 0.2.20 - 2026-07-07

- Added Codex Goal Tracking Recommendation for L2/L3, cross-session, continuous implementation, legacy onboarding, hotfix follow-up, and skill governance workflows.
- Required workflow help to output whether goal tracking is not needed, recommended, or strongly recommended.
- Required implementation completion reports for complex work to include goal status guidance: create, keep, or close a Codex goal.
- Clarified that Codex goals are cross-turn objective containers and never replace phase permission, implementation authorization, scope-change circuit breaker, validation levels, or user confirmation.
- Updated zh/en plugin packages, AGENTS, workflow help, implementation runner, README, quickstart, usage guide, pilot playbook, and skill tree docs.

## 0.2.19 - 2026-07-06

- Added controlled continuous implementation mode for confirmed task plans when users explicitly ask to batch remaining tasks.
- Added per-task continuous eligibility in planning and task templates: `continuous`, `careful-continuous`, and `must-stop`.
- Required implementation completion reports to output next-step guidance and a copyable recommended user phrase.
- Added stop conditions after every continuous task: scope change, phase conflict, verification failure, V3 risk, approval needs, unconfirmed business semantics, worktree conflict, and local resource anomalies.
- Updated zh/en plugin packages, AGENTS, implementation runner, workflow help, feature planning, templates, README, quickstart, usage guide, and skill tree docs.

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
