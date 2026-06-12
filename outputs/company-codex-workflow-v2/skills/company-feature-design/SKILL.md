---
name: company-feature-design
description: Use when company feature requirements are confirmed and a technical design, architecture decision, API contract, data flow, or test strategy is needed before task planning.
---

# Company Feature Design

## Purpose

Provide a Codex-ready design workflow.

## Workflow

1. Confirm requirements exist and include acceptance criteria.
2. Read routed project context, existing patterns, and relevant source files.
3. Use `company-expert-routing` for non-trivial architecture, framework, data, UI, or testing decisions; let it choose the stack bundle automatically.
4. Produce design, contracts, risk notes, and test strategy.
5. For frontend/backend or service boundaries, create an API contract before task planning.
6. Stop after design unless the user gives the task-planning handoff signal.

## Artifact

Use `design-template.md`; use `api-contract-template.md` when work crosses boundaries.

## Boundary

Design work must not edit implementation code.
