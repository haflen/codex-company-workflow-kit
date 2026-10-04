---
name: company-implementation-runner
description: Use when company requirements, design, and task plan are confirmed and Codex should implement feature work or approved change requests.
---

# Company Implementation Runner

## Document Ownership Check

Read the project policy at `specs/global/assets/document-ownership.md`; fall back to the bundled `../../specs/global/assets/document-ownership.md`. Before creating or updating phase documents, inherit confirmed ownership and choose record size. Continue the existing unaccepted task; small fixes do not automatically create root features or a full document package. Compact records do not remove necessary focused design or verification.

## Purpose

Provide a Codex orchestration skill that reuses Superpowers TDD and verification instead of duplicating them.

## Workflow

1. Confirm requirements, design, and task plan exist unless this is `/hotfix` or `/spike`; if the task involves `business-rules.md`, read it.
2. Run Phase Consistency Preflight: check whether `说明文档.md`, `specs/global/INDEX.md`, the current feature/version README, task document, and related public-doc patch agree.
3. If public entry docs, indexes, version README, or task docs conflict, pause implementation; output the conflict, provisional authoritative document, and repair recommendation before coding.
4. Run the scope-change circuit breaker check: confirm this turn did not add an architecture layer, data-preparation layer, table, API boundary, business semantics, field mapping, scheduler chain, or unconfirmed documentation artifact.
5. If the circuit breaker triggers, stop coding; update only requirements, design, tasks, field mappings, or public-doc impact, and output `Implementation authorization: expired; user confirmation required before coding`.
   - When this turn adds or moves files, read `.codex-workflow/asset-boundaries.json` and run `.codex-workflow/bin/asset_boundaries.py check <project> --path <path>` on complete planned paths before the first edit.
   - Stop and return to design/planning when the gate blocks, the task lacks allowed roots, or engineering assets target `specs/`/`docs/`. The label “executable specification” is not an exception.
6. Identify the next task, its verification, and whether controlled continuous implementation applies.
7. Explicitly use `superpowers:test-driven-development`; define the minimal failing case or verification anchor before implementation.
8. Use `company-expert-routing` when implementation depends on framework internals, typing, performance, concurrency, data modeling, or UI craft, and read its `Phase permission`; if permission is not `implementation allowed`, do not code.
9. Decide whether subagents are worth recommending: default to main-agent serial execution; recommend subagents only for independent tasks, independent failure domains, or independent review. Actual invocation requires an explicit user request or clear task authorization.
10. Make scoped edits.
11. In continuous implementation mode, re-check stop conditions after every task; continue only when no stop condition is hit.
12. Before claiming completion, run adversarial review for the relevant extreme input, abnormal state, permission, concurrency, performance, or UI rendering risks.
13. Explicitly use `superpowers:verification-before-completion` before claiming completion.
14. Check Chinese code logic comments: business rules, calculation semantics, data mapping, exceptional branches, and non-obvious technical decisions need useful comments.
15. Choose validation level `V0/V1/V2/V3` automatically and gather sufficient but not excessive evidence.
16. Check documentation drift: whether implementation changed requirements, business rules, technical design, API contracts, task plans, project entry docs, or indexes.
17. Run verification; when the company project uses progress documents, update according to branch strategy: integration branches may update public entry documents, business branches write `docs/public-doc-updates/<branch-or-feature>.md`.
18. After all executable tasks complete, automatically classify independent quality validation as `not required / required / mandatory`. When triggered, route to `company-quality-validation` instead of jumping directly to delivery closeout.
19. Output next-step guidance: whether to continue, why to stop, and any genuinely missing information, decision, or authority.
20. For L2/L3, continuous implementation, or cross-session tasks, output Codex goal status guidance.

## Superpowers Layer

- Default: `superpowers:test-driven-development` + `superpowers:verification-before-completion`.
- With a test harness: write or identify the failing test first, confirm the failure, then implement the smallest passing change.
- Without a test harness: define the minimal reproduction, input/output sample, page path, screenshot check, or manual verification checklist first.
- For pure copy, comment, or no-behavior edits, TDD may be skipped, but completion verification still applies and the reason must be stated.
- If subagents are recommended or used, explicitly state `Subagent capability status` and `Subagents actual calls`. If they were not actually invoked, record it under `Not called, lens only` and state whether the reason is missing explicit user request, missing custom agents, App activity display only, or insufficient value for this turn.

## Validation Levels

- `V0`: docs, comments, formatting, or no-behavior changes; a diff and target-file review are enough.
- `V1`: isolated low-risk changes; run a focused command, local test, or minimal manual path.
- `V2`: default feature implementation; run related tests, type/build checks, and browser/manual verification when needed.
- `V3`: production, permission, security, data, performance, money/metric formulas, cross-system work, or hotfix; run regression, adversarial cases, and rollback/recovery notes.

Do not downgrade V2/V3 to save time, and do not force full verification for V0/V1 small changes.

## Independent Quality Validation Decision

Implementation TDD and completion verification provide fast feedback; they do not equal independent delivery acceptance. After all implementation tasks complete, decide automatically:

- `V0/V1`: `not required` by default.
- Single-task `V2`: `not required` by default; use `required` for critical user journeys, browser behavior, API/database integration, or a material regression surface.
- Multi-task, cross-module, frontend-backend, or API/database `V2`: `required`.
- Milestone, release candidate, `V3`, or post-hotfix compensation: `mandatory`.

When `required/mandatory`, the next workflow is `company-quality-validation`. That node performs independent validation and never modifies production code. A `blocked` result enters `company-bugfix-runner`, then repeats the original validation scope.

## Fixture-to-Real-API State Machine

When requirements, design, or tasks require a real API, real database, or real business data, separate the frontend candidate from complete delivery:

1. After approved Fixture/Mock implementation and checks, mark only `FIXTURE_READY`.
2. While real API integration or real-page acceptance is incomplete, mark `API_PENDING` and keep the related API/acceptance tasks open.
3. If the API is unavailable and the user explicitly approves an ordinary business-branch merge, route only to `company-delivery-closeout` in `conditional-merge` mode; after merge mark `CONDITIONAL_MERGED`.
4. Mark `API_INTEGRATED` only after real API integration completes and the production path has no silent Fixture/Mock fallback.
5. Mark `QUALITY_PASS` and enter formal delivery only after independent quality validation passes.

**Conditional merge is not conditional pass.** `CONDITIONAL_MERGED` must not close the original task, must not prove real data, charts, or business calculations correct, and must not claim acceptance, delivery, release, or deployment.

When an API is unavailable, put a customer-facing warning near the start of the human summary: only the Fixture frontend candidate is complete; who approved which business-branch merge; real API integration and real-page acceptance remain incomplete; and which Compensating task runs after API restoration. The production path must not silently fall back to Fixture or Mock.

## Continuous Implementation Mode

Continuous implementation mode is for confirmed task plans where the user wants fewer approval loops. It is controlled batching, not unlimited autopilot.

### Enable Conditions

All conditions must be true:

- The user explicitly asks for "continue all remaining tasks", "continuous implementation", "batch progress", "finish the confirmed task list", or equivalent wording.
- Requirements, design, task planning, and required `business-rules.md` / API contracts are confirmed.
- The task document contains task IDs, order, verification anchors, and estimated validation levels.
- Phase Consistency Preflight passes.
- The scope-change circuit breaker does not trigger.

If any condition is missing, fall back to normal single-task or small-batch mode and explain why.

### Batch Boundary

- `V0` documentation or no-behavior tasks: one related group is acceptable.
- `V1` small tasks: 3-5 related low-risk tasks are acceptable.
- `V2` standard tasks: 1-3 tightly related tasks are acceptable.
- `V3` high-risk tasks: one task only by default, then stop for user confirmation.

Do not merge unrelated tasks just to keep the batch running.

### Stop Conditions After Every Task

