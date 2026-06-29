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

## First Principles And Adversarial Review

Company workflows include two checks by default; users do not need to type special prompt phrases:

- `First Principles Check`: return to underlying facts, constraints, and minimum conditions for the solution to be true. Do not replace root-cause analysis with analogy or surface symptoms.
- `Adversarial Review`: validate the plan against malicious users, extreme data, abnormal states, permission bypasses, concurrent retries, oversized input, future timestamps, cache false positives, and rendering pressure.

Automatic triggers:

- Requirements: for L2/L3 or complex business rules, state core assumptions, non-negotiable constraints, and adversarial scenarios.
- Design: for non-trivial architecture, data, permission, performance, security, external API, frontend rendering, or cross-service boundary decisions, run `First Principles Check`.
- Planning: every non-trivial task must include a minimum failing case or verification anchor and at least one adversarial scenario.
- Implementation: before completion, run `Adversarial Review` unless the change is pure copy, comments, or no-behavior work; state the reason if skipped.
- Bugfix/hotfix: before root-cause claims, run `First Principles Check`; before completion, run regression and adversarial review.
- Spike: before conclusion, state the first-principles hypothesis, counterexample experiment, and evidence boundary.
- Skill upgrade, security review, and self-improvement proposals default to `full-audit` and run adversarial review.

Output requirements:

- `First Principles Check:` list underlying facts, constraints, minimum conditions, or why it can be skipped.
- `Adversarial Review:` list extreme, malicious, or abnormal scenarios and results, or why it can be skipped.
- Do not write only "analyzed from first principles" or "ran adversarial review"; include concrete facts or scenarios.

## Visible Superpowers Layer

- Every workflow output must explicitly include `Workflow layer`, `Superpowers layer`, and `Execution strategy`.
- Every workflow opening must explicitly include `Actual calls`, `Expert/plugin capabilities`, and `Not called, lens only`; do not say "expert lens" without stating whether the skill was actually invoked.
- Every workflow closing must explicitly include `Verification evidence`, `Unverified items`, and `Remaining risk`. If verification is not needed for the current phase, state why.
- If a Superpowers skill, expert skill, MCP, browser capability, or other Codex plugin capability is not actually exposed or invoked in the current session, record it under `Not called, lens only` with the reason.
- Requirements exploration defaults to `superpowers:brainstorming`.
- Complex planning defaults to `superpowers:writing-plans`.
- Implementation defaults to `superpowers:test-driven-development` and `superpowers:verification-before-completion`.
- Bugfix defaults to `superpowers:systematic-debugging`, with `superpowers:verification-before-completion` before completion.
- If a simple task skips Superpowers, state the reason explicitly.

## Capability Trace

All company workflows use this trace protocol by default unless the user explicitly asks for a minimal answer:

### Automatic Levels

Users do not decide which trace level to use; the workflow must choose automatically:

- `light`: default mode for normal in-phase progress, small changes, doc updates, and low-risk continuation. Keep only the required actual calls, lens-only usage, verification evidence, and risk notes.
- `full-audit`: key-node or exception mode. Enable the full `Workflow Audit` when any of these is true:
  - Phase handoff: requirements to design, design to planning, planning to implementation.
  - Implementation completion, bugfix completion, any hotfix phase, or spike conclusion.
  - Skill upgrade, expert dependency update, security review, or self-improvement proposal.
  - An expert/plugin capability was not actually invoked and only used as a lens.
  - The current session lacks an expected Superpowers skill, expert skill, MCP, browser capability, or plugin capability.
  - Verification failed, is missing, or tests cannot be run.
  - Production, data, permission, architecture, performance, or security risk is involved.
  - The user asks to audit, check the process, or confirm compliance.

Opening:

- `Workflow layer:`
- `Trace mode: light` or `Trace mode: full-audit`
- `Actual calls:` list workflow, Superpowers, expert skill, MCP, browser, or plugin capabilities actually triggered or read.
- `Expert/plugin capabilities:` list the experts, Superpowers, or Codex plugin capabilities selected for this turn.
- `Not called, lens only:` list capabilities that were unavailable, unsuitable for the phase, or not worth invoking.
- `First Principles Check:`
- `Adversarial Review:`
- `Execution strategy:`

Closing:

- `Verification evidence:` include commands, check results, file changes, screenshots, logs, or manual evidence.
- `Unverified items:` include anything not checked or not applicable to this phase.
- `Remaining risk:`

Do not use "executed with expert lens" as a substitute for call evidence; always distinguish `actually invoked` from `lens only`.

When `full-audit` is active, also output:

- `Workflow Audit:`
- `Phase boundary:`
- `Superpowers declaration:`
- `Expert/plugin actual calls:`
- `Lens-only usage:`
- `Verification evidence:`
- `Unverified items:`
- `Conclusion:`

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

Use `company-expert-routing` as the single source of truth for expert selection. Use `BUNDLES.md` for expert combinations and `EXPERTS.lock.md` to check source, pin, license, and review status for external expert skills. Prefer project-root files; if project files are missing, read the plugin-bundled fallback instead of disabling expert routing.

When using templates, prefer project-local `specs/global/assets/`; if project templates are missing, read the plugin-bundled fallback and remind the user to run `bootstrap-project` or `update-templates` to repair project assets.

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
