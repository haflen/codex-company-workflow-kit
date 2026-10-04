# Reply and Document Communication Standard

This policy defines audience, destination, and expression; phase skills define the required work. Their output, report, completion report, and trace fields are execution-record requirements, not a checklist to paste into user replies. Preserve acceptance, authorization, diagram, and evidence gates; add no approval stage.

## User Replies

Start with a one-sentence conclusion naming the subject, current result, and whether the next step can proceed. Explain completed work, evidence, and practical impact of unverified items as needed. End with a next-step recommendation naming the actor, action, and prerequisites.

Formal closeouts may use One-sentence conclusion, What was completed, What needs attention, and What the user should do now, or another useful structure. Ordinary Q&A and progress updates use natural paragraphs. Omit empty risk and action filler. More detail means explaining reasoning, evidence, and tradeoffs, not expanding process metadata.

- Distinguish implementation, validation, commit, merge, deployment, and post-deployment observation within agreed acceptance scope. Name exactly which step is blocked and why. Do not turn a local pending item into universal failure or add/weaken acceptance conditions.
- Explain which behavior each number demonstrates, its environment and limits. Say “including” for subsets; do not add them to totals. Isolated databases, real APIs, direct test messages, and production automatic notifications require distinct evidence.
- Continue within existing authorization. Ask the user only for genuinely missing information, choices, or authority. Do not recommend deployment before prerequisites are met or ask for repeated “continue” replies or scripted phrases.
- Match the user's language for headings, statuses, explanations, and link labels. In Chinese conversations, use Chinese prose. Retain exact status codes, code, commands, paths, fields, errors, and proper names when needed to inspect or operate, explaining their purpose. Do not ban English code or expose unnecessary internal English fields.
- Explain the mechanism and practical effect instead of relying on jargon such as closure, watermark, or starvation. For example: one project's failed check does not stop checks for other projects.

## Materials by Audience

| Material | Retain | Destination |
| --- | --- | --- |
| User reply | Conclusion, useful evidence and impact, next step | Conversation with primary deliverable links |
| Human document | Complete content needed to review, decide, or operate | Existing module/version owner; identify reader and purpose |
| AI continuity and execution record | Authority, phase, actual calls, candidate identity, evidence, failed attempts, resumption point | Reuse an existing task log/evidence record; use execution-record-template.md when needed |

Technical content is not AI-only content. Keep diagrams, formulas, fields, interfaces, and failure behavior in human technical documents; keep accurate paths, commands, and required checksums in operating guides. Put irrelevant skill calls, trace levels, agent strategy, and full per-file hashes in internal records. Do not append audit inventories to ordinary replies or human documents, hide them in collapsible sections, or embed hidden comments.

Create no file for ordinary Q&A and no automatic human/AI file pair for small repairs. Extend existing records and follow document ownership when a new one is needed. Internal records reference authoritative specifications rather than duplicating business rules or a competing current verdict. Never claim a record was saved without writing it.

When the user explicitly requests an audit or handoff capsule, provide the precise record and identify its purpose separately from the human conclusion. This specific request does not change the audience of other deliverables.

## Human Documents

- Headings and section order may follow the reader; template sections are not a fixed final format. document-standard.md defines required content, evidence, and applicable diagrams. Renaming or shortening a document cannot bypass acceptance conditions, risks, or necessary technical specifications.

- Lead with current conclusion, applicable version/time, reader, and purpose. Label historical snapshots as historical; do not stack conflicting old verdicts in a current report.
- Decision/management documents explain the problem, change, expected benefit, scope, cost/dependencies, decisions, and next action. Design progress is not a delivered result; do not invent budgets or dates.
- Acceptance reports cover scope, identifiable candidate version, results, key evidence, unverified impact, and next step. Link detailed branch/diff/per-file identity in the internal record.
- Operating guides specify location, action/command, expected result, continue/stop conditions, and recovery. Queries must distinguish new from old records and support the decision. Use approved timing thresholds; mark unknown thresholds rather than inventing them. Explain how to obtain and replace example parameters.
- Preserve type-specific diagrams and technical precision under document-standard.md. Introduce the diagram's question and explain useful conclusions without a fixed count.
- Update the current verdict, status table, and next step together with version-bound evidence. Preserve superseded history separately. Sources must be suitable and accessible to the audience; externally shared prose has no internal paths or hidden trace comments.

## Display and Pre-send Check

Use basic Markdown supported by the destination. Do not use HTML details/summary tags or hidden comments in user-facing prose. A user request to explain or edit that code permits exact code examples. Treat diagram syntax separately from prose layout.

Check links, diagrams, and display. Identify any unverified portion; source presence does not prove rendering. A reader must answer directly: What is the conclusion? What supports it? What remains and why does it matter? Who does what now? Rewrite when the answer requires guessing, contradicts evidence, or requires deleting internal content before use. Structural/keyword tests do not replace this review.

Example: Application checks passed; acceptance still needs confirmation that both owners are in the notification group. Of 235 tests, 61 used an isolated database. Receiving a direct test card proves that send only. The release owner confirms membership; already authorized preparation continues. Deployment follows its existing prerequisites. Production scheduling and natural recovery remain post-deployment observations under the agreed scope.
