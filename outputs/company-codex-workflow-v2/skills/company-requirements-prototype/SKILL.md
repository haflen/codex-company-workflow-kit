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
7. Verify relevant viewports, interactions, states, accessibility, and console errors. Stop processes created in this turn.
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
