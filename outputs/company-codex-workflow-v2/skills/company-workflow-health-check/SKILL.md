---
name: company-workflow-health-check
description: Use when a company project needs to diagnose workflow installation health, project bootstrap completeness, template freshness, plugin exposure, or why company workflow skills and templates are not working as expected.
---

# Company Workflow Health Check

## Purpose

Diagnose whether a company project is correctly connected to the Codex workflow in read-only mode. This is especially useful for legacy projects, partially bootstrapped projects, missing templates, plugin upgrades that were not synced into the project, or cases where users say the workflow is installed but does not behave correctly.

## Difference From Nearby Skills

- `company-workflow-help` decides which workflow to enter.
- `company-expert-readiness` checks whether expert skills are installed, reviewed, exposed, and callable.
- `company-workflow-health-check` checks project-level workflow health: root files, templates, index, stale rules, version drift, diagnostic evidence, and repair commands.

## Workflow

1. Inspect the project root in read-only mode. Do not modify business code or project documents.
2. Check root files: `AGENTS.md`, `BUNDLES.md`, `EXPERTS.lock.md`.
3. Check index and templates: `specs/global/INDEX.md`, `specs/global/assets/`.
4. Check required templates: requirements, business-rules, design, api-contract, tasks, spike, hotfix, change-request, public-doc-update, skill-upgrade, workflow-health-report.
5. Check for current rule markers: visible Superpowers layer, first-principles check, adversarial review, business rules and calculation semantics, solution comparison, multi-branch public document protocol, validation level, documentation drift.
6. Check for stale legacy rules or old-source residue. Mark them as migration risk; do not delete them automatically.
7. Check current branch and public-document boundaries. Legacy projects on feature/spike/hotfix branches should not directly rewrite public entry documents.
8. If templates or rules are missing, provide safe repair commands. Prefer `update-templates` by default; do not overwrite user documents directly.

## Health Levels

- `green`: core files, index, templates, and current rules are present; workflow can be used normally.
- `yellow`: usable, but templates, stale rules, version drift, or public-document boundaries need attention before complex delivery.
- `red`: any critical entry is missing: `AGENTS.md`, `BUNDLES.md`, `EXPERTS.lock.md`, or `specs/global/INDEX.md`; complex work should not continue.

## Repair Guidance

- Missing templates only: recommend `bash scripts/install.sh update-templates <project-path> --lang en`.
- Missing project workflow entry files: recommend `bash scripts/install.sh bootstrap-project <project-path> --lang en`.
- Plugin missing or skills not exposed: reinstall the plugin, then restart Codex.
- Legacy rule residue: generate a migration checklist and ask the user to confirm before editing; do not delete automatically.

## Output

- Workflow layer: `company-workflow-health-check`
- Trace mode: `full-audit`
- Superpowers layer: usually none; use `superpowers:brainstorming` only when designing a repair plan
- Actual calls:
- Expert/plugin capabilities:
- Not called, lens only:
- First Principles Check: minimum conditions for workflow usability
- Adversarial Review: legacy project, stale rules, partial bootstrap, parallel branches, plugin refresh failure
- Health level: green / yellow / red
- Checked files:
- Missing items:
- Version or template drift:
- Public-document boundary:
- External expert status:
- Recommended repair commands:
- Do not auto-handle:
- Verification evidence:
- Unverified items:
- Next step:

## Boundaries

Do not repair a project during a health check unless the user explicitly asks to apply the recommended fixes.

Do not mark workflow health as green merely because the application can run; this skill diagnoses Codex workflow adoption, not runtime product health.
