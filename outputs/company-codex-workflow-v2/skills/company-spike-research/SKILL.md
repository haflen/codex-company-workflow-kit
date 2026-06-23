---
name: company-spike-research
description: Use when company work needs a time-boxed technical feasibility experiment, unfamiliar library evaluation, prototype, or architecture uncertainty reduction before design.
---

# Company Spike Research

## Purpose

Provide a controlled Codex spike workflow.

## Workflow

1. State the spike question and time box.
2. Isolate experiment code under `spikes/`, `playground/`, or another throwaway path.
3. Use `company-expert-routing` when the experiment depends on non-obvious stack or API behavior; prefer the `company-spike` bundle plus one stack expert.
4. Run the smallest experiment that answers the question.
5. Write findings, recommendation, and follow-up debt.

## Artifact

When a spike template is needed, resolve it in this order:

1. Project copy: `specs/global/assets/spike-report-template.md`.
2. Plugin fallback: read `../../specs/global/assets/spike-report-template.md` relative to this skill directory.

## Boundary

Spike code is not production code unless explicitly reviewed and converted through the normal design and implementation flow.
