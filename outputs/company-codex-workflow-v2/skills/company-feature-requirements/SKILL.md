---
name: company-feature-requirements
description: Use when a company project needs feature requirements, acceptance criteria, scope clarification, or change-request requirements before technical design or implementation.
---

# Company Feature Requirements

## Document Ownership Check

Read the project policy at `specs/global/assets/document-ownership.md`; fall back to the bundled `../../specs/global/assets/document-ownership.md`. Before creating or updating phase documents, inherit confirmed ownership and choose record size. Continue the existing unaccepted task; small fixes do not automatically create root features or a full document package. Compact records do not remove necessary focused design or verification.

## Purpose

Provide a Codex-ready requirements workflow.

## Workflow

1. Establish context with `company-context-index`.
2. Clarify goal, users, in-scope behavior, out-of-scope behavior, dependencies, and risks.
3. Use `company-expert-routing` when the requirement is non-trivial; let it select the matching bundle automatically from `BUNDLES.md`.
4. Explicitly use `superpowers:brainstorming` when the idea has multiple plausible directions or the user is still exploring options.
5. Decide whether an independent business-rules document is needed. Create or update `business-rules.md` only when trigger conditions are met; do not force it on small requests.
6. For L2/L3 or complex business rules, add a first-principles check: core assumptions, non-negotiable constraints, and minimum conditions.
7. Write Given-When-Then acceptance criteria and include key counterexamples or abnormal scenarios.
8. When the user wants to validate pages, interactions, copy, or mock states during requirements, route to `company-requirements-prototype`. If prototype feedback changes requirements, update the authoritative requirements or `business-rules.md` before continuing the prototype.
9. Stop after requirements. Prototype confirmation authorizes only promotion to a requirements baseline; do not enter design or create tasks without an explicit design handoff.

## Superpowers Layer

- L0 lightweight exploration: use `superpowers:brainstorming` and return goals, options, risks, open questions, and next-step recommendations only.
- L2 standard requirements: use `superpowers:brainstorming` to clarify intent, compare paths, and converge acceptance criteria.
- If requirements are already clear, the skill may skip Superpowers but must state why.

## Artifact

When a requirements template is needed, resolve it in this order:

1. Project copy: `specs/global/assets/requirements-template.md`.
2. Plugin fallback: read `../../specs/global/assets/requirements-template.md` relative to this skill directory.

When a business-rules template is needed, resolve it in this order:

1. Project copy: `specs/global/assets/business-rules-template.md`.
2. Plugin fallback: read `../../specs/global/assets/business-rules-template.md` relative to this skill directory.

For small work, reuse the owning directory and existing record from the ownership check; do not default to a separate features path. If the user explicitly wants lightweight solution exploration, do not force a full requirements document; provide goals, options, risks, open questions, and next-step recommendations.

## Business Rules Document Triggers

If any of the following apply, the requirements stage must create or update `business-rules.md` and link it from the requirements document:

- Metrics, money, scores, ordering, weights, aggregation, conversion, prediction, allocation, or any formula.
- State machines, approval flows, task flows, role differences, permission rules, or operation branches.
- Field source, unit, precision, rounding, mapping, semantics, data dictionary, or cross-system data consistency.
- Missing data, abnormal values, boundary values, batch processing, duplicate submission, concurrent operations, or conflict handling.
- The user mentions formula, semantics, logic, rule, calculation, operation flow, state change, or metric explanation.

If none apply, output: `Business rules document: not needed, reason: ...`.

## Boundary

Requirements work must not modify production implementation code or prescribe low-level architecture. Only `company-requirements-prototype` may edit an isolated, mock-only prototype under `.codex-workflow/prototypes/<feature>/draft/`; production source remains forbidden.

## Target Client Gate

- UI, interaction, or client work first reads the target clients baseline in `specs/global/INDEX.md` and states whether the feature inherits or overrides it.
- Requirements name supported clients, shared page/code/API boundaries, minimum viewport, browser, input method, and whether responsive, touch, or mobile verification is required.
- An unconfirmed client is unsupported; the workflow must not add mobile adaptation on its own, including breakpoints, touch behavior, screenshots, or mobile E2E.
- Backend-only, task, or API work may state “no direct client difference” instead of manufacturing multi-client scope.

## Human-First Output

Read `../../specs/global/assets/human-output-standard.md` first and respect the project's agreed audience and delivery purpose. Keep a one-sentence conclusion and next-step recommendation; explain results, evidence, and impact in the user's language. Internal fields in the output/report sections below belong in existing execution records, not ordinary user replies or human documents.

### Response Contract Gate

Before sending, check factual scope, prerequisites, actor, authority, audience, and display against the shared policy. Ordinary Q&A has no fixed headings; requests for detail receive useful evidence. Rewrite any part that fails the reading check.
## Output

- Workflow layer: `company-feature-requirements`
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
- Requirements conclusion:
- Options:
- Risks and open questions:
- Core assumptions and counterexamples:
- Business rules document decision:
- Business rules document:
- Next step:

## Document Quality Gates

Before creating or substantially changing a formal document, read the project copy of `specs/global/assets/document-standard.md`; if absent, read the bundled `../../specs/global/assets/document-standard.md`. This skill enforces `DOC-G01`, `DOC-G02`, `DOC-G05`, `DOC-G06`, `DOC-G07`, `DOC-G08`, `DOC-G09`, `DOC-G10`, `DOC-G11`, and `DOC-G12`. Also apply `DOC-G04` when complex business rules are triggered.
