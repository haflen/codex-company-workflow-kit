# Company Codex Workflow

This project uses a lightweight SDLC adapted from audited source skills. The goal is traceability and consistent delivery without slowing down simple work.

## Context First

- Read `specs/global/INDEX.md` before planning or editing.
- If present, read `说明文档.md` for current progress and project state.
- Read only the current version, milestone, feature docs, and source files relevant to the task.
- Do not scan all Markdown files unless the task is an audit or migration.

## Phase Boundaries

- Requirements work produces goals, scope, acceptance criteria, and edge cases. Do not edit implementation code.
- Design work produces architecture, contracts, data flow, risks, and test strategy. Do not edit implementation code.
- Planning work produces executable tasks and verification points. Do not edit implementation code.
- Implementation starts only after requirements, design, and task plan are confirmed, except for `/spike` or `/hotfix`.
- Ambiguous "continue" means continue the current phase, not advance to the next phase.

## Handoff Signals

- `需求已确认，进入技术设计`
- `方案已确认，进入任务拆解`
- `任务已确认，开始实现`
- `开始 bugfix`
- `/spike <technical question>`
- `/hotfix <incident>`
- `检查技能更新`
- `更新 <skill-name> 技能`
- `对比并升级 <skill-name>`

## Expert Usage

Use relevant experts or subagents when the work involves non-trivial architecture, framework APIs, concurrency, performance, security, data modeling, UI craft, or testing strategy. Do not invoke experts for trivial edits.

Users should not need to name experts in chat for normal work. Workflow skills should select the smallest matching bundle from `BUNDLES.md`, then route to the relevant expert only when the current phase needs it. If the user explicitly names an expert, honor that request unless it conflicts with safety or project constraints.

When third-party APIs or framework behavior may have changed, prefer official/current documentation. If a Context7-style MCP is not available, state that and use official docs or local package docs when possible.

Use `company-expert-routing` as the single source of truth for expert selection. Use `BUNDLES.md` for expert combinations and `EXPERTS.lock.md` to check source, pin, license, and review status for external expert skills.

Do not auto-update external expert skills. Use `company-skill-maintenance` and `company-skill-security-review` before adopting updates from open-source hubs or self-improvement output.

For user-friendly skill updates, use `company-skill-upgrade-runner`. It must fetch or inspect a candidate version, compare old and new versions, run security review, show the recommendation, and wait for explicit user confirmation before overwriting production skills.

Self-improvement is proposal-only by default. Use `company-skill-evolution-lab` to capture repeated workflow failures and propose reviewed changes; do not let skills rewrite themselves directly into production use.

## Verification

- Feature work needs tests when a test harness exists.
- Bug fixes need a reproduction or a clear evidence trail before code changes.
- Completion reports must include exact verification commands or manual checks.
- If automated verification is unavailable, provide a focused manual checklist.

## Documentation

- Company projects should keep `说明文档.md` or an equivalent progress document.
- Versioned specs may use `specs/versions/<version>/<milestone>/`.
- Small changes may use one compact feature spec under `specs/features/<feature>/`.
- Public APIs and complex logic need comments; routine functions do not need boilerplate comments.
