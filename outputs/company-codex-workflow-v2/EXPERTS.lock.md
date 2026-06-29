# Expert Skills Lock

All vertical expert skills in this workflow are managed as dependencies from:

- Repository: `sickn33/antigravity-awesome-skills`
- URL: https://github.com/sickn33/antigravity-awesome-skills
- README-observed release: `V13.4.0`
- README-observed size: `1,693+` skills
- Codex install mode: required experts are vendored inside this company plugin under `skills/`; users do not install them one by one.
- Repository code license: MIT
- Repository original non-code content license: CC BY 4.0 unless a more specific upstream notice applies
- Canonical manifest: `skills_index.json`
- Current vendored pin: `e0ef87efd0ad5a18a23e21bb08406b3eaf563b35`
- Candidate commit date: 2026-06-29T07:45:17Z
- Dependency review date: 2026-06-29

Important note: upstream README and package metadata can drift. This company plugin uses its bundled copy as the runtime dependency. Future updates must go through `company-skill-maintenance` and automated or human review.

## Policy

- Verify every required expert skill is bundled when the company plugin is installed.
- Do not auto-update expert skills from GitHub, npm, ClawHub-style hubs, or self-improvement output.
- Run install-time static security review and generate `EXPERT-READINESS.md` / `EXPERT-READINESS.json`.
- Use `company-skill-security-review` for new, updated, or self-improved skills.
- Use `company-skill-maintenance` to update this lock file and record rollback information.
- If a skill includes scripts, shell commands, network access, browser automation, or filesystem writes, treat it as higher risk even if the manifest marks setup as `none`.

## Install and Pin Guidance

Company users do not manually install expert skills. Plugin install and project bootstrap automatically perform:

- bundled expert completeness checks
- static security review and risk labeling
- project-level `.codex-workflow/EXPERT-READINESS.md`
- a reminder to open a new Codex thread after install so the session skill list refreshes

Recommended production pinning options:

- Git tag pin: `sickn33/antigravity-awesome-skills@<release-tag>`
- Commit pin: `https://github.com/sickn33/antigravity-awesome-skills/tree/<commit>/<skill-path>`
- Local vendored copy: copy approved skill folders into a company-controlled plugin and record the source commit here.

Do not use `--tag main` for production unless the team intentionally wants current repository tip and accepts churn.

## Locked Expert Dependencies

