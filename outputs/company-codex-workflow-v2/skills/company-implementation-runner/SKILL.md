---
name: company-implementation-runner
description: Use when company requirements, design, and task plan are confirmed and Codex should implement feature work or approved change requests.
---

# Company Implementation Runner

## Purpose

Provide a Codex orchestration skill that reuses Superpowers TDD and verification instead of duplicating them.

## Workflow

1. Confirm requirements, design, and task plan exist unless this is `/hotfix` or `/spike`.
2. Identify the next task and its verification.
3. Explicitly use `superpowers:test-driven-development`; define the minimal failing case or verification anchor before implementation.
4. Use `company-expert-routing` when implementation depends on framework internals, typing, performance, concurrency, data modeling, or UI craft; keep the bundle from design unless the touched area changed.
5. Make scoped edits.
6. Before claiming completion, run adversarial review for the relevant extreme input, abnormal state, permission, concurrency, performance, or UI rendering risks.
7. Explicitly use `superpowers:verification-before-completion` before claiming completion.
8. Run verification; when the company project uses progress documents, update according to branch strategy: integration branches may update public entry documents, business branches write `docs/public-doc-updates/<branch-or-feature>.md`.

## Superpowers Layer

- Default: `superpowers:test-driven-development` + `superpowers:verification-before-completion`.
- With a test harness: write or identify the failing test first, confirm the failure, then implement the smallest passing change.
- Without a test harness: define the minimal reproduction, input/output sample, page path, screenshot check, or manual verification checklist first.
- For pure copy, comment, or no-behavior edits, TDD may be skipped, but completion verification still applies and the reason must be stated.

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
- Verification evidence:
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

Non-integration branches must not write unmerged results directly into the current-state section of `说明文档.md`; record public entry changes as a public-doc update patch.
