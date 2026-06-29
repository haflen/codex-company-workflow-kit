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
4. Explicitly use `superpowers:brainstorming` when the idea has multiple plausible directions or the user is still exploring options.
5. For L2/L3 or complex business rules, add a first-principles check: core assumptions, non-negotiable constraints, and minimum conditions.
6. Write Given-When-Then acceptance criteria and include key counterexamples or abnormal scenarios.
7. Stop after requirements unless the user explicitly gives the design handoff signal.

## Superpowers Layer

- L0 lightweight exploration: use `superpowers:brainstorming` and return goals, options, risks, open questions, and next-step recommendations only.
- L2 standard requirements: use `superpowers:brainstorming` to clarify intent, compare paths, and converge acceptance criteria.
- If requirements are already clear, the skill may skip Superpowers but must state why.

## Artifact

When a requirements template is needed, resolve it in this order:

1. Project copy: `specs/global/assets/requirements-template.md`.
2. Plugin fallback: read `../../specs/global/assets/requirements-template.md` relative to this skill directory.

Save small work under `specs/features/<feature>/requirements.md`. If the user explicitly wants lightweight solution exploration, do not force a full requirements document; provide goals, options, risks, open questions, and next-step recommendations.

## Boundary

Requirements work must not modify implementation code or prescribe low-level architecture.

## Output

- Workflow layer: `company-feature-requirements`
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
- Requirements conclusion:
- Options:
- Risks and open questions:
- Core assumptions and counterexamples:
- Next step:
