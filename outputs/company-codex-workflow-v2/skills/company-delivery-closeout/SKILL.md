---
name: company-delivery-closeout
description: Use when a company task batch, feature, milestone, or version phase is complete and ready for formal closeout, local commit, or push of the current business branch.
---

# Company Delivery Closeout

## Core Principle

Task completion does not prove delivery readiness. Consolidate artifacts, evidence, and Git boundaries against the final candidate; unknown ownership, failed validation, or documentation conflict blocks commit and push.

## Select the Mode

| User intent | Mode | Git action |
| --- | --- | --- |
| “Start delivery closeout” | `prepare` | no commit or push |
| “Close out and commit” | `commit` | local commit, no push |
| “Close out and push the business branch” | `deliver` | local commit and normal push of the current business branch |

Default to `prepare` when intent is unclear. “All tasks are complete. Start delivery closeout and push the business branch.” grants one-shot `deliver` authorization; do not ask again on the normal path.

## Authorization Boundary

Authorization covers only an ordinary local commit and ordinary push for the confirmed closeout scope. It never expands to force push, rebase, amend, merge, branch deletion, release, deployment, unknown-file deletion, or out-of-scope work.

## Phase 1: Scope and Branch Gate

1. Confirm project root, current branch, upstream, remote, and authoritative task document.
2. Require every task to be complete, explicitly deferred, or explicitly rejected; never silently close unfinished work.
3. List allowed directories, files, and existing user changes.
4. Block `commit`/`deliver` on `main`, `master`, `develop`, `integration`, `release`, and project-defined protected branches.
5. Distinguish accumulated milestone work from true concurrent file conflicts; only the latter is a blocker.

## Phase 2: Inventory and Classify Every File

Use read-only status and diffs to inventory code, tests, configuration, migrations, documents, assets, generated artifacts, and untracked files. Classify every change as:

- `include`: belongs in this delivery.
- `retain-but-exclude`: remains in the worktree but not this commit.
- `cleanup-candidate`: temporary and provenance-confirmed.
- `blocking-unknown`: ownership, purpose, or safety is unclear.

Classify requirements prototypes by provenance and state: a manifest-owned active or awaiting-confirmation draft is `retain-but-exclude` with an explicit deferral/resume entry; only a withdrawn, superseded, or baseline-verified source draft is a `cleanup-candidate`; a confirmed baseline under `prototype/` beside authoritative requirements is `include`; a prototype with no manifest or requirements link is `blocking-unknown`.

Any `blocking-unknown` stops deletion, commit, and push. Never stage the whole repository.

## Phase 3: Reconcile Documents and Results

1. Compare requirements, business rules, design, API contract, tasks, and final behavior.
2. Update only existing authoritative entry, index, version/feature README, task status, and lifecycle records that own the relevant fact.
3. Preserve auditable history and do not publish branch-local results as shared facts prematurely.
4. Fix only delivery-related formatting, comments, and documentation drift; do not perform adjacent refactors.

If code and documents conflict and cannot be reconciled unambiguously, stop Git actions and return to the appropriate requirements, design, or planning workflow.

## Phase 4: Cleanup Dry Run and Provenance

Before deletion, report each candidate's path, origin, creator/command, tracked state, retention value, and proposed action.

- Auto-delete only workflow-created temporary files with recorded paths that are not formal artifacts.
- Delete prototype drafts only when they are withdrawn/superseded or baseline verification is complete, and `prototype.json.owned_files` proves ownership.
- For recurring generated files that should stay untracked, only propose a project `.gitignore` change.
- Preserve and stop for logs used as evidence, databases, attachments, design assets, nested repositories, and unknown files.

Inventory again after cleanup. Never run unscoped cleanup or destructive reset operations.

## Phase 5: Final Validation, Review, and Security Checks

1. Select `V0/V1/V2/V3` from the highest-risk task and re-validate after cleanup and reconciliation.
2. Run relevant tests, type checks, lint, build, necessary browser/E2E checks, and `git diff --check`.
3. For non-trivial code or L2/L3 delivery, use `superpowers:requesting-code-review` on the final diff.
4. For every formal delivery, use `superpowers:verification-before-completion` and accept only fresh evidence.
5. Check for suspected secrets, production configuration, databases, unexpected large files, dependency changes, and unverified generated artifacts.
6. Read `.codex-workflow/asset-boundaries.json` and run the changed-asset check. Any blocking new or moved file stops commit/push. Run a full historical audit only when requested or when workflow health requires it.
7. Use `company-expert-routing` only when domain risk warrants it.

Any failed check, unverified critical item, or high-severity review finding blocks commit and push.

## Phase 6: Exact Staging, Commit, and Normal Push

1. Show the final `include` list, deletion list, diff statistics, evidence, unverified items, and proposed commit message.
2. Stage only explicit paths; never stage the whole repository.
3. Require:

```bash
git diff --cached --name-status
git diff --cached --check
git diff --cached --stat
```

4. The staged list must exactly match `include`; then create one local commit and record its SHA.
5. `prepare` never commits; `commit` stops after local commit; `deliver` runs `git push -u origin HEAD` for an ordinary push.
6. Stop when a normal push is rejected, the remote is ahead, or permission/network state is unclear. Never rewrite history or escalate privileges automatically.
7. `superpowers:finishing-a-development-branch` supplies final branch checks only. It must not replace the selected mode with a PR, merge, worktree deletion, or another integration action.

## Phase 7: Closeout Report

Report:

- Workflow layer: `company-delivery-closeout`
- Execution mode: `prepare` / `commit` / `deliver`
- Closeout scope and authoritative task document:
- Task completion state:
- Artifacts: code / tests / documents / configuration / assets
- Deleted temporary files:
- Retained-but-excluded files:
- Blocking unknown files:
- Asset placement gate and check scope:
- Superpowers overlay:
- Actual calls:
- Expert capability: called / lens only
- Validation level, commands, and results:
- Unverified items and remaining risk:
- Staged files:
- Commit SHA:
- Current branch, remote, and push result:
- Stop reason:
- Next step and recommended user phrase:

## Stop Conditions

Stop for a protected branch, unfinished task, real ownership conflict, unknown/out-of-scope file, unproven cleanup candidate, failed validation or review, documentation conflict, suspected secret/production/database/large file, staged mismatch, remote-ahead state, rejected normal push, or unclear network/permission state.

The stop report names blockers, completed safe steps, Git actions not executed, and the recovery entry. Never claim commit or push success without evidence.

## Superpowers Overlay

- Non-trivial code or L2/L3: **REQUIRED SUB-SKILL:** Use `superpowers:requesting-code-review`.
- Every formal delivery: **REQUIRED SUB-SKILL:** Use `superpowers:verification-before-completion`.
- Git finalization: **REQUIRED SUB-SKILL:** Use `superpowers:finishing-a-development-branch`, subject to this skill's selected mode and authorization boundary.

## Document Quality Gates

Before creating or substantially changing a formal document, read the project copy of `specs/global/assets/document-standard.md`; if absent, read the bundled `../../specs/global/assets/document-standard.md`. This skill enforces `DOC-G01`, `DOC-G04`, `DOC-G05`, `DOC-G06`, `DOC-G07`, `DOC-G08`, `DOC-G09`, `DOC-G10`, `DOC-G11`, and `DOC-G12`.
