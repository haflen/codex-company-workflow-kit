# Codex Company Workflow

These instructions define the team workflow for Codex in this project. Keep changes simple, scoped, and verified.

## Operating Principles

- Prefer the smallest change that satisfies the accepted requirement.
- Match existing project style and architecture before introducing new patterns.
- Do not refactor unrelated code while delivering a feature or fix.
- State assumptions when requirements, ownership, or risk are unclear.
- Use current official documentation for unstable third-party APIs instead of relying on memory.

## Context Loading

- Start by reading `specs/global/INDEX.md`.
- Read only the specific specs relevant to the task.
- Do not scan every Markdown file unless the task explicitly requires broad audit work.
- If the index is stale, update it as part of planning or after completing the related spec change.

## Target Client Contract

- “Client” means PC Web, Mobile Web, an app, desktop client, or large display, not TCP/HTTP network ports.
- Read the baseline in `specs/global/INDEX.md`, then any feature exception in current requirements. Only explicitly supported target clients enter design, planning, implementation, and validation.
- When mobile is unconfirmed, do not add responsive layouts, mobile breakpoints, touch interactions, mobile screenshots, device matrices, or mobile E2E.
- A PC-only product covers only the confirmed minimum viewport, browser, and mouse/keyboard scenarios. A non-UI feature may state “no direct client difference.”
- A confirmed client-scope change triggers the scope-change circuit breaker: update requirements, design, and tasks for user confirmation before adapting code.

## Human-First Summary

- In final replies, state the business result and impact first, then risks and the next action. Do not begin with Workflow Audit, task IDs, validation levels, or internal terms.
- The first layer uses: `One-sentence conclusion`, `What was completed`, `What needs attention`, and `What the user should do now`. When no action is needed, say so plainly.
- Explain internal terms on first use, for example “V3 (high-risk verification)”. Describe a file's purpose before its path.
- Give one primary next action and one short reply phrase. Add alternatives only for a real decision branch.
- Put Superpowers, expert calls, commands, paths, hashes, evidence, and internal workflow fields in a `Technical Audit Appendix`. Do not dump internal workflow fields one by one into the human summary.

## Document Ownership And Numbering

- Before writing any project document, confirm its role, information level, numbering namespace, and update trigger.
- `说明文档.md` or an equivalent entry page is only for project entry, current state, recent important events, and reading route; it must not become a spike field log.
- Spike logs use spike-scoped IDs such as `SPK02-T001`; formal tasks use feature, version, or formal task IDs. Do not reuse bare `Task 001` across documents.
- `specs/global/INDEX.md` should maintain the document ownership map.

## Asset Placement Gate

- Before adding or moving directories, packages, schemas, fixtures, tests, scripts, migrations, or cross-module assets, read `.codex-workflow/asset-boundaries.json`.
- `specs/` and `docs/` are documentation-only by default. Files that are built, executed, tested, or released belong to their owning engineering project. Machine-contract exceptions must declare an owner and validator.
- Design records an asset ownership table; planning uses complete repository-relative paths plus allowed and forbidden roots, never ambiguous short paths.
- Implementation or bugfix checks planned paths before the first edit; closeout checks only new and moved files in the current change. Blocking issues return to design or planning.
- Run `generate-asset-boundaries` when config is missing and ask the user to confirm the generated draft. Pre-commit/CI blocking remains deferred.
- If `asset-boundaries.generated.json` exists, review and accept it with `accept-asset-boundaries`, or explicitly discard it, before adding or moving engineering assets. Do not continue against a known stale formal config.

## Phase Boundaries

- Requirements clarification produces acceptance criteria and edge cases. Do not edit production implementation code. Page/interaction validation may edit only isolated mock prototypes under `.codex-workflow/prototypes/<feature>/draft/`.
- Technical design produces architecture, API/data contracts, risk notes, and test strategy. Do not edit implementation code in this phase.
- Implementation begins only after requirements and design are confirmed, unless the user explicitly invokes `/spike` or `/hotfix`.
- Prototype confirmation authorizes only a requirements baseline under `prototype/` beside authoritative requirements; do not enter design or planning without explicit authorization.
- Real APIs, databases, authentication, production data/components, backend, schema, infrastructure, performance, or feasibility requests stop and reroute requirements-prototype work.
- Ambiguous "confirm", "continue", or "next" means continue the current phase, not advance to design or coding.

## Phase Consistency Preflight

- Before implementation, bugfix, or hotfix, lightly check whether `说明文档.md`, `specs/global/INDEX.md`, current feature/version README, task documents, and related public-doc patches agree.
- If entry docs, index, and task documents point to different phases, pause ordinary implementation/bugfix and repair document routing first.
- Production hotfixes may restore service first, but the completion report must record conflicts and follow-up documentation work.

## First Principles And Adversarial Review

- Before complex requirements, technical design, bugfix root-cause claims, and spike conclusions, run a first-principles check: underlying facts, key constraints, and minimum conditions.
- Before implementation completion, bugfix completion, hotfix closure, spike conclusions, and pre-release verification, run adversarial review: extreme input, abnormal states, permission bypasses, concurrent retries, future timestamps, cache false positives, performance, or UI rendering pressure.
- Trivial changes may skip these checks, but the reason must be stated.
- Do not write only "checked"; include concrete facts, counterexample scenarios, or skip reasons.

## Standard Handoff Signals

- "Requirements confirmed, enter design" moves from requirements to technical design.
- "Design confirmed, start implementation" moves from design to implementation.
- "Start bugfix" enters root-cause debugging and repair.
- `/spike <question>` enters time-boxed technical exploration.
- `/hotfix <incident>` enters emergency repair.

## Scope Change Circuit Breaker

- Implementation authorization applies only to the confirmed requirements, design, and task scope.
- If implementation reveals a missing architecture layer, data-preparation layer, table, API boundary, business rule, field semantics, or required document update, the old authorization expires.
- After the circuit breaker trips, only update requirements, design, tasks, field mappings, or public-doc impact patches, and output `Implementation authorization: expired; user confirmation required before coding`.
- Do not continue coding immediately after updating docs; wait for the user to reconfirm the implementation scope.

## Verification Rules

- Feature work must include executable tests when the project has a test harness.
- Bug fixes must reproduce or explain the failure before changing code.
- Completion claims must cite the exact verification commands or manual checks performed.
- If automated verification is unavailable, provide a focused manual checklist.

## Validation Levels And Documentation Drift

- Choose validation level automatically: `V0` docs-only or no-behavior change; `V1` low-risk small change; `V2` standard feature or ordinary bugfix; `V3` production, permission, security, data, performance, money/metric formulas, cross-system work, or hotfix.
- Before implementation, bugfix, or hotfix completion, output validation level, verification evidence, unverified items, and remaining risk.
- If code changes requirements, operation logic, calculation semantics, API contracts, technical design, task plans, or public entry docs, state the documentation drift impact and update docs or mark the drift for confirmation.

## Chinese Code Logic Comments

- Java, frontend TypeScript/Vue/React, Python, SQL, and scripts use the same comment standard.
- Business rules, formula thresholds, precision, field mapping, enum/region mapping, fallback/hiding/degradation, exceptional handling, compatibility strategy, performance/concurrency/cache, and other non-obvious logic need Chinese comments.
- Do not write syntax-translation comments such as "iterate list" or "set variable".
- If threshold, formula, or mapping provenance is unclear, complete requirements or business-rule docs first; do not use comments as a substitute for missing semantics.

## Exception Channels

- `/spike` may skip full SDLC documents, but must produce a short spike report.
- `/hotfix` may prioritize recovery over design completeness, but must produce a hotfix report and follow-up test debt.
- Exception work should be minimal, isolated, and followed by normal cleanup planning.

## Triggered Quality Validation

- V0/V1 skips by default; multi-task or cross-boundary V2 enters `company-quality-validation`; milestone, release, V3, and post-hotfix compensation mandate it.
- Results are pass, conditional-pass, or blocked. Blocked work returns to bugfix and reruns validation; conditional acceptance requires explicit user approval.
- Independent validation never edits production code, and mandatory validation must pass before delivery closeout.

## Human-Readable Formal Documents

- Read `specs/global/assets/document-standard.md` before creating or substantially rewriting a formal document.
- Use the reading order: decision first, diagrams second, key tables third, details and evidence last.
- Formal documents require a `work-item-id` and type-specific Mermaid diagrams. Only an explicit user request may create a `Diagram Waiver`.
- Apply `DOC-G01` through `DOC-G12` to new documents; improve legacy documents only within the touched scope.
