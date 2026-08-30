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
| “API unavailable; approve merge into `<business-branch>`” | `conditional-merge` | merge into the named ordinary business branch; push only if authorized; remain not delivered |

Default to `prepare` when intent is unclear. “All tasks are complete. Start delivery closeout and push the business branch.” grants one-shot `deliver` authorization; do not ask again on the normal path.

## Authorization Boundary

Authorization covers only an ordinary local commit and ordinary push for the confirmed closeout scope. It never expands to force push, rebase, amend, branch deletion, release, deployment, unknown-file deletion, or out-of-scope work. Only `conditional-merge` may perform one explicitly approved ordinary merge, and it must record the source candidate, Target business branch, and whether push is authorized.

## Conditional Merge When an API Is Unavailable

**Conditional merge is not conditional pass.** When real API integration is confirmed scope but the API/environment is unavailable, quality validation remains `blocked / API_PENDING`; this mode is only an engineering integration decision.

Enable `conditional-merge` only when every condition holds:

1. The user explicitly records Approved by, Approved at, source candidate and fingerprint, Target business branch, allowed files, API unavailable evidence, Expiry condition, and Compensating task.
2. The target is an ordinary business branch; it must not enter main, master, develop, integration, release, a protected branch, release tag, or production, and it must not release or deploy.
3. API unavailability is an external dependency or environment limitation, not a known implementation defect disguised as an environment problem.
4. Applicable contract, unit, type, lint, build, Fixture-isolation, and browser checks pass; the production path must not silently fall back to Fixture or Mock.
5. The original API-integration and acceptance tasks stay open with `FIXTURE_READY -> API_PENDING -> CONDITIONAL_MERGED`; do not claim `API_INTEGRATED`, `QUALITY_PASS`, or delivered.
6. Before merging, verify clean source and target workspaces and an unchanged candidate fingerprint. Follow the project's ordinary merge policy; prohibit rebase, force push, history rewrite, and automatic conflict resolution.

Put this customer notice near the start of the human summary, never buried in the audit appendix:

> Only the Fixture-based frontend candidate is complete and has been approved for merge into `<Target business branch>`. Because `<API/environment>` is unavailable, real API integration and real-page acceptance are incomplete. This merge does not mean formal delivery and must not prove real data, charts, or business calculations correct. Complete `<Compensating task>` after API restoration; until then the status remains "conditional merge / not delivered."

## Quality Validation State Handoff

1. At closeout, recompute the independent quality-validation trigger matrix instead of trusting only a decision from a previous conversation.
2. When validation is not required, require no new report; read the implementation or bugfix decision evidence and completion-verification evidence.
3. When validation is `required/mandatory`, locate `quality-validation-report.md` in the same directory as the authoritative task document, or read its registered path from the authoritative task document/current feature or version README.
4. Verify the result, conditional-acceptance record, and candidate fingerprint. The candidate fingerprint includes current branch, HEAD commit, validated paths, diff SHA-256, and untracked-file hashes.
5. When the fingerprint matches, reuse fresh validation evidence and add only closeout-specific cleanup, staging, secret, branch, and final-diff checks; closeout must not indiscriminately rerun the complete test suite.
6. When validated paths drift, return to `company-quality-validation` and rerun the original ACs and scope. Documentation-only reconciliation or provenance-backed cleanup outside the validated scope receives incremental checks only.
7. State flow permits `quality-validation -> delivery-closeout` and a revalidation route from `delivery-closeout -> quality-validation`; it must not create recursive invocation. Quality validation does not perform Git closeout, and closeout does not impersonate independent acceptance.

## Phase 1: Scope and Branch Gate

1. Confirm project root, current branch, upstream, remote, and authoritative task document.
2. Require every task to be complete, explicitly deferred, or explicitly rejected; never silently close unfinished work.
3. Read the implementation or bugfix decision through the Quality Validation State Handoff. When it is `required/mandatory`, require a fresh report and evidence for the current delivery candidate.
4. Stop when validation is missing, stale, or `blocked`. Continue from `conditional-pass` only when the risk is eligible and the user explicitly accepted it; high-risk `V3` cannot be conditionally released. The only exception is `conditional-merge` satisfying all six gates above; it remains blocked and not delivered.
5. List allowed directories, files, and existing user changes.
6. Block `commit`/`deliver`/`conditional-merge` on `main`, `master`, `develop`, `integration`, `release`, and project-defined protected branches.
7. Distinguish accumulated milestone work from true concurrent file conflicts; only the latter is a blocker.

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

