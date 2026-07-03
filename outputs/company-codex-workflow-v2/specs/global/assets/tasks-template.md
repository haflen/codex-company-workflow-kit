# Task Plan

## Metadata

- Feature:
- Owner:
- Status: draft / confirmed / in progress / complete
- Formal task numbering namespace: for example `FEAT-xxx`
- Requirements:
- Design:

## Preconditions

- Requirements confirmed:
- Design confirmed:
- API contract confirmed, if applicable:
- Test strategy confirmed:

## Implementation Tasks

| ID | Task | Files / modules | Estimated validation level | Minimal failing case or verification anchor | Adversarial scenario | Chinese comment coverage | Documentation drift check | Depends on |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T1 |  |  | V0/V1/V2/V3 |  |  | business rules / calculation semantics / data mapping / exceptional branch / none |  |  |

## AI Execution Notes

- Keep edits scoped to the task ID being executed.
- Do not advance to the next task when verification for the current task fails.
- Record any assumption changes as a requirement or design update.
- Formal tasks do not inherit spike-internal work-log IDs; create a new formal task namespace when converting spike output into production work.

## Verification Plan

| Check | Command or manual step | Expected result |
| --- | --- | --- |
|  |  |  |

## Validation Level Notes

- V0: docs, comments, formatting, or no-behavior changes.
- V1: low-risk isolated changes.
- V2: standard feature work or ordinary bugfix.
- V3: production, permission, security, data, performance, money/metric formulas, cross-system work, or hotfix.

The final validation level is confirmed by implementation or bugfix before completion.

## Documentation Drift Check

| Change Type | Affected | Documents To Update |
| --- | --- | --- |
| Requirements / AC |  |  |
| Business rules / calculation semantics |  |  |
| Technical design / API contract |  |  |
| Project entry / INDEX / public-doc update patch |  |  |

## Chinese Code Logic Comment Plan

| Comment Trigger | In Scope | Location Or Notes |
| --- | --- | --- |
| Business rules / state branches / permission differences |  |  |
| Formulas / thresholds / precision / sorting weights |  |  |
| Data source / field mapping / enum mapping / DTO mapping |  |  |
| Fallback / hiding / degradation / empty data / compatibility strategy |  |  |
| Performance / concurrency / cache / retry / rendering strategy |  |  |

## Adversarial Review Plan

| Risk type | Scenario | Check method |
| --- | --- | --- |
| Extreme input / abnormal state / permission / concurrency / performance / UI rendering |  |  |

## Completion Evidence

- Commands run:
- Manual checks:
- Screenshots or logs:
- Known residual risk:

## Human Confirmation

Implementation is complete only after the agreed verification evidence is recorded.
