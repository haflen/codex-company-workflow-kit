---
name: company-feature-planning
description: Use when company requirements and technical design are confirmed and the work needs an implementation task plan with verification points.
---

# Company Feature Planning

## Document Ownership Check

Read the project policy at `specs/global/assets/document-ownership.md`; fall back to the bundled `../../specs/global/assets/document-ownership.md`. Before creating or updating phase documents, inherit confirmed ownership and choose record size. Continue the existing unaccepted task; small fixes do not automatically create root features or a full document package. Compact records do not remove necessary focused design or verification.

## Purpose

Provide executable Codex task planning.

## Workflow

1. Confirm requirements and design are available; if requirements or design link `business-rules.md`, read it too.
2. If L2/L3 solution-comparison conditions were hit in design, confirm the user approved the recommended option; if not, stop and route back to `company-feature-design`.
3. Confirm API contracts exist when boundaries require them.
4. Split work into small tasks with verification and an estimated validation level for each task.
5. When a task adds or moves engineering assets, read `.codex-workflow/asset-boundaries.json`; record complete repository-relative paths plus allowed and forbidden roots, never ambiguous short paths such as `contracts/` or `scripts/`.
6. Run `.codex-workflow/bin/asset_boundaries.py check <project> --path <path>` on planned paths. Blocking issues must return to design, not become implementation-stage notes.
7. Explicitly use `superpowers:writing-plans` when the plan is complex enough to need a separate executable implementation plan.
8. Every non-trivial task must include a minimum failing case or verification anchor and at least one adversarial scenario.
9. If `business-rules.md` exists, convert its example cases, formulas, state transitions, and exception handling into task verification points; do not write only "implement per requirements".
10. Use `company-expert-routing` only if task boundaries are unclear, cross teams, or rely on complex stack details.
11. If merged work needs to update `说明文档.md`, `specs/global/INDEX.md`, or the reading route, add a public-doc update patch task instead of directly editing public docs on the business branch.
12. If a task may change requirements, business rules, technical design, API contracts, or project entry docs, add a documentation-drift check task.
13. If planning comes from a scope change discovered during implementation, state that old implementation authorization has expired and the new tasks require user reconfirmation.
14. Mark continuous implementation eligibility: which tasks can be batched and which tasks must stop for user confirmation.
15. Mark subagent split recommendations: which tasks should remain serial under the main agent, and which tasks are suitable for independent implementation, investigation, or review.
16. Estimate independent quality validation as `not required / required / mandatory`, recording trigger evidence, scope, critical ACs, environment/test data, and expected validation types. Implementation or bugfix makes the final decision after work completes and enters `company-quality-validation` when triggered.
17. Stop after task planning unless the user gives the implementation handoff signal.

## Superpowers Layer

- L1 small change: usually skip Superpowers and use a lightweight task card; if behavior changes, apply the minimal-failing-case idea from `superpowers:test-driven-development`.
- L2/L3 standard or complex work: use `superpowers:writing-plans`.
- Every task must include a verification anchor for later TDD and completion verification.
- Example cases from business-rules documents should become automated tests first; when automation is not practical, turn them into explicit manual checks.
- Estimate each task's validation level as `V0/V1/V2/V3`; implementation or bugfix confirms the final level before completion.
- Quality validation is only a planning estimate: multi-task/cross-module `V2`, milestone, release-candidate, `V3`, and post-hotfix compensation work normally requires it. A low-risk single-task `V2` requires it only for critical journeys, browser behavior, API/database integration, or a material regression surface.
- Mark a task as continuous-eligible only when boundaries, verification anchors, and stop conditions are clear.
- For L2/L3 multi-task plans, explicitly decide whether to recommend Codex subagents; if not, explain whether task coupling, file conflicts, or limited benefit makes subagents unnecessary. Actual invocation still requires an explicit user request.

## Artifact

When a task template is needed, resolve it in this order:

1. Project copy: `specs/global/assets/tasks-template.md`.
2. Plugin fallback: read `../../specs/global/assets/tasks-template.md` relative to this skill directory.

Resolve the public-doc update patch template in this order:

1. Project copy: `specs/global/assets/public-doc-update-template.md`.
2. Plugin fallback: read `../../specs/global/assets/public-doc-update-template.md` relative to this skill directory.

