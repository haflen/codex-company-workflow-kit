# NPM Entry Point And Doc Merge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a lightweight npm CLI wrapper for one-command installation and consolidate overlapping user-facing docs into a smaller, clearer set.

**Architecture:** Keep the workflow assets, templates, and behavior in the existing repository layout. Add a Node-based CLI shim that delegates to the current install scripts instead of reimplementing workflow logic. Reduce doc sprawl by merging overlapping onboarding/training content into a single primary guide while preserving the stable reference docs.

**Tech Stack:** Node.js, Bash, PowerShell, Markdown

---

### Task 1: Add a Node CLI shim for one-command installs

**Files:**
- Create: `bin/codex-company-workflow.js`
- Create: `package.json`
- Modify: `README.md`

- [ ] **Step 1: Write the failing test**

```bash
node bin/codex-company-workflow.js --help
```

Expected: command fails because the CLI file does not exist yet.

- [ ] **Step 2: Run test to verify it fails**

Run: `node bin/codex-company-workflow.js --help`

Expected: `MODULE_NOT_FOUND` or missing file error.

- [ ] **Step 3: Write minimal implementation**

```javascript
#!/usr/bin/env node
const { spawnSync } = require('node:child_process');
const path = require('node:path');

const root = path.resolve(__dirname, '..');
const args = process.argv.slice(2);
const command = args[0];
const passthrough = args.slice(1);

function run(script, scriptArgs) {
  const result = spawnSync(script, scriptArgs, { stdio: 'inherit' });
  if (result.error) throw result.error;
  process.exit(result.status ?? 0);
}

if (!command || command === '--help' || command === '-h') {
  console.log('Usage: codex-company-workflow <install-plugin|bootstrap-project|update-templates|generate-index|deactivate-project|uninstall-plugin|all|verify>');
  process.exit(0);
}

if (process.platform === 'win32') {
  run('powershell', ['-ExecutionPolicy', 'Bypass', '-File', path.join(root, 'scripts/install.ps1'), command, ...passthrough]);
} else {
  run('bash', [path.join(root, 'scripts/install.sh'), command, ...passthrough]);
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `node bin/codex-company-workflow.js --help`

Expected: usage text prints successfully.

- [ ] **Step 5: Commit**

```bash
git add bin/codex-company-workflow.js package.json README.md
git commit -m "Add npm CLI entry point"
```

### Task 2: Merge overlapping onboarding and training docs

**Files:**
- Modify: `docs/company-quickstart.md`
- Modify: `docs/codex-usage-guide.md`
- Modify: `README.md`

- [ ] **Step 1: Write the failing test**

```bash
rg -n "company-quickstart|codex-usage-guide|pilot-playbook|skill-tree|skill-upgrade-dry-run" README.md docs
```

Expected: multiple overlapping onboarding entry points still exist.

- [ ] **Step 2: Run test to verify it fails**

Run: `rg -n "company-quickstart|codex-usage-guide|pilot-playbook|skill-tree|skill-upgrade-dry-run" README.md docs`

Expected: the onboarding path points primarily to `company-quickstart.md` and `codex-usage-guide.md`, while the reference docs stay separate.

- [ ] **Step 3: Write minimal implementation**

```markdown
# Company Quickstart

This merged guide now includes installation, empty project startup, legacy project adoption, common prompts, Superpowers integration, update/uninstall/deactivate, and internal training guidance.
```

- [ ] **Step 4: Run test to verify it passes**

Run: `rg -n "company-quickstart|codex-usage-guide|pilot-playbook|skill-tree|skill-upgrade-dry-run" README.md docs`

Expected: README points to the merged onboarding guide plus a small set of stable references.

- [ ] **Step 5: Commit**

```bash
git add README.md docs/company-quickstart.md docs/codex-usage-guide.md
git commit -m "Consolidate onboarding docs"
```

## Self-Review

- The npm shim is intentionally thin and does not duplicate workflow logic.
- The merged docs keep stable reference material separate from the primary user path.
- No task introduces a new product concept beyond one-command install and doc consolidation.
- If the doc merge makes the onboarding guide too large, split the reference-heavy sections back out into appendices instead of adding another top-level guide.
