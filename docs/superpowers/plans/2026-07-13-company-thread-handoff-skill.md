# Company Thread Handoff Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a governed `company-thread-handoff` skill that exports the current task into a compact handoff package and safely resumes it in a new Codex conversation after risk-based verification.

**Architecture:** The new skill owns temporary conversation-to-conversation state transfer and does not replace `company-context-index` or formal project documents. The Chinese and English plugins expose the same protocol; `company-workflow-help` and project rules only recommend the skill at risk points, while file output remains explicit and limited to `.codex/handoff/current.md`.

**Tech Stack:** Codex Agent Skills (`SKILL.md`), plugin manifests, YAML skill metadata, Markdown documentation, Bash/PowerShell validation scripts.

## Global Constraints

- Use `superpowers:writing-skills` before editing or validating any skill.
- Default behavior outputs the handoff in chat and does not create a file.
- File mode requires explicit user authorization and only overwrites `.codex/handoff/current.md`.
- Never create dated handoff files, modify `.gitignore`, archive to `docs/` or `specs/`, create a new Codex task, or message another task automatically.
- The current main task is executable; side topics remain explicitly unauthorized.
- Resume mode must distinguish verified facts, prior-conversation judgments, and unverified items.
- Project facts override the handoff package when they conflict.
- Company and personal skills share field semantics but have no runtime dependency on each other.
- Preserve all unrelated working-tree changes and commit only files owned by each task.

---

### Task 1: Add the bilingual company handoff skill

**Files:**
- Create: `outputs/company-codex-workflow-v2-zh/skills/company-thread-handoff/SKILL.md`
- Create: `outputs/company-codex-workflow-v2-zh/skills/company-thread-handoff/agents/openai.yaml`
- Create: `outputs/company-codex-workflow-v2/skills/company-thread-handoff/SKILL.md`
- Create: `outputs/company-codex-workflow-v2/skills/company-thread-handoff/agents/openai.yaml`

**Interfaces:**
- Consumes: current conversation, current project path, Git state, authoritative workflow documents, validation evidence, and optional `.codex/handoff/current.md`.
- Produces: `quick` or `full` handoff output, optional `current.md`, a new-conversation startup prompt, and resume verification results classified as matching, changed, or unverified.

- [ ] **Step 1: Write a failing structural check**

Run:

```bash
test -f outputs/company-codex-workflow-v2-zh/skills/company-thread-handoff/SKILL.md \
  && test -f outputs/company-codex-workflow-v2/skills/company-thread-handoff/SKILL.md
```

Expected: non-zero exit because the skill files do not exist.

- [ ] **Step 2: Create the Chinese skill with the exact contract**

The file must start with:

```yaml
---
name: company-thread-handoff
description: 用于公司项目长对话准备切换到新对话、暂停未完成任务、跨成员交接，或新对话需要验证并接手已有任务时。
---
```

Add these required sections and rules:

```markdown
# 公司任务对话交接

## 模式判断
- 导出模式：用户准备开启新对话或要求生成任务交接摘要。
- 接手模式：用户粘贴交接摘要，或要求读取 `.codex/handoff/current.md` 后继续。

## 输出等级
- `quick`：纯讨论、无代码改动、无未完成验证、无阶段切换。
- `full`：代码或配置改动、未提交文件、阶段切换、范围变化、验证缺失、运行中服务或高风险事项。

## 共享字段
- 生成时间
- 当前主任务
- 当前状态
- 已完成
- 下一步
- 关键文件
- 已验证事实
- 旧对话判断
- 待确认事项
- 旁支事项（未纳入当前范围、未经授权）
- 新对话启动提示词

## 公司增强字段
- 项目路径与 Git 分支
- 工作区改动与并发风险
- 当前 workflow、阶段许可和实现授权
- 权威需求、设计、任务、业务规则和公共入口文档
- 验证等级、验证证据、未验证项与剩余风险
- 运行中服务、端口、浏览器和测试进程
- 文档与实现漂移
- Superpowers、专家 skill、插件和工具的实际调用

## 导出流程
只读取当前任务所需信息；区分事实、判断和待确认项；自动选择等级；默认只输出；用户明确要求时才覆盖 `.codex/handoff/current.md`。

## 接手预检
核对项目路径、交接时间、Git 分支、工作区、关键文件、未完成任务、阶段授权和高风险结论，并输出相符项、变化项和无法验证项。

## 风险处理
- 低风险差异：说明后继续。
- 中风险差异：重新验证并说明调整后的下一步。
- 高风险差异：停止并要求确认。

## 护栏
- 不复述完整聊天记录。
- 不把旁支事项转成当前任务。
- 不继承范围变化前的实现授权。
- 不自动创建新任务或跨任务发送消息。
- 不自动修改 `.gitignore`、正式文档或 Git 历史。
```

