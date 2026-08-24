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


## Human-First Output

Start the final reply with `One-sentence conclusion`, `What was completed`, `What needs attention`, and `What the user should do now`. Use business outcomes and user impact, give one primary next action, and explain internal terms on first use. Then place Superpowers, expert calls, commands, paths, hashes, verification evidence, and internal workflow fields in a `Technical Audit Appendix`; Do not dump internal workflow fields one by one into the human summary or use audit fields as a substitute for it.


### Response Contract Gate

- Trigger this gate for formal completion or phase closeout, an explicit user request for a progress summary, blocker conclusion, or next-step proposal, plus any substantial reply containing audit fields.
- One- or two-sentence working updates and ordinary Q&A never trigger the fixed format, even when they mention the current result, risk, or next step; do not attach full audit details to a lightweight reply.
- When the user asks for more detail, expand only the four sections or the `Technical Audit Appendix`; must not remove, rename, or reorder the four headings.
- Audit fields may appear only in the `Technical Audit Appendix`; they must not sit beside or before the four-section human summary.
- Before sending, check that the four headings are present in order, risks are translated into practical impact, and only one primary next action is given. If any check fails, rewrite it before sending.

## Output

- Workflow layer: `company-expert-readiness`
- Trace mode:
- Superpowers layer: none; this is installation and dependency diagnosis.
- Actual calls:
- Expert/plugin capabilities:
- Not called, lens only:
- First Principles Check:
- Adversarial Review:
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
