---
name: company-feature-planning
description: Use when company requirements and technical design are confirmed and the work needs an implementation task plan with verification points.
---

# Company Feature Planning

## Purpose

Provide executable Codex task planning.

## Workflow

1. Confirm requirements and design are available.
2. Confirm API contracts exist when boundaries require them.
3. Split work into small tasks with verification for each task.
4. Explicitly use `superpowers:writing-plans` when the plan is complex enough to need a separate executable implementation plan.
5. Use `company-expert-routing` only if task boundaries are unclear, cross teams, or rely on complex stack details.
6. Stop after task planning unless the user gives the implementation handoff signal.

## Superpowers Layer

- L1 small change: usually skip Superpowers and use a lightweight task card; if behavior changes, apply the minimal-failing-case idea from `superpowers:test-driven-development`.
- L2/L3 standard or complex work: use `superpowers:writing-plans`.
- Every task must include a verification anchor for later TDD and completion verification.

## Artifact

When a task template is needed, resolve it in this order:

1. Project copy: `specs/global/assets/tasks-template.md`.
2. Plugin fallback: read `../../specs/global/assets/tasks-template.md` relative to this skill directory.

## Good Tasks

- Small enough for one focused implementation pass.
- Have a concrete verification command or manual check.
- Avoid mixing unrelated refactors with feature delivery.

## Output

- Workflow layer: `company-feature-planning`
- Trace mode:
- Superpowers layer:
- Actual calls:
- Expert/plugin capabilities:
- Not called, lens only:
- Execution strategy:
- Verification evidence:
- Unverified items:
- Remaining risk:
- Tasks:
- Minimal failing case or verification anchor per task:
- Implementation handoff phrase:
