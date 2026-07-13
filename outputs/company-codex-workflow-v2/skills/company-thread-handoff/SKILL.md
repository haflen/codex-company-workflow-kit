---
name: company-thread-handoff
description: Use when a company project's long conversation must hand an unfinished task to a new Codex conversation or another owner, or when a new conversation must verify and resume an existing handoff.
---

# Company Task Conversation Handoff

## Core Principle

Transfer the minimum state needed for the active task. Project facts override the old conversation; a handoff never grants implementation authorization.

## Modes

- Export when opening a new conversation, pausing, or transferring work.
- Resume when a handoff was pasted or `.codex/handoff/current.md` must be read.

## Select the Level

- `quick`: discussion only, with no code/config changes, phase transition, incomplete verification, or running service.
- `full`: code/config changes, dirty Git state, phase transition, scope change, missing verification, running services, or production, data, permission, security, monetary, calculation, architecture, performance, or cross-system risk.

## Export Workflow

1. Identify one active task. Mark side topics `out of current scope and unauthorized`.
2. Read only relevant Git state, files, authoritative documents, validation, and runtime state.
   - For `quick` without a concrete project path, do not inspect Git or files; use only supplied facts.
3. Separate verified facts, prior judgments, and unverified items. Do not invent interfaces, fields, criteria, or implementation choices.
   - List only immediate blockers under `Unverified`; do not expand a generic requirements checklist.
4. Recheck authorization; scope added later is unauthorized by default.
5. Select the level and output the handoff plus a startup prompt.
6. Write `.codex/handoff/current.md` only on explicit request.

## Resume Preflight

1. Require generated time, active task, current state, and next step.
2. Check path, branch, working tree, key files, unfinished work, authoritative documents, and authorization.
3. Verify high-risk claims and report matching, changed, and unverified items.
4. Continue after low risk, re-verify medium risk, and stop for confirmation after high risk.

High-risk differences include a branch mismatch, changed scope, expired authorization, concurrently changed key files, conflicting authoritative documents, or a request to code when phase or validation conditions are not met.

## Output Contract

Keep `quick` to 8-12 short lines. Use `none` or `not provided` for empty fields instead of explaining them.

- Workflow layer: `company-thread-handoff`
- Transparency mode: `light`
- Handoff mode: export / resume
- Handoff level: `quick`
- Generated at:
- Active task:
- Current state:
- Completed:
- Next step:
- Key files:
- Verified facts:
- Prior-conversation judgments:
- Unverified items:
- Side topics: out of current scope and unauthorized
- Fact verification: matching / changed / unverified
- New-conversation startup prompt:

The startup prompt is a short prefix only. Never duplicate the handoff inside it; the handoff appears once.

For `full`, also include:

- Project path and Git branch:
- Working-tree changes and concurrency risk:
- Current workflow, phase permission, and implementation authorization:
- Authoritative requirements, design, tasks, business rules, and public entry documents:
- Validation level, evidence, unverified work, and remaining risk:
- Running services, ports, browsers, and test processes:
- Documentation/implementation drift:
- Actual calls:
- Superpowers overlay:
- Expert/plugin capabilities:
- Lens-only capabilities:

## File and Authorization Boundaries

- Never write a file automatically. On explicit request, only overwrite `.codex/handoff/current.md`.
- Never create history files, modify `.gitignore`, archive into `docs/` or `specs/`, commit, create a Codex task, or message another task automatically.
- Do not replace `company-context-index`, formal requirements/design/task documents, or phase confirmation with a handoff.
- Never extend implementation authorization from the old scope to newly added scope.