1. Select `V0/V1/V2/V3` from the highest-risk task and confirm that the independent validation result still covers the final candidate after cleanup and reconciliation. If behavior-relevant drift exists, return to `company-quality-validation` instead of indiscriminately rerunning every test.
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

## Human-First Output

Put the human summary before the Technical Audit Appendix:

1. One-sentence conclusion: state whether artifacts were committed or pushed.
2. What was completed: describe delivered artifacts, cleanup, and repository result.
3. What needs attention: explain excluded files, blockers, and residual risk impact.
4. What the user should do now: give one primary next action and one short reply phrase.

Then use `Technical Audit Appendix` for the Phase 7 internal fields. Explain acronyms and levels on first use. Do not dump internal workflow fields one by one into the human summary.


### Response Contract Gate

- Trigger this gate for formal completion or phase closeout, an explicit user request for a progress summary, blocker conclusion, or next-step proposal, plus any substantial reply containing audit fields.
- One- or two-sentence working updates and ordinary Q&A never trigger the fixed format, even when they mention the current result, risk, or next step; do not attach full audit details to a lightweight reply.
- When the user asks for more detail, expand only the four sections or the `Technical Audit Appendix`; must not remove, rename, or reorder the four headings.
- Audit fields may appear only in the `Technical Audit Appendix`; they must not sit beside or before the four-section human summary.
- Before sending, check that the four headings are present in order, risks are translated into practical impact, and only one primary next action is given. If any check fails, rewrite it before sending.

## Phase 7: Closeout Report

Report:

- Workflow layer: `company-delivery-closeout`
- Execution mode: `prepare` / `commit` / `deliver`
- Closeout scope and authoritative task document:
- Task completion state:
- Independent quality validation decision and result: not required / pass / conditional-pass / blocked
- Quality validation report path and candidate fingerprint:
- Quality validation report and evidence freshness:
- User acceptance record for conditional pass:
- Integration disposition: formal delivery / `CONDITIONAL_MERGED` and not delivered
- API status: not applicable / `API_PENDING` / `API_INTEGRATED`
- Conditional merge Approved by, Approved at, Target business branch, Expiry condition, and Compensating task:
- Customer notice: not applicable / summary states API unavailable and branch merge only
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

Stop for a protected branch, unfinished task, required quality validation that is missing/stale/blocked, an unaccepted conditional pass, real ownership conflict, unknown/out-of-scope file, unproven cleanup candidate, failed validation or review, documentation conflict, suspected secret/production/database/large file, staged mismatch, remote-ahead state, rejected normal push, or unclear network/permission state. `conditional-merge` may waive only the API-unavailable validation block and its corresponding unfinished API task; it cannot waive any other stop condition.

The stop report names blockers, completed safe steps, Git actions not executed, and the recovery entry. Never claim commit or push success without evidence.

## Superpowers Overlay

- Non-trivial code or L2/L3: **REQUIRED SUB-SKILL:** Use `superpowers:requesting-code-review`.
- Every formal delivery: **REQUIRED SUB-SKILL:** Use `superpowers:verification-before-completion`.
- Here completion verification proves the post-closeout candidate, cleanup, and staging boundary. The same capability in quality validation proves AC coverage and the acceptance result. Reuse fresh evidence instead of repeating the whole suite by default.
- Git finalization: **REQUIRED SUB-SKILL:** Use `superpowers:finishing-a-development-branch`, subject to this skill's selected mode and authorization boundary.

## Document Quality Gates

Before creating or substantially changing a formal document, read the project copy of `specs/global/assets/document-standard.md`; if absent, read the bundled `../../specs/global/assets/document-standard.md`. This skill enforces `DOC-G01`, `DOC-G04`, `DOC-G05`, `DOC-G06`, `DOC-G07`, `DOC-G08`, `DOC-G09`, `DOC-G10`, `DOC-G11`, and `DOC-G12`.
