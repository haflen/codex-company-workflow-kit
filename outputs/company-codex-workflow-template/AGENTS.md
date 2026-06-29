# Codex Company Workflow

These instructions define the team workflow for Codex in this project. Keep changes simple, scoped, and verified.

## Operating Principles

- Prefer the smallest change that satisfies the accepted requirement.
- Match existing project style and architecture before introducing new patterns.
- Do not refactor unrelated code while delivering a feature or fix.
- State assumptions when requirements, ownership, or risk are unclear.
- Use current official documentation for unstable third-party APIs instead of relying on memory.

## Context Loading

- Start by reading `specs/global/INDEX.md`.
- Read only the specific specs relevant to the task.
- Do not scan every Markdown file unless the task explicitly requires broad audit work.
- If the index is stale, update it as part of planning or after completing the related spec change.

## Document Ownership And Numbering

- Before writing any project document, confirm its role, information level, numbering namespace, and update trigger.
- `说明文档.md` or an equivalent entry page is only for project entry, current state, recent important events, and reading route; it must not become a spike field log.
- Spike logs use spike-scoped IDs such as `SPK02-T001`; formal tasks use feature, version, or formal task IDs. Do not reuse bare `Task 001` across documents.
- `specs/global/INDEX.md` should maintain the document ownership map.

## Phase Boundaries

- Requirements clarification produces acceptance criteria and edge cases. Do not edit implementation code in this phase.
- Technical design produces architecture, API/data contracts, risk notes, and test strategy. Do not edit implementation code in this phase.
- Implementation begins only after requirements and design are confirmed, unless the user explicitly invokes `/spike` or `/hotfix`.
- Ambiguous "continue" means continue the current phase, not advance to coding.

## First Principles And Adversarial Review

- Before complex requirements, technical design, bugfix root-cause claims, and spike conclusions, run a first-principles check: underlying facts, key constraints, and minimum conditions.
- Before implementation completion, bugfix completion, hotfix closure, spike conclusions, and pre-release verification, run adversarial review: extreme input, abnormal states, permission bypasses, concurrent retries, future timestamps, cache false positives, performance, or UI rendering pressure.
- Trivial changes may skip these checks, but the reason must be stated.
- Do not write only "checked"; include concrete facts, counterexample scenarios, or skip reasons.

## Standard Handoff Signals

- "Requirements confirmed, enter design" moves from requirements to technical design.
- "Design confirmed, start implementation" moves from design to implementation.
- "Start bugfix" enters root-cause debugging and repair.
- `/spike <question>` enters time-boxed technical exploration.
- `/hotfix <incident>` enters emergency repair.

## Verification Rules

- Feature work must include executable tests when the project has a test harness.
- Bug fixes must reproduce or explain the failure before changing code.
- Completion claims must cite the exact verification commands or manual checks performed.
- If automated verification is unavailable, provide a focused manual checklist.

## Exception Channels

- `/spike` may skip full SDLC documents, but must produce a short spike report.
- `/hotfix` may prioritize recovery over design completeness, but must produce a hotfix report and follow-up test debt.
- Exception work should be minimal, isolated, and followed by normal cleanup planning.
