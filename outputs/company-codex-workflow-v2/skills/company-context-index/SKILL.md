---
name: company-context-index
description: Use when starting work in a company project, resuming an existing feature, or needing to update project context routing before requirements, design, implementation, bugfix, spike, or hotfix work.
---

# Company Context Index

## Purpose

Build enough project context without loading everything.

## Workflow

1. Read `specs/global/INDEX.md`.
2. Confirm whether `INDEX.md` contains a document ownership map: entry page, work log, formal specs, lifecycle docs, public-doc update patches, numbering namespaces, and update triggers.
3. If present, read `说明文档.md` or the configured progress document.
4. Identify current version, milestone, feature, relevant docs, and commands.
5. Read only the routed docs and source files needed for the task.
6. Determine whether the current branch is an integration branch; non-integration branches do not directly update mainline facts in `说明文档.md` or `specs/global/INDEX.md` by default.
7. If routing is stale, propose a concise index update; if bare task numbers are reused across document levels, flag a document ownership risk first.
8. If the branch affects the public entry, reading route, current phase, or document ownership, recommend `docs/public-doc-updates/<branch-or-feature>.md`.
9. Output the context summary, document to update, and next step.

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
- Numbering namespaces:
- Relevant docs:
- Relevant code paths:
- Verification commands:
- Missing context:
- Recommended document to update:

## Guardrails

- Do not edit implementation code during context indexing.
- Do not read every spec by default.
- Do not block trivial tasks on missing company process documents; state the gap and continue if safe.
- Do not treat `说明文档.md`, spike work logs, and formal specs as one continuous task chain.
- Non-integration branches must not write branch-local status as mainline current state in public documents; use a public-doc update patch instead.
