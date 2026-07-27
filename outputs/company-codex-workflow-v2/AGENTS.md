# Company Codex Workflow

This project uses a lightweight SDLC adapted from audited source skills. The goal is traceability and consistent delivery without slowing down simple work.

## Context First

- Read `specs/global/INDEX.md` before planning or editing.
- If present, read `说明文档.md` for current progress and project state.
- Read only the current version, milestone, feature docs, and source files relevant to the task.
- Do not scan all Markdown files unless the task is an audit or migration.

## Workflow Document Ownership

Before writing any project document, confirm its role, information level, numbering namespace, and update trigger. Do not merge the project entry summary, spike work log, formal requirements/design/tasks, and lifecycle summaries into one continuous task chain.

Default ownership:

- `说明文档.md` or equivalent entry page: project entry, current state, recent important events, and reading route. It must not contain spike work-log flow and must not use spike-internal task IDs.
- `spike_*_工作日志.md` or spike-local log: spike field log, experiment flow, observations, and temporary decisions. Use spike-scoped IDs such as `SPK02-T001`; do not use bare `Task 001`.
- `specs/versions/...` or `specs/features/...`: formal requirements, design, task plans, and acceptance basis. Use feature, version, or formal task IDs, not spike work-log IDs.
- `docs/lifecycle/`: lifecycle phase summaries and milestone retrospectives. Summarize phases; do not track every small task.
- `specs/global/INDEX.md`: document ownership map and routing index; start here when deciding which document to update.

Update triggers:

- Project entry pages update only when current phase, recent important events, reading route, or key status changes.
- Spike logs update only when spike experiments, observations, decisions, or temporary tasks change.
- Formal specs update only when requirements, design, tasks, acceptance criteria, or approved changes are confirmed.
- Lifecycle docs update only at version phase completion, milestone changes, or management-summary needs.

If the same bare task number appears in documents at different levels, pause before writing and recommend namespace IDs such as `SPK02-T183`, `FEAT-DT-T01`, or date-based project events.

## Multi-Branch Public Document Protocol

When multiple branches run in parallel, public entry documents represent mainline facts, not the local state of one development branch.

- `说明文档.md`, `specs/global/INDEX.md`, and similar public mainline documents are updated by default only on `main`, `master`, `develop`, `integration`, or an explicit integration branch.
- Feature, spike, and hotfix branches must not write unmerged branch-local status into the public "current state" sections.
- If a branch affects the project entry, current phase, recent important events, reading route, document ownership, or numbering rules, write `docs/public-doc-updates/<branch-or-feature>.md`.
- Branch-private process notes belong in `specs/features/<feature>/`, `specs/versions/...`, `spikes/`, or the relevant work log, not the public entry page.
- During merge/integration, read the public-doc update patches and promote only merged facts into `说明文档.md` and `specs/global/INDEX.md`.
- If multiple branches affect the same public section, do not fight over the public document in feature branches; keep patches and rewrite the public section once on the integration branch.
- If a business branch must edit a public document directly, state why and mark `direct public-doc write risk` in the completion report.

## Phase Boundaries

- Requirements work produces goals, scope, acceptance criteria, and edge cases. Do not edit implementation code.
- Design work produces architecture, contracts, data flow, risks, and test strategy. Do not edit implementation code.
- Planning work produces executable tasks and verification points. Do not edit implementation code.
- Implementation starts only after requirements, design, and task plan are confirmed, except for `/spike` or `/hotfix`.
- Ambiguous "continue" means continue the current phase, not advance to the next phase.

## Delivery Closeout Boundary

- Task implementation and milestone delivery closeout are separate phases; a task completion report does not replace closeout.
- Use `company-delivery-closeout` only after every task is complete, explicitly deferred, or explicitly rejected.
- `prepare` never commits or pushes; `commit` creates only a local commit; only `deliver` permits an ordinary push of the current business branch.
- Stop for unknown ownership, unfinished tasks, failed validation, documentation conflict, sensitive/production/database/unexpected-large files, protected branches, staged-list mismatch, or a rejected normal push.
- Ordinary push authorization excludes rebase, force push, amend, merge, release, and deployment.
- Stage only classified files by exact path; delete temporary files only when provenance is proven.

## Conversation Handoff

