# Requirements Prototype Workflow Design

## Goal

Add a company requirements-stage HTML prototype workflow that validates pages, interactions, wording, and business presentation before technical design, without treating prototype edits as production implementation or forcing design and task planning.

## Problem

The current workflow has no explicit route between requirements clarification and technical design. `company-feature-requirements` aims to produce requirements ready for design, while `AGENTS.md` says requirements work must not edit implementation code. When a user asks to create or revise an HTML prototype during requirements, Codex can therefore misclassify the prototype as production code or as evidence that the project has entered `company-feature-design`, then request a design document and task breakdown prematurely.

The existing `company-spike-research` also mentions prototypes, but it means technical feasibility prototypes. A page and interaction prototype validates product requirements, not architecture feasibility.

## First-Principles Boundary

An artifact's stage is determined by its purpose and dependency boundary, not its file extension.

- Requirements prototype: validates what users see and do; mock-only; isolated from production source.
- Technical spike: validates whether a technology or architecture can work.
- Production implementation: changes the deployable system and must follow confirmed design, planning, implementation, and verification boundaries.

HTML is therefore allowed during requirements only when it is an isolated requirements-validation artifact. HTML inside the production frontend remains production code.

## Selected Approach

Create a dedicated bilingual `company-requirements-prototype` skill. It is a requirements-stage validation branch, not a new SDLC phase.

Alternatives rejected:

- A sub-mode inside `company-feature-requirements` would add fewer skills, but would make a high-frequency skill larger and easier to shortcut from its description.
- Reusing `company-spike-research` would mix product evidence with technical evidence and create incorrect routes, numbering, and completion criteria.

## Entry Conditions

Route to `company-requirements-prototype` when the current stage is requirements and the user asks to:

- create, draw, preview, revise, or confirm an HTML/page/interaction prototype;
- visualize confirmed or emerging requirements before technical design;
- inspect a page flow, navigation, wording, states, dashboards, forms, or mock business results;
- continue prototype feedback without entering design or implementation.

Do not require all requirements to be frozen. Require enough clarity to identify the target user, primary scenario, in-scope pages, key states, and unresolved questions that the prototype is intended to test.

## Workflow

1. Read the authoritative requirements and linked business rules.
2. State that the stage remains `requirements` and production implementation authorization is absent.
3. Define the prototype validation scope: questions to answer, screens, interactions, data states, and explicit non-goals.
4. Use `superpowers:brainstorming` for the first prototype or a material UX/interaction change. Mechanical revisions after a confirmed direction do not restart brainstorming.
5. Use `company-expert-routing` for non-trivial UI work. Prefer the existing `company-frontend-delivery` bundle, with `frontend-design` for visual/interaction quality and `webapp-testing` for browser evidence. Use `frontend-developer` only when the prototype itself needs non-trivial client behavior.
6. Create or revise isolated mock-only HTML/CSS/JavaScript. Do not connect production APIs, databases, credentials, or real customer data.
7. Verify the prototype in a browser at relevant desktop/mobile sizes, exercise key interactions and states, inspect console errors, and stop browser/server processes created by the workflow.
8. Present the prototype and collect feedback. New or changed requirements return to `company-feature-requirements`, then re-enter prototype iteration without design or task planning.
9. On explicit prototype confirmation, promote the approved files to a requirements baseline, update the requirements prototype section, verify checksums/links, and stop.
10. Only an explicit user instruction to enter technical design may route to `company-feature-design`. Prototype confirmation alone never enters design or planning.

## Artifact Lifecycle

### Draft

Default draft location:

```text
.codex-workflow/prototypes/<feature>/draft/
```

The workflow creates a small `prototype.json` manifest containing:

- feature identifier;
- source requirements path;
- status: `draft`;
- created and last-updated times;
- files created by the workflow;
- validation questions;
- latest browser verification summary.

Draft files remain untracked by default. The workflow does not silently modify `.gitignore`. Files listed in the manifest are workflow-owned temporary prototype artifacts and must not be described as unknown parallel business-code changes.

### Promotion

Trigger phrase or equivalent intent:

```text
需求和原型均确认，转为需求基线。
```

The approved prototype is copied next to the authoritative requirements document under:

```text
<requirements-directory>/prototype/
```

The requirements document records:

- prototype status: confirmed;
- baseline version and path;
- confirmation date;
- validated pages, interactions, wording, and states;
- known limitations and items not promised by the prototype;
- SHA-256 for the baseline entry HTML or approved archive.

