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

| ID | Task | Files / modules | Estimated validation level | Continuous eligibility | Subagent strategy | Minimal failing case or verification anchor | Adversarial scenario | Chinese comment coverage | Documentation drift check | Depends on |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T1 |  |  | V0/V1/V2/V3 | continuous / careful-continuous / must-stop | not needed / implementation / investigation / spec review / code-quality review / parallel forbidden |  |  | business rules / calculation semantics / data mapping / exceptional branch / none |  |  |

## AI Execution Notes

- Keep edits scoped to the task ID being executed.
- Do not advance to the next task when verification for the current task fails.
- Batch only tasks marked `continuous` or `careful-continuous` after explicit user authorization.
- Stop on `must-stop`, scope change, verification failure, V3 risk, user confirmation point, or local resource anomaly.
- Record any assumption changes as a requirement or design update.
- Formal tasks do not inherit spike-internal work-log IDs; create a new formal task namespace when converting spike output into production work.
- Use subagents only for independent implementation, independent investigation, or independent review. Forbid parallel subagents when tasks edit the same file, state model, database migration, API contract, or public-doc section.
- The main agent must review subagent diffs, verification evidence, documentation drift, and remaining risk.
- Tasks that add or move engineering assets must use complete repository-relative paths and list allowed plus forbidden roots; never use only short paths such as `contracts/` or `scripts/`.
- Run the asset placement gate against all planned paths before implementation. Blocking issues return to design/planning instead of entering code.
- Actual subagent invocation requires an explicit user request. For stable company roles, first run `bash scripts/install.sh install-agents <project-path> --lang en` to generate `.codex/agents/`.

## Asset Placement Plan

- Boundary config: `.codex-workflow/asset-boundaries.json`

| Task ID | Planned path | Allowed roots | Forbidden roots | Config status | Gate result |
| --- | --- | --- | --- | --- | --- |
|  |  |  | `specs/`, `docs/`, or project-declared roots | draft / confirmed | passed / blocked / not triggered |

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

## Continuous Implementation Plan

| Task range | Continuous allowed | Stop conditions | Recommended phrase |
| --- | --- | --- | --- |
|  |  | scope change / verification failure / V3 risk / user confirmation / local resource anomaly | `任务已确认，连续完成后续所有可执行任务；遇到范围变化或验证失败再停。` |

## Subagent Split Plan

Subagent capability status:

| Task range | Subagent recommended | Subagent role | Allowed files | Prohibited actions | Main-agent review method |
| --- | --- | --- | --- | --- | --- |
|  | not needed / recommended / strongly recommended | implementation / investigation / spec review / code-quality review / test-strategy review |  |  | diff / verification evidence / documentation drift / remaining risk |

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
