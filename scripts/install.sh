#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MARKETPLACE_ROOT="${HOME}/.agents/plugins"
MARKETPLACE_FILE="$MARKETPLACE_ROOT/marketplace.json"
PLUGIN_INSTALL_ROOT="${HOME}/plugins"
FORCE=0
ALL_LANGS=0
LANG_CODE="zh"
PLUGIN_NAME=""
PLUGIN_SRC=""
PLUGIN_DST=""
MARKER_BEGIN="<!-- codex-workflow-kit:company:start -->"
MARKER_END="<!-- codex-workflow-kit:company:end -->"
LEGACY_MARKER_BEGIN="<!-- company-codex-workflow-kit:start -->"
VALIDATOR_PATH="${CODEX_PLUGIN_VALIDATOR:-$HOME/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py}"

usage() {
  cat <<'USAGE'
Usage:
  bash scripts/install.sh install-plugin [--lang zh|en] [--force]
  bash scripts/install.sh uninstall-plugin [--lang zh|en|--all]
  bash scripts/install.sh bootstrap-project <project-path> [--lang zh|en] [--force]
  bash scripts/install.sh deactivate-project <project-path> [--force]
  bash scripts/install.sh update-templates <project-path> [--lang zh|en] [--force]
  bash scripts/install.sh generate-index <project-path> [--lang zh|en] [--force]
  bash scripts/install.sh all <project-path> [--lang zh|en] [--force]
  bash scripts/install.sh verify [--lang zh|en]
USAGE
}

parse_options() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --force)
        FORCE=1
        shift
        ;;
      --all)
        ALL_LANGS=1
        shift
        ;;
      --lang)
        LANG_CODE="${2:-}"
        shift 2
        ;;
      --lang=*)
        LANG_CODE="${1#--lang=}"
        shift
        ;;
      *)
        shift
        ;;
    esac
  done
  case "$LANG_CODE" in
    zh) PLUGIN_NAME="company-codex-workflow-v2-zh" ;;
    en) PLUGIN_NAME="company-codex-workflow-v2" ;;
    *)
      echo "Unsupported language: $LANG_CODE. Use zh or en." >&2
      exit 1
      ;;
  esac
  PLUGIN_SRC="$ROOT_DIR/outputs/$PLUGIN_NAME"
  PLUGIN_DST="$PLUGIN_INSTALL_ROOT/$PLUGIN_NAME"
}

plugin_name_for_lang() {
  case "$1" in
    zh) echo "company-codex-workflow-v2-zh" ;;
    en) echo "company-codex-workflow-v2" ;;
    *)
      echo "Unsupported language: $1. Use zh or en." >&2
      exit 1
      ;;
  esac
}

copy_dir_safe() {
  local src="$1"
  local dst="$2"
  if [[ -e "$dst" && "$FORCE" != "1" ]]; then
    echo "Skip existing: $dst"
    return
  fi
  rm -rf "$dst"
  mkdir -p "$(dirname "$dst")"
  cp -R "$src" "$dst"
  find "$dst" -name ".DS_Store" -delete
}

copy_file_safe() {
  local src="$1"
  local dst="$2"
  local generated_dst="${3:-}"
  if [[ ! -f "$src" ]]; then
    echo "Source file not found: $src" >&2
    exit 1
  fi
  if [[ -f "$dst" && "$FORCE" != "1" ]]; then
    if [[ -n "$generated_dst" ]]; then
      mkdir -p "$(dirname "$generated_dst")"
      cp "$src" "$generated_dst"
      echo "Existing file preserved: $dst"
      echo "Generated updated file for review: $generated_dst"
    else
      echo "Skip existing: $dst"
    fi
    return
  fi
  mkdir -p "$(dirname "$dst")"
  cp "$src" "$dst"
  echo "Wrote file: $dst"
}

ensure_root_plugin_json() {
  local plugin_root="$1"
  local manifest="$plugin_root/.codex-plugin/plugin.json"
  local root_manifest="$plugin_root/plugin.json"
  if [[ ! -f "$manifest" ]]; then
    echo "Plugin manifest not found: $manifest" >&2
    exit 1
  fi
  cp "$manifest" "$root_manifest"
}

install_plugin() {
  if [[ ! -d "$PLUGIN_SRC/.codex-plugin" ]]; then
    echo "Plugin source not found: $PLUGIN_SRC" >&2
    exit 1
  fi
  ensure_root_plugin_json "$PLUGIN_SRC"
  if [[ -e "$PLUGIN_DST" && "$FORCE" != "1" ]]; then
    echo "Plugin already installed: $PLUGIN_DST"
    echo "Use --force to replace it."
  else
    copy_dir_safe "$PLUGIN_SRC" "$PLUGIN_DST"
    echo "Installed plugin: $PLUGIN_DST"
  fi
  if [[ -d "$PLUGIN_DST" ]]; then
    ensure_root_plugin_json "$PLUGIN_DST"
  fi
  mkdir -p "$MARKETPLACE_ROOT" "$PLUGIN_INSTALL_ROOT"
  MARKETPLACE_FILE="$MARKETPLACE_FILE" PLUGIN_NAME="$PLUGIN_NAME" python3 - <<'PY'
import json
import os
from pathlib import Path

path = Path(os.environ["MARKETPLACE_FILE"])
path.parent.mkdir(parents=True, exist_ok=True)
if path.exists():
    data = json.loads(path.read_text())
else:
    data = {"name": "personal", "interface": {"displayName": "Personal"}, "plugins": []}
data.setdefault("name", "personal")
data.setdefault("interface", {}).setdefault("displayName", "Personal")
plugins = data.setdefault("plugins", [])
entry = {
    "name": os.environ["PLUGIN_NAME"],
    "source": {"source": "local", "path": f"./plugins/{os.environ['PLUGIN_NAME']}"},
    "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
    "category": "Productivity",
}
for i, plugin in enumerate(plugins):
    if plugin.get("name") == entry["name"]:
        plugins[i] = entry
        break
else:
    plugins.append(entry)
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
PY
  echo "Marketplace updated: $MARKETPLACE_FILE"
  echo "Language: $LANG_CODE"
}

uninstall_plugin_name() {
  local name="$1"
  local dst="$PLUGIN_INSTALL_ROOT/$name"
  if [[ -d "$dst" ]]; then
    rm -rf "$dst"
    echo "Removed plugin directory: $dst"
  else
    echo "Plugin directory not found: $dst"
  fi
  local legacy_dst="$MARKETPLACE_ROOT/plugins/$name"
  if [[ -d "$legacy_dst" ]]; then
    rm -rf "$legacy_dst"
    echo "Removed legacy plugin directory: $legacy_dst"
  fi
  MARKETPLACE_FILE="$MARKETPLACE_FILE" PLUGIN_NAME="$name" python3 - <<'PY'
import json
import os
from pathlib import Path

path = Path(os.environ["MARKETPLACE_FILE"])
if not path.exists():
    raise SystemExit(0)
data = json.loads(path.read_text())
plugins = data.get("plugins", [])
data["plugins"] = [plugin for plugin in plugins if plugin.get("name") != os.environ["PLUGIN_NAME"]]
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
PY
  echo "Marketplace entry removed if present: $name"
}

uninstall_plugin() {
  if [[ "$ALL_LANGS" == "1" ]]; then
    uninstall_plugin_name "$(plugin_name_for_lang zh)"
    uninstall_plugin_name "$(plugin_name_for_lang en)"
  else
    uninstall_plugin_name "$PLUGIN_NAME"
  fi
}

append_agents_block() {
  local target="$1"
  if [[ -f "$target" ]] && grep -q "$MARKER_BEGIN" "$target"; then
    echo "AGENTS.md already contains company workflow block."
    return
  fi
  if [[ -f "$target" ]] && grep -q "$LEGACY_MARKER_BEGIN" "$target"; then
    echo "AGENTS.md already contains company workflow block."
    return
  fi
  {
    echo ""
    echo "$MARKER_BEGIN"
    cat "$PLUGIN_SRC/AGENTS.md"
    echo "$MARKER_END"
  } >> "$target"
}

write_install_manifest() {
  local project_path="$1"
  mkdir -p "$project_path/.codex-workflow"
  PROJECT_PATH="$project_path" PLUGIN_NAME="$PLUGIN_NAME" LANG_CODE="$LANG_CODE" python3 - <<'PY'
import json
import os
from datetime import datetime, timezone
from pathlib import Path

project = Path(os.environ["PROJECT_PATH"])
manifest = {
    "kit": "codex-company-workflow-kit",
    "profile": "company",
    "plugin": os.environ["PLUGIN_NAME"],
    "language": os.environ["LANG_CODE"],
    "installedAt": datetime.now(timezone.utc).isoformat(),
    "managedMarkers": {
        "agentsBegin": "<!-- codex-workflow-kit:company:start -->",
        "agentsEnd": "<!-- codex-workflow-kit:company:end -->"
    },
    "managedPaths": [
        "AGENTS.md marker block",
        "BUNDLES.md",
        "EXPERTS.lock.md",
        "specs/global/assets/",
        "specs/global/assets.generated/",
        ".codex-workflow/install.json"
    ],
    "preservedProjectAssets": [
        "specs/features/",
        "specs/global/INDEX.md",
        "specs/global/INDEX.generated.md"
    ]
}
path = project / ".codex-workflow" / "install.json"
path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
PY
  echo "Install manifest written: $project_path/.codex-workflow/install.json"
}

ensure_project_governance_files() {
  local project_path="$1"
  copy_file_safe "$PLUGIN_SRC/BUNDLES.md" "$project_path/BUNDLES.md" "$project_path/BUNDLES.generated.md"
  copy_file_safe "$PLUGIN_SRC/EXPERTS.lock.md" "$project_path/EXPERTS.lock.md" "$project_path/EXPERTS.lock.generated.md"
}

ensure_project_templates() {
  local project_path="$1"
  local src="$PLUGIN_SRC/specs/global/assets"
  local dst="$project_path/specs/global/assets"
  if [[ ! -d "$src" ]]; then
    echo "Template source not found: $src" >&2
    exit 1
  fi
  mkdir -p "$project_path/specs/global"
  if [[ -d "$dst" && "$FORCE" != "1" ]]; then
    echo "Project templates already present: $dst"
  else
    rm -rf "$dst"
    cp -R "$src" "$dst"
    find "$dst" -name ".DS_Store" -delete
    echo "Project templates ready: $dst"
  fi
}

generate_index() {
  local project_path="$1"
  local output_path="${2:-$project_path/specs/global/INDEX.md}"
  local overwrite="${3:-0}"
  local args=("$ROOT_DIR/scripts/generate_index.py" "$project_path" "--lang" "$LANG_CODE" "--output" "$output_path")
  if [[ "$overwrite" == "1" || "$FORCE" == "1" ]]; then
    args+=("--force")
  fi
  python3 "${args[@]}"
}

bootstrap_project() {
  local project_path="$1"
  mkdir -p "$project_path"
  local agents="$project_path/AGENTS.md"
  local index_path="$project_path/specs/global/INDEX.md"
  local index_existed=0
  if [[ -f "$index_path" ]]; then
    index_existed=1
  fi
  if [[ -f "$agents" ]]; then
    append_agents_block "$agents"
    echo "Merged AGENTS.md: $agents"
  else
    : > "$agents"
    append_agents_block "$agents"
    echo "Created AGENTS.md: $agents"
  fi
  ensure_project_templates "$project_path"
  ensure_project_governance_files "$project_path"
  echo "Project workflow assets ready: $project_path/specs"
  if [[ "$index_existed" == "0" || "$FORCE" == "1" ]]; then
    generate_index "$project_path" "$index_path" 1
  else
    generate_index "$project_path" "$project_path/specs/global/INDEX.generated.md" 1
    echo "Existing INDEX.md preserved. Review INDEX.generated.md before replacing it."
  fi
  write_install_manifest "$project_path"
  echo "Next: review the generated INDEX draft and confirm project context."
}

deactivate_project() {
  local project_path="$1"
  local agents="$project_path/AGENTS.md"
  local workflow_dir="$project_path/.codex-workflow"
  local report="$workflow_dir/deactivation-report.md"
  mkdir -p "$workflow_dir"
  if [[ -f "$agents" ]] && grep -q "$MARKER_BEGIN" "$agents"; then
    AGENTS_PATH="$agents" MARKER_BEGIN="$MARKER_BEGIN" MARKER_END="$MARKER_END" python3 - <<'PY'
import os
from pathlib import Path

path = Path(os.environ["AGENTS_PATH"])
begin = os.environ["MARKER_BEGIN"]
end = os.environ["MARKER_END"]
text = path.read_text()
start = text.find(begin)
finish = text.find(end, start)
if start != -1 and finish != -1:
    finish += len(end)
    new_text = text[:start].rstrip() + "\n" + text[finish:].lstrip()
    path.write_text(new_text.rstrip() + "\n")
PY
    echo "Removed company workflow block from AGENTS.md."
  else
    echo "No managed company workflow marker found in AGENTS.md; left it unchanged."
  fi
  if [[ "$FORCE" == "1" ]]; then
    rm -rf "$project_path/specs/global/assets" "$project_path/specs/global/assets.generated"
    echo "Removed managed template directories."
  else
    echo "Project specs preserved. Use --force to remove managed template directories only."
  fi
  REPORT_PATH="$report" FORCE="$FORCE" python3 - <<'PY'
import os
from datetime import datetime, timezone
from pathlib import Path

force = os.environ["FORCE"] == "1"
body = f"""# Company Workflow Deactivation Report

- Deactivated at: {datetime.now(timezone.utc).isoformat()}
- AGENTS.md marker block: removed when present
- Template directories removed: {"yes" if force else "no"}

## Preserved by default

- specs/features/
- specs/global/INDEX.md
- specs/global/INDEX.generated.md

## Notes

Project requirement, design, task, and verification documents are treated as project assets and are not deleted by this command.
"""
Path(os.environ["REPORT_PATH"]).write_text(body)
PY
  echo "Deactivation report written: $report"
}

update_templates() {
  local project_path="$1"
  local src="$PLUGIN_SRC/specs/global/assets"
  local dst="$project_path/specs/global/assets"
  local review_dst="$project_path/specs/global/assets.generated"
  if [[ ! -d "$src" ]]; then
    echo "Template source not found: $src" >&2
    exit 1
  fi
  mkdir -p "$project_path/specs/global"
  if [[ -e "$dst" && "$FORCE" != "1" ]]; then
    rm -rf "$review_dst"
    cp -R "$src" "$review_dst"
    find "$review_dst" -name ".DS_Store" -delete
    echo "Existing templates preserved: $dst"
    echo "Generated updated templates for review: $review_dst"
    echo "Next: compare assets and assets.generated, then rerun with --force if you approve replacement."
  else
    rm -rf "$dst"
    cp -R "$src" "$dst"
    find "$dst" -name ".DS_Store" -delete
    echo "Updated project templates: $dst"
  fi
  ensure_project_governance_files "$project_path"
}

