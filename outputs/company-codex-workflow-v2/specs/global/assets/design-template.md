# Technical Design

## Metadata

- Feature:
- Owner:
- Status: draft / confirmed / changed
- Last updated:
- Requirements:

## Summary

State the chosen approach in a few sentences.

## Context Used

- Requirements:
- Business rules and calculation semantics:
- Existing source paths:
- Existing patterns:
- External docs checked:

## Non-Goals

- 

## Architecture and Data Flow

Describe the components, responsibilities, and data flow. Include diagrams only when they reduce ambiguity.

## API or Module Contracts

Use `api-contract-template.md` for service, frontend/backend, or module boundaries.

## Data and State

- Data model changes:
- State transitions:
- Persistence/cache behavior:

## Business Rules Mapping

| Rule/formula/operation | Source document location | Technical carrier | Verification method |
| --- | --- | --- | --- |
|  |  |  |  |

## First Principles Check

- Underlying facts:
- Key constraints:
- Minimum conditions:
- Evidence that would disprove this design:

## Solution Comparison Decision

| Decision item | Triggered | Notes |
| --- | --- | --- |
| Large feature module, core page, core workflow, or subsystem | No / Yes |  |
| Crosses frontend/backend, services, data model, permissions, security, performance, cache, concurrency, or external API | No / Yes |  |
| Involves business rules, calculation semantics, state machine, approval flow, task flow, or complex data mapping | No / Yes |  |
| Clear tradeoff between fast delivery and long-term maintainability | No / Yes |  |
| Affects extensibility, migration, testing, rollout/recovery, or team ownership boundaries | No / Yes |  |
| Requires solution comparison | No / Yes |  |

If comparison is not needed, state why. Suggested format: `Solution comparison: skipped, reason: L1 small change, single obvious technical path, low risk.`

## Implementation Approach

1. 

## Alternatives Considered

When L2/L3 solution-comparison conditions are hit, list at least 2 options. Large or high-risk designs should list 3 options.

| Option | Best fit | Pros | Cost/risk | Decision |
| --- | --- | --- | --- | --- |
| Recommended option: |  |  |  |  |
| Alternative A: |  |  |  |  |
| Alternative B: |  |  |  |  |

## User Confirmation Point

- Recommended option:
- Questions requiring user confirmation:
- Confirmed for task planning: No / Yes

## Risks and Mitigations

| Risk | Impact | Mitigation | Owner |
| --- | --- | --- | --- |
|  |  |  |  |

## Test Strategy

- Unit:
- Integration:
- E2E/manual:
- Regression:
- Adversarial review:

## Rollout and Recovery

- Rollout plan:
- Feature flag or config:
- Rollback:
- Data recovery:

## Human Confirmation

Design is ready for task planning when contracts, risks, rollout, and verification strategy are explicit.
