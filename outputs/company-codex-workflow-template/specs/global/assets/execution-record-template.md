# Internal Execution and Continuity Record

For AI continuity and audit. Extend existing records; do not create one for every reply. Human documents link required evidence. Specifications remain authoritative; update the human report when the conclusion changes.

## Ownership and Authority

- work-item-id:
- owner-path:
- record-path:
- release-target:
- Authoritative task/specification, human report, applicable version:
- Phase, existing authority, actions not authorized:
- Current result, next execution point, prerequisites, owner:
- Closing state: continue execution / await user / complete; match the conversational next step, record observation triggers, and reuse existing authority.

## Contract and State References

- Task contract: [template](task-contract-template.md); location of the adopted contract:
- Multi-stage state: `.codex-workflow/tasks/<task-id>/state.json`; current revision and actual latest validation:
- Evidence directory or original record links:

When structured state is used, reference its contract, state and evidence instead of maintaining a second progress or authorization list. Without state tooling, continue this record and disclose that structured validation has not run.

## Capability and Verification

- Workflow layer:
- Trace mode: light / full-audit; trigger:
- Superpowers layer:
- Actual calls:
- Expert/plugin capabilities:
- Not called, lens only:
- Validation level, environment, commands, actual results, evidence links:
- Unverified items, phase impact, follow-up validation:
- Diagram rendering and human-reading review:

## Final Candidate Identity

- Current branch and HEAD commit:
- Validated paths:
- Diff SHA-256: from `git diff --binary HEAD -- <validated paths>`
- Untracked file paths and SHA-256:
- Artifact checksums and evidence applicability:

## Continuity and History

- Failed attempts, outcomes, recovery:
- Superseded conclusions, timestamps, version-bound evidence:
- Other phase-specific audit fields: add applicable facts, never invent calls/results.

## Task Execution Arrangement (when applicable)

### Subagent Arrangement

| Task scope | Recommendation | Role | Allowed files | Forbidden work | Main-agent review |
| --- | --- | --- | --- | --- | --- |
|  | none / recommended / strongly recommended | implementation / investigation / spec / quality / test |  | shared state, same migration, and same contract cannot run in parallel | diff / verification / drift / risk |


### Continuous Execution and Stop Conditions

| Task scope | Continuous | Stop condition | User authorization |
| --- | --- | --- | --- |
|  |  | unauthorized scope / missing business decision / permission or file conflict / exhausted repairs / local resource limit |  |

Handle ordinary failures with bounded repair under REPAIR-01 in the [task execution policy](task-execution-policy.md). Keep item-by-item V3 review and full verification without repeated confirmation solely because of the risk level. Stop only affected actions; continue independent authorized work.