## Good Tasks

- Small enough for one focused implementation pass.
- Have a concrete verification command or manual check.
- Avoid mixing unrelated refactors with feature delivery.

## Continuous Implementation Eligibility

Task planning must help implementation decide whether batching is safe:

- `continuous`: `V0/V1` or tightly related `V2`; scope is clear, verification is explicit, and failure has limited blast radius.
- `careful-continuous`: `V2` across multiple files/pages/APIs but still inside one confirmed task chain; re-check every 1-3 tasks.
- `must-stop`: `V3`, production, permission, security, data migration, money/metric formulas, cross-system work, unconfirmed business rules, scope change, or user decision point.

Continuous tasks still require per-task verification. Do not skip TDD, documentation-drift checks, or completion verification because a batch is authorized.

## Subagent Split Strategy

Task planning must help implementation decide whether subagents are worth using:

- `not needed`: the task is small, has one boundary, touches concentrated shared files, and a main-agent serial pass is cheaper.
- `implementation subagent allowed`: the task has clear boundaries, clear input/output, few allowed files, explicit verification, and no shared write conflict with other tasks.
- `investigation subagent allowed`: multiple test failures, page issues, or module issues are independent enough to investigate by problem domain.
- `review subagent allowed`: L2/L3 work or continuous batches need separate spec-compliance, code-quality, test-coverage, or security-risk review.
- `parallel subagents forbidden`: tasks edit the same core file, shared state model, database migration, API contract, or public-doc section.
- `custom agents needed`: the plan recommends company reviewer/test/security/explorer roles, but the project has not generated `.codex/agents/`; recommend `bash scripts/install.sh install-agents <project-path> --lang en`.

For every task that recommends a subagent, write:

- Subagent role: implementation / investigation / spec review / code-quality review / test-strategy review.
- Input context: requirements, design, task ID, allowed files, prohibited actions.
- Expected output: change summary, verification evidence, risks, and blockers.
- Merge strategy: the main agent reviews diffs and verification instead of accepting the subagent's completion claim directly.

## Target Client Gate

- Every UI/client task cites confirmed target clients and verification viewports. Unconfirmed clients do not enter the task list.
- When mobile is not explicitly supported, the workflow must not add mobile adaptation on its own, including responsive, touch, screenshot, or mobile E2E tasks.
- If requirements and design disagree on target clients, stop planning and return to the conflicting document rather than choosing for the user.

## Human-First Output

Read `../../specs/global/assets/human-output-standard.md` first and respect the project's agreed audience and delivery purpose. Keep a one-sentence conclusion and next-step recommendation; explain results, evidence, and impact in the user's language. Internal fields in the output/report sections below belong in existing execution records, not ordinary user replies or human documents.

### Response Contract Gate

Before sending, check factual scope, prerequisites, actor, authority, audience, and display against the shared policy. Ordinary Q&A has no fixed headings; requests for detail receive useful evidence. Rewrite any part that fails the reading check.
## Output

- Workflow layer: `company-feature-planning`
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
- Tasks:
- Solution confirmation status:
- Minimal failing case or verification anchor per task:
- Estimated validation level per task:
- Independent quality validation estimate: not required / required / mandatory
- Validation trigger evidence, scope, and critical ACs:
- Validation environment, test data, and expected types:
- Continuous implementation eligibility per task:
- Must-stop tasks:
- Subagents recommendation: not needed / recommended / strongly recommended
- Subagent capability status: not checked / explicit user request needed / local custom agents needed / App activity display only
- Subagent strategy per task:
- Tasks forbidden from parallel or requiring main-agent serial execution:
- Subagent task packet draft:
- Adversarial scenario per task:
- Business rules verification coverage:
- Documentation-drift check task:
- Public-doc impact task:
- Asset placement gate: passed / blocked / not triggered
- Implementation handoff phrase:
- Implementation authorization:

## Document Quality Gates

Before creating or substantially changing a formal document, read the project copy of `specs/global/assets/document-standard.md`; if absent, read the bundled `../../specs/global/assets/document-standard.md`. This skill enforces `DOC-G01`, `DOC-G04`, `DOC-G05`, `DOC-G06`, `DOC-G07`, `DOC-G08`, `DOC-G09`, `DOC-G10`, `DOC-G11`, and `DOC-G12`.
