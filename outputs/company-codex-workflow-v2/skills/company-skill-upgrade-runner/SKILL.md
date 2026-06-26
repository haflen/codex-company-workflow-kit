---
name: company-skill-upgrade-runner
description: Use when a user wants to check, update, upgrade, replace, or install company workflow skills or expert skills from an external source.
---

# Company Skill Upgrade Runner

## Purpose

Provide a user-friendly upgrade workflow for external expert skills and internal workflow skills.

## User Triggers

Examples:

- "检查专家技能更新"
- "更新 `java-pro`"
- "把前端专家技能升级到最新稳定版"
- "从 antigravity-awesome-skills 同步这些专家"
- "对比新旧 skill 后让我确认是否覆盖"

## Workflow

1. Identify target skills, source repository or hub, current installed path, and expected destination.
2. Read `EXPERTS.lock.md` and `BUNDLES.md` to understand current pin, review status, and impacted bundles; prefer the project root, then plugin fallbacks `../../EXPERTS.lock.md` and `../../BUNDLES.md`.
3. Fetch or inspect the candidate version into a temporary review location. Do not overwrite current skills yet.
4. Compare old and new versions:
   - frontmatter name and description
   - trigger scope and likely overuse risk
   - workflow/body changes
   - scripts, tools, network access, shell commands, browser automation, filesystem writes
   - license, upstream source, pin, setup, and declared risk
5. Run `company-skill-security-review` on the candidate version.
6. Produce an upgrade report and recommendation.
7. Ask the user for explicit confirmation before replacing, installing, or deleting any production skill.
8. After approval, apply the update, update `EXPERTS.lock.md`, update `BUNDLES.md` only if bundle membership changed, and record rollback instructions.
9. Validate the plugin and run a trigger sanity check for the updated skill.

## Default Dry Run

Skill update requests are dry-run by default. Checking updates, fetching candidates into a temporary review location, comparing versions, and producing recommendations may happen without extra confirmation.

Overwriting, deleting, moving, or installing production skills requires explicit user confirmation after the upgrade report.

## Decision Rules

- If the candidate has broader triggers, scripts, shell commands, network access, credentials handling, or unclear license, recommend review or rejection.
- If the candidate only updates examples or narrow guidance, recommend pilot approval.
- If a skill is marked high or critical risk, require explicit user approval even for pilot use.
- If the update changes bundle membership, call out impacted workflows before asking for approval.
- If exact upstream commit or tag is unavailable, do not mark production-approved.

## User Confirmation Gate

Before applying changes, present:

- Workflow layer: `company-skill-upgrade-runner`
- Superpowers layer: `superpowers:verification-before-completion`
- Actual calls:
- Expert/plugin capabilities:
- Not called, lens only:
- Execution strategy: dry-run by default; overwrite only after explicit user confirmation.
- Verification evidence:
- Unverified items:
- Remaining risk:
- Skills to update:
- Source and candidate pin:
- Impacted bundles:
- Key differences:
- Security review result:
- Recommendation:
- Rollback path:
- Confirmation needed:

Do not overwrite production skills until the user clearly confirms.

Ambiguous phrases such as "looks good", "continue", "seems fine", or "anything else?" are not confirmation to overwrite.

## Upgrade Report

When a written artifact is useful, resolve the skill-upgrade report template in this order:

1. Project copy: `specs/global/assets/skill-upgrade-report-template.md`.
2. Plugin fallback: read `../../specs/global/assets/skill-upgrade-report-template.md` relative to this skill directory.

For small updates, a chat report is enough if it includes:

- Target:
- Current version:
- Candidate version:
- Diff summary:
- Risk:
- User decision:
- Files changed:
- Verification:
