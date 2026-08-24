---
name: company-skill-evolution-lab
description: Use when company workflow skills repeatedly misfire, feel too heavy or too weak, miss expert routing, or need controlled self-improvement proposals.
---

# Company Skill Evolution Lab

## Purpose

Bring self-improvement into the workflow without allowing skills to rewrite themselves unchecked.

## Principle

Self-improvement produces proposals first. Formal skills change only after review, security checks, and regression cases.

## Triggers

- Same skill misfires in the same way three times.
- Users repeatedly say the workflow is too heavy, too light, or missing a step.
- Expert routing fails or selects the wrong expert.
- Framework/API changes make guidance stale.
- A recurring manual workaround should become workflow knowledge.

## Workflow

1. Capture the friction or failure with concrete examples.
2. Identify whether the issue is trigger text, workflow body, expert routing, template shape, or missing dependency.
3. If the issue is expert selection, first propose a `BUNDLES.md` or `company-expert-routing` change before changing workflow skills.
4. Draft an improvement proposal, not a direct production edit.
5. Explain from first principles why the old rule failed: trigger condition, phase boundary, context assumption, or verification anchor.
6. Add or update a regression case that would catch the old failure, and run adversarial review to ensure the new rule will not over-trigger.
7. Run `company-skill-security-review` if the proposal changes permissions, tools, external skills, scripts, or expert dependencies.
8. Recommend accept, revise, or reject.


## Human-First Output

Start the final reply with `One-sentence conclusion`, `What was completed`, `What needs attention`, and `What the user should do now`. Use business outcomes and user impact, give one primary next action, and explain internal terms on first use. Then place Superpowers, expert calls, commands, paths, hashes, verification evidence, and internal workflow fields in a `Technical Audit Appendix`; Do not dump internal workflow fields one by one into the human summary or use audit fields as a substitute for it.


### Response Contract Gate

- Trigger this gate for formal completion or phase closeout, an explicit user request for a progress summary, blocker conclusion, or next-step proposal, plus any substantial reply containing audit fields.
- One- or two-sentence working updates and ordinary Q&A never trigger the fixed format, even when they mention the current result, risk, or next step; do not attach full audit details to a lightweight reply.
- When the user asks for more detail, expand only the four sections or the `Technical Audit Appendix`; must not remove, rename, or reorder the four headings.
- Audit fields may appear only in the `Technical Audit Appendix`; they must not sit beside or before the four-section human summary.
- Before sending, check that the four headings are present in order, risks are translated into practical impact, and only one primary next action is given. If any check fails, rewrite it before sending.

## Proposal Output

- Workflow layer: `company-skill-evolution-lab`
- Trace mode:
- Superpowers layer: `superpowers:brainstorming` for comparing improvement paths; `superpowers:verification-before-completion` before accepting the proposal.
- Actual calls:
- Expert/plugin capabilities:
- Not called, lens only:
- First Principles Check:
- Adversarial Review:
- Execution strategy: proposal only; do not directly edit production skills.
- Verification evidence:
- Unverified items:
- Remaining risk:
- Skill affected:
- Failure pattern:
- Evidence:
- Proposed change:
- Regression case:
- Security impact:
- Rollback:
