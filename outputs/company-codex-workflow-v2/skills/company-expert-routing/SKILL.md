---
name: company-expert-routing
description: Use when a company workflow needs to decide whether an expert skill, official documentation, or current-agent expert lens should be used.
---

# Company Expert Routing

Apply READ-01 in ../../specs/global/assets/task-execution-policy.md: read required sections and reuse unchanged rules. Single-point low-risk changes may finish after local verification here; formal delivery, packaging and independent acceptance retain their stages.

Expert skills in an ordinary workflow do not imply agent dispatch. Route explicit multi-agent delivery to the [dedicated agent entry](../company-agent-routing/SKILL.md) for roles, disclosure and continuation. This skill retains expert selection and dispatch safeguards. Preserve single-executor choices and quality gates.

For a task already dispatched by the agent entry, select current experts and checks only; do not route back or expand the agent team.

## DELEGATE-01: Review results and fall back to serial execution

Before dispatch, check effective authority, actual tools and independent scope; routing advice grants no permission. Without clear dispatch authority or capability, use serial execution for allowed work; do not install agents or create user chats. Adopt parallel work only when comparable samples preserve pass rate and show a real benefit after coordination overhead; no measured comparison means no speedup claim.

A narrow task packet records actual task_id, allowed paths, prohibited actions, acceptance, candidate_fingerprint, budget and output location. Before dispatch, include immutable field names, types and values (including closed status values), and the editable fields, body and file scope from the existing contract in the task packet itself, not only a coordinator scoring sheet. If a correction requires changing a fixed field, preserve it and report the concrete conflict instead of extending the contract. The main agent alone owns shared contracts, state and integration; read-only review writes no files by default. Reuse agreed limits and leave unknown budgets unknown. At a limit or cancellation, stop only the actual agents for this task, verify stopping and preserve usable work. Recover only affected failed work serially within scope; do not redispatch indefinitely.

Before adoption, verify result_id, actual candidate identity, changed paths and original check evidence. A DONE without evidence, stale candidate, out-of-scope action, unknown side effect or self-reported success is not completion; inspect actual results before acceptance or replay. Duplicate result_id must not cause repeated integration. Candidate drift requires checking affected evidence again. Synthetic replies test decisions only, not real dispatch, cancellation or parallel performance.

## Multi-agent delivery execution

When the user explicitly requests multi-agent delivery starting from business materials/requirements, implementation or independent review, read and execute the [complete procedure](references/multi-agent-delivery.md). Reuse actual authority and the current business workflow; add no approval phase, activation phrase or scheduler. DELEGATE-01 serial execution limits concurrent work based on measured benefit; an executor followed by a separate independent reviewer can run sequentially, without claiming speedup. Check native capabilities and explicitly supply role instructions; only actual calls and returned identities count as dispatch. Use section 1a to select existing phase workflows and necessary experts, preserving source meaning, requirement IDs, counterexamples and open issues. In existing inputs/results, retain exact skill paths/sections, actual read fingerprints and rule-to-artifact evidence; the main agent verifies tool traces or raw outputs and actual artifacts, not role names or self-report. An unavailable irreplaceable skill or required review remains unmet. Without tools, fall back to a single executor and do not claim independent review. Cancelling an agent does not prove its commands or services stopped; verify actual runtime identities and stop evidence before redispatch or dependency release.

## REVIEW-01: Blind-review inputs and evidence reuse

Only when the task explicitly requires blind review or withheld expected answers, inspect actual visible inputs before dispatch, including inherited conversation, historical summaries and injected memory; a new agent or no parent-history inheritance does not establish a clean context. Retain the input diagnostic and inspection result, and have the reviewer self-check at the start. If prior answers or scores are present, or input isolation cannot be established, do not count that attempt as blind; use a verified clean context within existing authority. Where supported, disable memory only for that invocation, without changing global settings or removing higher-priority safety rules; state limitations when verification is unavailable. Ordinary review does not require disabling memory. Keep answers and scoring with the coordinator, freeze the report before revealing answers, and add no agents or review rounds merely because of this rule.

Apply shared EVIDENCE-01 to verify existing raw logs against candidate/tool fingerprints, requirements, environment applicability, completeness and original outputs; reuse applicable evidence and recheck only missing, changed or contradictory portions. Retain necessary commands, cwd, actual start/end times, exit codes, stdout/stderr, key inputs/before-and-after states and provenance hashes. Reuse the host's existing tool trace for current access instead of building a temporary full file-access recorder. Use the verified historical-to-current path mapping; historical absolute paths are metadata, not permission to read outside scope. Preserve original timestamps and do not claim a fresh execution. A blind packet may include equally scoped unscored raw observations, but no prior conclusions, answers or scores. Old logs cannot replace required fresh external checks; insufficient evidence remains unverified. Record actual time, contamination aborts, sample reruns and capture/integrity-check reruns separately with their reasons; do not trade away evidence for speed or infer general savings from one comparison.