- Use `company-thread-handoff` when a long conversation must switch, pause, continue later, or transfer ownership; select `resume / compact / fork / handoff` first.
- Prefer resume for the same task, compact for context length only, fork when complete history matters, and a capsule only for a clean context.
- Output in chat by default; overwrite `.codex/handoff/current.md` only on explicit request.
- Keep one active task and mark side topics out of scope and unauthorized.
- Use `quick / standard / decision-rich` capsules; select `decision-rich` for product, architecture, business-rule, calculation, data, security, or rejected-option history.
- The target verifies path, branch, working tree, key files, unfinished work, and authorization, then restates goal, decisions, constraints, state, pending work, and permission.
- Fork or cross-task sending requires explicit user intent and a known target; report sent, read, and semantic receipt state.
- Project facts override the handoff. It does not replace `company-context-index` or formal documents and grants no implementation authorization.
- Workflows may recommend a continuity route after a phase, on scope confusion, with dirty changes, running services, or incomplete verification, but never silently write a file or create a task.

## Continuous Implementation Mode

Continuous implementation mode is only for confirmed implementation task plans. It reduces repeated approval loops; it does not remove workflow boundaries.

- Enable it only when the user explicitly asks to "continue all remaining tasks", "run continuously", "batch progress", or equivalent wording.
- Phase Consistency Preflight and Scope Change Circuit Breaker must pass before enabling it.
- Task plans should mark `continuous / careful-continuous / must-stop`.
- `V0/V1` tasks may be batched when related; `V2` tasks may batch only 1-3 tightly related items; `V3` tasks stop after one task by default.
- After every task, re-check scope change, verification failure, V3 risk, user confirmation points, worktree conflicts, high-permission commands, and local resource anomalies.
- If a stop condition is hit, do not continue to the next task; report the stop reason, evidence, and recommended next phrase.

Every implementation, bugfix, hotfix, spike, or document handoff completion must include next-step guidance:

- `Next-step guidance:` continue implementation / return to requirements / return to design / confirm tasks / add verification / pause.
- `Recommended next user phrase:` give a copyable sentence.

## Codex Goal Tracking

Codex goals are for cross-turn objective management. They do not replace company workflow phase boundaries.

- L0/L1 small tasks do not need goal tracking by default.
- L2 standard features, cross-phase work, cross-session work, multi-document work, or continuous implementation should recommend goal tracking.
- L3 high-risk work, legacy onboarding, skill upgrade/security review, expert maintenance, and hotfix follow-up chains should strongly recommend goal tracking.
- Goal descriptions must state final success criteria, not every workflow step.
- An active goal does not make implementation authorization valid; Phase Consistency Preflight, Scope Change Circuit Breaker, V3 stop conditions, verification failures, and user confirmation still take priority.
- Completion reports for complex tasks should output `Goal status guidance`: whether to create, keep, or close a Codex goal.

## Codex Plan Mode

Codex Plan Mode is for route selection before the formal workflow. It is not a new delivery phase.

- L0/L1 small tasks, clear single-point implementation, or single-point bugfixes usually do not need Plan Mode.
- L2 standard features with ambiguous requirements, solution comparison, legacy onboarding, route reset after scope change, or task-order/stop-condition confirmation before continuous implementation should recommend Plan Mode.
- L3 high-risk work, cross-system changes, data, permissions, security, performance, money/metric formulas, production incident follow-up, large migrations, or multi-person delivery should strongly recommend Plan Mode.
- Plan Mode may output route, risks, confirmation questions, and the next handoff phrase only; it must not edit files, code, or replace requirements/design/task confirmation.
- After Plan Mode, return to the formal company workflow: requirements, design, planning, implementation, bugfix, hotfix, spike, or skill governance.
- Workflow outputs must include `Codex Plan Mode recommendation`, with the recommendation, reason, prompt, and formal workflow after Plan Mode.

## Subagents

Subagents are for context isolation, independent investigation, independent execution, or independent review. They are not the default execution mode and are not a separate App button users should hunt for.

