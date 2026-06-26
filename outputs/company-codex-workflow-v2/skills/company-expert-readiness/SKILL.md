---
name: company-expert-readiness
description: Use when a company project needs to verify bundled expert skills, check whether external expert dependencies are installed and exposed, or explain expert readiness before workflow use.
---

# Company Expert Readiness

## Purpose

Ensure the company workflow works out of the box: required external experts must be bundled with the plugin, auto-reviewed, and reported during project bootstrap.

## Workflow

1. Read project-root `BUNDLES.md`, `EXPERTS.lock.md`, and `.codex-workflow/EXPERT-READINESS.md`.
2. If the report is missing, suggest `bash scripts/install.sh expert-preflight <project-path> --lang en`.
3. Check whether the current session exposes the expert skills required by the selected bundle.
4. If experts are installed with the plugin but hidden from the current session, tell the user to open a new Codex thread so the skill list refreshes.
5. If experts are missing, require `install-plugin --force` or `all <project-path> --force`.
6. Report available experts, hidden experts, missing experts, and next steps.

## Output

- Workflow layer: `company-expert-readiness`
- Trace mode:
- Superpowers layer: none; this is installation and dependency diagnosis.
- Actual calls:
- Expert/plugin capabilities:
- Not called, lens only:
- Execution strategy: check bundled experts first, then current-session exposure.
- Verification evidence:
- Unverified items:
- Remaining risk:
- Bundle:
- Installed and callable:
- Installed but not exposed in current session:
- Missing:
- Security review status:
- User next step:

## Guardrails

- Do not ask users to install required experts one by one.
- Do not treat the lock file alone as proof that a skill is callable in the current session.
- Do not silently update external hubs; updates must go through company skill maintenance and security review.