Stop and report the reason when any condition appears:

- Scope-change circuit breaker: new architecture layer, data-preparation layer, table, API, business semantics, field mapping, scheduler chain, or unconfirmed document.
- Phase consistency becomes invalid: entry docs, INDEX, README, task doc, or public-doc patch conflict.
- Current-task verification fails, tests are flaky, build fails, or critical browser verification fails.
- The next task becomes `V3`, or touches production, permissions, security, data migration, money/metric formulas, performance bottlenecks, or cross-system impact.
- Network, high-permission, destructive, database-write, or external-service action needs user approval.
- Business rules, operation logic, calculation semantics, field sources, exception/degradation behavior are not confirmed.
- The worktree has user changes that conflict with this batch.
- Local resource risk is visible, such as Playwright/browser zombie processes or Three.js pages driving sustained high CPU.

### Extra Report Fields

Continuous mode completion reports must include:

- Continuous implementation mode: enabled / not enabled
- Enable reason:
- Current batch:
- Completed tasks:
- Stop-condition check:
- Next candidate tasks:
- Auto-continue recommendation:
- Delivery closeout readiness: ready / not ready
- Closeout blockers:
- Independent quality validation decision: not required / required / mandatory
- Independent quality validation evidence:
- Expected quality validation report path: not applicable / `quality-validation-report.md` beside the authoritative task document
- Candidate awaiting validation: current branch, HEAD commit, validated paths
- Data source and integration state: `FIXTURE_READY` / `API_PENDING` / `CONDITIONAL_MERGED` / `API_INTEGRATED` / `QUALITY_PASS`
- Real API integration task and status:
- Conditional-merge approval and customer notice: not applicable / recorded
- Recommended next workflow: continue `company-implementation-runner` / enter `company-quality-validation` / enter `company-delivery-closeout`

When no candidate task remains and every task is complete, explicitly deferred, or explicitly rejected, first decide independent quality validation. If it is `not required`, recommend closeout. If it is `required/mandatory`, recommend: `Implementation is complete. Run independent quality validation.` The implementation runner must not perform milestone-level commit or push.

## Subagents Execution Strategy

Implementation defaults to not using subagents, because small tasks do not justify the extra token and coordination cost. Recommend subagents only when triggered; actual invocation still requires the user to explicitly ask to `spawn agents`, `delegate in parallel`, `use subagents for parallel review`, or equivalent wording.

- `not needed`: L0/L1, one task, one file, or many shared core files where main-agent serial execution is safer.
- `recommended`: L2 tasks with clear boundaries, or multiple independent tests/pages/modules failing; one subagent may implement or investigate while the main agent reviews.
- `strongly recommended`: L3 high-risk, cross-module/cross-system, data/permission/security/performance, or larger continuous batches; use at least an independent review subagent for spec compliance and code-quality/risk review.

Rules:

- The main agent must complete phase preflight, scope-change circuit breaker, and implementation authorization checks first.
- Subagents do not inherit the full conversation. Give them a narrow task packet: goal, boundary, allowed files, prohibited actions, verification method, and expected output.
- Do not dispatch parallel tasks that edit the same file, same state model, same database migration, same API contract, or same public-doc section.
- A subagent returning `DONE` is not completion. The main agent checks diffs, verification evidence, documentation drift, and remaining risk.
- Codex CLI can manage agent threads with `/agent`; the Codex App primarily surfaces subagent activity and does not require users to find a separate subagent entry button.
- For stable company roles, recommend running `bash scripts/install.sh install-agents <project-path> --lang en` first to generate `.codex/agents/company-*.toml`.
- If the user did not explicitly request subagents, output `Subagents actual calls: not called; reason: no explicit spawn/delegate request`, and state whether only the split strategy was used as a lens.

## Codex Goal Status Guidance

Implementation does not automatically create or close Codex goals, but complex work should report goal status guidance.

Output goal status guidance when:

- The current task is L2/L3 or clearly spans multiple phases or sessions.
- Continuous implementation mode is enabled.
- This implementation is one slice of a larger feature, legacy onboarding, skill upgrade, or hotfix follow-up chain.
- The completion report still has next candidate tasks, unverified items, or documentation drift awaiting confirmation.

It is enough to say "goal tracking not needed" for:

- L0/L1 one-turn tasks.
- Docs-only, comments-only, tiny config, one-off diagnosis, or no follow-up delivery chain.

When reporting goal status, state:

- A goal does not make implementation authorization valid.
- If scope-change circuit breaker, phase conflict, V3 risk, or verification failure appears, implementation must stop even when the goal remains active.
- Recommend closing the goal only when all final success criteria are satisfied.

## Chinese Code Logic Comments

Use the same Chinese-comment standard for Java, frontend TypeScript/Vue/React, Python, SQL, and scripts:

- Explain business rules, status branches, formulas/thresholds, precision, data mapping, fallback/hiding/degradation, compatibility strategy, and non-obvious performance/concurrency/cache handling.
- Do not write comments that merely translate syntax.
- If a threshold, formula, or mapping source is unclear, do not paper over it with a comment; route back to requirements, `business-rules.md`, or design docs.
- When logic changes, update related comments too.

## Phase Consistency Preflight

Before implementation, run a lightweight preflight. Do not scan every document. Check:

- Whether the current branch is main/develop/integration or a business branch.
- Whether `说明文档.md` current phase matches the task document.
- Whether `specs/global/INDEX.md` routes to the current feature/version.
- Whether the current version/feature README confirms implementation stage.
- Whether the task document includes confirmed tasks, task IDs, and verification anchors.
- Whether the current branch has a related `docs/public-doc-updates/` patch.

If the entry page still says spike/backlog while the current version README says formal implementation, treat the current task document as provisional authority, but first repair the public-entry impact record. On non-integration branches, prefer a public-doc patch.

## Scope-Change Circuit Breaker

Before implementation, decide whether the old authorization still applies. Pause coding when any of these is true:

- The user request contains signals such as "missing", "fill the gap", "analyze first", "why", "how to fit this in", "update docs", "business semantics", or "requirements/design/tasks need updates".
- This turn adds an architecture layer, data-preparation layer, database table, API boundary, scheduler chain, external system, key module, or cross-team responsibility.
- The task plan does not cover the new scope, or the new scope appeared after the previous implementation handoff.
- Field sources, calculation semantics, state transitions, exception/degradation strategy, permission boundaries, data-sync strategy, rerun strategy, or last-success snapshot strategy are not confirmed.
- Documentation work creates a new contract, field mapping, task list, or public-doc impact patch that the user has not confirmed.

After the circuit breaker trips:

- Only update requirements, `business-rules.md`, design, API contracts, task planning, field mappings, or public-doc patches.
- Output `Phase permission: documentation only / design first / planning needed / user confirmation required`.
- Output `Implementation authorization: expired; user confirmation required before coding`.
- Wait for the user to confirm the new scope and use the implementation handoff phrase before entering TDD or editing code.

## Target Client Gate

- Before UI/client work, compare INDEX, requirements, design, and tasks for target clients, viewports, browsers, and input methods.
- When mobile is not explicitly supported, the workflow must not add mobile adaptation on its own, including responsive breakpoints, touch behavior, mobile tests, or related dependencies.
- A new client or changed page/code/API sharing strategy is a scope change: stop coding and return to documents for confirmation.

## Human-First Output

Read `../../specs/global/assets/human-output-standard.md` first and respect the project's agreed audience and delivery purpose. Keep a one-sentence conclusion and next-step recommendation; explain results, evidence, and impact in the user's language. Internal fields in the output/report sections below belong in existing execution records, not ordinary user replies or human documents.

### Response Contract Gate

Before sending, check factual scope, prerequisites, actor, authority, audience, and display against the shared policy. Ordinary Q&A has no fixed headings; requests for detail receive useful evidence. Rewrite any part that fails the reading check.
## Completion Report

