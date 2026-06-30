# Project Context Index

Start here before using any company workflow.

## Project Snapshot

- Product:
- Current version:
- Current milestone:
- Primary stack:
- Package manager:
- Test command:
- Build command:
- Local run command:
- Progress document: `说明文档.md` or equivalent

## Routing

- Current feature specs:
- Current version directory:
- Current milestone directory:
- API contracts:
- Test locations:
- Main source entrypoints:

## Document Ownership Map

| Document | Role | Update trigger | Numbering namespace |
| --- | --- | --- | --- |
| `说明文档.md` or equivalent entry page | Project entry, current state, recent important events, reading route | Current phase, recent important event, reading route, or key status change | Do not use spike task IDs; use date-based project events or recent changes |
| `spike_*_工作日志.md` or spike-local log | Spike field log, experiment flow, temporary conclusions | Spike experiment, observation, decision, or temporary task change | `SPKxx-T001` or `Sxx-001` |
| `specs/versions/...` or `specs/features/...` | Formal requirements, design, task plan, acceptance basis | Requirements, design, tasks, acceptance criteria, or approved changes are confirmed | Feature, version, or formal task IDs |
| `docs/lifecycle/` | Lifecycle phase summaries and milestone retrospectives | Version phase completion, milestone change, or management-summary need | Date or version-phase IDs |
| `docs/public-doc-updates/` | Public document impact patches for parallel branches | A branch affects the entry page, current state, reading route, document ownership, or numbering rules before mainline merge | Branch name, feature ID, or PR ID |

## Multi-Branch Public Document Protocol

- Public documents represent mainline facts; feature, spike, and hotfix branches read `说明文档.md` and this index by default.
- Before a branch is merged, do not write branch-local progress as the project "current state".
- When a branch needs to change public entry or index content, write `docs/public-doc-updates/<branch-or-feature>.md` first.
- During integration, promote only merged facts into `说明文档.md` and this index.
- If multiple branches affect the same public section, rewrite that section once on the integration branch.

## Numbering Rules

- Documents at different levels must not share bare IDs such as `Task 001`.
- Spike-internal tasks use a spike namespace, for example `SPK02-T183`.
- Formal tasks use feature, version, or formal task IDs, for example `FEAT-DT-T01`.
- Project entry pages record "project events" or "recent changes"; they do not continue spike work-log IDs.
- If numbering conflicts appear, fix the document ownership map before writing more content.

## Workflow Documents

| Need | Template |
| --- | --- |
| Feature requirements | `specs/global/assets/requirements-template.md` |
| Technical design | `specs/global/assets/design-template.md` |
| API contract | `specs/global/assets/api-contract-template.md` |
| Task plan | `specs/global/assets/tasks-template.md` |
| Spike report | `specs/global/assets/spike-report-template.md` |
| Hotfix report | `specs/global/assets/hotfix-report-template.md` |
| Change request | `specs/global/assets/change-request-template.md` |
| Public doc update patch | `specs/global/assets/public-doc-update-template.md` |
| Skill upgrade report | `specs/global/assets/skill-upgrade-report-template.md` |

## Active Risks

- 
