# Multi-agent delivery procedure

This is an operating reference for `company-expert-routing`, reached through `company-workflow-help`; it creates no skill, scheduler, daemon or agent runner. It adds no dependency, network requirement or approval stage. Follow DELEGATE-01, REVIEW-01 and the existing AUTH, FLOW, REPAIR and EVIDENCE rules. Role separation does not replace required quality validation.

Activation and disclosure follow the two execution choices in [workflow entry](../../company-workflow-help/SKILL.md). Users may use the ordinary workflow alone; enter this collaborative procedure only with explicit dispatch intent or effective task-scoped authority. Briefly disclose approach, roles and capabilities at the start and actual participation/checks at delivery; users do not fill in the internal task packet.

## 1. Establish the task and current capabilities

Reuse the user's actual request and confirmed specifications: goal, scope, acceptance criteria, endpoint and authority sources. “Use multiple agents to finish this task with independent review” is sufficient dispatch intent; no special phrase or repeated approval is needed. It does not by itself authorize an unconfirmed implementation, commit, push, merge, deployment, production operation or external message. Continue all authorized work to its endpoint; ask only for genuinely missing decisions or permissions.

Inspect the current host's tool descriptions for dispatch, communication, waiting, interruption, result inspection and command/session control. Record available and missing capabilities. Tool names and parameters vary by host: use their current schema, not copied API calls. Agent TOML files may supply role text only when verified; their presence does not prove automatic loading. Explicitly include the role instructions and task packet in each native dispatch. Record the actual returned agent ID and invocation evidence, not a proposed name alone. Do not create a separate user chat as a substitute or install/configure agents automatically.

If native dispatch is unavailable, the main agent completes permitted work serially and records `single-executor fallback`; its self-check is not independent review. If independent review is required for acceptance, that acceptance remains unmet, while other authorized work continues. Missing runtime control limits which long-running commands can safely be delegated; prefer bounded checks and disclose the limitation.

## 1a. From business materials through delivery

Users may provide business materials or an idea and request continuous multi-agent delivery without first writing specifications, splitting tasks or naming skills. Read authorized materials and existing artifacts, find the earliest missing phase, then follow this map. These are workflow descriptions, not new state enum values; business understanding uses existing context/requirements work and optional handoff adds no state. Reuse completed applicable work. One executor may span phases; do not create an agent for every phase.

| Phase | Existing workflow skill | Expert only when needed | Checkable handoff |
| --- | --- | --- | --- |
| Business understanding | [company-context-index](../../company-context-index/SKILL.md) | [business-analyst](../../business-analyst/SKILL.md): process, metrics or conflicting sources | Source path/version/location, facts versus inferences, conflicts, open decisions and original business intent |
| Requirements | [company-feature-requirements](../../company-feature-requirements/SKILL.md) | [product-manager](../../product-manager/SKILL.md): scope and acceptance; business-analyst for unresolved semantics | Stable requirement IDs, source meaning, scope/exclusions, AC, abnormal counterexamples and open decisions |
| Design | [company-feature-design](../../company-feature-design/SKILL.md) | This router's expert map for the actual stack and risk | Requirement IDs mapped to design/contracts/data flow/risks/test strategy and unresolved material choices |
| Planning | [company-feature-planning](../../company-feature-planning/SKILL.md) | Only unresolved technical or verification questions | Requirements/AC mapped to task IDs, allowed paths, dependencies, checks and counterexamples |
| Implementation | [company-implementation-runner](../../company-implementation-runner/SKILL.md) or [company-bugfix-runner](../../company-bugfix-runner/SKILL.md) for defects | Current stack expert; testing-qa for difficult test design | Task/requirement IDs mapped to actual changes, tests, raw output and unfinished work |
| Quality validation | [company-quality-validation](../../company-quality-validation/SKILL.md), under existing trigger rules | [testing-qa](../../testing-qa/SKILL.md): independent expectations, regression and counterexamples | Per-requirement/AC pass, fail or unverified evidence and impact on the final candidate |
| Closeout | [company-delivery-closeout](../../company-delivery-closeout/SKILL.md) | Only remaining risks that need expertise | Authorized endpoint, actual artifacts, acceptance evidence, remaining items and delivery limits |
| Handoff when needed | [company-thread-handoff](../../company-thread-handoff/SKILL.md) | Usually none | Original goal/requirement IDs and meaning, decisions/reasons, candidate, valid evidence, open items, authority and next action |

