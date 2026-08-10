# Company Formal Document Reading and Diagram Standard

## Scope

This standard applies to new or materially updated requirements, business rules, technical designs, data models, API contracts, task plans, spikes, hotfixes, requirements prototype records, delivery closeouts, and project context indexes. It does not automatically rewrite historical documents.

## Shared Reading Order

1. Decision Summary.
2. What Changed.
3. Reading Guide and legend.
4. Core Mermaid diagrams.
5. Scenarios, flows, and logic.
6. Detailed specification.
7. Exceptions, risks, and verification.
8. Review decision and next step.

## Metadata and Trace IDs

Each feature or milestone defines a stable `work-item-id`. Cross-document references use `<work-item-id>/<local-id>`.

| Object | Local ID | Full reference example |
| --- | --- | --- |
| Flow node | `F-nnn` | `STP-M1/F-001` |
| Business rule | `BR-nnn` | `STP-M1/BR-001` |
| Acceptance criterion | `AC-nnn` | `STP-M1/AC-001` |
| Design decision | `D-nnn` | `STP-M1/D-001` |
| API contract | `API-nnn` | `STP-M1/API-001` |
| Implementation task | `T-nnn` | `STP-M1/T-001` |
| Test or verification | `TC-nnn` | `STP-M1/TC-001` |

Published IDs remain stable when sections are reordered. Retired objects keep their IDs and status. Cross-document references also include a document path or section link.

## What Changed

Place `What Changed` immediately after `Decision Summary`. Metadata records the comparison baseline as the previous approved path and Git commit. First editions state `Initial edition; no comparison baseline`.

| Change | Previous | Current | Reason | Impact |
| --- | --- | --- | --- | --- |

## Mermaid Rules

- State the question before each diagram and give three to five conclusions after it.
- Prefer business labels; place code, table, or endpoint names on the second line or in parentheses.
- Each diagram answers one main question. Split diagrams with more than roughly 20 nodes into overview and detail views.
- Do not use color as the only carrier of meaning; combine labels, line styles, and text.
- Requirements use business flows; technical designs use architecture and sequence diagrams; data models use relationship and formation flows; other documents use their defined diagram type.
- When rendering cannot be checked, state `Mermaid rendering: unverified`; do not claim success.

## Diagram Waiver

A waiver is valid only when the user explicitly says a specific diagram is not needed. Record the user, diagram, and reason. The AI cannot waive a diagram because work is small, time is short, or the technical path is unique.

## Complexity and Length

- L1 may combine adjacent sections but keeps the conclusion, required diagram, key rules, verification, and next step.
- L2 uses the complete template.
- L3 adds depth for cross-domain relationships, migration, concurrency, recovery, versioning, and consistency.

Complexity changes depth, not diagram or evidence requirements.

## Document Quality Gates

| Gate ID | Check | Pass condition |
| --- | --- | --- |
| `DOC-G01` | Conclusion structure | `Decision Summary` is non-empty and covers problem, decision, impact, and confirmation |
| `DOC-G02` | Requirements diagram | A target business-flow Mermaid diagram exists, or the user explicitly waived it |
| `DOC-G03` | Technical diagrams | Architecture and `sequenceDiagram` blocks both exist, or have separate waivers |
| `DOC-G04` | Type-specific diagram | Data and other formal documents contain their required diagram type, or an explicit waiver |
| `DOC-G05` | Waiver | User, object, and reason are recorded; AI-only judgment is invalid |
| `DOC-G06` | Diagram-text consistency | Diagram nodes, states, tables, and interfaces are explained in text |
| `DOC-G07` | Main and exception paths | Normal behavior and important failures are explicit |
| `DOC-G08` | Trace format | Local IDs use the defined format; cross-document references include `work-item-id` |
| `DOC-G09` | Trace completeness | Flows, rules, ACs, design, tasks, and tests can locate one another |
| `DOC-G10` | Visible result | Technical structure traces to a page, API, or business result |
| `DOC-G11` | Rendering | Mermaid rendering was checked, or is explicitly marked unverified |
| `DOC-G12` | Drift | Documents, scripts, code, and actual paths do not visibly conflict |

## Workflow Responsibility

- `company-feature-requirements`: `DOC-G01`, `DOC-G02`, and `DOC-G05` through `DOC-G12`; add `DOC-G04` when business rules are created.
- `company-feature-design`: `DOC-G01`, `DOC-G03`, and `DOC-G05` through `DOC-G12`; add `DOC-G04` for data models or separate API contracts.
- Planning, prototype, spike, context index, and closeout: `DOC-G01` and `DOC-G04` through `DOC-G12`.
- Bugfix checks `DOC-G06` through `DOC-G12`; add `DOC-G01`, `DOC-G04`, and `DOC-G05` for a hotfix report.
- Implementation checks only authoritative documents changed in the current run: `DOC-G06` through `DOC-G12`.
- Health check diagnoses `DOC-G01` through `DOC-G12` and reports by default without rewriting.

## Human Reading Check

Structural gates do not replace judgment. Before the phase ends, confirm that business, product, development, and QA can reach the same understanding from the conclusion, diagrams, details, and trace links.