The final output template must include `工作流层：company-thread-handoff`, `透明度模式`, `交接模式`, `交接等级`, `生成时间`, `实际调用`, `Superpowers 叠加`, `专家/插件能力`, `未调用但采用视角`, `事实验证结果`, `验证证据`, `未验证项`, `剩余风险`, `阶段许可`, `实现授权状态`, and `下一步`.

- [ ] **Step 3: Create the English skill with semantic parity**

Use this frontmatter:

```yaml
---
name: company-thread-handoff
description: Use when a company project needs to hand an unfinished task from a long conversation to a new Codex conversation, or when a new conversation must verify and resume an existing handoff.
---
```

Translate the Chinese company-specific instructions without changing field semantics, `quick`/`full` triggers, file path, authorization rules, or risk behavior.

- [ ] **Step 4: Add slash-menu metadata**

Chinese `agents/openai.yaml`:

```yaml
interface:
  display_name: "/company-thread-handoff"
  short_description: "生成或接手公司任务对话交接摘要"
  default_prompt: "Use $company-thread-handoff to export or safely resume the current company task handoff."
```

English `agents/openai.yaml`:

```yaml
interface:
  display_name: "/company-thread-handoff"
  short_description: "Export or resume a company task handoff"
  default_prompt: "Use $company-thread-handoff to export or safely resume the current company task handoff."
```

- [ ] **Step 5: Validate structure and forbidden behavior**

Run:

```bash
rg -n "name: company-thread-handoff|quick|full|\.codex/handoff/current\.md|未经授权|高风险差异" \
  outputs/company-codex-workflow-v2-zh/skills/company-thread-handoff
rg -n "name: company-thread-handoff|quick|full|\.codex/handoff/current\.md|unauthorized|high-risk" \
  outputs/company-codex-workflow-v2/skills/company-thread-handoff
```

Expected: every required contract term appears in the matching language tree.

- [ ] **Step 6: Commit the skill pair**

```bash
git add outputs/company-codex-workflow-v2-zh/skills/company-thread-handoff \
  outputs/company-codex-workflow-v2/skills/company-thread-handoff
git commit -m "Add company thread handoff skill"
```

### Task 2: Route handoff reminders through the company workflow

**Files:**
- Modify: `outputs/company-codex-workflow-v2-zh/skills/company-workflow-help/SKILL.md`
- Modify: `outputs/company-codex-workflow-v2/skills/company-workflow-help/SKILL.md`
- Modify: `outputs/company-codex-workflow-v2-zh/AGENTS.md`
- Modify: `outputs/company-codex-workflow-v2/AGENTS.md`

**Interfaces:**
- Consumes: stop/pause/new-conversation phrases, phase transitions, unfinished validation, running services, and signs of context drift.
- Produces: a recommendation to invoke `company-thread-handoff`; it never generates or writes a handoff automatically.

- [ ] **Step 1: Write a failing routing check**

Run:

```bash
rg -n "company-thread-handoff" \
  outputs/company-codex-workflow-v2-zh/skills/company-workflow-help/SKILL.md \
  outputs/company-codex-workflow-v2-zh/AGENTS.md
```

Expected: no matching routing rule before implementation.

- [ ] **Step 2: Add the workflow-help route**

Add one route row in both languages for users who say they are opening a new conversation, stopping for now, continuing next time, or handing work to another person. Route to `company-thread-handoff` and recommend:

```text
生成当前任务交接摘要，我准备开新对话。
```

Add a reminder protocol with these exact triggers: phase completed with more work remaining; phase transition; context repetition or scope confusion; uncommitted changes; running services; incomplete verification. State that the workflow only reminds and never auto-generates or auto-writes.

- [ ] **Step 3: Add the project-level rule**

Add a `对话交接` / `Conversation Handoff` section to both `AGENTS.md` files:

- Use the handoff skill for long-conversation transfer.
- Default to chat output.
- Only write `current.md` on explicit request.
- Keep side topics unauthorized.
- Require risk-based resume verification.
- A handoff never grants new implementation authorization.

- [ ] **Step 4: Verify routing parity**

Run:

```bash
rg -n "company-thread-handoff|current\.md|不自动生成|实现授权" \
  outputs/company-codex-workflow-v2-zh/skills/company-workflow-help/SKILL.md \
  outputs/company-codex-workflow-v2-zh/AGENTS.md
rg -n "company-thread-handoff|current\.md|never auto|implementation authorization" \
  outputs/company-codex-workflow-v2/skills/company-workflow-help/SKILL.md \
  outputs/company-codex-workflow-v2/AGENTS.md
```

Expected: both language variants expose reminders and preserve authorization boundaries.

- [ ] **Step 5: Commit routing integration**

```bash
git add outputs/company-codex-workflow-v2-zh/skills/company-workflow-help/SKILL.md \
  outputs/company-codex-workflow-v2/skills/company-workflow-help/SKILL.md \
  outputs/company-codex-workflow-v2-zh/AGENTS.md \
  outputs/company-codex-workflow-v2/AGENTS.md
git commit -m "Route company conversation handoffs"
```

