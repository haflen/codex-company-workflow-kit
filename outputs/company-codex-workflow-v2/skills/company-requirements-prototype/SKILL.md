---
name: company-requirements-prototype
description: Use when a company project is still in requirements and needs an isolated HTML, page, or interaction prototype created, reviewed, revised, or confirmed to validate requirements without entering technical design or production implementation.
---

# Company Requirements Prototype

## Core Boundary

A requirements prototype validates what users see and do. Purpose and dependencies determine its stage, not the extension.

## When to Use

Use when the user wants to draw, preview, revise, or confirm a page or interaction prototype during requirements.

Do not use for:

- technology, architecture, performance, or library feasibility: use `company-spike-research`;
- production-source changes or real-system integration: require design and implementation authorization;
- non-visual requirements: remain in `company-feature-requirements` without prototype artifacts.

## Execution Contract

1. Read the authoritative requirements, linked `business-rules.md`, and any existing prototype manifest.
2. Report `Current stage: requirements` and `Production implementation authorization: none`; list validation questions and non-goals.
3. For the first prototype or a material UX/interaction change, **REQUIRED SUB-SKILL:** Use `superpowers:brainstorming`. Do not restart it for confirmed mechanical revisions.
4. For non-trivial UI work, use `company-expert-routing`; prefer the `company-frontend-delivery` bundle with `frontend-design` and `webapp-testing`, adding `frontend-developer` only for complex client behavior.
5. Create only self-contained HTML/CSS/JavaScript with mock data and non-sensitive assets. Default draft path:

```text
.codex-workflow/prototypes/<feature>/draft/
```

6. Maintain `prototype.json` in the draft directory with `feature`, `source_requirements`, `status`, `created_at`, `updated_at`, `owned_files`, `validation_questions`, and `browser_verification`. Never edit `.gitignore` silently.
7. Verify only confirmed target clients, viewports, browsers, and input methods from requirements. Check relevant interactions, states, accessibility, and console errors. Stop processes created in this turn.
8. If feedback changes scope, rules, copy, or acceptance criteria, update authoritative documents through `company-feature-requirements`, then continue iteration.

## Promote to Requirements Baseline

Only explicit intent to confirm both requirements and prototype authorizes promotion:

1. Copy approved files to `prototype/` beside the authoritative requirements document.
2. Record status, version, path, confirmation date, validated scope, unpromised details, and SHA-256 of the entry HTML or approved archive.
3. Verify source/baseline content, links, and checksum.
4. Remove only draft files whose ownership is proven by `prototype.json`.
5. Stop. Do not create design/tasks or commit/push automatically.

If the user also explicitly authorizes technical design, promote first and route only to `company-feature-design`; do not create tasks.

## Circuit Breakers

Stop prototype edits when the user requests a real API, database, authentication, production data/component, framework migration, backend, schema, infrastructure, performance, or feasibility evidence. Explain the boundary and choose between `company-spike-research` and explicitly authorized `company-feature-design`.

Ambiguous “confirm”, “continue”, or “next” means continue the current requirements/prototype stage. It does not authorize design or production implementation.

## Target Client Gate

- The prototype inherits target clients from authoritative requirements; generic responsive advice from an expert skill cannot expand product scope.
- When mobile is not explicitly supported, the workflow must not add mobile adaptation on its own, including breakpoints, touch behavior, device frames, screenshots, or mobile browser tests.
- A new client request returns to `company-feature-requirements` to update the boundary and ACs before prototype work continues.

## Human-First Output

Put the human summary before the Technical Audit Appendix:

1. One-sentence conclusion: state what the prototype can now validate.
2. What was completed: describe page, interaction, or feedback changes.
3. What needs attention: explain unverified behavior and non-commitments.
4. What the user should do now: give one primary next action and one short reply phrase.

Then use `Technical Audit Appendix` for the internal fields below. Explain acronyms and levels on first use. Do not dump internal workflow fields one by one into the human summary.


### Response Contract Gate

- Trigger this gate for formal completion or phase closeout, an explicit user request for a progress summary, blocker conclusion, or next-step proposal, plus any substantial reply containing audit fields.
- One- or two-sentence working updates and ordinary Q&A never trigger the fixed format, even when they mention the current result, risk, or next step; do not attach full audit details to a lightweight reply.
- When the user asks for more detail, expand only the four sections or the `Technical Audit Appendix`; must not remove, rename, or reorder the four headings.
- Audit fields may appear only in the `Technical Audit Appendix`; they must not sit beside or before the four-section human summary.
- Before sending, check that the four headings are present in order, risks are translated into practical impact, and only one primary next action is given. If any check fails, rewrite it before sending.

## Output Contract

- Workflow layer: `company-requirements-prototype`
- Stage: requirements
- Prototype status: draft iteration / awaiting confirmation / confirmed / withdrawn
- Production implementation authorization: none
- Actual calls:
- Superpowers layered:
- Expert/plugin capabilities:
- Prototype validation target:
- Draft or baseline path:
- Browser verification evidence:
- Requirements feedback and document drift:
- Unverified items and remaining risk:
- Next step: continue requirements/prototype iteration / promote baseline / await explicit design authorization

Never recommend task planning while requirements or prototype confirmation is pending.

## Document Quality Gates

Before creating or substantially changing a formal document, read the project copy of `specs/global/assets/document-standard.md`; if absent, read the bundled `../../specs/global/assets/document-standard.md`. This skill enforces `DOC-G01`, `DOC-G04`, `DOC-G05`, `DOC-G06`, `DOC-G07`, `DOC-G08`, `DOC-G09`, `DOC-G10`, `DOC-G11`, and `DOC-G12`.
