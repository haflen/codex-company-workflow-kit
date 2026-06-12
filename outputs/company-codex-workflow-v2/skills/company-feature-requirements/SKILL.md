---
name: company-feature-requirements
description: Use when a company project needs feature requirements, acceptance criteria, scope clarification, or change-request requirements before technical design or implementation.
---

# Company Feature Requirements

## Purpose

Provide a Codex-ready requirements workflow.

## Workflow

1. Establish context with `company-context-index`.
2. Clarify goal, users, in-scope behavior, out-of-scope behavior, dependencies, and risks.
3. Use `company-expert-routing` when the requirement is non-trivial; let it select the matching bundle automatically from `BUNDLES.md`.
4. Use `brainstorming` when the idea has multiple plausible directions or the user is still exploring options.
5. Write Given-When-Then acceptance criteria.
6. Stop after requirements unless the user explicitly gives the design handoff signal.

## Artifact

Use `specs/global/assets/requirements-template.md`. Save under the team's active version/milestone path, or `specs/features/<feature>/requirements.md` for small work.

## Boundary

Requirements work must not modify implementation code or prescribe low-level architecture.