### Task 3: Document and version the company feature

**Files:**
- Modify: `outputs/company-codex-workflow-v2-zh/.codex-plugin/plugin.json`
- Modify: `outputs/company-codex-workflow-v2-zh/plugin.json`
- Modify: `outputs/company-codex-workflow-v2/.codex-plugin/plugin.json`
- Modify: `outputs/company-codex-workflow-v2/plugin.json`
- Modify: `README.md`
- Modify: `docs/codex-usage-guide.md`
- Modify: `docs/company-quickstart.md`
- Modify: `docs/skill-tree.md`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: the implemented skill name, trigger phrases, and file policy.
- Produces: discoverable user guidance and plugin version `0.2.23`.

- [ ] **Step 1: Write a failing documentation check**

Run:

```bash
rg -n "company-thread-handoff" README.md docs/codex-usage-guide.md docs/company-quickstart.md docs/skill-tree.md
```

Expected: no complete documentation entry before this task.

- [ ] **Step 2: Update both plugin manifests**

Set all four company manifest versions to `0.2.23`. Add “conversation handoff with risk-based resume verification” to English descriptions and “对话交接与风险分级接手验证” to Chinese descriptions without removing existing capability text.

- [ ] **Step 3: Add user guidance**

Document these two commands:

```text
生成当前任务交接摘要，我准备开新对话。
读取 .codex/handoff/current.md，验证当前状态后继续任务。
```

Explain that chat-only output is the default, file output is explicit, the file is overwritten, side topics remain unauthorized, and new conversations revalidate project facts.

- [ ] **Step 4: Add the skill-tree entry and changelog**

Add `company-thread-handoff` to the workflow skill list, distinguish it from `company-context-index`, and add a dated `0.2.23` changelog entry.

- [ ] **Step 5: Verify version and documentation**

Run:

```bash
rg -n '"version": "0\.2\.23"' \
  outputs/company-codex-workflow-v2-zh/.codex-plugin/plugin.json \
  outputs/company-codex-workflow-v2-zh/plugin.json \
  outputs/company-codex-workflow-v2/.codex-plugin/plugin.json \
  outputs/company-codex-workflow-v2/plugin.json
rg -n "company-thread-handoff|current\.md|风险分级" README.md docs CHANGELOG.md
```

Expected: four version matches and user guidance in all intended documents.

- [ ] **Step 6: Commit docs and version**

```bash
git add README.md CHANGELOG.md docs/codex-usage-guide.md docs/company-quickstart.md docs/skill-tree.md \
  outputs/company-codex-workflow-v2-zh/.codex-plugin/plugin.json \
  outputs/company-codex-workflow-v2-zh/plugin.json \
  outputs/company-codex-workflow-v2/.codex-plugin/plugin.json \
  outputs/company-codex-workflow-v2/plugin.json
git commit -m "Document company thread handoffs"
```

### Task 4: Verify and reinstall the Chinese company plugin

**Files:**
- Test: all files changed in Tasks 1-3
- Runtime target: `~/.codex/plugins/cache/personal/company-codex-workflow-v2-zh/0.2.23`

**Interfaces:**
- Consumes: completed source plugin.
- Produces: validated source, a refreshed local Codex plugin cache, and visible `/company-thread-handoff` metadata.

- [ ] **Step 1: Run repository validation**

```bash
bash scripts/install.sh verify --lang zh
bash scripts/install.sh verify --lang en
git diff --check
```

Expected: both validations pass; PowerShell syntax may be explicitly skipped when `pwsh` is unavailable; `git diff --check` prints nothing.

- [ ] **Step 2: Check skill metadata directly**

```bash
python3 /Users/dan/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py \
  outputs/company-codex-workflow-v2-zh
python3 /Users/dan/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py \
  outputs/company-codex-workflow-v2
```

Expected: both plugins validate successfully.

- [ ] **Step 3: Reinstall the Chinese plugin**

```bash
bash scripts/install.sh install-plugin --lang zh --force
/Applications/Codex.app/Contents/Resources/codex plugin remove \
  company-codex-workflow-v2-zh@personal --json
/Applications/Codex.app/Contents/Resources/codex plugin add \
  company-codex-workflow-v2-zh@personal --json
```

Expected: the personal marketplace points to version `0.2.23` and the plugin is enabled.

- [ ] **Step 4: Verify the installed cache**

```bash
/Applications/Codex.app/Contents/Resources/codex plugin list --marketplace personal
rg -n "name: company-thread-handoff|display_name: \"/company-thread-handoff\"" \
  ~/.codex/plugins/cache/personal/company-codex-workflow-v2-zh/0.2.23/skills/company-thread-handoff
```

Expected: plugin list reports company version `0.2.23`; both skill and slash-menu metadata are present in the cache.

- [ ] **Step 5: Record final verification without committing generated artifacts**

Confirm `git status --short` contains no generated readiness files or cache files. Preserve unrelated pre-existing modifications and do not commit them as part of this task.
