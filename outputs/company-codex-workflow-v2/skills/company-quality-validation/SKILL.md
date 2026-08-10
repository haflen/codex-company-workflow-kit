---
name: company-quality-validation
description: Use when company implementation is complete and integrated acceptance, regression, milestone, release, V3, cross-module, cross-system, or post-hotfix quality evidence may be required before delivery closeout.
---

# Company Quality Validation

## Purpose

Independently decide whether the completed candidate satisfies approved requirements and has delivery-ready evidence. This supplements TDD without duplicating development-time testing.

## Automatic Trigger Decision

The user does not choose the level. The workflow reports the decision and evidence.

| Situation | Independent quality validation |
| --- | --- |
| V0/V1 documentation, comments, or low-risk point changes | not triggered by default; proceed to closeout when implementation evidence is sufficient |
| Single-task V2 | not triggered by default, except for critical user journeys, real-browser behavior, API/database integration, or material regression risk |
| multi-task, cross-module, frontend/backend, API, or database V2 | required |
| milestone, release, or V3 delivery | mandatory |
| Ordinary bugfix | decide from regression impact |
| post-hotfix compensation | mandatory |

Skipping this independent stage never means skipping tests. The implementation or bugfix workflow still retains TDD, regression, and completion verification evidence.

## Persisted Report Contract

- Create a formal report only when validation is `required/mandatory`. When validation is not required, create no new document; the implementation or bugfix completion report retains the decision evidence.
- Name the report `quality-validation-report.md` and place it in the same directory as the authoritative task document. A project numbering prefix is allowed, but the filename must retain `quality-validation-report`, and the authoritative task document or current feature/version README records the actual path.
- Bind the report to the current candidate: record the current branch, `HEAD commit`, validated paths, `diff SHA-256`, and the path plus per-file SHA-256 for untracked files inside the validated scope.
- Compute `diff SHA-256` from `git diff --binary HEAD -- <validated paths>`. Fingerprint only behavior-relevant code, tests, configuration, migrations, and assets so later documentation-only reconciliation does not invalidate acceptance.

## Minimum Context

Read only the current acceptance scope:

1. Approved requirements, ACs, and any required `business-rules.md`.
2. Current design, API/data contracts, and task completion state.
3. Current branch, final candidate diff, test entrypoints, environment, and test-data notes.
4. Verification evidence and unverified items from implementation or bugfix completion.

Stop on conflicting entry, task, or acceptance sources. Return to requirements, design, or planning instead of selecting a convenient interpretation.

## Validation Flow

1. Output `Independent quality validation: not-required / required / mandatory` with the trigger evidence.
2. Build an `AC -> scenario -> evidence -> result` trace matrix. Coverage percentage does not replace AC traceability.
3. Select unit, integration, API, E2E, browser, permission, data, performance, or recovery checks by highest risk. Reuse fresh evidence and avoid indiscriminate reruns.
4. Use `testing-qa` by default. Add `e2e-testing-patterns` or `webapp-testing` for critical Web paths; use `company-expert-routing` only for complex domain risk.
5. **REQUIRED SUB-SKILL:** Use `superpowers:verification-before-completion`. Accept only fresh evidence from the current final candidate.
6. Perform adversarial review for relevant abnormal, boundary, permission, concurrency, data, performance, compatibility, or rendering scenarios.
7. Produce exactly one result: `pass / conditional-pass / blocked`.

## Result Routing

- `pass`: continue to `company-delivery-closeout`.
- `conditional-pass`: list gaps, impact, and expiry condition; record Accepted by, Accepted at, Accepted scope, Expiry condition, and compensating task, and require explicit user acceptance. Security, permission, data-integrity, money or metric-formula, migration, rollback, or recovery risks cannot receive conditional pass.
- `blocked`: route implementation defects to `company-bugfix-runner`, then rerun the same acceptance scope.
- Unclear requirements, business rules, or acceptance criteria enter `company-feature-requirements`.
- Unclear architecture, API, data, or technical design enters `company-feature-design`.
- Missing test assets or repair-task authorization enters `company-feature-planning`.

## Production-Code Boundary

This skill must not modify production code. It may write the acceptance report, run read-only checks, and execute approved tests. Missing automated coverage becomes an explicit test task; adding or changing test code returns to planning/implementation or bugfix for scope authorization.

## Report

Template lookup order:

1. Project `specs/global/assets/quality-validation-report-template.md`.
2. Plugin fallback `../../specs/global/assets/quality-validation-report-template.md`.

Completion output includes:

- Workflow layer: `company-quality-validation`
- Trace mode: `full-audit`
- Independent quality validation: not-required / required / mandatory
- Decision evidence:
- Acceptance scope and final candidate:
- Formal report path: not applicable / actual path in the same directory as the authoritative task document
- Current branch and HEAD commit:
- Validated paths, diff SHA-256, and untracked file hashes:
- Superpowers overlay:
- Actual calls:
- Expert/plugin capabilities:
- Not called, lens only:
- AC trace matrix:
- Validation environment and data:
- Verification evidence:
- Adversarial review:
- Validation result: pass / conditional-pass / blocked
- Defects and route:
- Unverified items:
- Remaining risk:
- Delivery closeout readiness: ready / not-ready
- Next step:
- Recommended user phrase:

## Document Quality Gates

Before creating or substantially changing a formal validation report, read the project `specs/global/assets/document-standard.md`; use the plugin fallback when absent. Check `DOC-G01`, `DOC-G04`, `DOC-G05`, `DOC-G06`, `DOC-G07`, `DOC-G08`, `DOC-G09`, `DOC-G10`, `DOC-G11`, and `DOC-G12`.
