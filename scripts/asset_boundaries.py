#!/usr/bin/env python3
"""Generate and enforce lightweight project asset-placement boundaries."""

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath


CONFIG_RELATIVE = Path(".codex-workflow/asset-boundaries.json")
GENERATED_RELATIVE = Path(".codex-workflow/asset-boundaries.generated.json")
BACKUP_RELATIVE = Path(".codex-workflow/asset-boundaries.backup.json")
SKIP_DIRS = {
    ".git",
    ".idea",
    ".vscode",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "target",
    "venv",
}
MANIFEST_NAMES = {
    "Cargo.toml",
    "Gemfile",
    "Package.swift",
    "build.gradle",
    "build.gradle.kts",
    "composer.json",
    "go.mod",
    "mix.exs",
    "package.json",
    "pom.xml",
    "pubspec.yaml",
    "pyproject.toml",
    "requirements.txt",
    "setup.py",
    "settings.gradle",
    "settings.gradle.kts",
}
MANIFEST_SUFFIXES = {".csproj", ".fsproj", ".sln", ".vbproj"}
BUILD_ASSET_NAMES = MANIFEST_NAMES | {
    "Cargo.lock",
    "composer.json",
    "composer.lock",
    "gradle.properties",
    "package-lock.json",
    "pnpm-lock.yaml",
    "poetry.lock",
    "requirements.txt",
    "yarn.lock",
}
DEPENDENCY_DIRS = {"node_modules", ".venv", "venv", "vendor"}
GENERATED_OUTPUT_DIRS = {"build", "dist", "target"}
EXECUTABLE_SUFFIXES = {
    ".bat",
    ".cjs",
    ".go",
    ".java",
    ".js",
    ".jsx",
    ".kt",
    ".kts",
    ".mjs",
    ".php",
    ".ps1",
    ".py",
    ".rb",
    ".rs",
    ".sh",
    ".sql",
    ".ts",
    ".tsx",
    ".vue",
}
MACHINE_CONTRACT_DIRS = {"assertions", "contracts", "fixtures"}
MACHINE_CONTRACT_SUFFIXES = {".json", ".yaml", ".yml"}
MACHINE_CONTRACT_PREFIXES = ("asyncapi", "openapi", "swagger")


TEXT = {
    "zh": {
        "generated": "已生成资产边界草案：{path}",
        "candidate": "已保留现有配置，并生成待审候选：{path}",
        "confirmed": "资产边界已由用户确认：{path}",
        "accepted": "已采纳并确认资产边界候选；旧配置备份至：{path}",
        "clean": "资产落点检查通过：检查 {count} 个路径。",
        "draft": "提示：资产边界仍为自动生成草案；明显违规会阻断，工程根目录归属异常暂作警告。",
        "violations": "资产落点检查失败：发现 {count} 个阻断项。",
        "warnings": "资产落点检查发现 {count} 个警告。",
        "not_git": "项目尚未初始化 Git，无法执行 changed-only 检查。请先运行 git init，或改用 audit-assets/显式 --path 检查。",
    },
    "en": {
        "generated": "Generated asset-boundary draft: {path}",
        "candidate": "Preserved the existing config and generated a review candidate: {path}",
        "confirmed": "Asset boundaries confirmed by the user: {path}",
        "accepted": "Accepted and confirmed the generated asset boundaries; previous config backed up to: {path}",
        "clean": "Asset placement check passed: {count} path(s) checked.",
        "draft": "Note: asset boundaries are still an auto-generated draft; obvious violations block, while engineering-root ownership mismatches remain warnings.",
        "violations": "Asset placement check failed: {count} blocking issue(s).",
        "warnings": "Asset placement check found {count} warning(s).",
        "not_git": "The project is not a Git worktree, so changed-only checks are unavailable. Run git init, or use audit-assets/an explicit --path check.",
    },
}


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def normalize_relative(project, raw_path):
    path = Path(raw_path)
    if path.is_absolute():
        try:
            path = path.resolve().relative_to(project.resolve())
        except ValueError as exc:
            raise ValueError("path is outside project root: {}".format(raw_path)) from exc
    normalized = PurePosixPath(path.as_posix())
    if ".." in normalized.parts:
        raise ValueError("path escapes project root: {}".format(raw_path))
    value = normalized.as_posix()
    while value.startswith("./"):
        value = value[2:]
    return value or "."


