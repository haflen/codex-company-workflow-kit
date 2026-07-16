# Company Delivery Closeout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a bilingual `company-delivery-closeout` workflow that safely consolidates a completed company milestone, verifies the final candidate, creates one local commit, and optionally performs a normal push to the current business branch.

**Architecture:** Keep milestone closeout separate from task implementation. The new skill is a policy-and-orchestration layer: it classifies every changed file, reconciles authoritative documents, performs provenance-based cleanup, composes existing Superpowers review/verification/branch-finishing skills, and permits Git mutation only after explicit gates pass. No generic cleanup script is added in this release; behavior is verified through static contract checks and isolated temporary Git repositories.

**Tech Stack:** Codex plugin skills (`SKILL.md`), Codex skill menu metadata (`agents/openai.yaml`), Markdown documentation, JSON plugin manifests, Bash/PowerShell installation tooling, Git.

## Global Constraints

- Implement the approved design in `docs/superpowers/specs/2026-07-16-company-delivery-closeout-design.md` without widening its scope.
- Add the same workflow semantics to `outputs/company-codex-workflow-v2-zh` and `outputs/company-codex-workflow-v2`; only user-facing language differs.
- Expose one English slash entry in both packages: `/company-delivery-closeout`.
- Support exactly three modes: `prepare`, `commit`, and `deliver`.
- Treat `所有任务已完成，开始交付收口并推送业务分支。` and its English equivalent as one-shot authorization for ordinary commit plus ordinary push only.
- Never authorize force push, rebase, amend, merge, release, deploy, branch deletion, unknown-file deletion, or protected-branch delivery.
- Never use `git add .`, unscoped `git clean -fdx`, `git reset --hard`, or implicit whole-worktree staging.
- Compose `superpowers:requesting-code-review`, `superpowers:verification-before-completion`, and `superpowers:finishing-a-development-branch`; use `company-expert-routing` only when domain risk justifies it.
- Do not add `scripts/closeout.sh`, `scripts/closeout.ps1`, a machine-readable closeout configuration, or a new permanent project document in this release.
- Bump all company package manifests from `0.2.23` to `0.2.24` only after both language packages validate.
- Preserve all pre-existing dirty-worktree changes. Stage explicit paths and inspect `git diff --cached` before every commit.
- Do not invoke subagents unless the user explicitly requests them.

## File Map

- Create `outputs/company-codex-workflow-v2-zh/skills/company-delivery-closeout/SKILL.md`: authoritative Chinese closeout workflow.
- Create `outputs/company-codex-workflow-v2-zh/skills/company-delivery-closeout/agents/openai.yaml`: Chinese menu description with the English slash entry.
- Create `outputs/company-codex-workflow-v2/skills/company-delivery-closeout/SKILL.md`: semantically equivalent English workflow.
- Create `outputs/company-codex-workflow-v2/skills/company-delivery-closeout/agents/openai.yaml`: English menu metadata.
- Modify both `skills/company-workflow-help/SKILL.md`: route completed-batch and milestone-closeout language into the new workflow.
- Modify both `skills/company-implementation-runner/SKILL.md`: recommend closeout when no implementation task remains.
- Modify both package `AGENTS.md`: define project-level delivery-closeout authority and stop conditions.
- Modify four manifests under the two packages: version and capability copy.
- Modify `README.md`, `docs/company-quickstart.md`, `docs/codex-usage-guide.md`, `docs/skill-tree.md`, and `CHANGELOG.md`: user entry, examples, skill tree, and release record.

---

### Task 1: Add the bilingual delivery-closeout skill

**Files:**
- Create: `outputs/company-codex-workflow-v2-zh/skills/company-delivery-closeout/SKILL.md`
- Create: `outputs/company-codex-workflow-v2-zh/skills/company-delivery-closeout/agents/openai.yaml`
- Create: `outputs/company-codex-workflow-v2/skills/company-delivery-closeout/SKILL.md`
- Create: `outputs/company-codex-workflow-v2/skills/company-delivery-closeout/agents/openai.yaml`

**Interfaces:**
- Consumes: completed task documents, Git branch/worktree state, project verification commands, existing authoritative project documents, and the three Superpowers skills named in Global Constraints.
- Produces: a selected mode, seven-phase closeout execution, stop/continue decision, exact staged-file allowlist, optional commit/push, and a structured closeout report.

- [ ] **Step 1: Invoke the skill-authoring process before editing**

Read and follow:

```bash
sed -n '1,280p' "$HOME/.codex/plugins/cache/openai-curated-remote/superpowers/6.1.1/skills/writing-skills/SKILL.md"
```

Expected: the implementation uses scenario-based skill verification, concise trigger metadata, and no copied implementation of existing Superpowers workflows.

- [ ] **Step 2: Write a failing structural contract check**

Run before creating the directories:

```bash
for lang in company-codex-workflow-v2-zh company-codex-workflow-v2; do
  test -f "outputs/$lang/skills/company-delivery-closeout/SKILL.md"
  test -f "outputs/$lang/skills/company-delivery-closeout/agents/openai.yaml"
done
```

Expected: FAIL because the new skill files do not exist.

- [ ] **Step 3: Create the Chinese skill with the complete behavioral contract**

The YAML front matter must be:

```yaml
---
name: company-delivery-closeout
description: Use when 公司项目的任务批次、功能、里程碑或版本阶段已经完成，需要规整代码与文档成果、清理可证明的临时产物、完成最终验证，并按授权本地提交或推送当前业务分支时。
---
```

The body must define all of these exact sections and rules:

```text
核心原则
模式判断: prepare / commit / deliver
授权边界
阶段一: 范围与分支门禁
阶段二: 成果盘点与逐文件分类
阶段三: 文档与成果规整
阶段四: 临时产物 dry-run 与来源证明
阶段五: 最终验证、代码审查与安全检查
阶段六: 精确暂存、commit 与普通 push
阶段七: 交付报告
停止条件
Superpowers 叠加
输出契约
```

Include these normative requirements:

```text
- Every changed/untracked file is classified as include, retain-but-exclude, cleanup-candidate, or blocking-unknown.
- Unknown ownership blocks deletion, commit, and push.
- prepare never commits or pushes; commit never pushes; deliver may run git push -u origin HEAD.
- main, master, develop, integration, release branches, and project-defined protected branches block commit/push.
- Final verification runs on the exact final candidate after cleanup and documentation reconciliation.
- Staging uses explicit paths only, followed by git diff --cached --name-status and git diff --cached --check.
- A rejected normal push stops; the workflow never rebases or force-pushes automatically.
- `superpowers:finishing-a-development-branch` supplies branch-finalization checks only; it must not replace the selected `prepare`/`commit`/`deliver` mode with PR, merge, worktree deletion, or another integration action.
- Completion claims include fresh verification evidence, commit SHA, branch, remote, and push result.
```

- [ ] **Step 4: Create Chinese menu metadata**

Write exactly:

```yaml
interface:
  display_name: "/company-delivery-closeout"
  short_description: "规整成果、验证并安全提交或推送业务分支"
  default_prompt: "Use $company-delivery-closeout to consolidate completed company work, verify the final candidate, and safely commit or push the current business branch."
```

- [ ] **Step 5: Create the English skill and menu metadata**

Translate the complete Chinese contract without weakening any gate. Use this front matter and menu metadata:

```yaml
---
name: company-delivery-closeout
description: Use when a company task batch, feature, milestone, or version phase is complete and the resulting code and documents must be consolidated, provenance-confirmed temporary artifacts cleaned, the final candidate verified, and the current business branch committed or pushed as authorized.
---
```

```yaml
interface:
  display_name: "/company-delivery-closeout"
  short_description: "Consolidate, verify, commit, or push completed work"
  default_prompt: "Use $company-delivery-closeout to consolidate completed company work, verify the final candidate, and safely commit or push the current business branch."
```

