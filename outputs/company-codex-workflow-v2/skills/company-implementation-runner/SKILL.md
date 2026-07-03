---
name: company-implementation-runner
description: Use when company requirements, design, and task plan are confirmed and Codex should implement feature work or approved change requests.
---

# Company Implementation Runner

## Purpose

Provide a Codex orchestration skill that reuses Superpowers TDD and verification instead of duplicating them.

## Workflow

1. Confirm requirements, design, and task plan exist unless this is `/hotfix` or `/spike`; if the task involves `business-rules.md`, read it.
2. Run Phase Consistency Preflight: check whether `说明文档.md`, `specs/global/INDEX.md`, the current feature/version README, task document, and related public-doc patch agree.
3. If public entry docs, indexes, version README, or task docs conflict, pause implementation; output the conflict, provisional authoritative document, and repair recommendation before coding.
4. Run the scope-change circuit breaker check: confirm this turn did not add an architecture layer, data-preparation layer, table, API boundary, business semantics, field mapping, scheduler chain, or unconfirmed documentation artifact.
5. If the circuit breaker triggers, stop coding; update only requirements, design, tasks, field mappings, or public-doc impact, and output `Implementation authorization: expired; user confirmation required before coding`.
6. Identify the next task and its verification.
7. Explicitly use `superpowers:test-driven-development`; define the minimal failing case or verification anchor before implementation.
8. Use `company-expert-routing` when implementation depends on framework internals, typing, performance, concurrency, data modeling, or UI craft, and read its `Phase permission`; if permission is not `implementation allowed`, do not code.
9. Make scoped edits.
10. Before claiming completion, run adversarial review for the relevant extreme input, abnormal state, permission, concurrency, performance, or UI rendering risks.
11. Explicitly use `superpowers:verification-before-completion` before claiming completion.
12. Check Chinese code logic comments: business rules, calculation semantics, data mapping, exceptional branches, and non-obvious technical decisions need useful comments.
13. Choose validation level `V0/V1/V2/V3` automatically and gather sufficient but not excessive evidence.
14. Check documentation drift: whether implementation changed requirements, business rules, technical design, API contracts, task plans, project entry docs, or indexes.
15. Run verification; when the company project uses progress documents, update according to branch strategy: integration branches may update public entry documents, business branches write `docs/public-doc-updates/<branch-or-feature>.md`.

## Superpowers Layer

- Default: `superpowers:test-driven-development` + `superpowers:verification-before-completion`.
- With a test harness: write or identify the failing test first, confirm the failure, then implement the smallest passing change.
- Without a test harness: define the minimal reproduction, input/output sample, page path, screenshot check, or manual verification checklist first.
- For pure copy, comment, or no-behavior edits, TDD may be skipped, but completion verification still applies and the reason must be stated.

## Validation Levels

- `V0`: docs, comments, formatting, or no-behavior changes; a diff and target-file review are enough.
- `V1`: isolated low-risk changes; run a focused command, local test, or minimal manual path.
- `V2`: default feature implementation; run related tests, type/build checks, and browser/manual verification when needed.
- `V3`: production, permission, security, data, performance, money/metric formulas, cross-system work, or hotfix; run regression, adversarial cases, and rollback/recovery notes.

Do not downgrade V2/V3 to save time, and do not force full verification for V0/V1 small changes.

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
- Scope-change circuit breaker:
- Phase permission:
- Implementation authorization:
- Authoritative document for this turn:
- Validation level:
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

## Boundary

Do not implement tasks that are not in the approved plan unless the user explicitly approves scope expansion.

Do not reuse an implementation handoff phrase from before a scope change for the new scope. The changed scope must be documented and confirmed by the user before coding.

If implementation reveals missing operation logic, formulas, field semantics, state transitions, or exception handling, do not guess; stop implementation and route back to `company-feature-requirements` to complete `business-rules.md`.

Non-integration branches must not write unmerged results directly into the current-state section of `说明文档.md`; record public entry changes as a public-doc update patch.

If implementation changes a documented promise but docs are not synchronized, the completion report must state `Documentation drift impact` and mark whether it was fixed, needs user confirmation, or should be handled by a later public-document patch.

If implementation contains complex business logic without necessary Chinese comments, do not claim completion; add comments or explain why the code is low-risk and self-explanatory.