- Workflow layer: `company-implementation-runner`
- Trace mode:
- Superpowers layer:
- Actual calls:
- Expert/plugin capabilities:
- Not called, lens only:
- First Principles Check:
- Adversarial Review:
- Execution strategy:
- Phase Consistency Preflight:
- Asset placement gate: passed / blocked / not triggered
- Scope-change circuit breaker:
- Phase permission:
- Implementation authorization:
- Authoritative document for this turn:
- Validation level:
- Independent quality validation decision: not required / required / mandatory
- Independent quality validation evidence:
- Expected quality validation report path: not applicable / `quality-validation-report.md` beside the authoritative task document
- Candidate awaiting validation: current branch, HEAD commit, validated paths
- Verification evidence:
- Code comment check:
- Comment coverage:
- Documentation drift impact:
- Unverified items:
- Remaining risk:
- Minimal failing case or verification anchor:
- Adversarial review result:
- Task completed:
- Files changed:
- Public-doc impact:
- Verification:
- Progress document update:
- Residual risk:
- Continuous implementation mode:
- Enable reason:
- Current batch:
- Completed tasks:
- Stop-condition check:
- Next candidate tasks:
- Auto-continue recommendation:
- Delivery closeout readiness: ready / not ready
- Closeout blockers:
- Recommended next workflow: continue `company-implementation-runner` / enter `company-quality-validation` / enter `company-delivery-closeout`
- Subagents recommendation: not needed / recommended / strongly recommended
- Subagents actual calls: not called / called / split lens only
- Subagent capability status: not checked / available in current session / explicit user request needed / local custom agents needed / App activity display only
- Subagents reason:
- Reason subagents were not called:
- Subagent task packets:
- Subagent result review:
- Next-step guidance:
- User action needed (only for missing prerequisites):
- Goal status guidance:
- Recommend create/keep/close Codex goal:
- Recommended goal description or close condition:

## Boundary

Do not implement tasks that are not in the approved plan unless the user explicitly approves scope expansion.

Do not reuse an implementation handoff phrase from before a scope change for the new scope. The changed scope must be documented and confirmed by the user before coding.

If implementation reveals missing operation logic, formulas, field semantics, state transitions, or exception handling, do not guess; stop implementation and route back to `company-feature-requirements` to complete `business-rules.md`.

Non-integration branches must not write unmerged results directly into the current-state section of `说明文档.md`; record public entry changes as a public-doc update patch.

If implementation changes a documented promise but docs are not synchronized, the completion report must state `Documentation drift impact` and mark whether it was fixed, needs user confirmation, or should be handled by a later public-document patch.

If implementation contains complex business logic without necessary Chinese comments, do not claim completion; add comments or explain why the code is low-risk and self-explanatory.

Every completion report must include next-step guidance. Do not only say the work is complete; state whether continuing implementation, returning to requirements/design/planning, adding verification, pausing, or waiting for confirmation is the right next move.

If executable tasks remain, continue the current task or next batch. If none remain and task states are complete, decide independent quality validation first. Enter `company-delivery-closeout` only when validation is `not required`, returns `pass`, or returns an eligible `conditional-pass` explicitly accepted by the user. Never present task-level verification as independent validation or milestone closeout.

Milestone artifact inventory, temporary-file cleanup, final-candidate revalidation, exact staging, commit, and push belong only to `company-delivery-closeout`.

Goal tracking is only for cross-turn objective management. It must not replace phase permission, implementation authorization, TDD, validation levels, or user confirmation.

## Document Quality Gates

Before creating or substantially changing a formal document, read the project copy of `specs/global/assets/document-standard.md`; if absent, read the bundled `../../specs/global/assets/document-standard.md`. This skill enforces `DOC-G06`, `DOC-G07`, `DOC-G08`, `DOC-G09`, `DOC-G10`, `DOC-G11`, and `DOC-G12`. Check only formal documents synchronized in this implementation; do not rewrite all legacy documents.
