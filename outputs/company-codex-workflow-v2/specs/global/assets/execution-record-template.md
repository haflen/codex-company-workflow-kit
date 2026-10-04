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
|  |  | scope change / verification failure / V3 / user confirmation / local resource anomaly |  |