Actually read and apply the phase entry skill. Load experts only for the current concrete issue, never every skill in the table. Resolve links to verified exact paths before dispatch; a role name, skill name or table alone is not invocation. With confirmed requirements, start at the earliest missing design work; with valid design/tasks, enter implementation. Discussion-only requests create no formal documents; requirements-only authority stops after requirements. End-to-end authority and satisfied prerequisites allow FLOW-01/02 continuation without stage phrases. Ask only for missing business decisions, unresolved conflicting meaning or material new architectural tradeoffs; read available answers before asking again.

### Skill reading and application evidence

Within the existing section 3 `inputs`, list required skills by exact path and relevant sections (explicitly say full text when needed), applicable shared-rule sections, business source materials and upstream artifacts by path/version/location, requirement IDs/AC and open issues with their phase impact. Read permission must cover those sources; “use best practices” is insufficient, and agents must not search outside scope for skills. The main agent's prior read does not mean the child read it. The same agent may cite its actual prior read evidence for unchanged content instead of rereading.

Within the existing section 4 result and execution record, return actual read paths, content SHA-256, sections read, tool trace or original command-output location; specific rule applied mapped to artifact path/section or line; relevant rules not applied with reasons, and unread/unexecuted items. The main agent cross-checks current tool traces or retrievable raw outputs, file fingerprints and artifacts. Self-report, a hash list or a role name alone cannot prove skill application; hashes identify content, not reading or correct execution. If traces are inaccessible or output incomplete, retain the limitation and check affected items; missing evidence cannot pass.

If skills cannot be invoked, distinguish “actually read and applied bundled file rules” from “expert lens only”; neither claims native skill invocation. Disclose degradation for replaceable auxiliary expertise. Missing irreplaceable skills, required review or their necessary evidence leave the corresponding requirement unmet; continue independent authorized work without claiming that phase or overall acceptance. Do not change `task_state` schema or add packet fields.

### Preserve meaning and judge independently

Keep the same requirement IDs across “source location and original meaning → requirement/AC → design → task → implementation/tests → quality evidence → closeout or handoff.” The receiver checks upstream version, inherited scope, counterexamples, open issues and authority. Author summaries do not replace original materials; exclusions and unresolved inferences cannot become confirmed facts across phases. Preserve each conflicting source's origin, date and scope; precedence requires evidence, not just a later date overriding a still-applicable rule.

Review objects vary by phase: business/requirements review uses source meaning, scope, AC and exceptions; design/planning review checks coverage, contracts, dependencies and verifiability; implementation review and quality validation examine actual code/tests/runtime outputs. When review is needed, identify the relevant document/material or code snapshot by fingerprint. Do not force code diffs or one frozen-code procedure onto every phase, or require a separate review agent in every phase.

Requirements review follows [Independent coverage of original materials](../../company-feature-requirements/SKILL.md#independent-coverage-of-original-materials): first read only original materials to extract mandatory business relationships, key attributes and core user operations. Save the independent coverage basis and order evidence before reading author requirements and AC. Map each item to requirements/AC, omissions, unknowns or deferrals with source/authority and explainable boundaries. Test all author AC passing while original requirements remain omitted; unsupported omission or narrowing cannot pass. Keep unknown facts unconfirmed without imposing business rules or production algorithms. Disclose prior author-content contamination rather than backfilling records or adding rounds. Quality validation must revisit this basis and originals, not trust author AC alone. Then check facts presented as inferences or vice versa, ignored source conflicts, missing values treated as zero, abnormal data silently treated as normal, and scope/denominator drift. Report traceable alternatives for ambiguous business rules instead of selecting an answer. Quality validation inherits these counterexamples and independently derives expected results from original rules before comparing actual output. Passing author tests or agent voting cannot replace independent judgment. Findings retain requirement ID, source location, semantic conflict, counterexample and impact; use the bounded section 4 correction loop. Changes to original business rules require an actual decision source.

## 2. Select the smallest roles and schedule

| Role | Responsibility | Boundary |
| --- | --- | --- |
| Main agent | Own authority, shared contract, task state, dispatch, integration, evidence checks and final conclusion | Sole writer of shared state and acceptance decisions; child output is evidence to assess |
| Executor | Produce and verify the assigned phase artifact, return changed paths and raw evidence | No shared-state edits, acceptance changes, Git delivery or external effects beyond explicit packet authority |
| Independent reviewer | Read the current phase snapshot against source materials and acceptance, inspect applicable diffs and evidence, run permitted focused checks, return actionable findings | A different agent from the executor; read-only by default, no implementation fixes; ordinary independent review is not automatically blind review |
| Explorer, only when needed | Investigate a specific unresolved fact and return evidence or options | Read-only; no architecture/business decision or implementation authority; omit if existing evidence is sufficient |

When independent review is needed, use executor → current phase candidate → reviewer → main-agent acceptance; section 1a determines the phase. The main agent may itself execute and use a separate reviewer. Do not add agents just to fill roles. Apply REVIEW-01 only if blind review was actually requested.

Concurrent work requires independent inputs, disjoint write paths, no dependency on unfinished results and evidence of benefit under DELEGATE-01. With no comparable measurement, keep role handoffs sequential and make no speed claim. Never concurrently edit the same file, shared contract/state, migration or public-document section. Reviewing a changing candidate is not acceptance: freeze or finish affected edits first. A read-only explorer may run alongside independent work only when these conditions hold. Available slots are a limit, not a target.

## 2a. Minimal coordination across projects

Coordinate only projects authorized for this task; task names and tool visibility grant no access to others. Each project retains its own owner, authoritative task state and evidence. The coordinator reads concise status, dependencies and open decisions; executors receive narrow project inputs, not a giant context containing every project's full text.

Keep this summary in existing execution records; add no scheduling service or task_state fields:

| Project/task and state reference | Owner/sole writer | Priority and basis | Prerequisites/resume conditions | Exclusive resource and current holder | Current result/evidence | Next authorized action/actual open decision |
| --- | --- | --- | --- | --- | --- | --- |

Assign one authoritative state writer per task at a time. State the concurrency limit before dispatch, respecting user constraints and host capacity. Without comparable benefit evidence, proceed serially; do not dispatch to fill slots. Select the highest-priority ready task with available resources; retain existing order for ties without inventing business priorities. Independent authorized lower-priority work may continue while higher-priority work waits; record why.

Resources include write paths, shared state, ports, services, browser sessions and actions with the same external side effect. Verify actual ownership before acquiring a resource, with one holder only; an agent's completion text does not release it. After interruption/cancellation, verify real stopping under section 5; unknown stopping retains ownership and blocks dependent tasks while unrelated work continues. Before changing owners, verify the old executor and its work stopped, check existing results and record handoff. Prevent duplicate writes and operations.

Project owners verify their facts; the coordinator checks the candidate, state revision and evidence behind summaries. A stale summary triggers only the affected fact check, not a rerun of all projects. A missing business decision becomes one specific question with impact, not a stop for every project. Overall reporting aggregates results, choices/reasons, evidence, next actions and actual open decisions without replacing project acceptance.

Consolidate disputes into one feedback packet with original requirements/AC, fixed candidate, reproducible counterexample, raw output and impact. Apply focused section 4 correction; decide from recheck evidence, not role voting. With no new evidence or at the repair limit, stop debate, retain the unmet check and continue independent tasks without lowering acceptance.

## 3. Dispatchable narrow task packet

Copy this packet, fill from real sources, then append exactly the selected role instructions below. Keep unknown budgets unknown; no invented time/token limits. This is a dispatch record, not a new state schema: do not add fields or status values to an existing contract automatically.

```text
task_id: <existing task ID and scoped assignment>
role: <executor | independent reviewer | explorer>
authority_source: <retrievable user request / approved record, scope>
goal_and_endpoint: <specific outcome and authorized stopping point>
acceptance: <AC IDs, exact expected behavior and failure cases>
candidate_fingerprint: <actual revision plus dirty-file/content hashes; source paths>
inputs: <section 1a exact phase skill paths/sections, business sources, upstream artifacts, requirement IDs/AC, open issues and raw evidence>
allowed_paths: <complete permitted read/write paths, distinguish read-only>
forbidden_actions: <excluded paths, shared state, Git/external operations>
immutable_contract: <exact field names, types, values and closed status set>
editable_contract: <only permitted fields, body sections and file ranges>
verification: <commands/checks, cwd, required observations and raw log destination>
budget: <agreed time/token/attempt limits or unknown>
output_location: <return in agent response by default; exact path if authorized>
runtime_ownership: <how to register real session/process identity and stop it>
stop_conditions: <cancel, limit, scope conflict, unavailable dependency>
result_format: <use section 4; report unknowns instead of guessing>
```

Executor role text: “Read the phase skills and sources in inputs, produce this phase artifact and return rule-application evidence. Execute only this packet, preserving immutable fields exactly. Check the candidate and scope before editing. Do not alter acceptance or shared state. Run the specified verification and preserve actual outputs. Register any real long-running session/service before proceeding when the host permits. On conflict or cancellation stop affected work, retain artifacts and report actual runtime state. Return the result format; do not declare overall task completion.”

Reviewer role text: “Read the phase skills and original materials in inputs, independently derive expectations and counterexamples under section 1a, then check the phase candidate, acceptance and immutable fields. Inspect applicable artifacts, actual diffs and raw evidence; do not rely on executor conclusions. Do not edit implementation or shared state. Run only permitted focused checks. Return findings with path/location, concrete failure case, impact and required correction, or state no findings with coverage and limits. Check candidate identity again before returning. Do not claim blind review unless REVIEW-01 was satisfied.”

Explorer role text: “Read applicable skills and sources in inputs and return applied rules with evidence. Answer only the specified unresolved question using scoped evidence. Do not edit files or decide unconfirmed business rules. Return sources, observed facts, unknowns and effect on this task; do not expand the assignment.”

## 4. Result contract and one correction cycle

Return section 1a skill-read/application evidence and requirement-meaning traceability, plus actual `task_id`, `result_id`, agent ID, role, input and output `candidate_fingerprint`, changed/read paths, acceptance mapping, immutable-field check, raw verification evidence, findings, unknowns, remaining runtime identities and next action. For each check retain command, cwd, actual start/end, exit code and original stdout/stderr or their retrievable location. Include actual elapsed time and limits consumed when available; never fabricate token use. A result marker such as DONE is not evidence or a new persisted status value.

Bind raw records to the tested command's actual executed argv and cwd, not assumptions from the outer capture command. For sample properties such as encoding, check the actual input bytes against the property before the existing execution. Capture corrections recheck only affected cases; preserve and distinguish each round's raw results instead of overwriting prior rounds, and reuse valid evidence when the candidate and applicability conditions are unchanged.

The main agent checks skill use and requirement traceability under section 1a, then identity, scope, fixed fields, raw results and candidate freshness. Duplicate result IDs do not cause repeated integration. If results conflict, retain both and investigate only the disputed facts. Quarantine out-of-scope changes for inspection; do not overwrite user work or silently adopt them.

For ordinary in-scope findings, send the executor one consolidated feedback packet containing the concrete defects, original AC, unchanged immutable contract, permitted correction scope and recheck command. Allow one local correction cycle; review the changed portions against the new fingerprint and rerun affected checks. Do not restart the entire task or alter fixed fields to satisfy a score. If still failing, stop redispatch loops and use bounded serial repair under the existing repair policy. A main-agent fix invalidates affected reviewer evidence; if independent review is required, a separate reviewer must check that final candidate within existing limits, otherwise report the unmet review. Missing business decisions or new scope go to the user while unaffected work continues. One correction cycle is not authorization for unlimited retries.

## 5. Long-running work, cancellation and recovery

Before a delegated long command/service starts, arrange recording of the actual tool session ID and, where available, process ID plus start time, command, cwd and ownership link to this task. Register the returned identity immediately. A PID alone can be reused; never infer ownership from a number or an old log. Use current host mechanisms and existing task records, not a new background controller. If identity/control cannot be established, do not launch unsafe unattended work; use a bounded alternative within scope or leave that check pending.

On cancellation or budget exhaustion, the main agent stops new dispatches and dependent actions, requests the actual task agents to stop, and checks their known owned sessions/services through native controls. Preserve useful artifacts and raw results. An agent marked interrupted, cancelled or completed does not prove its shell command, child process or service has stopped. Confirm current session termination/exit and, when applicable, absence of the identified owned process or service. If stop evidence is unavailable or contradictory, record `stop unverified` in the execution note: do not redispatch that work or release its dependent resources/actions. Continue only independent work. Never kill an unowned or out-of-scope PID, use broad process-name matching, import an experimental `stop_gate` script as a general process killer, or treat historical logs as current stop evidence. If stopping needs missing authority, report the exact owned runtime and required action.

On recovery, inspect current user intent, authorization, candidate fingerprints, actual agents/sessions/processes, existing results and task state before acting. Cancellation remains effective until the user actually resumes; old records cannot reactivate work. Investigate unknown side effects without replaying them. Once stopping is verified and resumption authorized, select only unfinished affected work; reuse valid evidence and recheck drift. Keep past IDs and evidence, and record the new assignment identity. Failed or inaccessible checks remain unverified, not accepted.

## 6. Acceptance, closeout and measurement

The main agent maps each AC to final-candidate evidence, checks immutable fields and permitted changed paths, confirms required independent review, and applies the existing `company-quality-validation` trigger rules. Review findings alone are not integrated acceptance, and local tests are not real API or production evidence. Resolve or explicitly report remaining failures and live runtimes. Required missing evidence blocks the corresponding acceptance.

Start at the earliest missing business/requirements/design/planning phase and its workflow, then continue through implementation/bugfix, required validation and `company-delivery-closeout` to the already authorized prepare/commit/deliver endpoint. Reuse existing state tools only in their supported schema and revision protocol; the main agent is the sole writer. Do not hand-edit state, introduce new status values, commit/push automatically, or treat role separation as permission for external business operations. No new approval gate is introduced.

In the existing execution record capture actual start/end and wall elapsed time; per-role execution, coordination/wait and correction time; user intervention count and reasons; AC pass/fail/unverified counts; reruns, changed candidate IDs and capability limits. Separate missing-decision requests from avoidable repeat approvals. Do not sum overlapping role times as wall time. Unknown measurements remain unknown. Claim speed improvement only with comparable acceptance, scope, environment and evidence completeness, including coordination and rerun costs; a single example is not general performance proof.

The user-facing result states the delivered outcome, authorized endpoint reached, actual role use or fallback, verification and review coverage, remaining limitations and one next action. Distinguish implementation, review, acceptance, commit, push and deployment. Do not stop at a proposed next phase when authorized work remains executable.
