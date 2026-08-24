---
name: company-feature-design
description: Use when company feature requirements are confirmed and a technical design, architecture decision, API contract, data flow, or test strategy is needed before task planning.
---

# Company Feature Design

## Purpose

Provide a Codex-ready design workflow.

## Workflow

1. Confirm requirements exist, include acceptance criteria, and the user explicitly authorized technical design. A requirements prototype or its confirmed status is not design authorization.
2. Read routed project context, existing patterns, and relevant source files; if requirements say `business-rules.md` is needed, read business rules and calculation semantics first.
3. When adding directories, packages, schemas, fixtures, tests, scripts, migrations, or cross-module assets, read `.codex-workflow/asset-boundaries.json`, inspect real manifests plus build/test entry points, and report artifact type, owning project, complete repository-relative path, executor/validator, and placement evidence.
4. Do not confirm design while ownership is unproven or a planned path fails the gate; fix ownership or declare an explicit exception with an owner and validator.
5. Run a solution-comparison level decision: L1 small changes may skip comparison with a reason; L2/L3 work that hits trigger conditions must compare 2-3 options.
6. When solution comparison is required, explicitly use `superpowers:brainstorming` and output the recommended option, alternatives, tradeoffs, and user-confirmation point.
7. Use `company-expert-routing` for non-trivial architecture, framework, data, UI, or testing decisions; let it choose the stack bundle automatically.
8. For non-trivial architecture, data, permission, performance, security, external API, frontend rendering, or cross-service boundaries, run a first-principles check.
9. Do not reinvent business formulas in design; map operation logic, state transitions, field semantics, and calculation formulas from `business-rules.md` into modules, APIs, data structures, and tests.
10. Produce design, contracts, risk notes, counterexample scenarios, and test strategy.
11. For frontend/backend or service boundaries, create an API contract before task planning.
12. If this design comes from a scope change discovered during implementation, mark `Implementation authorization: expired; user confirmation required before coding`, and state that the old task authorization does not cover the new scope.
13. If L2/L3 solution comparison was triggered, get user confirmation on the recommended option before task planning.
14. Stop after design unless the user gives the task-planning handoff signal.

## Superpowers Layer

- Default: use `superpowers:brainstorming` when multiple design paths exist or L2/L3 solution-comparison triggers are hit.
- High-risk design: use `company-expert-routing`, then use brainstorming to converge the design when useful.
- If the design is obvious and low-risk, the skill may skip Superpowers but must state why.

## Solution Comparison Triggers

If any of the following apply, compare options and get user confirmation on the recommended option before task planning:

- A large feature module, core page, core workflow, or subsystem is being added.
- Work crosses frontend/backend boundaries, service boundaries, data models, permissions, security, performance, cache, concurrency, or external APIs.
- Work involves `business-rules.md`, calculation semantics, state machines, approval flows, task flows, or complex data mapping.
- There is an obvious tradeoff between fast delivery and long-term maintainability.
- The solution affects extensibility, migration cost, testing strategy, rollout/recovery, or team ownership boundaries.
- The user mentions large module, architecture, solution, technical direction, whether to do it this way, or asks for comparison.

If none apply, the skill may skip comparison but must state: `Solution comparison: skipped, reason: L1 small change, single obvious technical path, low risk.`

## Artifact

When templates are needed, resolve them in this order:

1. Project copy: `specs/global/assets/design-template.md`; use `specs/global/assets/api-contract-template.md` when work crosses boundaries.
2. Plugin fallback: read `../../specs/global/assets/design-template.md` or `../../specs/global/assets/api-contract-template.md` relative to this skill directory.

If requirements link `business-rules.md`, the design artifact must list it under used context and state where each critical rule is implemented or verified.

`specs/` and `docs/` are documentation-only by default. Anything built, executed, tested, or released belongs to its owning engineering project; a machine-contract exception must explicitly declare its owner and validator in `asset-boundaries.json`.

## Boundary

Design work must not edit implementation code.

If the user confirmed only a requirements prototype, stop and route to `company-requirements-prototype` to complete its baseline; do not infer design or task-planning authorization.

Design work after a scope change must not flow directly back into implementation. It must go through task planning and wait for user confirmation of the new scope.

## Target Client Gate

- Read confirmed target clients, sharing boundaries, viewports, browsers, and input methods from requirements. Generic frontend best practices do not create new product promises.
- Unconfirmed clients do not enter architecture, components, responsive, touch, compatibility, or test design; the workflow must not add mobile adaptation on its own.
- If client scope is unclear or design introduces a new client, stop and return to `company-feature-requirements`.

## Human-First Output

Put the human summary before the Technical Audit Appendix:

1. One-sentence conclusion: state the recommended design and problem solved.
2. What was completed: describe key decisions and their effect.
3. What needs attention: explain tradeoffs, risks, and confirmation points plainly.
4. What the user should do now: give one primary next action and one short reply phrase.

Then use `Technical Audit Appendix` for the internal fields below. Explain acronyms and levels on first use. Do not dump internal workflow fields one by one into the human summary.


### Response Contract Gate

- Trigger this gate for formal completion or phase closeout, an explicit user request for a progress summary, blocker conclusion, or next-step proposal, plus any substantial reply containing audit fields.
- One- or two-sentence working updates and ordinary Q&A never trigger the fixed format, even when they mention the current result, risk, or next step; do not attach full audit details to a lightweight reply.
- When the user asks for more detail, expand only the four sections or the `Technical Audit Appendix`; must not remove, rename, or reorder the four headings.
- Audit fields may appear only in the `Technical Audit Appendix`; they must not sit beside or before the four-section human summary.
- Before sending, check that the four headings are present in order, risks are translated into practical impact, and only one primary next action is given. If any check fails, rewrite it before sending.

## Output

- Workflow layer: `company-feature-design`
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
- Recommended design:
- Implementation authorization:
- Solution comparison decision:
- Alternatives and trade-offs:
- User confirmation point:
- Business rules mapping:
- Underlying facts and minimum conditions:
- Key counterexample scenarios:
- Risks:
- Test strategy:
- Asset ownership table and placement gate:
- Next step: L2/L3 work can enter `company-feature-planning` only after the recommended option is confirmed.

## Document Quality Gates

Before creating or substantially changing a formal document, read the project copy of `specs/global/assets/document-standard.md`; if absent, read the bundled `../../specs/global/assets/document-standard.md`. This skill enforces `DOC-G01`, `DOC-G03`, `DOC-G05`, `DOC-G06`, `DOC-G07`, `DOC-G08`, `DOC-G09`, `DOC-G10`, `DOC-G11`, and `DOC-G12`. Also apply `DOC-G04` for data models, APIs, or complex rules.