## Purpose

Centralize bundle and expert selection so workflow skills do not duplicate and drift.

## Difference From Workflow Help

- `company-workflow-help` decides which workflow the user should enter.
- `company-expert-routing` is used only after the workflow is clear, and chooses the smallest needed bundle, expert skill, Superpowers skill, MCP, browser capability, or official documentation source.
- If the user is only asking "what should I do next?", route back to `company-workflow-help`.
- If the task is already in requirements, design, planning, implementation, bugfix, hotfix, spike, or skill governance and contains a non-trivial decision, use this skill.

## Routing Method

1. First decide phase permission: implementation allowed, documentation only, design first, planning needed, user confirmation required, or route back to `company-workflow-help`.
2. Check whether the task is non-trivial enough to need a bundle or expert.
3. Read `BUNDLES.md` and select the smallest matching bundle from request, spec, file paths, and stack.
4. Check `EXPERTS.lock.md` and `.codex-workflow/EXPERT-READINESS.md`; required experts should be bundled with the company plugin.
5. Within the selected bundle, use only the experts needed for the current phase.
6. If the expert is exposed as a Codex skill in the current session, use it when its trigger matches.
7. If multi-agent support is available and the issue is complex, apply DELEGATE-01 to authority, scope and benefit before deciding whether to dispatch a focused review.
8. If an expert is bundled but not visible in the current session, record it under `Not called, lens only`, say that a new Codex thread is needed to refresh the skill list, and do not ask users to install experts one by one.
9. For fast-moving APIs, prefer current official docs or local package docs.

## Phase Permission

Expert routing is not implementation authorization. Every routing response must preserve `Phase permission` in the internal execution record:

- `implementation allowed`: requirements, design, task plan, and current scope are confirmed, with no new scope change.
- `documentation only`: the user asks to update requirements, design, tasks, field mappings, business semantics, or public-doc impact, or the changed scope must be documented first.
- `design first`: a new architecture layer, data-preparation layer, API boundary, table, external system, performance/permission/data strategy, or technical tradeoff appears.
- `planning needed`: the design is confirmed but the new scope lacks tasks, verification anchors, and documentation-drift checks.
- `user confirmation required`: a new business rule, material architectural choice, contract conflict or scope change is not covered by existing authority and sources; block only dependent actions. Documenting confirmed meaning or tasks does not itself invalidate authority.
- `route back to workflow help`: the user is only asking what to do next and no workflow is clear.

When implementation is not yet permitted, record the specific missing prerequisite or authority boundary; a requirements/design prerequisite does not automatically revoke end-to-end authority. Complete authorized phases under FLOW-01/02 and continue once prerequisites are satisfied. Ask only for actual missing decisions or permissions. Discussion-only and requirements-only requests stop at their agreed endpoint.

When the scope-change circuit breaker triggers, do not treat expert selection as coding permission. Experts may only help complete requirements, design, tasks, or confirmation points.

## File Lookup Order

Prefer expert dependency files from the business project. If they are missing, use the plugin-bundled fallback instead of disabling expert routing.

1. Project root: `BUNDLES.md`, `EXPERTS.lock.md`.
2. Project specs directory: `specs/global/BUNDLES.md`, `specs/global/EXPERTS.lock.md`.
3. Plugin fallback: read `../../BUNDLES.md`, `../../EXPERTS.lock.md`, and `../../EXPERT-READINESS.md` relative to this skill directory.

Only state that expert dependency files are unavailable when all three locations fail, then continue with the current agent's explicit expert lens.

## Automatic Bundle Selection

Workflow skills should call this routing skill without requiring the user to name experts. Use these defaults:

| Signal | Bundle |
| --- | --- |
| Generic product/process/QA feature | `company-core-delivery` |
| Chinese reports, weekly updates, proposals and review drafts or edits (excluding single-sentence polishing) | `company-document-writing` |
| Java, Spring, JVM, transactions, persistence | `company-backend-java` |
| Python service, automation, async job | `company-python-service` |
| Django, DRF, Celery, ORM-heavy work | `company-django-service` |
| React, Next, Vue, TypeScript UI, browser behavior | `company-frontend-delivery` |
| LLM, RAG, prompt, agent workflow, AI provider API | `company-ai-feature` |
| Urgent production issue or rollback-sensitive defect | `company-hotfix` |
| Feasibility experiment or unfamiliar technical choice | `company-spike` |
| Skill update, expert dependency update, self-improvement proposal | `company-skill-governance` |
| User unsure where to start, asks what to do next, asks for a prompt phrase, or needs expert readiness checking | `company-workflow-entry` |
| Existing project adoption, context index draft, or first workflow pilot | `company-legacy-onboarding` |

If more than one bundle matches, choose the one that owns the riskiest decision in the current phase. Add one secondary expert only if needed.

## Expert Map

| Trigger | Expert |
| --- | --- |
| Product scope, user stories, prioritization, AC quality | `product-manager` |
| Chinese reports, weekly updates, proposals and review drafts or edits (excluding single-sentence polishing) | `company-document-writing` |
| Business process, metrics, reporting, policy, approvals, state transitions | `business-analyst` |
| Vague idea with multiple viable directions | `superpowers:brainstorming` |
| LLM, RAG, prompt, agent workflow, AI safety, provider APIs | `ai-product` |
| Java/Spring backend, transactions, concurrency, JVM behavior | `java-pro` |
| Python runtime, async, tooling, FastAPI-style APIs | `python-pro` or `python-patterns` |
| Django, DRF, Celery, Channels, ORM behavior | `django-pro` |
| React, Next, Vue, frontend state, accessibility | `frontend-developer` |
| TypeScript types, module boundaries, monorepos | `typescript-expert` |
| Visual craft, design system, responsive or visual regression | `frontend-design` |
| Test strategy, QA gates, regression coverage | `testing-qa` |
| Browser automation or E2E validation | `webapp-testing` |
| Adversarial review, extreme input, abnormal states, or pre-release counterexample validation | `testing-qa`; add `webapp-testing` for browser-facing work |
| First-principles architecture reasoning, cross-boundary design, or root-cause fact chain | Current stack expert + `testing-qa` |
| User needs workflow entry guidance or next-step routing | `company-workflow-help` |
| User needs expert dependency install, review, or exposure status | `company-expert-readiness` |
| Existing project onboarding or project context draft review | `company-legacy-project-onboarding` |
| User-friendly skill update, comparison, security review, confirmation, and apply workflow | `company-skill-upgrade-runner` |
| Unclear root cause, flaky tests, regressions, hangs | `superpowers:systematic-debugging` |
| Non-trivial behavior implementation or bug-prone logic | `superpowers:test-driven-development` |

## Do Not Route

- Trivial copy, label, field, or single-line configuration changes.
- Tasks where the workflow already has enough local evidence.
- Expert use that would reopen confirmed requirements without a concrete inconsistency.
- Expert advice remains subordinate to the target clients confirmed in the INDEX and current requirements. Generic responsive, mobile, or device-coverage advice in upstream expert text is not a product requirement; the workflow must not add mobile adaptation on its own or execute related advice until confirmed.

## Trace-Level Decision

This skill must choose the trace level automatically:

- `light`: default mode when experts are actually callable, risk is low, and expert use is only auxiliary.
- `full-audit`: automatically enable when any of these is true:
  - Any expert, Superpowers skill, MCP, browser capability, or plugin capability is only listed as `Not called, lens only`.
  - `BUNDLES.md`, `EXPERTS.lock.md`, or `EXPERT-READINESS.md` is missing or has an abnormal source.
  - Security review, expert dependency update, skill upgrade, or self-improvement proposal is involved.
  - Official documentation cannot verify a fast-moving API.
  - First-principles check finds an unverified core assumption, or adversarial review finds an uncovered high-risk counterexample.
  - Production, data, permission, architecture, performance, or security risk is involved.
  - The user asks to audit, review the process, or confirm actual invocation.

If `full-audit` is active, preserve the trigger reason and `Workflow Audit` in the internal execution record; supply the audit only when explicitly requested.


## Human-First Output

Read `../../specs/global/assets/human-output-standard.md` first and respect the project's agreed audience and delivery purpose. Keep a one-sentence conclusion and next-step recommendation; explain results, evidence, and impact in the user's language. Internal fields in the output/report sections below belong in existing execution records, not ordinary user replies or human documents.

### Response Contract Gate

Before sending, check factual scope, prerequisites, actor, authority, audience, and display against the shared policy. Ordinary Q&A has no fixed headings; requests for detail receive useful evidence. Rewrite any part that fails the reading check.
## Output

When routing matters, include:

- Workflow layer: `company-expert-routing`
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
- Phase permission:
- Implementation authorization:
- Bundle selected:
- Expert used:
- Why:
- Source status from `EXPERTS.lock.md`:
- Readiness status from `EXPERT-READINESS.md`:
- Result:
- Any official docs checked:
- Workflow Audit (only in full-audit mode):

## Document Translation Route

Use `company-document-translation` / `professional-translation` for customer manuals, technical/business translation and bilingual review; ordinary short phrases need no workflow. When existing project BUNDLES/EXPERTS files lack this new entry, supplement from the bundled entry instead of treating absence as an unavailable skill or overwriting project customisations. Explicit project restrictions take precedence. This route handles documents and grants no code-change or publication authority.

## Report and review writing route

Use `company-document-writing` for Chinese reports, weekly updates, proposals and review drafts. Do not force the route for single-sentence edits. Use verified source facts; add `business-analyst` only for unresolved business meaning. If old project BUNDLES/EXPERTS omit this new entry, consult bundled entries while preserving explicit project restrictions and custom content. The executor completes internal editing without new approval tables or stage prompts. This route grants no business changes, sending or publishing permission.
