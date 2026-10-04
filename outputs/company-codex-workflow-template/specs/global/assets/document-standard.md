# Company Formal Document Reading and Diagram Standard

## Scope

This standard applies to new or materially updated requirements, business rules, technical designs, data models, API contracts, task plans, spikes, hotfixes, requirements prototype records, delivery closeouts, project context indexes, acceptance reports, operating guides, and management reports. It does not automatically rewrite historical documents.

Apply human-output-standard.md to identify audience and purpose. Keep execution records separate; retain identifiers, fields, formulas, and diagrams needed for engineering review.

## Organize for the Reader

Headings may be renamed, sections combined, and their order changed. Templates provide a starting structure; check completeness of content rather than literal headings. Lead with the conclusion and impact; retain applicable evidence, risks, and the owner of the next action. The following reading order is a suggestion; keep applicable content and honor a structure explicitly requested by the user.

1. Decision Summary.
2. What Changed.
3. Reading Guide and legend.
4. Core Mermaid diagrams.
5. Scenarios, flows, and logic.
6. Detailed specification.
7. Exceptions, risks, and verification.
8. Review decision and next step.

## Metadata and Trace IDs

Each feature or milestone in engineering specifications defines a stable `work-item-id`. Acceptance reports retain the related task and candidate version. Operating guides and management reports cite existing tasks, versions, or sources as needed without inventing IDs to fill a template. Cross-document references use `<work-item-id>/<local-id>`.

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

A version-change review must explain changes against the last approved version, their reasons, impact, and a verifiable baseline. Use a table for multiple changes or prose for a single change. Cite the applicable version, source path, or Git commit; disclose unknown baselines. First drafts do not require a change table. Operating guides and management reports include comparisons only when reviewing version changes. The template heading `What Changed` has no fixed position.

| Change | Previous | Current | Reason | Impact |
| --- | --- | --- | --- | --- |

## Mermaid Rules

- State the question before each diagram and explain the conclusions the reader needs, without a fixed count.
- Prefer business labels; place code, table, or endpoint names on the second line or in parentheses.
- Each diagram answers one main question. Split diagrams with more than roughly 20 nodes into overview and detail views.
- Do not use color as the only carrier of meaning; combine labels, line styles, and text.
- Use the table below to determine diagram requirements. Documents serving multiple purposes retain each applicable requirement. A management report does not replace a technical design; changing its name cannot bypass required diagrams or evidence.
- When rendering cannot be checked, state `Mermaid rendering: unverified`; do not claim success.

## Diagrams by Document Purpose

| Type or purpose | Required diagrams and content |
| --- | --- |
| Requirements and business rules | Retain the relevant business flow and key decisions |
| Technical design | Retain architecture and `sequenceDiagram`; check each separately |
| Data model and API contract | Data models retain relationships and data formation sequences; API contracts retain interaction sequences |
| Tasks, prototypes, spikes, hotfixes, closeouts, and project indexes | Retain dependency, business-flow, experiment, repair, artifact-relationship, or reading-route diagrams defined by the relevant template; do not combine every template requirement into one document |
| Acceptance report | Retain scope, candidate, results, evidence, and unverified impact; use a flow diagram for cross-phase acceptance, delivery, and post-deployment observation, and an evidence table for a single result check |
| Operating guide | Use steps and decision tables for sequential operations, retaining location, commands, expected results, stop conditions, and recovery; add a flow diagram for cross-role handoffs or recovery loops |
| Management report | Use a responsibility diagram for architecture roles and a progression diagram for staged delivery; status, risk, or decision reports may use prose and tables without engineering sequence diagrams |

Not applicable is not a diagram waiver: first determine requirements from purpose and actual content. Do not delete previously confirmed or user-requested diagrams to shorten a document. Waiving an applicable diagram still follows the next section.

## Diagram Waiver

A waiver is valid only when the user explicitly says a specific diagram is not needed. Record the user, diagram, and reason. The AI cannot waive a diagram because work is small, time is short, or the technical path is unique.

## Complexity and Length

- L1 may combine adjacent sections but keeps the conclusion, required diagram, key rules, verification, and next step.
- L2 covers the complete applicable content for its document type; headings and order may follow reader needs.
- L3 adds depth for cross-domain relationships, migration, concurrency, recovery, versioning, and consistency.

Complexity changes depth, not diagram or evidence requirements.

## Document Quality Gates

| Gate ID | Check | Pass condition |
| --- | --- | --- |
| `DOC-G01` | Conclusion content | The opening explains problem, conclusion, and impact; the body provides evidence, remaining work, and the next owner/action, plus any pending decision; no literal heading is required |
| `DOC-G02` | Requirements diagram | A target business-flow Mermaid diagram exists, or the user explicitly waived it |
| `DOC-G03` | Technical diagrams | Architecture and `sequenceDiagram` blocks both exist, or have separate waivers |
| `DOC-G04` | Type-specific diagram | Include diagrams applicable to purpose and content; missing required diagrams need explicit user waivers, not a document rename |
| `DOC-G05` | Waiver | User, object, and reason are recorded; AI-only judgment is invalid |
| `DOC-G06` | Diagram-text consistency | Diagram nodes, states, tables, and interfaces are explained in text |
| `DOC-G07` | Main and exception paths | Normal behavior and important failures are explicit |
| `DOC-G08` | Trace format | Local IDs use the defined format; cross-document references include `work-item-id` |
| `DOC-G09` | Trace completeness | Flows, rules, ACs, design, tasks, and tests can locate one another |
| `DOC-G10` | Visible result | Technical structure traces to a page, API, or business result |
| `DOC-G11` | Rendering | Mermaid rendering was checked, or is explicitly marked unverified |
| `DOC-G12` | Drift | Documents, scripts, code, and actual paths do not visibly conflict |

Diagram gates apply only to the corresponding document purpose and content. DOC-G11 is not applicable when no diagram is required or included; still check prose display under human-output-standard.md. Trace gates check engineering specifications, acceptance relationships, or source citations as appropriate, without requiring management reports to add engineering ID matrices. Structural checks do not replace evidence review.

## Workflow Responsibility

- `company-feature-requirements`: `DOC-G01`, `DOC-G02`, and `DOC-G05` through `DOC-G12`; add `DOC-G04` when business rules are created.
- `company-feature-design`: `DOC-G01`, `DOC-G03`, and `DOC-G05` through `DOC-G12`; add `DOC-G04` for data models or separate API contracts.
- Planning, prototype, spike, context index, and closeout: `DOC-G01` and `DOC-G04` through `DOC-G12`.
- Bugfix checks `DOC-G06` through `DOC-G12` within the affected scope. New standalone formal Bugfix/Hotfix reports also check `DOC-G01`, `DOC-G04`, and `DOC-G05`, including a Mermaid problem-to-cause-to-fix-to-verification diagram. Updating task/fix-log entries does not trigger a full historical rewrite; see document-ownership.md for record size.
- Implementation checks only authoritative documents changed in the current run: `DOC-G06` through `DOC-G12`.
- Health check diagnoses `DOC-G01` through `DOC-G12` and reports by default without rewriting.

## Human Reading Check

Structural gates do not replace judgment. Before the phase ends, confirm that business, product, development, and QA can reach the same understanding from the conclusion, diagrams, details, and trace links.
