---
name: company-expert-routing
description: Use when a company workflow needs to decide whether an expert skill, subagent review, official documentation, or current-agent expert lens should be used.
---

# Company Expert Routing

## Purpose

Centralize bundle and expert selection so workflow skills do not duplicate and drift.

## Routing Method

1. Check whether the task is non-trivial enough to need a bundle or expert.
2. Read `BUNDLES.md` and select the smallest matching bundle from request, spec, file paths, and stack.
3. Check `EXPERTS.lock.md` for expected source, pin, status, and review notes before using external expert skills.
4. Within the selected bundle, use only the experts needed for the current phase.
5. If the expert is installed as a Codex skill, use it when its trigger matches.
6. If multi-agent support is available and the issue is complex, dispatch a focused expert review.
7. If no skill or subagent is available, apply the expert lens explicitly and state that no separate expert was available.
8. For fast-moving APIs, prefer current official docs or local package docs.

## File Lookup Order

Prefer expert dependency files from the business project. If they are missing, use the plugin-bundled fallback instead of disabling expert routing.

1. Project root: `BUNDLES.md`, `EXPERTS.lock.md`.
2. Project specs directory: `specs/global/BUNDLES.md`, `specs/global/EXPERTS.lock.md`.
3. Plugin fallback: read `../../BUNDLES.md`, `../../EXPERTS.lock.md` relative to this skill directory.

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
| User unsure where to start, asks what to do next, or asks for a prompt phrase | `company-workflow-entry` |
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
| User needs workflow entry guidance or next-step routing | `company-workflow-help` |
| Existing project onboarding or project context draft review | `company-legacy-project-onboarding` |
| User-friendly skill update, comparison, security review, confirmation, and apply workflow | `company-skill-upgrade-runner` |
| Unclear root cause, flaky tests, regressions, hangs | `superpowers:systematic-debugging` |
| Non-trivial behavior implementation or bug-prone logic | `superpowers:test-driven-development` |

## Do Not Route

- Trivial copy, label, field, or single-line configuration changes.
- Tasks where the workflow already has enough local evidence.
- Expert use that would reopen confirmed requirements without a concrete inconsistency.

## Output

When routing matters, include:

- Workflow layer: `company-expert-routing`
- Superpowers layer:
- Execution strategy:
- Bundle selected:
- Expert used:
- Why:
- Source status from `EXPERTS.lock.md`:
- Result:
- Any official docs checked:
