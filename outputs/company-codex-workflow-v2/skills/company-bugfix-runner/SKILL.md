---
name: company-bugfix-runner
description: Use when company code behavior differs from requirements, design, acceptance criteria, tests, or documented expectations.
---

# Company Bugfix Runner

## Purpose

Provide a Codex bugfix flow that distinguishes bugs from change requests.

## Workflow

1. Decide whether the issue is a bug or a requirement change.
2. If it is a change request, route to requirements/change planning; if the root cause is missing business rules, formulas, semantics, or state transitions, complete `business-rules.md` before deciding whether code should change.
3. Run Phase Consistency Preflight: confirm that entry docs, index, current version/feature docs, and the bug's task context agree.
4. For production hotfix recovery, record preflight conflicts and continue with minimal service restoration if needed; for ordinary bugfix, pause and repair document routing before code changes.
5. Reproduce the issue or collect the strongest available evidence.
6. Explicitly use `superpowers:systematic-debugging`; reproduce or collect evidence before fixing.
7. Before claiming root cause, run a first-principles check: fact chain, minimum reproduction conditions, and the difference between surface symptoms and underlying cause.
8. Use `company-expert-routing` for non-trivial failures, unclear root cause, or stack-specific failure modes; let it select `company-hotfix` or the affected stack bundle automatically.
   - When a bugfix adds or moves files, read `.codex-workflow/asset-boundaries.json` and check planned paths before editing. Existing-file-only fixes that preserve ownership may report “not triggered.”
   - A blocked placement means the fix design or task boundary is wrong. Ordinary bugfix work stops; a production hotfix may perform only a minimal recovery that does not add another invalid placement and must record follow-up work.
9. Make the minimal fix.
10. Add or identify regression verification, and run adversarial review for scenarios related to the defect.
11. Check Chinese code logic comments: root-cause fixes, exceptional branches, compatibility strategy, business rules, and regression guards need useful comments.
12. Choose validation level `V1/V2/V3` automatically; use `V0` only for docs-only corrections.
13. Check documentation drift: whether the bug exposes gaps in requirements, business rules, design, API contracts, or task plans.
14. Explicitly use `superpowers:verification-before-completion` before claiming completion.
15. After the fix, decide independent quality validation automatically: ordinary bugs depend on regression impact; post-hotfix compensation is mandatory; bugs found by quality validation return to the original validation scope.
15. Record root cause, fix, and verification; if the fix affects public entry or current state, non-integration branches write a public-doc update patch.

## Superpowers Layer

- Default: `superpowers:systematic-debugging`.
- High-risk, regression, or hotfix work: also use `superpowers:verification-before-completion`.
- For obvious low-risk bugs, keep systematic debugging lightweight but still report reproduction/evidence, minimal fix, and regression verification.

## Validation Levels

- `V0`: docs-only corrections, test wording, or no-behavior typos.
- `V1`: isolated low-risk bug with a clear reproduction path and small impact.
- `V2`: default bugfix involving user-visible behavior, cross-file logic, APIs, state, or data.
- `V3`: production, permissions, security, money/metric calculations, data corruption, concurrency, performance, external APIs, or hotfix.

If the root cause is a missing rule or wrong documented promise, do not only fix code; output `Documentation drift impact` and route back to requirements or change request.

## Independent Quality Validation Loop

- `V1` ordinary bugfixes skip independent validation by default.
- `V2` enters `company-quality-validation` for critical user paths, cross-module behavior, API/database integration, or a material regression surface.
- `V3`, production hotfix compensation, data/permission/money/metric-formula/cross-system fixes require `company-quality-validation`.
- If `company-quality-validation` found the bug with a `blocked` result, re-run the original ACs, scenarios, and environment after the fix. A new unit test alone cannot close the finding.

## Chinese Code Logic Comments

Use the same Chinese-comment standard for Java, frontend TypeScript/Vue/React, Python, SQL, and scripts:

- When the root-cause fix changes business decisions, state transitions, field mapping, exceptional handling, compatibility strategy, or thresholds, explain the reason and protected scenario in Chinese.
- Do not write vague comments such as "fix bug" or "check null".
- If correct behavior cannot be derived from requirements, design, or `business-rules.md`, complete the rule first; do not use comments as a substitute for missing requirements.
- If regression coverage depends on special input, historical data, or edge conditions, explain the business meaning near the test or code.

## Phase Consistency Preflight

Before bugfix work, check the minimum context:

- Which feature, version, hotfix, or production incident owns this bug.
- Whether `说明文档.md` and `specs/global/INDEX.md` point to the correct current phase or entry.
- Whether the current task/version document explains expected behavior.
- Whether a related public-doc patch records branch impact on public entry docs.

For ordinary bugfixes, repair document routing before changing code when entry or index state is wrong. For production hotfixes, service recovery may proceed first, but the completion report must record preflight conflicts and follow-up documentation work.

## Artifact

For urgent production work, resolve the hotfix template in this order:

1. Project copy: `specs/global/assets/hotfix-report-template.md`.
2. Plugin fallback: read `../../specs/global/assets/hotfix-report-template.md` relative to this skill directory.

For ordinary bugs, update feature notes or branch-local progress documents. Non-integration branches must not directly edit public entry current-state sections; write `docs/public-doc-updates/<branch-or-feature>.md`.

## Boundary

Do not bundle new feature behavior into a bugfix.

Do not disguise "missing rule documentation" as a code bug. If correct behavior cannot be derived from requirements, design, or `business-rules.md`, complete the rule document or change request first.

## Output

- Workflow layer: `company-bugfix-runner`
- Trace mode:
- Superpowers layer:
- Actual calls:
- Expert/plugin capabilities:
- Not called, lens only:
- First Principles Check:
- Adversarial Review:
- Execution strategy:
- Phase Consistency Preflight:
- Asset placement gate: passed / blocked / not triggered
- Authoritative document for this turn:
- Validation level:
- Independent quality validation decision: not required / required / mandatory
- Validation loop: first acceptance / post-fix revalidation / hotfix compensation
- Quality validation report path: not applicable / `quality-validation-report.md` beside the authoritative task document / reuse the original blocked report
- Post-fix candidate awaiting validation: current branch, HEAD commit, validated paths
- Recommended next workflow: `company-quality-validation` / `company-delivery-closeout` / `company-feature-requirements` / `company-feature-design` / `company-feature-planning`
- Verification evidence:
- Code comment check:
- Comment coverage:
- Documentation drift impact:
- Unverified items:
- Remaining risk:

## Document Quality Gates

Before creating or substantially changing a formal document, read the project copy of `specs/global/assets/document-standard.md`; if absent, read the bundled `../../specs/global/assets/document-standard.md`. This skill enforces `DOC-G01`, `DOC-G04`, `DOC-G05`, `DOC-G06`, `DOC-G07`, `DOC-G08`, `DOC-G09`, `DOC-G10`, `DOC-G11`, and `DOC-G12`. Trigger these only when creating or substantially changing a formal hotfix or bugfix record.
- Reproduction or evidence:
- Fact chain and minimum reproduction conditions:
- Root cause:
- Minimal fix:
- Regression verification:
- Public-doc impact:
- Remaining risk:
