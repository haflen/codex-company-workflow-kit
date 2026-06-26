---
name: company-skill-maintenance
description: Use when updating, pinning, auditing, replacing, or reviewing open-source or internal expert skills used by the company workflow.
---

# Company Skill Maintenance

## Purpose

Treat expert skills like dependencies: pinned, reviewed, updated deliberately, and reversible.

## Workflow

1. For ordinary user-initiated updates, route to `company-skill-upgrade-runner`.
2. Read `EXPERTS.lock.md`.
3. Identify the skill to add, update, replace, or remove.
4. Check `BUNDLES.md` to understand which workflows depend on the skill.
5. Inspect source, license, pin, changed files, and risky instructions.
6. Run `company-skill-security-review` before adopting external changes.
7. Compare old and new trigger descriptions for drift.
8. Update `EXPERTS.lock.md` only after review.
9. Update `BUNDLES.md` only if bundle membership or default routing changes.
10. Record release notes and rollback instructions.

## Update Policy

- Company default: monthly review or immediate review after major framework/runtime upgrades.
- Security or supply-chain concern: review immediately.
- Do not auto-merge skill updates from external hubs.
- Do not introduce new external experts without a lock entry and review.

## Output

- Workflow layer: `company-skill-maintenance`
- Trace mode:
- Superpowers layer: `superpowers:verification-before-completion`
- Actual calls:
- Expert/plugin capabilities:
- Not called, lens only:
- Execution strategy: dependency review, version lock, reversible change.
- Verification evidence:
- Unverified items:
- Remaining risk:
- Skill:
- Source and pin:
- License:
- Diff summary:
- Security review:
- Compatibility notes:
- Recommendation:
- Rollback:
