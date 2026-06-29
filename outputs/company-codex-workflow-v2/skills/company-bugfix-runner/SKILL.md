---
name: company-bugfix-runner
description: Use when company code behavior differs from requirements, design, acceptance criteria, tests, or documented expectations.
---

# Company Bugfix Runner

## Purpose

Provide a Codex bugfix flow that distinguishes bugs from change requests.

## Workflow

1. Decide whether the issue is a bug or a requirement change.
2. If it is a change request, route to requirements/change planning.
3. Reproduce the issue or collect the strongest available evidence.
4. Explicitly use `superpowers:systematic-debugging`; reproduce or collect evidence before fixing.
5. Before claiming root cause, run a first-principles check: fact chain, minimum reproduction conditions, and the difference between surface symptoms and underlying cause.
6. Use `company-expert-routing` for non-trivial failures, unclear root cause, or stack-specific failure modes; let it select `company-hotfix` or the affected stack bundle automatically.
7. Make the minimal fix.
8. Add or identify regression verification, and run adversarial review for scenarios related to the defect.
9. Explicitly use `superpowers:verification-before-completion` before claiming completion.
10. Record root cause, fix, and verification.

## Superpowers Layer

- Default: `superpowers:systematic-debugging`.
- High-risk, regression, or hotfix work: also use `superpowers:verification-before-completion`.
- For obvious low-risk bugs, keep systematic debugging lightweight but still report reproduction/evidence, minimal fix, and regression verification.

## Artifact

For urgent production work, resolve the hotfix template in this order:

1. Project copy: `specs/global/assets/hotfix-report-template.md`.
2. Plugin fallback: read `../../specs/global/assets/hotfix-report-template.md` relative to this skill directory.

For ordinary bugs, update the feature notes or progress document.

## Boundary

Do not bundle new feature behavior into a bugfix.

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
- Verification evidence:
- Unverified items:
- Remaining risk:
- Reproduction or evidence:
- Fact chain and minimum reproduction conditions:
- Root cause:
- Minimal fix:
- Regression verification:
- Remaining risk:
