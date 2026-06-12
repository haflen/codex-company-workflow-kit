# Expert Bundles

Bundles are small expert combinations used by workflow skills. They are not a new process layer.

The workflow should pick the smallest matching bundle automatically. Users may still name a specific expert in chat; an explicit user request overrides the default bundle.

## Selection Rules

1. Identify the work type from the request, current spec, files, and stack.
2. Select one primary bundle only.
3. Add a secondary expert only when the current phase clearly needs it.
4. Check `EXPERTS.lock.md` before using external expert skills.
5. Prefer installed Superpowers skills for debugging, TDD, and verification when available.

## Bundles

| Bundle | Use When | Default Experts | Optional Experts |
| --- | --- | --- | --- |
| `company-core-delivery` | Generic feature work with product, process, and QA concerns | `product-manager`, `business-analyst`, `testing-qa` | `systematic-debugging`, `test-driven-development` |
| `company-backend-java` | Java/Spring backend, transactions, concurrency, APIs, persistence | `business-analyst`, `java-pro`, `testing-qa` | `systematic-debugging`, `test-driven-development` |
| `company-python-service` | Python services, automation, FastAPI-style APIs, async jobs | `business-analyst`, `python-pro`, `testing-qa` | `python-patterns`, `systematic-debugging` |
| `company-django-service` | Django, DRF, Celery, Channels, ORM-heavy work | `business-analyst`, `django-pro`, `testing-qa` | `python-pro`, `webapp-testing` |
| `company-frontend-delivery` | Frontend behavior, React/Next/Vue, UI states, accessibility, browser validation | `product-manager`, `frontend-developer`, `typescript-expert`, `testing-qa` | `frontend-design`, `webapp-testing` |
| `company-ai-feature` | LLM, RAG, prompt, agent workflow, AI safety, provider API design | `product-manager`, `ai-product`, `testing-qa` | `python-pro`, `frontend-developer` |
| `company-hotfix` | Urgent production defect or rollback-sensitive change | `systematic-debugging`, `testing-qa` | stack expert matching the failing area |
| `company-spike` | Time-boxed feasibility, unfamiliar library, architecture uncertainty | stack expert matching the question | `ai-product`, `webapp-testing`, `testing-qa` |
| `company-skill-governance` | Adding, updating, reviewing, upgrading, or evolving workflow/expert skills | `company-skill-upgrade-runner`, `company-skill-maintenance`, `company-skill-security-review` | `company-skill-evolution-lab` |
| `company-workflow-entry` | User is unsure which workflow to start or asks what to do next | `company-workflow-help` | `company-expert-routing` |
| `company-legacy-onboarding` | Existing project adoption, project context draft generation, or first workflow pilot | `company-legacy-project-onboarding`, `company-context-index` | `company-workflow-help`, stack expert matching the project |

## Phase Defaults

| Phase | Bundle Use |
| --- | --- |
| Requirements | Usually `company-core-delivery`; use `company-ai-feature` when AI behavior is the product. |
| Design | Pick the stack bundle that owns the architecture risk. |
| Planning | Keep the design bundle; add `testing-qa` if verification is unclear. |
| Implementation | Use the selected design bundle only when implementation choices depend on expert knowledge. |
| Bugfix | Start with `company-hotfix` for urgent incidents or the affected stack bundle for normal bugs. |
| Spike | Start with `company-spike`; keep output short and decision-focused. |
| Legacy project onboarding | Start with `company-legacy-onboarding`; do not expand to full SDLC until one pilot task is reviewed. |
