# Install Company Codex Workflow v2

Start with the company quickstart in `docs/company-quickstart.md` if you are trying this workflow for the first time.

1. For project-only use, copy or merge `AGENTS.md` into the company project root, copy `specs/global/assets/` into the project, and place `BUNDLES.md` plus `EXPERTS.lock.md` at the project root.
2. For plugin use, install this directory as a local Codex plugin; `.codex-plugin/plugin.json` points at `./skills/`.
3. Use the installer to generate a draft `specs/global/INDEX.md`, then have the project owner confirm stack, commands, current version, and active milestone.
4. Fill `EXPERTS.lock.md` with the real source, license, and pin for every external expert skill the team will trust.
5. Run `company-skill-security-review` before adding external or self-improved skills to the trusted set.
6. Pilot with one feature and one bugfix before making the workflow mandatory.

Recommended command:

```bash
bash scripts/install.sh bootstrap-project /path/to/project --lang en
```

Generate or refresh only the index draft:

```bash
bash scripts/install.sh generate-index /path/to/project --lang en
```

If an existing project already has `INDEX.md`, the installer preserves it by default and writes `specs/global/INDEX.generated.md` for review.

If a project reports missing templates, `BUNDLES.md`, or `EXPERTS.lock.md`, run:

```bash
bash scripts/install.sh update-templates /path/to/project --lang en
```

Existing files are preserved by default; the installer writes `.generated` files for comparison.

This v2 starter kit is based on the audited source skills. It intentionally removes fear-based language, unconditional expert delegation, and hard requirements that do not fit Codex.

External expert skills remain dependencies. They should be pinned in `EXPERTS.lock.md`, reviewed before use, and updated through the dry-run upgrade workflow rather than auto-pulled from a hub.

Skill updates default to dry-run. Use `company-skill-upgrade-runner` or say `检查专家技能更新`; Codex should compare old and new versions, run security review, and wait for explicit confirmation before overwriting production skills.
