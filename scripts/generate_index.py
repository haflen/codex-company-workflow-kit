#!/usr/bin/env python3
import argparse
import json
import re
from datetime import date
from pathlib import Path
from xml.etree import ElementTree


def read_text(path):
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(errors="ignore")
    except OSError:
        return ""


def first_existing(root, names):
    for name in names:
        path = root / name
        if path.exists():
            return path
    return None


def read_json(path):
    try:
        return json.loads(read_text(path))
    except Exception:
        return {}


def markdown_title(path):
    text = read_text(path)
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def detect_product(root):
    readme = first_existing(root, ["README.md", "readme.md", "README"])
    title = markdown_title(readme) if readme else ""
    return title or root.name


def detect_package_json(root):
    package = root / "package.json"
    if not package.exists():
        return {}, []
    data = read_json(package)
    scripts = data.get("scripts", {}) if isinstance(data.get("scripts"), dict) else {}
    return data, list(scripts.items())


def detect_pom(root):
    pom = root / "pom.xml"
    if not pom.exists():
        return ""
    try:
        tree = ElementTree.fromstring(read_text(pom))
    except Exception:
        return ""
    ns_match = re.match(r"\{.*\}", tree.tag)
    ns = ns_match.group(0) if ns_match else ""
    artifact = tree.findtext(f"{ns}artifactId") or ""
    version = tree.findtext(f"{ns}version") or ""
    return f"{artifact} {version}".strip()


def detect_stack(root, fallback):
    stack = []
    markers = [
        ("package.json", "Node.js / JavaScript / TypeScript"),
        ("tsconfig.json", "TypeScript"),
        ("next.config.js", "Next.js"),
        ("vite.config.ts", "Vite"),
        ("vite.config.js", "Vite"),
        ("pyproject.toml", "Python"),
        ("requirements.txt", "Python"),
        ("manage.py", "Django"),
        ("pom.xml", "Java / Maven"),
        ("build.gradle", "Java / Gradle"),
        ("build.gradle.kts", "Java / Gradle"),
        ("go.mod", "Go"),
        ("Cargo.toml", "Rust"),
        ("Dockerfile", "Docker"),
    ]
    for marker, label in markers:
        if (root / marker).exists() and label not in stack:
            stack.append(label)
    return stack or [fallback]


def detect_package_manager(root, fallback):
    if (root / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (root / "yarn.lock").exists():
        return "yarn"
    if (root / "package-lock.json").exists():
        return "npm"
    if (root / "poetry.lock").exists():
        return "poetry"
    if (root / "uv.lock").exists():
        return "uv"
    if (root / "pom.xml").exists():
        return "maven"
    if (root / "build.gradle").exists() or (root / "build.gradle.kts").exists():
        return "gradle"
    if (root / "go.mod").exists():
        return "go"
    if (root / "Cargo.toml").exists():
        return "cargo"
    if (root / "package.json").exists():
        return "npm"
    return fallback


def script_command(manager, name):
    if manager == "pnpm":
        return f"pnpm {name}"
    if manager == "yarn":
        return f"yarn {name}"
    return f"npm run {name}"


def detect_commands(root, manager, scripts, fallback):
    script_names = {name for name, _ in scripts}
    test = []
    build = []
    run = []
    for name in ["test", "test:unit", "test:e2e"]:
        if name in script_names:
            test.append(script_command(manager, name))
    for name in ["build", "typecheck", "lint"]:
        if name in script_names:
            build.append(script_command(manager, name))
    for name in ["dev", "start"]:
        if name in script_names:
            run.append(script_command(manager, name))
    if (root / "pom.xml").exists():
        test.append("mvn test")
        build.append("mvn package")
        run.append("mvn spring-boot:run")
    if (root / "pyproject.toml").exists() or (root / "requirements.txt").exists():
        if not test:
            test.append("pytest")
    return (
        ", ".join(test) or fallback,
        ", ".join(build) or fallback,
        ", ".join(run) or fallback,
    )


def detect_dirs(root, candidates):
    found = []
    for name in candidates:
        path = root / name
        if path.exists():
            found.append(name)
    return found


def detect_entrypoints(root):
    candidates = [
        "src/main.ts",
        "src/main.tsx",
        "src/index.ts",
        "src/index.tsx",
        "src/App.tsx",
        "app/page.tsx",
        "pages/index.tsx",
        "main.py",
        "app.py",
        "manage.py",
        "src/main/java",
        "cmd",
    ]
    return [name for name in candidates if (root / name).exists()]


def list_matching(root, patterns, limit=8):
    matches = []
    seen = set()
    for pattern in patterns:
        for path in root.glob(pattern):
            if ".git" in path.parts or "node_modules" in path.parts:
                continue
            if path.name == ".keep" or "specs/global/assets" in path.as_posix():
                continue
            if path.is_file() or path.is_dir():
                rel = path.relative_to(root).as_posix()
                if rel in seen:
                    continue
                seen.add(rel)
                matches.append(rel)
                if len(matches) >= limit:
                    return matches
    return matches


def format_list(values, fallback):
    return ", ".join(values) if values else fallback


def render_zh(root):
    pkg, scripts = detect_package_json(root)
    fallback = "待用户确认"
    manager = detect_package_manager(root, fallback)
    test_cmd, build_cmd, run_cmd = detect_commands(root, manager, scripts, fallback)
    progress = first_existing(root, ["说明文档.md", "CHANGELOG.md", "README.md"])
    version = pkg.get("version") or detect_pom(root) or "待用户确认"
    feature_specs = list_matching(root, ["specs/features/*", "docs/features/*"])
    version_dirs = list_matching(root, ["specs/versions/*", "docs/versions/*"])
    api_contracts = list_matching(root, ["**/*contract*.md", "**/*api*.md", "**/openapi*.yaml", "**/swagger*.json"])
    tests = detect_dirs(root, ["test", "tests", "__tests__", "e2e", "cypress", "playwright"])
    entries = detect_entrypoints(root)
    today = date.today().isoformat()
    return f"""# 项目上下文索引

每次使用公司工作流前先从这里开始。

> 自动生成草稿：{today}
> 确认状态：待用户确认。请检查下面的推断是否符合项目实际，再作为 Codex 工作入口使用。

## 项目快照

- 产品：{detect_product(root)}
- 当前版本：{version}
- 当前里程碑：待用户确认
- 主要技术栈：{format_list(detect_stack(root, fallback), fallback)}
- 包管理器：{manager}
- 测试命令：{test_cmd}
- 构建命令：{build_cmd}
- 本地启动命令：{run_cmd}
- 进度文档：{progress.name if progress else "待用户确认"}

## 路由

- 当前功能 specs：{format_list(feature_specs, fallback)}
- 当前版本目录：{format_list(version_dirs, fallback)}
- 当前里程碑目录：待用户确认
- API 契约：{format_list(api_contracts, fallback)}
- 测试位置：{format_list(tests, fallback)}
- 主要源码入口：{format_list(entries, fallback)}

## 文档职责地图

| 文档 | 职责 | 更新触发 | 编号命名空间 |
| --- | --- | --- | --- |
| `说明文档.md` 或等价入口页 | 项目入口、当前状态、最近重要事件、阅读路线 | 当前阶段、最近重要事件、阅读路线或关键状态变化 | 不使用 spike 任务号；使用日期型项目事件或最近变更 |
| `spike_*_工作日志.md` 或 spike 目录日志 | spike 现场流水、实验过程、临时结论 | spike 实验、观察、决策或临时任务变化 | `SPKxx-T001` 或 `Sxx-001` |
| `specs/versions/...` 或 `specs/features/...` | 正式需求、设计、任务计划、验收依据 | 需求、设计、任务、验收或正式变更被确认 | feature、版本或正式任务编号 |
| `docs/lifecycle/` | 生命周期阶段总结、里程碑回顾 | 版本阶段结束、里程碑变化或管理层摘要 | 日期或版本阶段编号 |
| `docs/public-doc-updates/` | 多分支并行时的公共文档影响补丁 | 分支影响入口页、当前状态、阅读路线、文档职责或编号规则，但尚未合并主线 | 分支名、feature ID 或 PR ID |

## 多分支公共文档协议

- 公共文档代表主线事实；feature、spike、hotfix 分支默认只读 `说明文档.md` 和本索引。
- 分支未合并前，不把分支局部进展写成项目“当前状态”。
- 分支需要改变公共入口或索引时，先写 `docs/public-doc-updates/<branch-or-feature>.md`。
- 集成阶段再统一把已合并事实写入 `说明文档.md` 和本索引。
- 如果多个分支影响同一公共段落，公共段落只在集成分支统一重写。

## 编号规则

- 不同层级文档不得共享裸 `任务 001` 这类编号。
- Spike 内部任务使用 spike 命名空间，例如 `SPK02-T183`。
- 正式任务使用 feature、版本或正式任务编号，例如 `FEAT-DT-T01`。
- 项目入口页记录“项目事件”或“最近变更”，不延续 spike 流水号。
- 发现编号冲突时，先修正文档职责地图，再继续写入。

## 工作流文档

| 需求 | 模板 |
| --- | --- |
| 功能需求 | `specs/global/assets/requirements-template.md` |
| 技术设计 | `specs/global/assets/design-template.md` |
| API 契约 | `specs/global/assets/api-contract-template.md` |
| 任务计划 | `specs/global/assets/tasks-template.md` |
| Spike 报告 | `specs/global/assets/spike-report-template.md` |
| Hotfix 报告 | `specs/global/assets/hotfix-report-template.md` |
| 变更请求 | `specs/global/assets/change-request-template.md` |
| 公共文档影响补丁 | `specs/global/assets/public-doc-update-template.md` |
| 技能升级报告 | `specs/global/assets/skill-upgrade-report-template.md` |

## 需要用户确认

- 产品名称和业务边界是否准确。
- 当前版本、里程碑、进度文档是否准确。
- 测试、构建、本地启动命令是否可以直接运行。
- 主要源码入口和测试位置是否完整。

## 当前风险

- 这是自动生成草稿，正式使用前需要项目负责人确认。
"""


def render_en(root):
    pkg, scripts = detect_package_json(root)
    fallback = "Needs user confirmation"
    manager = detect_package_manager(root, fallback)
    test_cmd, build_cmd, run_cmd = detect_commands(root, manager, scripts, fallback)
    progress = first_existing(root, ["CHANGELOG.md", "README.md", "说明文档.md"])
    version = pkg.get("version") or detect_pom(root) or "Needs user confirmation"
    feature_specs = list_matching(root, ["specs/features/*", "docs/features/*"])
    version_dirs = list_matching(root, ["specs/versions/*", "docs/versions/*"])
    api_contracts = list_matching(root, ["**/*contract*.md", "**/*api*.md", "**/openapi*.yaml", "**/swagger*.json"])
    tests = detect_dirs(root, ["test", "tests", "__tests__", "e2e", "cypress", "playwright"])
    entries = detect_entrypoints(root)
    today = date.today().isoformat()
    return f"""# Project Context Index

Start here before using any company workflow.

> Auto-generated draft: {today}
> Confirmation status: needs user confirmation. Check these inferences before using this as the Codex work entrypoint.

## Project Snapshot

- Product: {detect_product(root)}
- Current version: {version}
- Current milestone: Needs user confirmation
- Primary stack: {format_list(detect_stack(root, fallback), fallback)}
- Package manager: {manager}
- Test command: {test_cmd}
- Build command: {build_cmd}
- Local run command: {run_cmd}
- Progress document: {progress.name if progress else "Needs user confirmation"}

## Routing

- Current feature specs: {format_list(feature_specs, fallback)}
- Current version directory: {format_list(version_dirs, fallback)}
- Current milestone directory: Needs user confirmation
- API contracts: {format_list(api_contracts, fallback)}
- Test locations: {format_list(tests, fallback)}
- Main source entrypoints: {format_list(entries, fallback)}

## Document Ownership Map

| Document | Role | Update trigger | Numbering namespace |
| --- | --- | --- | --- |
| `说明文档.md` or equivalent entry page | Project entry, current state, recent important events, reading route | Current phase, recent important event, reading route, or key status change | Do not use spike task IDs; use date-based project events or recent changes |
| `spike_*_工作日志.md` or spike-local log | Spike field log, experiment flow, temporary conclusions | Spike experiment, observation, decision, or temporary task change | `SPKxx-T001` or `Sxx-001` |
| `specs/versions/...` or `specs/features/...` | Formal requirements, design, task plan, acceptance basis | Requirements, design, tasks, acceptance criteria, or approved changes are confirmed | Feature, version, or formal task IDs |
| `docs/lifecycle/` | Lifecycle phase summaries and milestone retrospectives | Version phase completion, milestone change, or management-summary need | Date or version-phase IDs |
| `docs/public-doc-updates/` | Public document impact patches for parallel branches | A branch affects the entry page, current state, reading route, document ownership, or numbering rules before mainline merge | Branch name, feature ID, or PR ID |

## Multi-Branch Public Document Protocol

- Public documents represent mainline facts; feature, spike, and hotfix branches read `说明文档.md` and this index by default.
- Before a branch is merged, do not write branch-local progress as the project "current state".
- When a branch needs to change public entry or index content, write `docs/public-doc-updates/<branch-or-feature>.md` first.
- During integration, promote only merged facts into `说明文档.md` and this index.
- If multiple branches affect the same public section, rewrite that section once on the integration branch.

## Numbering Rules

- Documents at different levels must not share bare IDs such as `Task 001`.
- Spike-internal tasks use a spike namespace, for example `SPK02-T183`.
- Formal tasks use feature, version, or formal task IDs, for example `FEAT-DT-T01`.
- Project entry pages record "project events" or "recent changes"; they do not continue spike work-log IDs.
- If numbering conflicts appear, fix the document ownership map before writing more content.

## Workflow Documents

| Need | Template |
| --- | --- |
| Feature requirements | `specs/global/assets/requirements-template.md` |
| Technical design | `specs/global/assets/design-template.md` |
| API contract | `specs/global/assets/api-contract-template.md` |
| Task plan | `specs/global/assets/tasks-template.md` |
| Spike report | `specs/global/assets/spike-report-template.md` |
| Hotfix report | `specs/global/assets/hotfix-report-template.md` |
| Change request | `specs/global/assets/change-request-template.md` |
| Public doc update patch | `specs/global/assets/public-doc-update-template.md` |
| Skill upgrade report | `specs/global/assets/skill-upgrade-report-template.md` |

## Needs User Confirmation

- Product name and business boundary.
- Current version, milestone, and progress document.
- Test, build, and local run commands.
- Source entrypoints and test locations.

## Active Risks

- This is an auto-generated draft and needs project-owner confirmation before formal use.
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project_path")
    parser.add_argument("--lang", choices=["zh", "en"], default="zh")
    parser.add_argument("--output", required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    root = Path(args.project_path).resolve()
    output = Path(args.output).resolve()
    if output.exists() and not args.force:
        raise SystemExit(f"Output exists, use --force to overwrite: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    content = render_zh(root) if args.lang == "zh" else render_en(root)
    output.write_text(content, encoding="utf-8")
    print(f"Generated index draft: {output}")


if __name__ == "__main__":
    main()
