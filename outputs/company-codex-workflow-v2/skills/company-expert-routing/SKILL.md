---
name: company-expert-routing
description: Use when a company workflow needs to decide whether an expert skill, subagent review, official documentation, or current-agent expert lens should be used.
---

# Company Expert Routing

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
7. If multi-agent support is available and the issue is complex, dispatch a focused expert review.
8. If an expert is bundled but not visible in the current session, record it under `Not called, lens only`, say that a new Codex thread is needed to refresh the skill list, and do not ask users to install experts one by one.
9. For fast-moving APIs, prefer current official docs or local package docs.

## Phase Permission

Expert routing is not implementation authorization. Every routing response must output `Phase permission`:

- `implementation allowed`: requirements, design, task plan, and current scope are confirmed, with no new scope change.
- `documentation only`: the user asks to update requirements, design, tasks, field mappings, business semantics, or public-doc impact, or the changed scope must be documented first.
- `design first`: a new architecture layer, data-preparation layer, API boundary, table, external system, performance/permission/data strategy, or technical tradeoff appears.
- `planning needed`: the design is confirmed but the new scope lacks tasks, verification anchors, and documentation-drift checks.
- `user confirmation required`: documentation creates a new contract, field mapping, task list, or changed scope; old implementation authorization cannot be reused.
- `route back to workflow help`: the user is only asking what to do next and no workflow is clear.

If phase permission is not `implementation allowed`, output `Implementation authorization: expired; user confirmation required before coding` or explain why no implementation authorization exists.

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

If `full-audit` is active, output the trigger reason and `Workflow Audit`.


## Human-First Output

Start the final reply with `One-sentence conclusion`, `What was completed`, `What needs attention`, and `What the user should do now`. Use business outcomes and user impact, give one primary next action, and explain internal terms on first use. Then place Superpowers, expert calls, commands, paths, hashes, verification evidence, and internal workflow fields in a `Technical Audit Appendix`; Do not dump internal workflow fields one by one into the human summary or use audit fields as a substitute for it.


### Response Contract Gate

- Trigger this gate for formal completion or phase closeout, an explicit user request for a progress summary, blocker conclusion, or next-step proposal, plus any substantial reply containing audit fields.
- One- or two-sentence working updates and ordinary Q&A never trigger the fixed format, even when they mention the current result, risk, or next step; do not attach full audit details to a lightweight reply.
- When the user asks for more detail, expand only the four sections or the `Technical Audit Appendix`; must not remove, rename, or reorder the four headings.
- Audit fields may appear only in the `Technical Audit Appendix`; they must not sit beside or before the four-section human summary.
- Before sending, check that the four headings are present in order, risks are translated into practical impact, and only one primary next action is given. If any check fails, rewrite it before sending.

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