- L0/L1 small tasks, single-file small changes, docs/comments only, copy/UI labels/config, or one-path bugfixes usually do not use subagents.
- L2 multi-task delivery with clear task boundaries, or multiple independent failure domains, should recommend subagents.
- L3 high-risk, cross-module/cross-system, data/permission/security/performance, complex legacy onboarding, skill-upgrade security review, or larger continuous batches should strongly recommend subagents, at least for independent review.
- Codex spawns subagents only when the user explicitly asks to `spawn agents`, `delegate in parallel`, `use subagents for parallel review`, or equivalent wording. A workflow recommendation is not an actual invocation.
- Codex CLI can manage agent threads with `/agent`; the Codex App primarily surfaces subagent activity and does not require a separate subagent button.
- For stable company roles, first run `bash scripts/install.sh install-agents <project-path> --lang en` to generate project-scoped `.codex/agents/`.
- The main agent always owns phase permission, implementation authorization, dispatch, diff review, verification evidence, and final conclusion.
- Subagents receive only narrow task packets: goal, boundary, allowed files, prohibited actions, verification method, and expected output.
- Do not dispatch parallel tasks that edit the same file, same state model, same database migration, same public-doc section, or other shared state.
- A subagent output is not a completion claim; the main agent must review and verify it.
- Workflow outputs must include `Subagents recommendation`, `Subagent capability status`, and `Subagents actual calls`, distinguishing actual calls, no calls, explicit-user-request needed, custom-agents needed, and split-lens-only usage just like Superpowers.

## Scope Change Circuit Breaker

Implementation authorization applies only to the requirements, design, and task scope that was confirmed at the time. After implementation starts, if the user or Codex discovers a material scope change, the old "start implementation" authorization immediately expires; pause coding and reconfirm the phase.

Trigger the `Scope Change Circuit Breaker` by default when any of these appears:

- A new or previously missing architecture layer, data-preparation layer, table, API boundary, scheduler chain, external system, or key module.
- User intent such as "missing", "analyze first", "why", "how to fit this in", "update the docs", "business semantics are not confirmed", or "requirements/design/tasks need updates".
- The implementation scope exceeds confirmed task planning, solution comparison, API contracts, or `business-rules.md`.
- Field sources, calculation semantics, state transitions, exception/degradation strategy, permission boundaries, or data-sync strategy are not confirmed.
- Documentation updates create a new contract, field mapping, task list, or public-doc impact note that the user has not confirmed.

After the circuit breaker trips, allowed actions are:

- Update only requirements, business rules, technical design, task planning, field mappings, or public-doc impact patches.
- Output `Implementation authorization: expired; user confirmation required before coding`.
- List the scope change, authoritative documents, and the next user phrase needed.

After the circuit breaker trips, forbidden actions are:

- Do not reuse an old `tasks confirmed, start implementation` authorization for the new scope.
- Do not continue into coding immediately after updating docs.
- Do not treat expert-routing output as a substitute for user confirmation on the changed implementation scope.

## Phase Consistency Preflight

Before implementation, bugfix, or hotfix work, run a lightweight `Phase Consistency Preflight` so public entry docs, indexes, and current task documents do not contradict each other after coding has already started.

Read only the minimum necessary documents. Do not scan every Markdown file:

- Current branch name and working-tree state.
- `说明文档.md` or equivalent project entry page.
- `specs/global/INDEX.md`.
- Current feature, version, or milestone README/task document.
- Current requirements, design, tasks, business-rules, and API contract when present.
- `docs/public-doc-updates/` patches related to the current branch or feature.

Authority order:

- The current execution truth comes first from the confirmed feature/version task document.
- `specs/global/INDEX.md` owns routing and document roles; it may not represent branch-local real-time state.
- `说明文档.md` represents mainline entry and mainline current state, not feature/spike branch-local state.
- On non-integration branches, public-entry impacts should be written to `docs/public-doc-updates/<branch-or-feature>.md` instead of directly rewriting public entry state.

If phase, entry, version, task numbering, current state, or authoritative documents conflict, pause implementation and output:

- `Phase Consistency Preflight: failed`
- Conflicting files and concrete conflicts.
- Provisional authoritative document for this turn.
- Recommended repair: update public-doc patch, fix INDEX, fix entry summary, or wait for user confirmation.

Only start code implementation or repair after the preflight passes, or after the user confirms which authoritative document to follow.

## First Principles And Adversarial Review