def is_under(path, root):
    if root == ".":
        return True
    return path == root or path.startswith(root.rstrip("/") + "/")


def iter_project_files(project):
    for current, dirs, files in os.walk(str(project)):
        current_path = Path(current)
        relative = current_path.relative_to(project)
        dirs[:] = [
            name
            for name in dirs
            if name not in SKIP_DIRS
            and not (relative == Path(".codex-workflow") and name == "cache")
        ]
        for name in files:
            yield (relative / name).as_posix()


def iter_audit_paths(project, documentation_roots):
    docs = [entry["path"] for entry in documentation_roots]
    for current, dirs, files in os.walk(str(project)):
        current_path = Path(current)
        relative = current_path.relative_to(project)
        retained = []
        for name in dirs:
            child = (relative / name).as_posix()
            if name in DEPENDENCY_DIRS:
                if any(is_under(child, root) for root in docs):
                    yield child
                continue
            if name in GENERATED_OUTPUT_DIRS:
                if any(is_under(child, root) for root in docs):
                    yield child
                continue
            if name in SKIP_DIRS:
                continue
            if relative == Path(".codex-workflow") and name == "cache":
                continue
            retained.append(name)
        dirs[:] = retained
        for name in files:
            yield (relative / name).as_posix()


def discover_engineering_roots(project, documentation_roots):
    roots = {}
    docs = [entry["path"] for entry in documentation_roots]
    for relative in iter_project_files(project):
        if any(is_under(relative, root) for root in docs):
            continue
        path = PurePosixPath(relative)
        if path.name not in MANIFEST_NAMES and path.suffix.lower() not in MANIFEST_SUFFIXES:
            continue
        parent = path.parent.as_posix()
        if parent == ".":
            parent = "."
        roots.setdefault(parent, []).append(relative)
    return [
        {
            "name": "project-root" if path == "." else path.replace("/", "-"),
            "path": path,
            "evidence": sorted(evidence),
        }
        for path, evidence in sorted(roots.items())
    ]


def build_config(project):
    documentation_roots = []
    root_policies = (
        ("specs", "docs-only"),
        ("docs", "docs-only"),
        ("product-docs", "reference-assets"),
    )
    for path, policy in root_policies:
        if (project / path).exists() or path in {"specs", "docs"}:
            documentation_roots.append({"path": path, "policy": policy})

    tooling_roots = [
        path
        for path in ("scripts", "tools", "bin", ".codex-workflow/bin")
        if (project / path).exists() or path == ".codex-workflow/bin"
    ]
    return {
        "schemaVersion": 1,
        "status": "generated-review-required",
        "generatedAt": now_iso(),
        "documentationRoots": documentation_roots,
        "engineeringRoots": discover_engineering_roots(project, documentation_roots),
        "toolingRoots": tooling_roots,
        "prototypeRoots": [".codex-workflow/prototypes"],
        "exceptions": [],
        "enforcement": {
            "workflow": "blocking",
            "changedFiles": "blocking",
            "preCommit": "deferred",
            "ci": "deferred",
        },
    }


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def merge_by_path(generated, existing):
    merged = {str(entry.get("path")): entry for entry in generated if entry.get("path")}
    for entry in existing:
        if isinstance(entry, dict) and entry.get("path"):
            merged.setdefault(str(entry["path"]), entry)
    return [merged[path] for path in sorted(merged)]


def merge_existing_config(config, existing):
    if not isinstance(existing, dict):
        return config
    config["documentationRoots"] = merge_by_path(
        config["documentationRoots"], existing.get("documentationRoots", [])
    )
    config["engineeringRoots"] = merge_by_path(
        config["engineeringRoots"], existing.get("engineeringRoots", [])
    )
    for key in ("toolingRoots", "prototypeRoots"):
        config[key] = sorted(set(config[key]) | set(existing.get(key, [])))
    config["exceptions"] = existing.get("exceptions", [])
    if isinstance(existing.get("enforcement"), dict):
        config["enforcement"].update(existing["enforcement"])
    return config


def validate_config(config):
    if not isinstance(config, dict):
        raise ValueError("asset boundary config must be an object")
    required = {"schemaVersion", "status", "documentationRoots", "engineeringRoots", "exceptions"}
    missing = sorted(required.difference(config))
    if missing:
        raise ValueError("asset boundary config is incomplete: {}".format(", ".join(missing)))
    if config["schemaVersion"] != 1:
        raise ValueError("schemaVersion must be 1")
    if config["status"] not in {"generated-review-required", "confirmed"}:
        raise ValueError("status must be generated-review-required or confirmed")

    for field in ("documentationRoots", "engineeringRoots"):
        entries = config[field]
        if not isinstance(entries, list):
            raise ValueError("{} must be a list".format(field))
        for index, entry in enumerate(entries):
            if not isinstance(entry, dict):
                raise ValueError("{}[{}] must be an object".format(field, index))
            path = entry.get("path")
            if not isinstance(path, str) or not path:
                raise ValueError("{}[{}].path must be a non-empty string".format(field, index))
            pure = PurePosixPath(path)
            if pure.is_absolute() or ".." in pure.parts:
                raise ValueError("{}[{}].path must stay inside the project".format(field, index))
            if field == "documentationRoots" and entry.get("policy") not in {
                "docs-only",
                "reference-assets",
            }:
                raise ValueError(
                    "documentationRoots[{}].policy must be docs-only or reference-assets".format(index)
                )
            if field == "engineeringRoots" and "evidence" in entry and not (
                isinstance(entry["evidence"], list)
                and all(isinstance(value, str) for value in entry["evidence"])
            ):
                raise ValueError("engineeringRoots[{}].evidence must be a string list".format(index))

    for field in ("toolingRoots", "prototypeRoots"):
        values = config.get(field, [])
        if not isinstance(values, list) or not all(isinstance(value, str) for value in values):
            raise ValueError("{} must be a string list".format(field))
    if not isinstance(config["exceptions"], list):
        raise ValueError("exceptions must be a list")
    if "enforcement" in config and not isinstance(config["enforcement"], dict):
        raise ValueError("enforcement must be an object")

    for exception in config["exceptions"]:
        if not isinstance(exception, dict):
            raise ValueError("asset boundary exception must be an object")
        required_exception = {"path", "type", "reason", "owner", "validation"}
        missing_exception = sorted(required_exception.difference(exception))
        if missing_exception:
            raise ValueError(
                "asset boundary exception is incomplete: {}".format(", ".join(missing_exception))
            )
        if exception.get("type") != "machine-contract":
            raise ValueError("unsupported asset boundary exception type: {}".format(exception.get("type")))


def generate(project, lang, force=False, output=None):
    target = Path(output) if output else project / CONFIG_RELATIVE
    if not target.is_absolute():
        target = project / target
    config = build_config(project)
    if target.exists():
        config = merge_existing_config(config, json.loads(target.read_text()))
    if target.exists() and not force:
        candidate = project / GENERATED_RELATIVE
        write_json(candidate, config)
        print(TEXT[lang]["candidate"].format(path=candidate))
        return candidate
    write_json(target, config)
    print(TEXT[lang]["generated"].format(path=target))
    return target


