---
name: company-context-index
description: Use when starting work in a company project, resuming an existing feature, or needing to update project context routing before requirements, design, implementation, bugfix, spike, or hotfix work.
---

# Company Context Index

## Document Ownership Check

Read the project policy at `specs/global/assets/document-ownership.md`; fall back to the bundled `../../specs/global/assets/document-ownership.md`. Establish the existing task, owner-path, record-path, and release-target; reuse its record and clarify only unresolved ownership.

## Purpose

Build enough project context without loading everything.

## Workflow

1. Read `specs/global/INDEX.md`.
2. Confirm whether `INDEX.md` contains a document ownership map: entry page, work log, formal specs, business rules and calculation semantics, lifecycle docs, public-doc update patches, numbering namespaces, and update triggers.
3. If present, read `说明文档.md` or the configured progress document.
4. Identify current version, milestone, feature, relevant docs, and commands.
5. Read `.codex-workflow/asset-boundaries.json`; record documentation, engineering, tooling/migration roots, confirmation status, and explicit exceptions, and check for `asset-boundaries.generated.json`. If config is missing, recommend `generate-asset-boundaries`; if a candidate exists, review and `accept-asset-boundaries` or explicitly discard it before inventing a new engineering root.
6. Read only the routed docs and source files needed for the task.
7. Determine whether the current branch is an integration branch; non-integration branches do not directly update mainline facts in `说明文档.md` or `specs/global/INDEX.md` by default.
8. If routing is stale, propose a concise index update; if bare task numbers are reused across document levels, flag a document ownership risk first.
9. If the branch affects the public entry, reading route, current phase, or document ownership, recommend `docs/public-doc-updates/<branch-or-feature>.md`.
10. Output the context summary, document to update, and next step.

## Target Client Check

- Generated or refreshed INDEX content includes a target clients baseline for PC Web, Mobile Web, apps, desktop clients, and large displays for user confirmation.
- Technical stack or existing CSS cannot prove product support. Keep inferred clients unconfirmed and unsupported; the workflow must not add mobile adaptation on its own.
- Record shared page/code/API boundaries, minimum viewport, browsers, and input methods. A non-UI project may state “no direct client difference.”


## Human-First Output

Read `../../specs/global/assets/human-output-standard.md` first and respect the project's agreed audience and delivery purpose. Keep a one-sentence conclusion and next-step recommendation; explain results, evidence, and impact in the user's language. Internal fields in the output/report sections below belong in existing execution records, not ordinary user replies or human documents.

### Response Contract Gate

Before sending, check factual scope, prerequisites, actor, authority, audience, and display against the shared policy. Ordinary Q&A has no fixed headings; requests for detail receive useful evidence. Rewrite any part that fails the reading check.
## Output

- Workflow layer: `company-context-index`
- Trace mode:
- Superpowers layer: none; context indexing only routes and minimizes context. For migration strategy discussion, route to `company-legacy-project-onboarding` with `superpowers:brainstorming`.
- Actual calls:
- Expert/plugin capabilities:
- Not called, lens only:
- First Principles Check:
- Adversarial Review:
- Execution strategy: read on demand; do not scan everything.
- Verification evidence:
- Unverified items:
- Remaining risk:
- Current task:
- Current version/milestone:
- Document ownership map:
- Current branch public-doc strategy:
- Public-doc update patch:
- Business rules and calculation semantics:
- Numbering namespaces:
- Relevant docs:
- Relevant code paths:
- Verification commands:
- Asset boundary status: missing / generated review required / confirmed
- Documentation roots, engineering roots, and explicit exceptions:
- Missing context:
- Recommended document to update:

## Guardrails

- Do not edit implementation code during context indexing.
- Do not read every spec by default.
- Do not block trivial tasks on missing company process documents; state the gap and continue if safe.
- Do not treat `说明文档.md`, spike work logs, and formal specs as one continuous task chain.
- Non-integration branches must not write branch-local status as mainline current state in public documents; use a public-doc update patch instead.

## Document Quality Gates

Before creating or substantially changing a formal document, read the project copy of `specs/global/assets/document-standard.md`; if absent, read the bundled `../../specs/global/assets/document-standard.md`. This skill enforces `DOC-G01`, `DOC-G04`, `DOC-G05`, `DOC-G06`, `DOC-G07`, `DOC-G08`, `DOC-G09`, `DOC-G10`, `DOC-G11`, and `DOC-G12`.
