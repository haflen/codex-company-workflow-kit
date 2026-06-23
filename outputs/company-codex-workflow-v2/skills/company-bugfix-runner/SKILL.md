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
4. Use `systematic-debugging` when the root cause is unclear, flaky, repeated, or regression-prone.
5. Use `company-expert-routing` for non-trivial failures, unclear root cause, or stack-specific failure modes; let it select `company-hotfix` or the affected stack bundle automatically.
6. Make the minimal fix.
7. Add or identify regression verification.
8. Record root cause, fix, and verification.

## Artifact

For urgent production work, resolve the hotfix template in this order:

1. Project copy: `specs/global/assets/hotfix-report-template.md`.
2. Plugin fallback: read `../../specs/global/assets/hotfix-report-template.md` relative to this skill directory.

For ordinary bugs, update the feature notes or progress document.

## Boundary

Do not bundle new feature behavior into a bugfix.
