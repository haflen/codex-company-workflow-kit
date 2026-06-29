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
