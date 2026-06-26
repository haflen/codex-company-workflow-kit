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
3. Explicitly use `superpowers:brainstorming` when design direction is not obvious or trade-offs need comparison.
4. Use `company-expert-routing` for non-trivial architecture, framework, data, UI, or testing decisions; let it choose the stack bundle automatically.
5. Produce design, contracts, risk notes, and test strategy.
6. For frontend/backend or service boundaries, create an API contract before task planning.
7. Stop after design unless the user gives the task-planning handoff signal.

## Superpowers Layer

- Default: use `superpowers:brainstorming` when multiple design paths exist.
- High-risk design: use `company-expert-routing`, then use brainstorming to converge the design when useful.
- If the design is obvious and low-risk, the skill may skip Superpowers but must state why.

## Artifact

When templates are needed, resolve them in this order:

1. Project copy: `specs/global/assets/design-template.md`; use `specs/global/assets/api-contract-template.md` when work crosses boundaries.
2. Plugin fallback: read `../../specs/global/assets/design-template.md` or `../../specs/global/assets/api-contract-template.md` relative to this skill directory.

## Boundary

Design work must not edit implementation code.

## Output

- Workflow layer: `company-feature-design`
- Trace mode:
- Superpowers layer:
- Actual calls:
- Expert/plugin capabilities:
- Not called, lens only:
- Execution strategy:
- Verification evidence:
- Unverified items:
- Remaining risk:
- Recommended design:
- Alternatives and trade-offs:
- Risks:
- Test strategy:
- Next step:
