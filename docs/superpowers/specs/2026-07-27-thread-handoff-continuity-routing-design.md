# Thread Handoff Continuity Routing Design

## Goal

Make company conversation handoff choose the right continuity mechanism before generating a summary, and prove that a target conversation understood the transferred state.

## Problem

The existing `company-thread-handoff` always exports a `quick` or `full` summary. It cannot distinguish these different user outcomes:

- continue the same saved conversation;
- reduce context pressure without changing conversations;
- open a new conversation with the complete transcript;
- open a clean conversation with only task state.

This caused a real handoff to transport a detailed summary successfully while the target conversation still stated that it did not know the historical discussion. The failure was semantic rather than transport-related: the workflow promised a summary, while the user expected complete historical continuity.

## Design

### Continuity routes

The skill recommends one route and asks for confirmation only when the user's intent does not already select it:

| User outcome | Route | Summary |
| --- | --- | --- |
| Continue the same task later | `resume` | None |
| Keep the current conversation but reduce context | `compact` | Codex-native compaction |
| Open a new conversation with complete completed history | `fork` | Final anchor only when needed |
| Open a clean conversation with selected task state | `handoff` | `quick`, `standard`, or `decision-rich` |

Users choose the outcome, not the implementation command. When a target conversation already exists, history cannot be retroactively forked into it; use a single handoff capsule plus receipt verification.

### Summary levels

- `quick`: goal, state, next step, key files, and immediate blockers.
- `standard`: `quick` plus decisions, constraints, authorization, evidence, unresolved work, and risks.
- `decision-rich`: `standard` plus rejected/deferred options and reasons, disputes, knowledge boundaries, and decisions that must not be reopened without new evidence.

Default to `standard`. Use `decision-rich` for architecture, product boundaries, business rules, calculations, data, security, production, multiple rejected options, or explicit requests not to repeat prior discussion.

### Capsule contract

A handoff capsule is one indivisible block. It contains:

- goal, context, constraints, and done condition;
- project path, branch, working tree, authoritative documents, and key files when applicable;
- verified facts, prior judgments, confirmed decisions, rejected/deferred options, unresolved work, risks, and authorization;
- next workflow and next action;
- a knowledge boundary stating that the target knows the history covered by the capsule, not unrecorded verbatim dialogue.

### Receipt protocol

When task tools and a target ID are available, the workflow may send the capsule only after explicit user intent to transfer. The lifecycle is:

`generated -> sent -> read -> semantically verified`

The target must restate the goal, key decisions, constraints, current state, pending work, and authorization. A mismatch triggers a delta correction. Manual transfer uses the same capsule and requires the same receipt response in the target conversation.

### Project facts

Git, authoritative project documents, current files, and verification evidence remain the source of truth. A handoff is navigation and temporary task state; it does not replace project context or grant new implementation authorization.

## Company strictness

- Risk-based project preflight remains mandatory for `standard` and `decision-rich` handoffs.
- Scope changes invalidate old implementation authorization.
- A target must not execute side topics marked out of scope.
- High-risk verification differences stop execution for confirmation.

## Success criteria

- A request for complete historical continuity recommends `fork`, not a longer summary.
- A request for a clean new conversation recommends `standard` or `decision-rich` handoff.
- An existing target conversation receives one complete capsule and returns a semantic receipt.
- The target says it knows capsule-covered historical decisions while clearly limiting claims about unrecorded verbatim dialogue.
- Company and personal workflows share the model while preserving different strictness.
