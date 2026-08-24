---
name: company-skill-security-review
description: Use when reviewing third-party, open-source, hub-downloaded, or self-improved skills before they are trusted by company workflows.
---

# Company Skill Security Review

## Purpose

Prevent malicious, overbroad, or unsafe skills from entering company workflows.

## Review Checklist

- Source and maintainer are identified.
- License is acceptable for company use.
- Current version and candidate version are identified.
- Old and new frontmatter are compared.
- Trigger scope did not become broader without a reason.
- Skill does not ask for secrets, tokens, cookies, SSH keys, or credentials.
- Skill does not hide network exfiltration, shell execution, or filesystem writes.
- Any scripts are inspected before use.
- Trigger description is narrow enough to avoid accidental overuse.
- Skill does not override user, company, sandbox, or security instructions.
- Skill does not instruct the agent to ignore verification, approvals, or review.
- External docs or APIs are current enough for the intended use.
- Adversarial review covers misfires, permission expansion, hidden tool calls, context growth, and rollback failure.

## Risk Rating

- Low: documentation-only, no scripts, narrow trigger.
- Medium: includes tool workflows or broad expert guidance.
- High: includes scripts, network access, shell commands, credentials, browser automation, or broad authority.


## Human-First Output

Start the final reply with `One-sentence conclusion`, `What was completed`, `What needs attention`, and `What the user should do now`. Use business outcomes and user impact, give one primary next action, and explain internal terms on first use. Then place Superpowers, expert calls, commands, paths, hashes, verification evidence, and internal workflow fields in a `Technical Audit Appendix`; Do not dump internal workflow fields one by one into the human summary or use audit fields as a substitute for it.


### Response Contract Gate

- Trigger this gate for formal completion or phase closeout, an explicit user request for a progress summary, blocker conclusion, or next-step proposal, plus any substantial reply containing audit fields.
- One- or two-sentence working updates and ordinary Q&A never trigger the fixed format, even when they mention the current result, risk, or next step; do not attach full audit details to a lightweight reply.
- When the user asks for more detail, expand only the four sections or the `Technical Audit Appendix`; must not remove, rename, or reorder the four headings.
- Audit fields may appear only in the `Technical Audit Appendix`; they must not sit beside or before the four-section human summary.
- Before sending, check that the four headings are present in order, risks are translated into practical impact, and only one primary next action is given. If any check fails, rewrite it before sending.

## Output

- Workflow layer: `company-skill-security-review`
- Trace mode:
- Superpowers layer: `superpowers:verification-before-completion`
- Actual calls:
- Expert/plugin capabilities:
- Not called, lens only:
- First Principles Check:
- Adversarial Review:
- Execution strategy: evidence-based checklist review.
- Verification evidence:
- Unverified items:
- Remaining risk:
- Skill reviewed:
- Source:
- Current version:
- Candidate version:
- Version diff:
- Risk:
- Findings:
- Required changes:
- Approved for use: yes/no
- Expiry or next review date:
