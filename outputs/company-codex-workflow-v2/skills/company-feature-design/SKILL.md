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

When templates are needed, resolve them in this order:

1. Project copy: `specs/global/assets/design-template.md`; use `specs/global/assets/api-contract-template.md` when work crosses boundaries.
2. Plugin fallback: read `../../specs/global/assets/design-template.md` or `../../specs/global/assets/api-contract-template.md` relative to this skill directory.

## Boundary

Design work must not edit implementation code.
