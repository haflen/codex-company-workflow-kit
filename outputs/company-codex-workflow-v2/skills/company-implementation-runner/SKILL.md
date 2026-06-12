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
3. Use `test-driven-development` for non-trivial behavior changes and bug-prone logic.
4. Use `company-expert-routing` when implementation depends on framework internals, typing, performance, concurrency, data modeling, or UI craft; keep the bundle from design unless the touched area changed.
5. Make scoped edits.
6. Use verification discipline before claiming completion.
7. Run verification and update the progress document when the company project uses one.

## Completion Report

- Task completed:
- Files changed:
- Verification:
- Progress document update:
- Residual risk:

## Boundary

Do not implement tasks that are not in the approved plan unless the user explicitly approves scope expansion.