- [ ] **Step 6: Run structural and safety assertions**

```bash
for lang in company-codex-workflow-v2-zh company-codex-workflow-v2; do
  skill="outputs/$lang/skills/company-delivery-closeout/SKILL.md"
  menu="outputs/$lang/skills/company-delivery-closeout/agents/openai.yaml"
  test "$(sed -n '2p' "$skill")" = "name: company-delivery-closeout"
  rg -q 'prepare' "$skill"
  rg -q 'commit' "$skill"
  rg -q 'deliver' "$skill"
  rg -q 'superpowers:requesting-code-review' "$skill"
  rg -q 'superpowers:verification-before-completion' "$skill"
  rg -q 'superpowers:finishing-a-development-branch' "$skill"
  rg -q 'git diff --cached' "$skill"
  rg -q '/company-delivery-closeout' "$menu"
done

! rg -n 'git add \.|git clean -fdx|git reset --hard|git push --force|git push -f' \
  outputs/company-codex-workflow-v2{,-zh}/skills/company-delivery-closeout
```

Expected: all positive assertions pass and the forbidden-command scan has no matches.

- [ ] **Step 7: Review and commit only the four new files**

```bash
git diff --check -- \
  outputs/company-codex-workflow-v2-zh/skills/company-delivery-closeout \
  outputs/company-codex-workflow-v2/skills/company-delivery-closeout
git add \
  outputs/company-codex-workflow-v2-zh/skills/company-delivery-closeout/SKILL.md \
  outputs/company-codex-workflow-v2-zh/skills/company-delivery-closeout/agents/openai.yaml \
  outputs/company-codex-workflow-v2/skills/company-delivery-closeout/SKILL.md \
  outputs/company-codex-workflow-v2/skills/company-delivery-closeout/agents/openai.yaml
git diff --cached --name-status
git commit -m "Add company delivery closeout workflow"
```

Expected: staged paths are exactly the four new files; no pre-existing modified file enters the commit.

### Task 2: Connect workflow routing and project guardrails

**Files:**
- Modify: `outputs/company-codex-workflow-v2-zh/skills/company-workflow-help/SKILL.md`
- Modify: `outputs/company-codex-workflow-v2/skills/company-workflow-help/SKILL.md`
- Modify: `outputs/company-codex-workflow-v2-zh/skills/company-implementation-runner/SKILL.md`
- Modify: `outputs/company-codex-workflow-v2/skills/company-implementation-runner/SKILL.md`
- Modify: `outputs/company-codex-workflow-v2-zh/AGENTS.md`
- Modify: `outputs/company-codex-workflow-v2/AGENTS.md`

**Interfaces:**
- Consumes: closeout trigger phrases and the implementation runner's task-completion decision.
- Produces: automatic user routing, mandatory next-step guidance, and project-level protection against premature or unsafe delivery.

- [ ] **Step 1: Capture current diffs for the six already-modified files**

```bash
mkdir -p /private/tmp/company-closeout-baseline
for f in \
  outputs/company-codex-workflow-v2-zh/skills/company-workflow-help/SKILL.md \
  outputs/company-codex-workflow-v2/skills/company-workflow-help/SKILL.md \
  outputs/company-codex-workflow-v2-zh/skills/company-implementation-runner/SKILL.md \
  outputs/company-codex-workflow-v2/skills/company-implementation-runner/SKILL.md \
  outputs/company-codex-workflow-v2-zh/AGENTS.md \
  outputs/company-codex-workflow-v2/AGENTS.md; do
  git diff -- "$f" > "/private/tmp/company-closeout-baseline/$(echo "$f" | tr '/' '_').patch"
done
```

Expected: six baseline patch files preserve the exact pre-existing unstaged changes for later comparison.

- [ ] **Step 2: Add closeout routing to both workflow-help tables**

Add one row after continuous implementation:

```text
Trigger: all tasks are complete; consolidate results; clean temporary files; close out and push
Complexity: L2/L3
Route: company-delivery-closeout
Superpowers: requesting-code-review + verification-before-completion + finishing-a-development-branch
Recommended phrase: All tasks are complete. Start delivery closeout and push the business branch.
```

Also add an automatic-routing rule: use closeout only when no implementation task remains; if tasks remain, route back to implementation or require an explicit defer/not-do decision.

- [ ] **Step 3: Add the implementation-to-closeout transition in both runners**

Add to completion and continuous-execution guidance:

```text
- If executable tasks remain, recommend the next task or batch.
- If every task is completed, explicitly deferred, or explicitly rejected, recommend company-delivery-closeout.
- Never perform milestone commit/push inside company-implementation-runner.
- Recommended phrase: All tasks are complete. Start delivery closeout and push the business branch.
```

Add report fields:

```text
- Delivery closeout readiness: ready / not ready
- Closeout blockers:
- Recommended next workflow:
```

- [ ] **Step 4: Add project-level closeout boundaries to both AGENTS files**

Require the following policy:

```text
- Task implementation and milestone closeout are separate workflow stages.
- Commit/push requires company-delivery-closeout in commit or deliver mode.
- Unknown ownership, incomplete tasks, failed final verification, documentation conflict, sensitive/large files, protected branches, staged mismatch, or rejected normal push stops delivery.
- Ordinary push authorization never includes rebase, force, amend, merge, release, or deploy.
```

- [ ] **Step 5: Run routing and parity checks**

```bash
for lang in company-codex-workflow-v2-zh company-codex-workflow-v2; do
  rg -q 'company-delivery-closeout' "outputs/$lang/skills/company-workflow-help/SKILL.md"
  rg -q 'company-delivery-closeout' "outputs/$lang/skills/company-implementation-runner/SKILL.md"
  rg -q 'company-delivery-closeout' "outputs/$lang/AGENTS.md"
done

git diff --check -- \
  outputs/company-codex-workflow-v2-zh/skills/company-workflow-help/SKILL.md \
  outputs/company-codex-workflow-v2/skills/company-workflow-help/SKILL.md \
  outputs/company-codex-workflow-v2-zh/skills/company-implementation-runner/SKILL.md \
  outputs/company-codex-workflow-v2/skills/company-implementation-runner/SKILL.md \
  outputs/company-codex-workflow-v2-zh/AGENTS.md \
  outputs/company-codex-workflow-v2/AGENTS.md
```

Expected: each package routes and constrains closeout, with no whitespace errors.

- [ ] **Step 6: Stage with hunk-level care and commit**

Because all six files already contain unrelated user changes, inspect the new closeout hunks against the baseline snapshots. Stage only if `git diff --cached` contains both the preserved prior work intentionally intended for the same release and the new closeout changes; otherwise leave these files unstaged and report the dependency instead of making a mixed commit.

```bash
git diff -- \
  outputs/company-codex-workflow-v2-zh/skills/company-workflow-help/SKILL.md \
  outputs/company-codex-workflow-v2/skills/company-workflow-help/SKILL.md \
  outputs/company-codex-workflow-v2-zh/skills/company-implementation-runner/SKILL.md \
  outputs/company-codex-workflow-v2/skills/company-implementation-runner/SKILL.md \
  outputs/company-codex-workflow-v2-zh/AGENTS.md \
  outputs/company-codex-workflow-v2/AGENTS.md
```

Expected: every new hunk traces to routing or closeout safety. Do not use an interactive Git console; if selective staging cannot be proved safe, defer this commit.

### Task 3: Version and document the new workflow

**Files:**
- Modify: `outputs/company-codex-workflow-v2-zh/.codex-plugin/plugin.json`
- Modify: `outputs/company-codex-workflow-v2-zh/plugin.json`
- Modify: `outputs/company-codex-workflow-v2/.codex-plugin/plugin.json`
- Modify: `outputs/company-codex-workflow-v2/plugin.json`
- Modify: `README.md`
- Modify: `docs/company-quickstart.md`
- Modify: `docs/codex-usage-guide.md`
- Modify: `docs/skill-tree.md`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: the implemented bilingual skill and routing behavior.
- Produces: discoverable installation/use guidance and a consistent `0.2.24` package release.

- [ ] **Step 1: Update all four manifests**

Set `version` to `0.2.24`. Add delivery closeout to `description` and `interface.longDescription` without removing existing capabilities, and keep author/repository metadata unchanged.

- [ ] **Step 2: Assert manifest identity and version**

```bash
for f in \
  outputs/company-codex-workflow-v2-zh/.codex-plugin/plugin.json \
  outputs/company-codex-workflow-v2-zh/plugin.json \
  outputs/company-codex-workflow-v2/.codex-plugin/plugin.json \
  outputs/company-codex-workflow-v2/plugin.json; do
  test "$(jq -r '.version' "$f")" = "0.2.24"
  test "$(jq -r '.author.name' "$f")" = "haflen"
  test "$(jq -r '.repository' "$f")" = "https://github.com/haflen/codex-company-workflow-kit"
done
```

Expected: all four manifests report `0.2.24` and retain the public project metadata.

- [ ] **Step 3: Update user documentation**

Add concise content in the existing relevant sections, not duplicate standalone guides:

```text
README: add closeout to capabilities and common phrases.
company-quickstart: explain when implementation ends and closeout begins.
codex-usage-guide: document prepare/commit/deliver, authorization, stop conditions, and a milestone example.
skill-tree: add company-delivery-closeout after implementation and before completed delivery.
CHANGELOG: add 0.2.24 dated 2026-07-16.
```

The complete example must use neutral names such as `example-service` and `feature/order-summary`; it must not contain personal names, local user paths, or private business names.

- [ ] **Step 4: Run documentation checks**

```bash
rg -n 'company-delivery-closeout|交付收口' \
  README.md docs/company-quickstart.md docs/codex-usage-guide.md docs/skill-tree.md CHANGELOG.md
! rg -n '/Users/[[:alnum:]_.-]+|[[:alnum:]_.-]+@[^ ]*MacBook-Pro|private-project-name' \
  README.md docs/company-quickstart.md docs/codex-usage-guide.md docs/skill-tree.md
git diff --check -- \
  README.md docs/company-quickstart.md docs/codex-usage-guide.md docs/skill-tree.md CHANGELOG.md \
  outputs/company-codex-workflow-v2{,-zh}/plugin.json \
  outputs/company-codex-workflow-v2{,-zh}/.codex-plugin/plugin.json
```

Expected: closeout is documented in every required entry point; public docs contain no personal/project-specific examples or whitespace errors.

- [ ] **Step 5: Stage only reviewed release hunks**

All files in this task already have pre-existing modifications. Compare against `git diff`, stage only after confirming the combined file is intended for release `0.2.24`, then inspect:

```bash
git diff --cached --name-status
git diff --cached --check
git diff --cached --stat
```

Expected: no unreviewed script, generated directory, personal data, or unrelated file is staged. If clean separation cannot be proved, leave the files unstaged and continue validation without claiming a release commit.

### Task 4: Validate source packages and install only the Chinese package locally

**Files:**
- Verify: `outputs/company-codex-workflow-v2-zh/`
- Verify: `outputs/company-codex-workflow-v2/`
- Verify: `scripts/install.sh`
- Verify: `scripts/install.ps1`
- Local install target: `~/.codex/plugins/cache/personal/company-codex-workflow-v2-zh/0.2.24/`

**Interfaces:**
- Consumes: versioned source packages.
- Produces: validated bilingual source and one locally installed Chinese plugin, preserving the user's Chinese-only local preference.

- [ ] **Step 1: Run repository verification and plugin validation**

```bash
bash scripts/install.sh verify --lang zh
bash scripts/install.sh verify --lang en
python3 "$HOME/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py" \
  outputs/company-codex-workflow-v2-zh
python3 "$HOME/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py" \
  outputs/company-codex-workflow-v2
bash -n scripts/install.sh
```

Expected: both packages validate and the shell installer passes syntax checking. If `pwsh` exists, also parse `scripts/install.ps1`; otherwise record PowerShell validation as not run.

- [ ] **Step 2: Verify skill counts and bilingual parity**

```bash
zh_count=$(find outputs/company-codex-workflow-v2-zh/skills -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')
en_count=$(find outputs/company-codex-workflow-v2/skills -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')
test "$zh_count" = "$en_count"
test "$zh_count" = "31"
comm -3 \
  <(find outputs/company-codex-workflow-v2-zh/skills -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort) \
  <(find outputs/company-codex-workflow-v2/skills -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort)
```

Expected: both packages have 31 identically named skill directories and `comm` prints nothing.

- [ ] **Step 3: Install the Chinese package and verify discovery**

```bash
bash scripts/install.sh install-plugin --lang zh --force
/Applications/Codex.app/Contents/Resources/codex plugin list
```

Expected: `company-codex-workflow-v2-zh` is installed at `0.2.24`; no English company package is installed by this step.

- [ ] **Step 4: Verify the installed closeout files**

```bash
installed="$HOME/.codex/plugins/cache/personal/company-codex-workflow-v2-zh/0.2.24"
test -f "$installed/skills/company-delivery-closeout/SKILL.md"
test -f "$installed/skills/company-delivery-closeout/agents/openai.yaml"
rg -q '/company-delivery-closeout' "$installed/skills/company-delivery-closeout/agents/openai.yaml"
```

Expected: the local Chinese plugin exposes the new English slash entry with Chinese description.

### Task 5: Exercise stop and success paths in isolated Git repositories

**Files:**
- Test fixture only: `/private/tmp/company-closeout-runtime/`
- No production repository files are modified by runtime tests.

**Interfaces:**
- Consumes: locally installed Chinese `company-delivery-closeout` skill and Codex CLI.
- Produces: evidence that unknown files and protected branches stop, while a clean business branch can commit and push normally.

- [ ] **Step 1: Create an isolated remote and business-branch fixture**

```bash
rm -rf /private/tmp/company-closeout-runtime
mkdir -p /private/tmp/company-closeout-runtime
git init --bare /private/tmp/company-closeout-runtime/remote.git
git init -b main /private/tmp/company-closeout-runtime/work
cd /private/tmp/company-closeout-runtime/work
git config user.name "Workflow Test"
git config user.email "workflow-test@example.invalid"
printf '# Fixture\n' > README.md
git add README.md
git commit -m "Initial fixture"
git remote add origin /private/tmp/company-closeout-runtime/remote.git
git push -u origin main
git switch -c feature/milestone-closeout
mkdir -p src .tmp
printf 'export const value = 1;\n' > src/value.ts
printf 'known temporary output\n' > .tmp/closeout-known.txt
printf 'unknown user material\n' > unknown-notes.txt
```

Expected: the feature branch contains one code change, one known temporary fixture, and one unknown untracked file.

- [ ] **Step 2: Run the blocking-unknown scenario**

```bash
cd /private/tmp/company-closeout-runtime/work
before=$(git rev-parse HEAD)
"$HOME/.local/bin/codex" exec -m gpt-5.4 \
  'Use $company-delivery-closeout in deliver mode. Treat .tmp/closeout-known.txt as workflow-created temporary output. Do not assume ownership of unknown-notes.txt. Follow the skill and report the decision.'
test "$(git rev-parse HEAD)" = "$before"
test -e unknown-notes.txt
```

Expected: Codex reports `unknown-notes.txt` as blocking, does not delete it, creates no new commit, and does not push the feature branch.

