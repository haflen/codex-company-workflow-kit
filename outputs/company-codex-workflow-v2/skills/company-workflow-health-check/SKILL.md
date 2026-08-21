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
4. Check required templates: requirements, business-rules, design, api-contract, tasks, spike, hotfix, change-request, public-doc-update, quality-validation-report, skill-upgrade, workflow-health-report.
5. Check `.codex-workflow/asset-boundaries.json`, `asset-boundaries.generated.json`, the local validator, and confirmation status. Run a changed-file check; run `audit-assets` only when the user requests a full audit. A pending candidate is `yellow` and must be accepted or explicitly discarded before adding or moving engineering assets.
6. Missing configuration is `yellow`; blocking findings under a confirmed config are `red`. Draft status does not block a pilot, but engineering roots and exceptions should be confirmed before complex design or implementation.
7. Check for current rule markers: visible Superpowers layer, first-principles check, adversarial review, business rules and calculation semantics, solution comparison, multi-branch public document protocol, phase consistency preflight, validation level, triggered independent quality validation, documentation drift.
8. Check for stale legacy rules or old-source residue. Mark them as migration risk; do not delete them automatically.
9. Check current branch, public-document boundaries, and phase consistency: entry page, `INDEX.md`, current version/feature README, and task documents should point to the same phase.
10. If the entry page still points to spike/backlog while current task docs have entered formal implementation, mark this `yellow` or `red` and recommend repairing the public-doc patch or entry route first.
11. Check whether `company-quality-validation` is exposed, AGENTS/BUNDLES contain its trigger rules, and the project has the validation report template. If validation is required but its result or evidence is missing, mark the project `red` for closeout.
12. For an existing validation report, check whether it is beside the authoritative task document or at a registered path and whether it records current branch, HEAD, validated paths, diff SHA-256, and untracked-file hashes. Mark stale candidate fingerprints or conditional passes without acceptance records as `red`.
13. If templates or rules are missing, provide safe repair commands. Prefer `update-templates` by default; do not overwrite user documents directly.

## Target Client Check

- Check that INDEX has a confirmed target clients baseline and that requirements, design, and tasks inherit it consistently.
- A UI project with no client baseline is `yellow`; implementation or tests for unauthorized clients are `red`. The workflow must not add mobile adaptation on its own as a repair.
- Health checks report the gap and repair route but never confirm product support for the user.

## Health Levels

- `green`: core files, index, templates, and current rules are present; workflow can be used normally.
- `yellow`: usable, but templates, stale rules, version drift, or public-document boundaries need attention before complex delivery.
- `red`: any critical entry is missing: `AGENTS.md`, `BUNDLES.md`, `EXPERTS.lock.md`, or `specs/global/INDEX.md`; complex work should not continue.

## Repair Guidance

- Missing templates only: recommend `bash scripts/install.sh update-templates <project-path> --lang en`.
- Missing project workflow entry files: recommend `bash scripts/install.sh bootstrap-project <project-path> --lang en`.
- Plugin missing or skills not exposed: reinstall the plugin, then restart Codex.
- Legacy rule residue: generate a migration checklist and ask the user to confirm before editing; do not delete automatically.


## Human-First Output

Start the final reply with `One-sentence conclusion`, `What was completed`, `What needs attention`, and `What the user should do now`. Use business outcomes and user impact, give one primary next action, and explain internal terms on first use. Then place Superpowers, expert calls, commands, paths, hashes, verification evidence, and internal workflow fields in a `Technical Audit Appendix`; Do not dump internal workflow fields one by one into the human summary or use audit fields as a substitute for it.

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
- Phase Consistency Preflight:
- Independent quality validation integration and evidence state:
- Quality validation report path, candidate fingerprint, and conditional-acceptance record:
- Recommended authoritative document:
- External expert status:
- Asset boundary status, check scope, and findings:
- Recommended repair commands:
- Do not auto-handle:
- Verification evidence:
- Unverified items:
- Next step:

## Boundaries

Do not repair a project during a health check unless the user explicitly asks to apply the recommended fixes.

Do not mark workflow health as green merely because the application can run; this skill diagnoses Codex workflow adoption, not runtime product health.

## Document Quality Gates

Before creating or substantially changing a formal document, read the project copy of `specs/global/assets/document-standard.md`; if absent, read the bundled `../../specs/global/assets/document-standard.md`. This skill checks `DOC-G01`, `DOC-G02`, `DOC-G03`, `DOC-G04`, `DOC-G05`, `DOC-G06`, `DOC-G07`, `DOC-G08`, `DOC-G09`, `DOC-G10`, `DOC-G11`, and `DOC-G12` individually. Diagnose templates, formal documents, and waiver records gate by gate; do not use line or section counts as proxies.
