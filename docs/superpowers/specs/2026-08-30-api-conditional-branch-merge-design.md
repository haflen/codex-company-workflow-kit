# API Unavailable Conditional Branch Merge Design

## Decision

When a real API or integration environment is unavailable, Fixture or Mock evidence may prove a frontend candidate but cannot prove integrated acceptance. The workflow may merge that candidate into an ordinary business branch only after explicit user approval.

The governing distinction is:

> Conditional branch merge is an engineering integration decision, not a conditional quality pass.

## State Model

1. `FIXTURE_READY`: the frontend candidate passes its approved Fixture or Mock checks.
2. `API_PENDING`: the required real API integration or real-data browser acceptance is unavailable or incomplete.
3. `CONDITIONAL_MERGED`: the user explicitly approved merging the candidate into a named ordinary business branch while `API_PENDING` remains open.
4. `API_INTEGRATED`: the exact candidate has completed real API integration without Fixture or Mock fallback.
5. `QUALITY_PASS`: the exact integrated candidate passed required API, browser, business-semantic, data, permission, and other risk-based checks.
6. `DELIVERY_READY`: formal delivery closeout may proceed.

`CONDITIONAL_MERGED` does not change the quality result. When required real API evidence is missing, independent quality validation remains `blocked` and delivery remains incomplete.

## Conditional Merge Guardrails

Conditional merge is allowed only when all conditions hold:

- The user explicitly records approver, approval time, approved source candidate, target branch, scope, reason, expiry condition, and compensating API-integration task.
- The target is an ordinary business branch. `main`, `master`, `develop`, `integration`, `release`, protected branches, release tags, deployment, and production are excluded.
- API unavailability is an external dependency or environment limitation, not a known implementation defect disguised as an environment problem.
- Applicable local contract, unit, type, lint, build, Fixture-isolation, and browser checks pass.
- Production code cannot silently fall back to Fixture or Mock data.
- The original task stays open as `API_PENDING`; no workflow may report acceptance, delivery, release, or data correctness.
- API restoration triggers real integration and quality validation against the exact candidate or a newly fingerprinted candidate.

## Customer Communication Contract

Every conditional merge completion response and closeout report must put a plain-language warning before technical audit fields:

> 当前仅完成基于 Fixture 的前端开发，并经批准先合入 `<业务分支>`。由于 `<API/环境>` 不可用，尚未完成真实 API 联调和真实页面验收。本次合入不代表功能正式交付，也不能证明真实数据、图表或业务计算正确。API 恢复后必须完成 `<补偿任务>`，通过前状态保持“有条件合入 / 未交付”。

The English version carries the same meaning. The response must also provide exactly one primary next action.

## Workflow Ownership

- `company-implementation-runner`: separates Fixture candidate completion from real API integration completion.
- `company-quality-validation`: treats missing required real API evidence as `blocked`; it never converts conditional merge approval into `conditional-pass`.
- `company-delivery-closeout`: executes a narrowly authorized conditional merge into an ordinary business branch and reports that delivery remains incomplete.
- `company-workflow-help`: routes API-unavailable work to the conditional-merge decision or to waiting for integration.
- `AGENTS.md`: establishes the project-wide default.
- Task, quality-validation, and delivery-closeout templates persist the state and approval evidence.

## Non-Goals

- No new skill is introduced.
- Fixture use is not prohibited during frontend development.
- This design does not permit bypassing security, permission, data-integrity, money/metric, migration, rollback, recovery, or production gates.
- This design does not authorize force-push, history rewrite, deployment, or protected-branch integration.
