---
name: company-legacy-project-onboarding
description: Use when introducing the company workflow into an existing project, generating or reviewing project context, or planning a gradual migration from legacy project practices.
---

# Legacy Project Onboarding

## Purpose

Introduce the company Codex workflow into an existing project without disrupting established rules or delivery rhythm.

## Workflow

1. Inspect existing `AGENTS.md`, README, manifests, docs, test folders, and run commands.
2. Use the installer or `generate-index` command to create a draft `specs/global/INDEX.md`.
3. Run `generate-asset-boundaries` to infer `.codex-workflow/asset-boundaries.json` from manifests plus build/test entry points. Use `confirm` for a first draft and `accept-asset-boundaries` for a generated update candidate; preserve existing exceptions and back up the old config before acceptance.
4. Before confirmation, block only obvious violations such as new package managers, dependency trees, or executable tests under `specs`/`docs`; after confirmation, enforce engineering-root ownership too.
5. Generate or complete the document ownership map: entry page, field logs, formal specs, lifecycle docs, numbering namespaces, and update triggers.
6. Mark inferred fields and fields that need user or project-owner confirmation.
7. Preserve existing project rules and append the company workflow block only.
8. Explicitly use `superpowers:brainstorming` to choose one small feature, one bugfix, or one spike as the pilot.
9. After the pilot, review process cost, verification evidence, expert routing accuracy, and document ownership fit.
10. Promote the workflow to the team default only after the pilot is stable.

## Recommended Prompts

- `Help me introduce the company Codex workflow into this existing project.`
- `Generate and review an INDEX.md draft for this project.`
- `Suggest the first pilot task for this legacy project migration.`

## Output

- Workflow layer: `company-legacy-project-onboarding`
- Trace mode:
- Superpowers layer: `superpowers:brainstorming`
- Actual calls:
- Expert/plugin capabilities:
- Not called, lens only:
- First Principles Check:
- Adversarial Review:
- Execution strategy: gradual adoption; do not edit business code.
- Verification evidence:
- Unverified items:
- Remaining risk:
- Current project state:
- Auto-inferred context:
- Asset boundary status and confirmation items:
- Document ownership map:
- Numbering namespaces:
- Needs user confirmation:
- Recommended pilot task:
- Risks against immediate migration:
- Document ownership conflicts to fix:
- Next step:
