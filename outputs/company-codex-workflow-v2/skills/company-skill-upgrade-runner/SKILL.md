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
3. Derive an exact target list from lock/bundle data; inspect only external experts referenced by the company workflow, not the whole upstream skill catalog.
4. Prefer GitHub raw/API, sparse checkout, or single-file download into a temporary review location; expand the fetch only when manifest, directory, or license review requires it.
5. For each candidate skill, fetch `SKILL.md` plus only its own `references/`, `resources/`, `scripts/`, `LICENSE`, or other directly related support files.
6. Compare old and new versions:
   - frontmatter name and description
   - trigger scope and likely overuse risk
   - workflow/body changes
   - scripts, tools, network access, shell commands, browser automation, filesystem writes
   - license, upstream source, pin, setup, and declared risk
7. When adopting external skill content, preserve local Codex frontmatter by default, especially `name` and `description: Use when...`; write upstream risk, source, version, author, or category into `upstream_*` metadata.
8. Overwrite local `description` only when the user explicitly asks to reset trigger strategy and the trigger sanity check passes.
9. Run `company-skill-security-review` on the candidate version, including adversarial review for misfires, permission expansion, context growth, tool calls, script permission drift, generated artifact pollution, and rollback failure.
10. Produce an upgrade report and recommendation.
11. Ask the user for explicit confirmation before replacing, installing, or deleting any production skill.
12. After approval, apply the update, update `EXPERTS.lock.md`, update `BUNDLES.md` only if bundle membership changed, and record rollback instructions.
13. Validate the plugin and run a trigger sanity check for the updated skill.

## Sync Scope and Local Preservation

- Sync only external expert skills listed in `EXPERTS.lock.md` or explicitly named by the user.
- Do not clone or download thousands of upstream skills to update a small expert set; if full clone is slow or wasteful, switch to raw/API/sparse immediately.
- Do not update internal workflow skills unless the user explicitly asks for internal workflow upgrades.
- Do not overwrite local Codex trigger `description`, naming conventions, routing constraints, Superpowers layering, or company safety guardrails.
- External bodies, examples, references, resources, and scripts may be synced, but local frontmatter trigger semantics must stay intact.
- If upstream adds scripts, executable bits, network access, shell commands, browser automation, or credential handling, call it out separately and require runtime approval before script execution.
- Clean generated install/verification artifacts after validation, such as `EXPERT-READINESS.md` and `EXPERT-READINESS.json`; do not commit temporary reports as source.
- If raw download drops executable bits, restore the previous executable bit or explain why the script became a plain file.

## Default Dry Run

Skill update requests are dry-run by default. Checking updates, fetching candidates into a temporary review location, comparing versions, and producing recommendations may happen without extra confirmation.

Overwriting, deleting, moving, or installing production skills requires explicit user confirmation after the upgrade report.

## Decision Rules

- If the candidate has broader triggers, scripts, shell commands, network access, credentials handling, or unclear license, recommend review or rejection.
- If the candidate body is useful but would overwrite local trigger descriptions, reject direct overwrite and merge as "preserve local description + sync upstream body".
- If the candidate only updates examples or narrow guidance, recommend pilot approval.
- If a skill is marked high or critical risk, require explicit user approval even for pilot use.
- If the update changes bundle membership, call out impacted workflows before asking for approval.
- If exact upstream commit or tag is unavailable, do not mark production-approved.

## User Confirmation Gate

Before applying changes, present:

- Workflow layer: `company-skill-upgrade-runner`
- Trace mode:
- Superpowers layer: `superpowers:verification-before-completion`
- Actual calls:
- Expert/plugin capabilities:
- Not called, lens only:
- First Principles Check:
- Adversarial Review:
- Execution strategy: dry-run by default; overwrite only after explicit user confirmation.
- Verification evidence:
- Unverified items:
- Remaining risk:
- Skills to update:
- Source and candidate pin:
- Impacted bundles:
- Sync scope:
- Local preserved fields:
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