Company workflows include two checks by default; users do not need to type special prompt phrases:

- `First Principles Check`: return to underlying facts, constraints, and minimum conditions for the solution to be true. Do not replace root-cause analysis with analogy or surface symptoms.
- `Adversarial Review`: validate the plan against malicious users, extreme data, abnormal states, permission bypasses, concurrent retries, oversized input, future timestamps, cache false positives, and rendering pressure.

Automatic triggers:

- Requirements: for L2/L3 or complex business rules, state core assumptions, non-negotiable constraints, and adversarial scenarios; when metrics, formulas, state transitions, complex operations, field semantics, or abnormal-data handling are involved, create or update `business-rules.md`.
- Design: for non-trivial architecture, data, permission, performance, security, external API, frontend rendering, or cross-service boundary decisions, run `First Principles Check`.
- Design: for L2/L3 large features, core modules, cross-boundary work, data models, permissions, security, performance, business rules, or clear technical tradeoffs, compare 2-3 options and get user confirmation; L1 small changes may skip comparison with a reason.
- Planning: every non-trivial task must include a minimum failing case or verification anchor and at least one adversarial scenario.
- Implementation: before completion, run `Adversarial Review` unless the change is pure copy, comments, or no-behavior work; state the reason if skipped.
- Bugfix/hotfix: before root-cause claims, run `First Principles Check`; before completion, run regression and adversarial review.
- Spike: before conclusion, state the first-principles hypothesis, counterexample experiment, and evidence boundary.
- Skill upgrade, security review, and self-improvement proposals default to `full-audit` and run adversarial review.

Output requirements:

- `First Principles Check:` list underlying facts, constraints, minimum conditions, or why it can be skipped.
- `Adversarial Review:` list extreme, malicious, or abnormal scenarios and results, or why it can be skipped.
- Do not write only "analyzed from first principles" or "ran adversarial review"; include concrete facts or scenarios.

## Visible Superpowers Layer

- Every workflow output must explicitly include `Workflow layer`, `Superpowers layer`, and `Execution strategy`.
- Every workflow opening must explicitly include `Actual calls`, `Expert/plugin capabilities`, and `Not called, lens only`; do not say "expert lens" without stating whether the skill was actually invoked.
- Every workflow closing must explicitly include `Verification evidence`, `Unverified items`, and `Remaining risk`. If verification is not needed for the current phase, state why.
- If a Superpowers skill, expert skill, MCP, browser capability, or other Codex plugin capability is not actually exposed or invoked in the current session, record it under `Not called, lens only` with the reason.
- Requirements exploration defaults to `superpowers:brainstorming`.
- Complex planning defaults to `superpowers:writing-plans`.
- Implementation defaults to `superpowers:test-driven-development` and `superpowers:verification-before-completion`.
- Bugfix defaults to `superpowers:systematic-debugging`, with `superpowers:verification-before-completion` before completion.
- If a simple task skips Superpowers, state the reason explicitly.

## Business Rules And Calculation Semantics

- `business-rules.md` is triggered only for complex business cases, not pure copy, small UI, small configuration, or other low-risk changes.
- Trigger conditions include metrics/formulas/money/scores/ordering/weights/aggregation/conversion, state transitions, approval/task flows, role differences, permission rules, field source/unit/precision/mapping, missing data, abnormal values, batch processing, duplicate submission, and concurrency conflicts.
- Requirements own the decision on whether `business-rules.md` is needed; if not needed, state the reason.
- Design maps business rules; it must not reinvent formulas or semantics.
- Planning turns rule examples into automated tests or explicit manual verification steps.
- Implementation or bugfix work that discovers missing rules must stop guessing and route back to requirements for a rule document or change request.

## Chinese Code Logic Comments

When AI writes or changes code, add necessary code-logic comments in Chinese by default. Comments should help later review, handoff, and business-semantics audits; they must not translate obvious syntax line by line.

Chinese comments are required for these cases across Java, frontend TypeScript/Vue/React, Python, SQL, scripts, and generated configuration logic:

- Business rules, status decisions, approval/task flows, permission branches, or role-specific behavior.
- Metrics, formulas, money, precision, rounding, thresholds, sorting weights, and aggregation semantics.
- Data sources, field mapping, region/enum/dictionary mapping, unit conversion, frontend-backend DTO/API mapping.
- Fallback, hiding, degradation, empty data, abnormal values, legacy compatibility, or temporary transition strategies.
- Non-obvious performance, concurrency, cache, retry, idempotency, or browser-rendering handling.
- Implementation points tied to `business-rules.md`, API contracts, or design constraints.

Do not write low-value comments:

- Do not explain syntax itself, such as "iterate list", "set variable", or "return result".
- Do not invent business provenance. If a threshold or formula source is unclear, route back to requirements or `business-rules.md`.
- Do not use comments to hide complex code. Prefer names, extracted methods, and constants first; then add key rationale comments.
- When logic changes, update related comments so comments do not drift from code.

Implementation, bugfix, and hotfix completion must output `Code comment check: completed / not needed / needs comments`, with coverage points such as business rules, calculation semantics, data mapping, exceptional branches, performance strategy, or none.

## Technical Solution Comparison

- Solution comparison is trigger-based, not mandatory for every design.
- L1 copy, small UI, small config, single-path low-risk changes may skip comparison, but must state why.
- L2/L3 work involving new modules, core flows, service/frontend-backend boundaries, data models, permissions, security, performance, cache, concurrency, external APIs, business rules, or maintainability tradeoffs must compare 2-3 options.
- Comparison must include the recommended option, alternatives, tradeoffs, risks, and a user confirmation point.
- When L2/L3 comparison is triggered, task planning must not start until the user confirms the recommended option.

## Validation Levels And Documentation Drift

Workflow skills choose the validation level automatically. Users do not need to pick one. The goal is to control risk while keeping token, time, and local-machine cost low.

- `V0`: docs, comments, formatting, prompts, or no-behavior changes. Evidence is a diff check, target-file review, or rendering check.
- `V1`: low-risk small behavior, small UI, small config, or single-path changes. Evidence is a focused command, local test, manual path, or minimal page check.
- `V2`: standard feature work, bugfixes, cross-file behavior, API/data contracts, or user-visible flows. Evidence is related automated tests, type/build checks, and browser/manual verification when needed.
- `V3`: production, permissions, security, money/metric calculations, data migration, concurrency, performance, external APIs, hotfixes, or broad refactors. Evidence includes regression, adversarial cases, rollback/recovery notes, and E2E or performance checks when needed.

Automatic selection:

- Pure docs with no semantic rule change use `V0`.
- Isolated low-risk changes use `V1`.
- Normal feature work and ordinary bugfixes use `V2`.
- Production, data, permission, security, performance, money/metric formulas, cross-system work, or hotfixes upgrade to `V3`.

Implementation, bugfix, and hotfix completion must output:

- `Validation level: V0/V1/V2/V3`
- `Verification evidence:` actual commands, check results, screenshots, logs, or manual checks.
- `Documentation drift impact:` whether requirements, business-rules, design, api-contract, tasks, `说明文档.md`, `specs/global/INDEX.md`, or public-doc update patches need changes.
- `Unverified items:` why they were not verified and how to verify them later.

If code changes operation logic, calculation semantics, field meaning, API contract, acceptance criteria, or user flow while docs remain stale, do not claim completion; update the docs or mark the drift as pending confirmation.

## Capability Trace

All company workflows use this trace protocol by default unless the user explicitly asks for a minimal answer:

### Automatic Levels

Users do not decide which trace level to use; the workflow must choose automatically:

- `light`: default mode for normal in-phase progress, small changes, doc updates, and low-risk continuation. Keep only the required actual calls, lens-only usage, verification evidence, and risk notes.
- `full-audit`: key-node or exception mode. Enable the full `Workflow Audit` when any of these is true:
  - Phase handoff: requirements to design, design to planning, planning to implementation.
  - Implementation completion, bugfix completion, any hotfix phase, or spike conclusion.
  - Skill upgrade, expert dependency update, security review, or self-improvement proposal.
  - An expert/plugin capability was not actually invoked and only used as a lens.
  - The current session lacks an expected Superpowers skill, expert skill, MCP, browser capability, or plugin capability.
  - Verification failed, is missing, or tests cannot be run.
  - Production, data, permission, architecture, performance, or security risk is involved.
  - The user asks to audit, check the process, or confirm compliance.

Opening:

- `Workflow layer:`
- `Trace mode: light` or `Trace mode: full-audit`
- `Actual calls:` list workflow, Superpowers, expert skill, MCP, browser, or plugin capabilities actually triggered or read.
- `Expert/plugin capabilities:` list the experts, Superpowers, or Codex plugin capabilities selected for this turn.
- `Not called, lens only:` list capabilities that were unavailable, unsuitable for the phase, or not worth invoking.
- `Codex Plan Mode recommendation:` state not needed, recommended, or strongly recommended with the reason.
- `Subagents recommendation:` state not needed, recommended, or strongly recommended.
- `Subagent capability status:` state not checked, available in current session, explicit user request needed, local custom agents needed, or App activity display only.
- `Subagents actual calls:` state not called, called, split lens only, or not called with the reason.
- `First Principles Check:`
- `Adversarial Review:`
- `Execution strategy:`

Closing:

- `Verification evidence:` include commands, check results, file changes, screenshots, logs, or manual evidence.
- `Unverified items:` include anything not checked or not applicable to this phase.
- `Remaining risk:`

Do not use "executed with expert lens" as a substitute for call evidence; always distinguish `actually invoked` from `lens only`.

When `full-audit` is active, also output:

- `Workflow Audit:`
- `Phase boundary:`
- `Superpowers declaration:`
- `Expert/plugin actual calls:`
- `Lens-only usage:`
- `Verification evidence:`
- `Unverified items:`
- `Conclusion:`

## Handoff Signals

- `需求已确认，进入技术设计`
- `方案已确认，进入任务拆解`
- `任务已确认，开始实现`
- `开始 bugfix`
- `/spike <technical question>`
- `/hotfix <incident>`
- `检查技能更新`
- `更新 <skill-name> 技能`
- `对比并升级 <skill-name>`

## Expert Usage

Use relevant experts or subagents when the work involves non-trivial architecture, framework APIs, concurrency, performance, security, data modeling, UI craft, or testing strategy. Do not invoke experts for trivial edits.

Users should not need to name experts in chat for normal work. Workflow skills should select the smallest matching bundle from `BUNDLES.md`, then route to the relevant expert only when the current phase needs it. If the user explicitly names an expert, honor that request unless it conflicts with safety or project constraints.

When third-party APIs or framework behavior may have changed, prefer official/current documentation. If a Context7-style MCP is not available, state that and use official docs or local package docs when possible.

Use `company-expert-routing` as the single source of truth for expert selection. Use `BUNDLES.md` for expert combinations and `EXPERTS.lock.md` to check source, pin, license, and review status for external expert skills. Prefer project-root files; if project files are missing, read the plugin-bundled fallback instead of disabling expert routing.

When using templates, prefer project-local `specs/global/assets/`; if project templates are missing, read the plugin-bundled fallback and remind the user to run `bootstrap-project` or `update-templates` to repair project assets.

Do not auto-update external expert skills. Use `company-skill-maintenance` and `company-skill-security-review` before adopting updates from open-source hubs or self-improvement output.

For user-friendly skill updates, use `company-skill-upgrade-runner`. It must fetch or inspect a candidate version, compare old and new versions, run security review, show the recommendation, and wait for explicit user confirmation before overwriting production skills.

Self-improvement is proposal-only by default. Use `company-skill-evolution-lab` to capture repeated workflow failures and propose reviewed changes; do not let skills rewrite themselves directly into production use.

## Verification

- Feature work needs tests when a test harness exists.
- Bug fixes need a reproduction or a clear evidence trail before code changes.
- Completion reports must include exact verification commands or manual checks.
- If automated verification is unavailable, provide a focused manual checklist.

## Documentation

- Company projects should keep `说明文档.md` or an equivalent progress document.
- Projects should keep a document ownership map, preferably in `specs/global/INDEX.md`.
- Documents at different levels must not share bare task numbers; spike tasks, feature tasks, version tasks, and project events must use separate namespaces.
- Versioned specs may use `specs/versions/<version>/<milestone>/`.
- Small changes may use one compact feature spec under `specs/features/<feature>/`.
- Public APIs and complex logic need comments; routine functions do not need boilerplate comments.