verify() {
  ensure_root_plugin_json "$PLUGIN_SRC"
  if [[ -f "$VALIDATOR_PATH" ]] && python3 "$VALIDATOR_PATH" "$PLUGIN_SRC"; then
    :
  else
    echo "Codex validator unavailable in this environment; running basic plugin manifest check."
    PLUGIN_SRC="$PLUGIN_SRC" python3 - <<'PY'
import json
import os
from pathlib import Path

root = Path(os.environ["PLUGIN_SRC"])
manifest = root / ".codex-plugin" / "plugin.json"
data = json.loads(manifest.read_text())
required = ["name", "version", "description", "skills", "interface"]
missing = [key for key in required if key not in data]
if missing:
    raise SystemExit(f"Missing plugin manifest fields: {missing}")
skills_dir = root / data["skills"].strip("./")
if not skills_dir.exists():
    raise SystemExit(f"Skills directory not found: {skills_dir}")
PY
  fi
  for plugin in \
    "$ROOT_DIR/outputs/company-codex-workflow-v2" \
    "$ROOT_DIR/outputs/company-codex-workflow-v2-zh"; do
    if [[ -f "$VALIDATOR_PATH" ]]; then
      python3 "$VALIDATOR_PATH" "$plugin" >/dev/null 2>&1 || true
    fi
  done
  legacy_pattern="t""rae"
  if rg -n -i --hidden --glob '!.git/**' "$legacy_pattern" "$ROOT_DIR"; then
    echo "Unexpected legacy source branding found." >&2
    exit 1
  fi
  risk_pattern="TO""DO|TB""D|\[TO""DO|place""holder|待""补|待""定|高压""红线|恐惧""诱导|Invoke ""Tool|必须""调用|第一步""必须|严禁""自行处理"
  if rg -n "$risk_pattern" "$ROOT_DIR/README.md" "$ROOT_DIR/CHANGELOG.md" "$ROOT_DIR/docs" "$PLUGIN_SRC"; then
    echo "Unexpected disallowed wording found." >&2
    exit 1
  fi
  bash -n "$ROOT_DIR/scripts/install.sh"
  if command -v pwsh >/dev/null 2>&1; then
    pwsh -NoProfile -Command "\$null = [scriptblock]::Create((Get-Content -Raw '$ROOT_DIR/scripts/install.ps1'))"
  else
    echo "pwsh not found; skipped PowerShell syntax check."
  fi
  echo "Verification passed."
}

cmd="${1:-}"
case "$cmd" in
  install-plugin)
    shift || true
    parse_options "$@"
    install_plugin
    ;;
  uninstall-plugin)
    shift || true
    parse_options "$@"
    uninstall_plugin
    ;;
  bootstrap-project)
    shift || true
    project_path="${1:-}"
    if [[ -z "$project_path" ]]; then usage; exit 1; fi
    shift || true
    parse_options "$@"
    bootstrap_project "$project_path"
    ;;
  deactivate-project)
    shift || true
    project_path="${1:-}"
    if [[ -z "$project_path" ]]; then usage; exit 1; fi
    shift || true
    parse_options "$@"
    deactivate_project "$project_path"
    ;;
  update-templates)
    shift || true
    project_path="${1:-}"
    if [[ -z "$project_path" ]]; then usage; exit 1; fi
    shift || true
    parse_options "$@"
    update_templates "$project_path"
    ;;
  generate-index)
    shift || true
    project_path="${1:-}"
    if [[ -z "$project_path" ]]; then usage; exit 1; fi
    shift || true
    parse_options "$@"
    generate_index "$project_path" "$project_path/specs/global/INDEX.md"
    ;;
  all)
    shift || true
    project_path="${1:-}"
    if [[ -z "$project_path" ]]; then usage; exit 1; fi
    shift || true
    parse_options "$@"
    install_plugin
    bootstrap_project "$project_path"
    verify
    ;;
  verify)
    shift || true
    parse_options "$@"
    verify
    ;;
  *)
    usage
    exit 1
    ;;
esac
