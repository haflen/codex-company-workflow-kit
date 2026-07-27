# Thread Handoff Continuity Routing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade company conversation handoff from summary-only export to Codex-native continuity routing with tiered capsules and semantic receipt verification.

**Architecture:** `company-workflow-help` detects conversation-transition intent. `company-thread-handoff` then selects `resume`, `compact`, `fork`, or `handoff`; only `handoff` generates a `quick`, `standard`, or `decision-rich` capsule. Project facts remain authoritative and a target conversation must prove receipt before execution.

**Tech Stack:** Markdown skills, Codex task tools, JSON plugin manifests, shell-based plugin validation.

## Global Constraints

- Preserve English and Chinese source variants.
- Do not change external expert skill content.
- Do not claim task tools are available when they are absent.
- Cross-task sending requires explicit user transfer intent and a concrete target.
- Do not stage the unrelated `docs/company-internal-training.md` file.

---

### Task 1: Capture the failing baseline

**Files:** None.

- [x] Run a company scenario against the old skill.
- [x] Verify that it always chooses a summary and cannot preserve the full transcript.
- [x] Run a personal scenario against the old skill.
- [x] Verify that it forbids direct transfer and has no semantic receipt.

### Task 2: Upgrade company handoff behavior

**Files:**
- Modify: `outputs/company-codex-workflow-v2-zh/skills/company-thread-handoff/SKILL.md`
- Modify: `outputs/company-codex-workflow-v2/skills/company-thread-handoff/SKILL.md`
- Modify: both `agents/openai.yaml` files.

- [x] Add outcome-first continuity routing.
- [x] Replace `quick/full` with `quick/standard/decision-rich` capsule levels.
- [x] Add direct/manual transport rules and semantic receipt verification.
- [x] Add explicit historical-knowledge wording and fallback behavior.

### Task 3: Wire routing and project guardrails

**Files:**
- Modify: both `company-workflow-help/SKILL.md` files.
- Modify: both company `AGENTS.md` files.

- [x] Route same-task continuation, compaction, complete inheritance, and clean handoff separately.
- [x] Require target receipt verification before risky execution.

### Task 4: Document and release

**Files:**
- Modify: `README.md`
- Modify: `docs/codex-usage-guide.md`
- Modify: `docs/company-quickstart.md`
- Modify: `docs/skill-tree.md`
- Modify: `CHANGELOG.md`
- Modify: four company plugin manifests.

- [x] Add user-facing selection guidance and examples.
- [x] Release company packages as `0.2.25`.

### Task 5: Verify and deploy

**Files:** Source and local plugin cache.

- [x] Validate both language plugins.
- [x] Run structural searches for all routes, levels, receipt fields, and knowledge boundaries.
- [x] Re-run pressure scenarios and confirm corrected behavior.
- [x] Install only the Chinese company plugin locally.
- [x] Commit and push tracked company changes without staging unrelated files.