| Expert | AAS path | Category | Risk | Upstream source | License basis | Pin | Codex target | Setup | Status | Last Reviewed | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `product-manager` | `skills/product-manager` | business | safe | `Digidai/product-manager-skills (MIT)` | Upstream MIT plus AAS metadata | `e0ef87efd0ad5a18a23e21bb08406b3eaf563b35` | supported | none | Approved for pilot | 2026-06-29 | Good for AC quality, PRD-level scope, user stories. Verify upstream MIT attribution before production. |
| `business-analyst` | `skills/business-analyst` | business | safe | community | AAS content license / upstream unknown | `e0ef87efd0ad5a18a23e21bb08406b3eaf563b35` | supported | none | Approved for pilot | 2026-06-29 | Use for business processes, metrics, reporting, policy, and state transitions. |
| `ai-product` | `skills/ai-product` | ai-ml | safe | `vibeship-spawner-skills (Apache 2.0)` | Apache 2.0 upstream plus AAS metadata | `e0ef87efd0ad5a18a23e21bb08406b3eaf563b35` | supported | none | Approved for pilot | 2026-06-29 | Use for LLM/RAG/prompt/agent workflow architecture. Prefer current official provider docs for APIs. |
| `java-pro` | `skills/java-pro` | code | medium | community | AAS content license / upstream unknown | Bundled from `e0ef87efd0ad5a18a23e21bb08406b3eaf563b35` | supported | none | Bundled auto-reviewed approved | 2026-06-29 | High-value if company stack is Java/Spring. Replace with internal standards where possible. |
| `python-pro` | `skills/python-pro` | code | medium | community | AAS content license / upstream unknown | Bundled from `e0ef87efd0ad5a18a23e21bb08406b3eaf563b35` | supported | none | Bundled auto-reviewed approved | 2026-06-29 | Confirm runtime and dependency manager before relying on advice. |
| `python-patterns` | `skills/python-patterns` | development | medium | community | AAS content license / upstream unknown | Bundled from `e0ef87efd0ad5a18a23e21bb08406b3eaf563b35` | supported | none | Bundled auto-reviewed approved | 2026-06-29 | Architecture guidance; may be long. Prefer selective use or internal summary. |
| `django-pro` | `skills/django-pro` | framework | medium | community | AAS content license / upstream unknown | Bundled from `e0ef87efd0ad5a18a23e21bb08406b3eaf563b35` | supported | none | Bundled auto-reviewed approved | 2026-06-29 | Use only for Django projects; verify Django version-specific claims. |
| `frontend-developer` | `skills/frontend-developer` | front-end | medium | community | AAS content license / upstream unknown | Bundled from `e0ef87efd0ad5a18a23e21bb08406b3eaf563b35` | supported | none | Bundled auto-reviewed approved | 2026-06-29 | React/Next-oriented. For Vue projects, combine with project standards. |
| `typescript-expert` | `skills/typescript-expert` | framework | high | community | AAS content license / upstream unknown | `e0ef87efd0ad5a18a23e21bb08406b3eaf563b35` | supported | diagnostic script; approval required before execution | Bundled review passed; runtime script approval required | 2026-06-29 | Upstream marks critical; use for type and module-boundary guidance. Major migrations still need review. |
| `frontend-design` | `skills/frontend-design` | front-end | medium | community | AAS content license / upstream unknown | Bundled from `e0ef87efd0ad5a18a23e21bb08406b3eaf563b35` | supported | none | Bundled auto-reviewed approved | 2026-06-29 | Use for UI craft and visual correctness; still follow project UI standards. |
| `testing-qa` | `skills/testing-qa` | workflow-bundle | safe | personal | AAS content license / upstream unknown | `e0ef87efd0ad5a18a23e21bb08406b3eaf563b35` | supported | none | Approved for pilot | 2026-06-29 | Use for QA strategy and gates; keep Superpowers verification as final evidence rule. |
| `webapp-testing` | `skills/webapp-testing` | test-automation | medium | community | AAS content license / upstream unknown | `e0ef87efd0ad5a18a23e21bb08406b3eaf563b35` | supported | helper script; approval required before execution | Bundled review passed; runtime script approval required | 2026-06-29 | Helper script uses allowlisted executables, rejects shell metacharacters, and confines cwd to the project. Confirm Codex Browser/Playwright availability. |
| `e2e-testing-patterns` | `skills/e2e-testing-patterns` | test-automation | safe | community | AAS content license / upstream unknown | `e0ef87efd0ad5a18a23e21bb08406b3eaf563b35` | supported | none | Approved for pilot | 2026-06-29 | Use for E2E strategy. Prefer `webapp-testing` for concrete browser execution. |
| `systematic-debugging` | `skills/systematic-debugging` or Superpowers | development-and-testing | unknown | community / Superpowers | Prefer installed Superpowers | Superpowers bundled; AAS fallback not vendored | supported | none | Prefer Superpowers | 2026-06-11 | Use installed Superpowers version when available; AAS copy is fallback only. |
| `test-driven-development` | `skills/test-driven-development` or Superpowers | testing | unknown | community / Superpowers | Prefer installed Superpowers | Superpowers bundled; AAS fallback not vendored | supported | none | Prefer Superpowers | 2026-06-11 | Use installed Superpowers version when available; AAS copy is fallback only. |

## Deferred or Optional Experts

