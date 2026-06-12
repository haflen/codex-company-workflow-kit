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
4. Use `writing-plans` style decomposition when the plan is complex enough to need a separate executable implementation plan.
5. Use `company-expert-routing` only if task boundaries are unclear, cross teams, or rely on complex stack details.
6. Stop after task planning unless the user gives the implementation handoff signal.

## Artifact

Use `tasks-template.md`.

## Good Tasks

- Small enough for one focused implementation pass.
- Have a concrete verification command or manual check.
- Avoid mixing unrelated refactors with feature delivery.
