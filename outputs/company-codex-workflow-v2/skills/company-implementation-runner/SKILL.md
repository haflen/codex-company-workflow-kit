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
4. Identify the next task and its verification.
5. Explicitly use `superpowers:test-driven-development`; define the minimal failing case or verification anchor before implementation.
6. Use `company-expert-routing` when implementation depends on framework internals, typing, performance, concurrency, data modeling, or UI craft; keep the bundle from design unless the touched area changed.
7. Make scoped edits.
8. Before claiming completion, run adversarial review for the relevant extreme input, abnormal state, permission, concurrency, performance, or UI rendering risks.
9. Explicitly use `superpowers:verification-before-completion` before claiming completion.
10. Choose validation level `V0/V1/V2/V3` automatically and gather sufficient but not excessive evidence.
11. Check documentation drift: whether implementation changed requirements, business rules, technical design, API contracts, task plans, project entry docs, or indexes.
12. Run verification; when the company project uses progress documents, update according to branch strategy: integration branches may update public entry documents, business branches write `docs/public-doc-updates/<branch-or-feature>.md`.

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

## Phase Consistency Preflight

Before implementation, run a lightweight preflight. Do not scan every document. Check:

- Whether the current branch is main/develop/integration or a business branch.
- Whether `说明文档.md` current phase matches the task document.
- Whether `specs/global/INDEX.md` routes to the current feature/version.
- Whether the current version/feature README confirms implementation stage.
- Whether the task document includes confirmed tasks, task IDs, and verification anchors.
- Whether the current branch has a related `docs/public-doc-updates/` patch.

If the entry page still says spike/backlog while the current version README says formal implementation, treat the current task document as provisional authority, but first repair the public-entry impact record. On non-integration branches, prefer a public-doc patch.

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
- Authoritative document for this turn:
- Validation level:
- Verification evidence:
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

If implementation reveals missing operation logic, formulas, field semantics, state transitions, or exception handling, do not guess; stop implementation and route back to `company-feature-requirements` to complete `business-rules.md`.

Non-integration branches must not write unmerged results directly into the current-state section of `说明文档.md`; record public entry changes as a public-doc update patch.

If implementation changes a documented promise but docs are not synchronized, the completion report must state `Documentation drift impact` and mark whether it was fixed, needs user confirmation, or should be handled by a later public-document patch.
