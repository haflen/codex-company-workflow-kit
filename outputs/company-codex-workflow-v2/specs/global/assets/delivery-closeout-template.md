# Delivery Closeout Report

## Decision Summary

- User-visible result actually delivered:
- Code, document, script, and configuration artifacts:
- Verification level and result:
- Known remaining risk:
- Confirmation needed now: commit / push / do not release

## Metadata

- work-item-id:
- Feature/task batch/milestone:
- Owner:
- Status: awaiting closeout / verified / committed / pushed
- Last updated:
- Comparison baseline: initial edition, no comparison baseline / previous closeout report + Git commit
- Business branch:

## What Changed

| Change | Before delivery | After delivery | Reason | Impact |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Reading Guide

- Business/product: decision, delivered artifacts, remaining risk, and release state.
- Development: artifact relationship, cleanup, verification, commit, and push.
- QA/operations: evidence, migration, release, rollback, and observation.

## Artifact Relationship and Release Flow

This diagram answers: how do requirements, code, documents, scripts, and verification form a committable, releasable, and recoverable delivery?

```mermaid
flowchart LR
    BASE["Approved requirements/design/tasks"] --> CODE["Code and configuration artifacts"]
    BASE --> DOCS["Authoritative document artifacts"]
    CODE --> SCRIPTS["Versioned migration/data scripts<br/>when applicable"]
    CODE --> VERIFY["Automated and manual verification"]
    DOCS --> VERIFY
    SCRIPTS --> VERIFY
    VERIFY -->|pass| CLEAN["Clean temporary files and residual processes"]
    VERIFY -->|fail| STOP["Stop commit and repair"]
    CLEAN --> COMMIT["Local commit"]
    COMMIT --> PUSH["Push business branch"]
    PUSH --> OBSERVE["Release or later observation"]
```

Key conclusions:

- Documents, code, and versioned scripts form the delivery together; runtime success alone is insufficient.
- A failed verification cannot produce a completion claim.
- Temporary files, browser processes, and local services are cleaned within scope before commit.

## Delivered Artifact Inventory

| Artifact | Type | Path | Task/AC | Status | Explanation |
| --- | --- | --- | --- | --- | --- |
|  | code / document / config / script / data migration |  |  | complete / incomplete / not applicable |  |

## Cleanup and Repository Check

- Temporary files, generated output, and debug code:
- Local services, Playwright/browser, and residual processes:
- Pre-existing user changes in `git status`:
- Current change scope and unexpectedly large files:
- Versioned database scripts, checksums, and execution boundaries:

## Verification Evidence

| Test ID | Command/step | Expected | Actual | Evidence |
| --- | --- | --- | --- | --- |
| `TC-001` |  |  |  |  |

## Release, Commit, and Recovery

- Commit:
- Push branch and remote:
- Database/config/infrastructure state: generated in repository / executed in environment / not executed
- Release or deployment state:
- Rollback and recovery:
- Observation window and metrics:

## Remaining and Adjacent Work

| Item | Current scope | Risk | Owner | Follow-up entry |
| --- | --- | --- | --- | --- |
|  | no / yes |  |  |  |

## Traceability

| Object | Full reference | Document path or section |
| --- | --- | --- |
| Task | `<work-item-id>/T-001` |  |
| Verification | `<work-item-id>/TC-001` | Verification Evidence |

## Diagram Waiver

No waiver by default. After an explicit user request, record the user, waived artifact/release diagram, and reason.

## Human Readability Check

| Gate | Result | Evidence or explanation |
| --- | --- | --- |
| `DOC-G01`, `DOC-G04` | pass / waived / blocked |  |
| `DOC-G05` through `DOC-G12` | pass / blocked |  |

## Human Confirmation and Next Step

- Allow local commit: no / yes
- Allow push of the current business branch: no / yes
- Closeout state: incomplete / complete
- Recommended next step: repair blocker / commit / push / release observation