| Expert | AAS path | Reason |
| --- | --- | --- |
| `competitive-landscape` | `skills/competitive-landscape` | Useful for product/market work, not default engineering flow. Add only when company product planning needs it. |
| `startup-metrics-framework` | `skills/startup-metrics-framework` | Useful for startup/SaaS metrics, not default engineering flow. |
| `copywriting` | `skills/copywriting` | Marketing/content workflow; keep out of engineering starter kit unless needed. |
| `ui-ux-pro-max` | `skills/ui-ux-pro-max` | Overlaps with `frontend-design`; heavy guidance. Add only after UI team review. |

## Bundle Membership

Use `BUNDLES.md` as the runnable bundle map. This section is a dependency-maintenance view for lock reviews.

| Expert | Bundles |
| --- | --- |
| `product-manager` | `company-core-delivery`, `company-frontend-delivery`, `company-ai-feature` |
| `business-analyst` | `company-core-delivery`, `company-backend-java`, `company-python-service`, `company-django-service` |
| `ai-product` | `company-ai-feature`, `company-spike` |
| `java-pro` | `company-backend-java`, `company-hotfix`, `company-spike` |
| `python-pro` | `company-python-service`, `company-django-service`, `company-ai-feature`, `company-hotfix`, `company-spike` |
| `python-patterns` | `company-python-service` |
| `django-pro` | `company-django-service`, `company-hotfix`, `company-spike` |
| `frontend-developer` | `company-frontend-delivery`, `company-ai-feature`, `company-hotfix`, `company-spike` |
| `typescript-expert` | `company-frontend-delivery` |
| `frontend-design` | `company-frontend-delivery` |
| `testing-qa` | `company-core-delivery`, `company-backend-java`, `company-python-service`, `company-django-service`, `company-frontend-delivery`, `company-ai-feature`, `company-hotfix`, `company-spike` |
| `webapp-testing` | `company-frontend-delivery`, `company-django-service`, `company-spike` |
| `e2e-testing-patterns` | optional add-on for browser-heavy bundles |
| `systematic-debugging` | `company-core-delivery`, `company-hotfix` |
| `test-driven-development` | `company-core-delivery`, `company-backend-java`, `company-frontend-delivery` |
| `company-skill-upgrade-runner` | `company-skill-governance` |
| `company-skill-maintenance` | `company-skill-governance` |
| `company-skill-security-review` | `company-skill-governance` |
| `company-skill-evolution-lab` | `company-skill-governance` |

## Update Record

| Date | Expert | Change | Review Result | Rollback |
| --- | --- | --- | --- | --- |
| 2026-06-11 | all listed experts | Initial dependency lock normalized to `sickn33/antigravity-awesome-skills`; source, path, risk, target, setup, and status recorded | Pilot approved for safe entries; unknown/critical entries require production review | Revert this file or use prior starter-kit template |
| 2026-06-11 | all listed experts | Added bundle membership and automatic workflow routing dependency view | Keeps bundle routing separate from expert pin/license review | Revert `BUNDLES.md`, `company-expert-routing`, and this membership section |
| 2026-06-11 | skill governance workflow | Added user-friendly skill upgrade workflow with candidate fetch, diff, security review, confirmation gate, apply, validation, and rollback record | Upgrade operations now route through `company-skill-upgrade-runner` before production overwrite | Revert `company-skill-upgrade-runner`, upgrade report template, and related routing updates |
| 2026-06-24 | all required expert skills | Vendored required AAS expert skills into the company plugin and added install-time readiness/security reports | Out-of-box usable after plugin install and new Codex thread; future updates stay controlled | Revert vendored expert skill directories and this lock update |
| 2026-06-29 | 13 vendored expert skills | Synced upstream `sickn33/antigravity-awesome-skills@e0ef87efd0ad`; preserved Codex trigger descriptions and updated bodies/resources | Static review passed; pure Markdown remains safe/medium, `typescript-expert`/`webapp-testing` scripts require runtime approval | Revert this commit or restore previous vendored `skills/<expert>` directories |
