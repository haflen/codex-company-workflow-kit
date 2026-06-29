---
name: company-spike-research
description: Use when company work needs a time-boxed technical feasibility experiment, unfamiliar library evaluation, prototype, or architecture uncertainty reduction before design.
---

# Company Spike Research

## Purpose

Provide a controlled Codex spike workflow.

## Workflow

1. State the spike question and time box.
2. Explicitly use `superpowers:brainstorming` when multiple experiment paths are possible.
3. State the first-principles hypothesis: what must be proven, the minimum conditions, and what evidence would disprove it.
4. Confirm the spike numbering namespace, for example `SPK02`; spike-internal tasks use `SPK02-T001`, never bare `Task 001`.
5. Isolate experiment code under `spikes/`, `playground/`, or another throwaway path.
6. Use `company-expert-routing` when the experiment depends on non-obvious stack or API behavior; prefer the `company-spike` bundle plus one stack expert.
7. Run the smallest experiment that answers the question, plus at least one counterexample or boundary experiment.
8. Explicitly use `superpowers:verification-before-completion` to check that evidence answers the spike question.
9. Write findings, recommendation, and follow-up debt; if converting to production work, return to requirements/design/planning and create a new formal task namespace.

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
The spike work log is not the project entry page; do not write spike-internal task IDs into `说明文档.md` as project-mainline task IDs.

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
- Next step:
