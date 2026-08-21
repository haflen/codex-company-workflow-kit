---
name: company-thread-handoff
description: Use when a company project's long Codex conversation must continue, compact, fork with complete history, transfer into a clean conversation, or verify and resume an existing handoff.
---

# Company Conversation Continuity and Handoff

## Core Principle

Choose the continuity mechanism before deciding whether to summarize. Use native resume or fork for full history and a handoff capsule for a clean context. Current project facts override history and summaries; a handoff never grants new implementation authorization.

## Choose the User Outcome First

Users choose an outcome, not an implementation command. Act directly when intent is explicit; otherwise recommend one route and ask once.

| User outcome | Route | Summary |
| --- | --- | --- |
| Continue the same saved task | `resume` | None; continue the original task |
| Keep the task but reduce context pressure | `compact` | Prefer Codex `/compact`; fall back to `standard` handoff when unavailable |
| Open a new task without losing completed history | `fork` | Native fork; add only a final anchor not included in the fork |
| Open a clean task with selected state | `handoff` | `quick`, `standard`, or `decision-rich` capsule |
| Target task already exists | `handoff` | History cannot be injected retroactively; send one capsule and verify receipt |

Offer plain-language choices: continue the original task; compact and continue; create a new task with complete history; or create a clean handoff with decisions and progress.

Default recommendations: `compact` when the goal is unchanged and only length is a concern; `fork` when all history matters; `standard handoff` for a new milestone or lower token use.

## Native Codex Continuity

- `resume`: do not generate a handoff. Guide the user to resume the saved task or use an available native task control.
- `compact`: use only when the goal, scope, and active task remain stable. Preserve decisions, unfinished work, and authoritative project facts.
- `fork`: use only when the user explicitly requests a new task with complete completed history. If the source task is still running, the active turn is not copied; send a final anchor after it completes.
- If the required native control is unavailable, state the limitation and fall back to `handoff`. Never claim an unavailable action succeeded.

## Capsule Levels

- `quick`: low-risk discussion; goal, state, next action, key files, and immediate blockers.
- `standard`: default for code, configuration, dirty worktrees, phase transitions, or verification state; add decisions, constraints, authorization, evidence, unfinished work, and risks.
- `decision-rich`: product boundaries, architecture, business rules, calculations, data, security, production, cross-system work, multiple rejected options, or an explicit request not to repeat prior discussion; add rejected/deferred choices, reasons, disputes, and decisions that require new evidence to reopen.

Prefer recall over brevity when uncertain whether information affects later decisions.

## Build One Indivisible Capsule

1. Identify one active task. Mark side topics `related but out of current scope and unauthorized`.
2. Read only necessary project path, Git state, key files, authoritative documents, validation, and runtime state.
3. Separate verified facts, historical judgments, and unverified items. Do not invent interfaces, fields, criteria, or implementation choices.
4. Recheck phase permission and authorization; new scope is unauthorized by default.
5. Put startup instructions and state in one block. Do not split a short prompt from a separate summary.

### `quick`

Keep it to 8-12 short lines:

- Workflow layer: `company-thread-handoff`
- Continuity route: `handoff`
- Summary level: `quick`
- Generated at:
- Active task and goal:
- Current state / completed:
- Next action and done condition:
- Key files:
- Verified facts / historical judgments / unverified items:
- Side topics: related but out of current scope and unauthorized
- Knowledge boundary: knows capsule-covered decisions, not unrecorded verbatim dialogue

### `standard` additions

- Goal / Context / Constraints / Done when:
- Project path, branch, HEAD, and working tree:
- Workflow, phase permission, and implementation authorization:
- Confirmed decisions and hard boundaries:
- Authoritative requirements, design, tasks, business rules, and entry documents:
- Validation level, evidence, unverified work, and remaining risk:
- Unfinished work, blockers, next workflow:
- Running services, ports, browsers, and test processes:
- Documentation/implementation drift:

### `decision-rich` additions

- Rejected or deferred options, reasons, and reopening conditions:
- Historical disputes and final conclusions:
- Critical business rules, calculations, data, and permission boundaries:
- Confirmed statements likely to be misunderstood:
- Boundary of unrecorded historical information:

Every capsule instructs the target to validate project facts and restate the receipt fields before any high-risk action.

## Transport and Semantic Receipt

Show: `generated -> sent/manual paste -> read -> semantically verified/not verified`.

- Use `send_message_to_thread` only after explicit transfer intent and with a known target ID.
- Use `fork_thread` only after an explicit request for a new task with full history. Do not substitute an empty `create_thread`.
- Without task tools or a target ID, output one copyable capsule.
- After sending, use available `wait_threads` or `read_thread` to inspect the target response; otherwise mark receipt as pending user confirmation.

The target must restate:

1. Goal and done condition.
2. Confirmed decisions.
3. Hard constraints and scope.
4. Project, branch, working tree, key files, and validation state.
5. Unfinished work, risks, and next action.
6. Phase permission and implementation authorization.

On mismatch, send only a corrective delta and verify again. Do not ask the user to repeat the whole history.

After passing, use accurate wording:

```text
I understand the historical decisions and current state covered by the handoff capsule. I do not claim unrecorded verbatim history. Current project facts and authoritative documents remain the source of truth.
```

Do not say only “I do not know the history,” and do not claim knowledge outside the fork or capsule.

## Resume Preflight

Check generated time, goal, state, next action, summary level, and knowledge boundary. Verify path, branch, HEAD, working tree, key files, unfinished work, authoritative documents, and authorization. Report matching, changed, and unverified items, then complete the six-field receipt. Continue after low-risk differences, re-verify medium risk, and stop for high-risk branch, scope, authorization, key-file, or authoritative-document conflicts.


## Human-First Output

Start the final reply with `One-sentence conclusion`, `What was completed`, `What needs attention`, and `What the user should do now`. Use business outcomes and user impact, give one primary next action, and explain internal terms on first use. Then place Superpowers, expert calls, commands, paths, hashes, verification evidence, and internal workflow fields in a `Technical Audit Appendix`; Do not dump internal workflow fields one by one into the human summary or use audit fields as a substitute for it.

## Transparency

- Workflow layer: `company-thread-handoff`
- Continuity route: `resume / compact / fork / handoff`
- Summary level: `none / quick / standard / decision-rich`
- Native Codex capability: recommended / actually used / unavailable and fallback
- Superpowers overlay: usually none; continuity and fact transfer do not replace the formal workflow
- Transport status:
- Semantic receipt: passed / failed / pending
- Next step:

## File and Authorization Boundaries

- Do not write by default. On explicit request, only overwrite `.codex/handoff/current.md`.
- Do not create history files, modify `.gitignore`, archive into project documentation, or commit Git automatically.
- Creating, forking, or messaging another task requires explicit user intent.
- Do not replace `company-context-index`, formal requirements/design/tasks, or phase confirmation with a capsule.
- Never extend old implementation authorization to newly added scope.