- [ ] **Step 3: Remove only the test blocker and run the success scenario**

```bash
rm /private/tmp/company-closeout-runtime/work/unknown-notes.txt
cd /private/tmp/company-closeout-runtime/work
"$HOME/.local/bin/codex" exec -m gpt-5.4 \
  'Use $company-delivery-closeout in deliver mode. All fixture tasks are complete. .tmp/closeout-known.txt is a workflow-created temporary output and may be deleted. Verify the final candidate, create one local commit, and normally push the current business branch.'
```

Expected: the known temporary file is removed, `src/value.ts` is committed, and `feature/milestone-closeout` is pushed to the local bare remote without force.

- [ ] **Step 4: Verify Git evidence independently**

```bash
cd /private/tmp/company-closeout-runtime/work
test ! -e .tmp/closeout-known.txt
test -z "$(git status --porcelain)"
test "$(git rev-parse HEAD)" = "$(git rev-parse refs/remotes/origin/feature/milestone-closeout)"
git log -1 --format='%H %s'
git ls-tree -r --name-only HEAD
```

Expected: worktree clean, local and remote feature heads equal, and the final tree contains `README.md` and `src/value.ts` but no temporary file.

- [ ] **Step 5: Exercise protected-branch refusal**

```bash
cd /private/tmp/company-closeout-runtime/work
git switch main
printf 'must not deliver from main\n' >> README.md
before=$(git rev-parse HEAD)
"$HOME/.local/bin/codex" exec -m gpt-5.4 \
  'Use $company-delivery-closeout in deliver mode for this completed fixture.'
test "$(git rev-parse HEAD)" = "$before"
```

Expected: Codex stops because `main` is protected; no commit or push occurs.

### Task 6: Final verification and completion report

**Files:**
- Verify all files listed in Tasks 1-4.
- Do not modify or stage unrelated dirty-worktree files.

**Interfaces:**
- Consumes: source checks, plugin validation, installation evidence, and isolated runtime evidence.
- Produces: final release-readiness report and an exact account of committed versus preserved changes.

- [ ] **Step 1: Run final static checks**

```bash
rg -n 'company-delivery-closeout' \
  outputs/company-codex-workflow-v2-zh \
  outputs/company-codex-workflow-v2 \
  README.md docs/company-quickstart.md docs/codex-usage-guide.md docs/skill-tree.md CHANGELOG.md

! rg -n 'git add \.|git clean -fdx|git reset --hard|git push --force|git push -f' \
  outputs/company-codex-workflow-v2{,-zh}/skills/company-delivery-closeout

git diff --check
git diff --cached --check
```

Expected: all intended routes are discoverable, forbidden commands are absent from the skill, and both unstaged/staged diffs are whitespace-clean.

- [ ] **Step 2: Re-run package verification**

```bash
bash scripts/install.sh verify --lang zh
bash scripts/install.sh verify --lang en
/Applications/Codex.app/Contents/Resources/codex plugin list
```

Expected: source verification succeeds and the local Chinese plugin reports `0.2.24`.

- [ ] **Step 3: Audit repository state before any final commit**

```bash
git status --short
git diff --cached --name-status
git log --oneline -5
```

Expected: each created commit contains only reviewed closeout files. Pre-existing dirty files that were not safely separable remain unstaged and are listed explicitly in the report.

- [ ] **Step 4: Produce the completion report**

Report:

```text
Workflow layer: company-delivery-closeout implementation
Superpowers used: writing-skills, verification-before-completion
Source version: 0.2.24
Chinese/English skill parity:
Local Chinese plugin installation:
Static verification:
Runtime stop-path verification:
Runtime deliver-path verification:
Commits created:
Pre-existing changes preserved:
Uncommitted closeout files, if any:
Remaining risks:
Recommended next action:
```

Do not claim that the GitHub repository was updated or that a release was published unless a separate, explicit push succeeds.