After source and baseline checksums match and links are valid, the workflow may remove only draft files proven by `prototype.json`. It must not delete unrelated files. Promotion does not commit or push unless separately authorized.

### Replacement and Withdrawal

- A later confirmed baseline replaces the requirements reference but does not silently delete an older committed baseline.
- A rejected draft is marked `withdrawn` and may be removed using manifest provenance.
- Delivery closeout classifies unpromoted manifest-owned drafts as temporary artifacts and asks for cleanup or deferral before commit.

## Requirements Template

Add an optional `需求原型验证` / `Requirements Prototype Validation` section:

- 是否触发：否 / 草稿迭代 / 待确认 / 已确认 / 已撤回
- 验证目标：
- 草稿位置：
- 基线版本与路径：
- 已验证页面、交互、状态和文案：
- 原型未承诺内容：
- 用户反馈与需求变更：
- 确认日期与 SHA-256：

The section appears only when a prototype is requested. Small non-visual requirements do not gain prototype paperwork.

## Production Boundary and Circuit Breakers

Allowed in the requirements prototype:

- self-contained HTML and CSS;
- mock JavaScript interactions;
- generated/mock data and non-sensitive static assets;
- responsive, accessibility, interaction, and browser verification.

Stop and reroute when the user asks for:

- real API, database, authentication, production data, or production components;
- framework migration, deployable integration, backend behavior, schema, or infrastructure;
- performance or technology feasibility evidence.

Use `company-spike-research` for technical feasibility. Use `company-feature-design` only after the user authorizes technical design. Use `company-implementation-runner` only after requirements, design, and tasks are confirmed.

## Workflow Integration

Update:

- `company-workflow-help`: add a requirements-prototype route and prevent automatic design/planning.
- `company-feature-requirements`: allow the prototype validation loop and return prototype feedback to requirements.
- `company-feature-design`: state that an HTML prototype does not prove design authorization.
- `company-spike-research`: distinguish technical prototypes from requirements prototypes.
- Company `AGENTS.md` and bootstrap templates: allow isolated requirements prototypes while continuing to forbid production code changes.
- `company-delivery-closeout`: recognize manifest-owned draft prototypes and promoted baselines.
- Requirements templates, quickstart, usage guide, common prompts, skill tree, README, changelog, and bilingual manifests.

## Output Contract

Every prototype turn reports:

- 工作流层：`company-requirements-prototype`
- 当前阶段：需求阶段
- 原型状态：草稿迭代 / 待确认 / 已确认 / 已撤回
- 生产实现授权：无
- 实际调用：
- Superpowers 叠加：
- 专家/插件能力：
- 原型验证目标：
- 草稿或基线路径：
- 浏览器验证证据：
- 需求反馈与文档漂移：
- 未验证项与剩余风险：
- 下一步：继续需求/原型迭代；转需求基线；或等待用户明确进入技术设计

The completion message must not recommend task planning while prototype or requirement confirmation is pending.

## Adversarial Review

| Failure | Control |
| --- | --- |
| Prototype silently becomes production architecture | Mock-only and isolated-path rules; record unpromised technical details |
| Prototype completion triggers design/tasks | Explicit authorization gate and requirements-stage output |
| Draft files create recurring dirty-worktree alarms | Manifest-based known temporary classification |
| Cleanup deletes unrelated files | Delete only paths proven by `prototype.json` |
| Prototype contradicts business rules | Read linked `business-rules.md`; return conflicts to requirements |
| Real integration sneaks into requirements | API/database/auth/production-component circuit breakers |
| Visual approval is mistaken for complete requirements | Record validated scope, limitations, unresolved requirements, and explicit confirmation state |

## Verification Scenarios

1. After requirements clarification, “先画 HTML 原型” routes to `company-requirements-prototype`, not design or planning.
2. “修改这个原型的页面和交互” edits only the isolated draft and remains in requirements.
3. Prototype feedback changes a business rule; the workflow updates requirements/business rules and continues the prototype loop.
4. “接真实接口看看” stops prototype work and asks whether the goal is technical spike or authorized design.
5. “需求和原型均确认，转为需求基线” promotes verified files, updates requirements metadata, and stops without creating design/tasks.
6. “需求和原型均确认，进入技术设计” promotes the baseline and then routes to `company-feature-design`; it still does not create tasks.
7. A non-visual small requirement does not create prototype files or template sections.

## Release

Release bilingual company packages as `0.2.26`. Install only the Chinese package locally. Validate source and installed caches, run RED/GREEN skill scenarios, and push the company repository without staging unrelated files.
