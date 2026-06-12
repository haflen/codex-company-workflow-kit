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

## Phase Boundaries

- Requirements clarification produces acceptance criteria and edge cases. Do not edit implementation code in this phase.
- Technical design produces architecture, API/data contracts, risk notes, and test strategy. Do not edit implementation code in this phase.
- Implementation begins only after requirements and design are confirmed, unless the user explicitly invokes `/spike` or `/hotfix`.
- Ambiguous "continue" means continue the current phase, not advance to coding.

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