def load_config(project, config_path=None):
    path = Path(config_path) if config_path else project / CONFIG_RELATIVE
    if not path.is_absolute():
        path = project / path
    if not path.exists():
        raise FileNotFoundError("asset boundary config not found: {}".format(path))
    return path, json.loads(path.read_text())


def confirm(project, lang, config_path=None):
    path, config = load_config(project, config_path)
    validate_config(config)
    config["status"] = "confirmed"
    config["confirmedAt"] = now_iso()
    write_json(path, config)
    print(TEXT[lang]["confirmed"].format(path=path))


def accept_generated(project, lang):
    target = project / CONFIG_RELATIVE
    candidate = project / GENERATED_RELATIVE
    backup = project / BACKUP_RELATIVE
    if not candidate.exists():
        raise FileNotFoundError("generated asset boundary candidate not found: {}".format(candidate))
    config = json.loads(candidate.read_text())
    validate_config(config)
    config["status"] = "confirmed"
    config["confirmedAt"] = now_iso()
    config["acceptedFrom"] = GENERATED_RELATIVE.as_posix()
    if target.exists():
        shutil.copy2(str(target), str(backup))
    temporary = target.with_name(target.name + ".tmp")
    write_json(temporary, config)
    os.replace(str(temporary), str(target))
    candidate.unlink()
    print(TEXT[lang]["accepted"].format(path=backup))


def git_paths(project, lang):
    probe = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        cwd=str(project),
        text=True,
        capture_output=True,
    )
    if probe.returncode != 0 or probe.stdout.strip() != "true":
        raise RuntimeError(TEXT[lang]["not_git"])
    commands = [
        ["git", "diff", "--name-only", "--diff-filter=ACMR"],
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    ]
    paths = set()
    for command in commands:
        result = subprocess.run(command, cwd=str(project), text=True, capture_output=True)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "git path discovery failed")
        paths.update(line.strip() for line in result.stdout.splitlines() if line.strip())
    return sorted(paths)


def is_exception(path, config, issue_code):
    if issue_code != "AB004":
        return False
    for exception in config.get("exceptions", []):
        configured = str(exception.get("path", "")).rstrip("/")
        if (
            exception.get("type") == "machine-contract"
            and configured
            and is_under(path, configured)
        ):
            return True
    return False


def documentation_policy(path, config):
    matches = [
        entry
        for entry in config.get("documentationRoots", [])
        if is_under(path, str(entry.get("path", "")))
    ]
    if not matches:
        return None
    return max(matches, key=lambda entry: len(str(entry.get("path", ""))))


def engineering_allowed(path, config):
    roots = [entry.get("path", "") for entry in config.get("engineeringRoots", [])]
    roots += config.get("toolingRoots", [])
    roots += config.get("prototypeRoots", [])
    return any(root and is_under(path, root) for root in roots)


def looks_engineering(path):
    pure = PurePosixPath(path)
    name = pure.name.lower()
    return (
        pure.suffix.lower() in EXECUTABLE_SUFFIXES
        or is_build_asset(pure)
        or ".test." in name
        or ".spec." in name
        or name.endswith(".schema.json")
    )


def is_build_asset(pure):
    return pure.name in BUILD_ASSET_NAMES or pure.suffix.lower() in MANIFEST_SUFFIXES


def looks_machine_contract(path):
    pure = PurePosixPath(path)
    name = pure.name.lower()
    contract_name = any(
        name == prefix + suffix
        or name.startswith(prefix + ".")
        or name.startswith(prefix + "-")
        or name.startswith(prefix + "_")
        for prefix in MACHINE_CONTRACT_PREFIXES
        for suffix in MACHINE_CONTRACT_SUFFIXES
    )
    return (
        pure.suffix.lower() in MACHINE_CONTRACT_SUFFIXES
        and (
            bool(set(pure.parts).intersection(MACHINE_CONTRACT_DIRS))
            or name.endswith(".schema.json")
            or contract_name
        )
    )


def inspect_path(path, config):
    policy_entry = documentation_policy(path, config)
    pure = PurePosixPath(path)
    parts = set(pure.parts)
    issues = []
    if policy_entry:
        policy = policy_entry.get("policy", "docs-only")
        if is_build_asset(pure):
            issues.append(("error", "AB001", path, "build/package asset is under a documentation root"))
        elif parts.intersection(DEPENDENCY_DIRS):
            issues.append(("error", "AB002", path, "dependency tree is under a documentation root"))
        elif parts.intersection(GENERATED_OUTPUT_DIRS):
            issues.append(("error", "AB006", path, "generated build output is under a documentation root"))
        elif policy == "docs-only" and (
            pure.suffix.lower() in EXECUTABLE_SUFFIXES
            or ".test." in pure.name.lower()
            or ".spec." in pure.name.lower()
        ):
            issues.append(("error", "AB003", path, "executable or test asset is under a docs-only root"))
        elif policy == "docs-only" and looks_machine_contract(path) and not is_exception(path, config, "AB004"):
            issues.append(("error", "AB004", path, "machine contract or fixture is under a docs-only root"))
        return issues

    if looks_engineering(path) and not engineering_allowed(path, config):
        level = "error" if config.get("status") == "confirmed" else "warning"
        issues.append((level, "AB005", path, "engineering asset is outside confirmed engineering/tooling roots"))
    return issues


def check(project, lang, raw_paths, changed=False, audit_all=False, config_path=None):
    _, config = load_config(project, config_path)
    validate_config(config)
    paths = []
    paths.extend(raw_paths or [])
    if changed:
        paths.extend(git_paths(project, lang))
    if audit_all:
        paths.extend(iter_audit_paths(project, config.get("documentationRoots", [])))
    normalized = sorted({normalize_relative(project, path) for path in paths})
    issues = []
    for path in normalized:
        issues.extend(inspect_path(path, config))

    errors = [issue for issue in issues if issue[0] == "error"]
    warnings = [issue for issue in issues if issue[0] == "warning"]
    if config.get("status") != "confirmed":
        print(TEXT[lang]["draft"])
    for level, code, path, message in issues:
        print("{} {} {}: {}".format(level.upper(), code, path, message))
    if warnings:
        print(TEXT[lang]["warnings"].format(count=len(warnings)))
    if errors:
        print(TEXT[lang]["violations"].format(count=len(errors)))
        return 2
    print(TEXT[lang]["clean"].format(count=len(normalized)))
    return 0


def parser():
    root = argparse.ArgumentParser(description=__doc__)
    subparsers = root.add_subparsers(dest="command", required=True)
    for name in ("generate", "confirm", "accept-generated", "check"):
        command = subparsers.add_parser(name)
        command.add_argument("project")
        command.add_argument("--lang", choices=("zh", "en"), default="zh")
        command.add_argument("--config")
        if name == "generate":
            command.add_argument("--force", action="store_true")
            command.add_argument("--output")
        if name == "check":
            command.add_argument("--path", action="append", default=[])
            command.add_argument("--changed", action="store_true")
            command.add_argument("--all", action="store_true", dest="audit_all")
    return root


def main(argv=None):
    args = parser().parse_args(argv)
    project = Path(args.project).resolve()
    if not project.is_dir():
        print("project directory not found: {}".format(project), file=sys.stderr)
        return 1
    try:
        if args.command == "generate":
            generate(project, args.lang, args.force, args.output)
            return 0
        if args.command == "confirm":
            confirm(project, args.lang, args.config)
            return 0
        if args.command == "accept-generated":
            accept_generated(project, args.lang)
            return 0
        return check(
            project,
            args.lang,
            args.path,
            changed=args.changed,
            audit_all=args.audit_all,
            config_path=args.config,
        )
    except (FileNotFoundError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
