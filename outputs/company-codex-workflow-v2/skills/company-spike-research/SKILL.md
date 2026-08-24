---
name: company-spike-research
description: Use when company work needs a time-boxed technical feasibility experiment, unfamiliar library evaluation, technical prototype, performance evidence, or architecture uncertainty reduction before design.
---

# Company Spike Research

## Purpose

Provide a controlled Codex spike workflow.

## Workflow

1. Classify the validation purpose first: only technology, architecture, performance, or library feasibility is a spike. Route page, interaction, copy, or mock business-state validation to `company-requirements-prototype`. Then state the spike question and time box.
2. Explicitly use `superpowers:brainstorming` when multiple experiment paths are possible.
3. State the first-principles hypothesis: what must be proven, the minimum conditions, and what evidence would disprove it.
4. Confirm the spike numbering namespace, for example `SPK02`; spike-internal tasks use `SPK02-T001`, never bare `Task 001`.
5. Isolate experiment code under `spikes/`, `playground/`, or another throwaway path.
6. Use `company-expert-routing` when the experiment depends on non-obvious stack or API behavior; prefer the `company-spike` bundle plus one stack expert.
7. Run the smallest experiment that answers the question, plus at least one counterexample or boundary experiment.
8. Explicitly use `superpowers:verification-before-completion` to check that evidence answers the spike question.
9. Write findings, recommendation, and follow-up debt; if converting to production work, return to requirements/design/planning and create a new formal task namespace.
10. If the spike conclusion affects the project entry, reading route, or current phase, non-integration branches write a public-doc update patch instead of directly editing `说明文档.md`.

## Superpowers Layer

- Default: `superpowers:brainstorming` for minimal experiment design.
- Completion: `superpowers:verification-before-completion` for evidence sufficiency.
- If the spike question is already obvious, brainstorming may be skipped but the reason must be stated.

## Artifact

When a spike template is needed, resolve it in this order:

1. Project copy: `specs/global/assets/spike-report-template.md`.
2. Plugin fallback: read `../../specs/global/assets/spike-report-template.md` relative to this skill directory.

## Boundary

Spike code is not production code unless explicitly reviewed and converted through the normal design and implementation flow.
Requirements-stage page prototypes do not belong here; never use a spike to bypass requirements-prototype confirmation and baseline rules.
The spike work log is not the project entry page; do not write spike-internal task IDs into `说明文档.md` as project-mainline task IDs.
Before a spike branch is merged, do not write temporary spike conclusions as the public document's mainline current state.


## Human-First Output

Start the final reply with `One-sentence conclusion`, `What was completed`, `What needs attention`, and `What the user should do now`. Use business outcomes and user impact, give one primary next action, and explain internal terms on first use. Then place Superpowers, expert calls, commands, paths, hashes, verification evidence, and internal workflow fields in a `Technical Audit Appendix`; Do not dump internal workflow fields one by one into the human summary or use audit fields as a substitute for it.


### Response Contract Gate

- Trigger this gate for formal completion or phase closeout, an explicit user request for a progress summary, blocker conclusion, or next-step proposal, plus any substantial reply containing audit fields.
- One- or two-sentence working updates and ordinary Q&A never trigger the fixed format, even when they mention the current result, risk, or next step; do not attach full audit details to a lightweight reply.
- When the user asks for more detail, expand only the four sections or the `Technical Audit Appendix`; must not remove, rename, or reorder the four headings.
- Audit fields may appear only in the `Technical Audit Appendix`; they must not sit beside or before the four-section human summary.
- Before sending, check that the four headings are present in order, risks are translated into practical impact, and only one primary next action is given. If any check fails, rewrite it before sending.

## Output

- Workflow layer: `company-spike-research`
- Trace mode:
- Superpowers layer:
- Actual calls:
- Expert/plugin capabilities:
- Not called, lens only:
- First Principles Check:
- Adversarial Review:
- Execution strategy:
- Verification evidence:
- Unverified items:
- Remaining risk:
- Spike question:
- Spike numbering namespace:
- First-principles hypothesis:
- Minimal experiment:
- Counterexample or boundary experiment:
- Evidence:
- Conclusion:
- New numbering recommendation when converting to formal work:
- Public-doc impact:
- Next step:

## Document Quality Gates

Before creating or substantially changing a formal document, read the project copy of `specs/global/assets/document-standard.md`; if absent, read the bundled `../../specs/global/assets/document-standard.md`. This skill enforces `DOC-G01`, `DOC-G04`, `DOC-G05`, `DOC-G06`, `DOC-G07`, `DOC-G08`, `DOC-G09`, `DOC-G10`, `DOC-G11`, and `DOC-G12`.
