# Reply and Document Communication Standard

This policy defines audience, destination, and expression; phase skills define the required work. Their output, report, completion report, and trace fields are execution-record requirements, not a checklist to paste into user replies. Preserve acceptance, authorization, diagram, and evidence gates; add no approval stage.

At workflow task start, follow entry rules to briefly state ordinary workflow or multi-agent collaboration, responsible roles and relevant capabilities; at delivery report actual usage and check results. Keep this short user disclosure visible while internal skill identifiers, paths, trace levels and detailed audits stay in execution records. Ordinary Q&A needs no repeated mode declaration; authorized collaboration needs no extra confirmation.

## User Replies

Start with a one-sentence conclusion naming the subject, current result, and whether the next step can proceed. Explain completed work, evidence, and practical impact of unverified items as needed. End with a next-step recommendation naming the actor, action, and prerequisites.

Formal closeouts may use One-sentence conclusion, What was completed, What needs attention, and What the user should do now, or another useful structure. Ordinary Q&A and progress updates use natural paragraphs. Omit empty risk and action filler. More detail means explaining reasoning, evidence, and tradeoffs, not expanding process metadata.

- Distinguish implementation, validation, commit, merge, deployment, and post-deployment observation within agreed acceptance scope. Name exactly which step is blocked and why. Do not turn a local pending item into universal failure or add/weaken acceptance conditions.
- Explain which behavior each number demonstrates, its environment and limits. Say “including” for subsets; do not add them to totals. Isolated databases, real APIs, direct test messages, and production automatic notifications require distinct evidence.
- Continue within existing authorization. Ask the user only for genuinely missing information, choices, or authority. Do not recommend deployment before prerequisites are met or ask for repeated “continue” replies or scripted phrases.
- Match the user's language for headings, statuses, explanations, and link labels. In Chinese conversations, use Chinese prose. Retain exact status codes, code, commands, paths, fields, errors, and proper names when needed to inspect or operate, explaining their purpose. Do not ban English code or expose unnecessary internal English fields.
- Explain the mechanism and practical effect instead of relying on jargon such as closure, watermark, or starvation. For example: one project's failed check does not stop checks for other projects.

## Next Step at Phase Closeout

At phase completion, delivery summary, a blocking stop, or an answer to “what next”, put the next step in the last standalone paragraph beginning with **Next step:**. Give one primary action, its owner, and necessary prerequisites; explicitly state when the user has no action. This does not impose fixed headings on the body. Localize the label to the user's language, using **下一步：** in Chinese.

| Current state | Closing content and execution |
| --- | --- |
| Already authorized and prerequisites met | State “I will next…” with a concrete action and continue within that authority; do not end the task at a progress update or wait for another “continue” |
| User action required | Specify the missing information, decision, or action and which step it blocks; request only what is missing, with no new approval gate or wider authority |
| Agreed scope complete | State “This task is complete; no action is needed from you now”; do not invent extra work to fill a next step |

Ordinary Q&A and progress updates stay concise without a mandatory closing paragraph; use the table when a phase actually closes or work is blocked. For previously agreed observation or acceptance that cannot yet run, give its trigger and owner; do not promise automatic monitoring or future notifications without an actual execution mechanism. Distinguish candidate fixes, branch integration, commit, push, and deployment; unfinished agreed delivery is not “all complete”.

Before sending, check that the reader can immediately find the next step, its owner, and whether they must act. Rewrite that paragraph if unclear. This rule applies to conversational closeout; human documents retain their type-specific structure.

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

## Delivery reading check

Apply to deliverables people read, present or operate, especially reports, proposals and prototypes assembled by multiple roles, not machine handoff records.

- Establish existing capabilities, the specific change and recommendation before details. Existing-system proposals start from verified pages, workflows and code; unknown is not missing or new work. Do not invent a baseline for a new project.
- Organize around reader questions and actions, not agent assignments, test IDs or source arrival order. The coordinator unifies terminology and narrative. When an overview helps, put it before details and connect its steps to actual sections or prototype entries; do not force diagrams into short answers.
- Use familiar, complete expressions. “Sample not loaded” could mean “No demonstration data for this time slot” or “This result has not arrived”; preserve the actual cause. Explain necessary technical terms by their effect on actions or decisions; retain precise fields in technical sections. Banned-word substitutions, shorter text and removed conditions do not prove readability.
- Separate business scope from agent permissions. Unsupported product behavior and release dependencies matter to readers and stay in the document. “Do not commit Git or send to colleagues,” file-write limits and explanations of why a draft may be delivered belong in execution records and necessary user progress updates, not a colleague-facing proposal. Permissions belong in the body when the requested document itself is an operating or authorization procedure.
- Describe product behavior and changes in reader prose. Source arbitration, historic review narration, author defenses and agent scores belong in internal records. Keep consequential limits next to their claims: explain who must assess interface work before setting a schedule instead of an unsupported delivery-date disclaimer.
- Walk the reader's real entry using only deliverable text, diagrams and pages. Restate existing capabilities, intended changes, the usage flow and required coordination or decisions. Identify exact sentences or pages causing ambiguity or unanswered questions, then check the sources. For instructions, locate actions, expected results and failure handling. Do not rely on oral coaching or hidden logs to make a document understandable.

When multi-agent delivery already includes independent review, use that reviewer, uninvolved in writing, for this check; add no role or round. Factual review still derives expectations from sources first. For the reading check use the deliverable as the basis for understanding and disclose previous source exposure; do not claim a blind test. The coordinator checks the restatement against the sources, fixes affected passages and verifies those changes. In ordinary mode the current executor self-checks and labels it honestly.

Working links, passing checklists and expected keywords do not prove comprehension. Distinguish factual checks, understanding and actual rendering. Agent restatement is evidence of that check, not human acceptance. When users cannot understand a delivered artifact, retract the relevant ready-to-use claim and inspect related passages and pages, not only the named phrases. Keep rejected drafts in existing history and maintain one current reader entry.


## Actual-use feedback

When actual feedback affects delivery, when resuming a related task or handling a similar delivery, use [feedback reuse and rule consolidation](experience-candidate-template.md) to extend the existing internal record and check subsequent outcomes. Fix the artifact first; require no user form. Feedback itself does not authorize skill edits or new background monitoring.
