#!/usr/bin/env python3
"""Manage bundled company expert skill readiness.

The company workflow treats selected third-party expert skills as required
runtime dependencies. They are vendored inside the company plugin so users do
not have to install them one by one. This script verifies presence, runs a
static safety review, and writes readiness reports for plugin and project
installs.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


EXPERTS = [
    ("product-manager", "skills/product-manager", "business", "company-core-delivery"),
    ("business-analyst", "skills/business-analyst", "business", "company-core-delivery"),
    ("ai-product", "skills/ai-product", "ai-ml", "company-ai-feature"),
    ("java-pro", "skills/java-pro", "code", "company-backend-java"),
    ("python-pro", "skills/python-pro", "code", "company-python-service"),
    ("python-patterns", "skills/python-patterns", "development", "company-python-service"),
    ("django-pro", "skills/django-pro", "framework", "company-django-service"),
    ("frontend-developer", "skills/frontend-developer", "front-end", "company-frontend-delivery"),
    ("typescript-expert", "skills/typescript-expert", "framework", "company-frontend-delivery"),
    ("frontend-design", "skills/frontend-design", "front-end", "company-frontend-delivery"),
    ("testing-qa", "skills/testing-qa", "workflow-bundle", "all delivery bundles"),
    ("webapp-testing", "skills/webapp-testing", "test-automation", "company-frontend-delivery"),
    ("e2e-testing-patterns", "skills/e2e-testing-patterns", "test-automation", "company-frontend-delivery"),
]

SOURCE = {
    "repository": "sickn33/antigravity-awesome-skills",
    "url": "https://github.com/sickn33/antigravity-awesome-skills",
    "observed_version": "V13.4.0",
    "observed_size": "1,693+ skills",
    "vendored_pin": "e0ef87efd0ad5a18a23e21bb08406b3eaf563b35",
    "review_date": "2026-06-29",
    "license": "MIT for code; CC BY 4.0 for original non-code content unless upstream states otherwise",
}

RISK_PATTERNS = {
    "secret_or_credential": re.compile(r"\b(secret|api[_-]?key|token|cookie|ssh[_-]?key|password|credential)\b", re.I),
    "network_or_install": re.compile(r"\b(curl|wget|npm install|pip install|npx|fetch\(|requests\.|http://|https://)\b", re.I),
    "shell_or_process": re.compile(r"\b(subprocess|os\.system|child_process|exec\(|spawn\(|shell)\b", re.I),
    "destructive_file_op": re.compile(r"\b(rm -rf|Remove-Item\s+-Recurse|delete all|format disk)\b", re.I),
    "browser_automation": re.compile(r"\b(playwright|browser automation|selenium|puppeteer)\b", re.I),
}


@dataclass
class ExpertReview:
    name: str
    path: str
    category: str
    bundle: str
    installed: bool
    status: str
    risk: str
    findings: list[str]
    file_count: int


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def review_expert(plugin_root: Path, item: tuple[str, str, str, str]) -> ExpertReview:
    name, upstream_path, category, bundle = item
    skill_dir = plugin_root / "skills" / name
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return ExpertReview(
            name=name,
            path=upstream_path,
            category=category,
            bundle=bundle,
            installed=False,
            status="missing",
            risk="blocking",
            findings=["Required bundled expert skill is missing from the company plugin."],
            file_count=0,
        )

    files = [p for p in skill_dir.rglob("*") if p.is_file()]
    text = "\n".join(read_text(p) for p in files if p.suffix.lower() in {".md", ".txt", ".py", ".js", ".ts", ".json"})
    findings = [label for label, pattern in RISK_PATTERNS.items() if pattern.search(text)]
    has_scripts = any(part in {"scripts", "tools"} for p in files for part in p.parts)
    if has_scripts and "bundled_helper_script" not in findings:
        findings.append("bundled_helper_script")

    if "destructive_file_op" in findings or "secret_or_credential" in findings:
        risk = "high"
    elif findings:
        risk = "medium"
    else:
        risk = "low"
    status = "installed-auto-reviewed-approved"

    return ExpertReview(
        name=name,
        path=upstream_path,
        category=category,
        bundle=bundle,
        installed=True,
        status=status,
        risk=risk,
        findings=findings or ["no static risk signals found"],
        file_count=len(files),
    )


def collect_reviews(plugin_root: Path) -> list[ExpertReview]:
    return [review_expert(plugin_root, item) for item in EXPERTS]


def fail_if_missing_or_blocking(reviews: list[ExpertReview]) -> None:
    blocking = [r for r in reviews if not r.installed or r.status == "missing"]
    if blocking:
        names = ", ".join(r.name for r in blocking)
        raise SystemExit(f"Missing required bundled expert skills: {names}")


def render_markdown(reviews: list[ExpertReview], lang: str, project_path: Path | None = None) -> str:
    now = datetime.now(timezone.utc).isoformat()
    missing = [r for r in reviews if not r.installed]
    approved = [r for r in reviews if r.installed and "approved" in r.status]
    high_risk = [r for r in reviews if r.installed and r.risk == "high"]

    if lang == "en":
        title = "Company Expert Readiness Report"
        project = f"\n- Project: `{project_path}`" if project_path else ""
        intro = (
            "All required external expert skills are bundled with the company plugin. "
            "Users do not need to install them one by one."
        )
        summary = [
            f"- Generated at: `{now}`",
            f"- Source: `{SOURCE['repository']}`",
            f"- Observed upstream version: `{SOURCE['observed_version']}`",
            f"- Observed catalog size: `{SOURCE['observed_size']}`",
            f"- Vendored pin: `{SOURCE['vendored_pin']}`",
            f"- Installed experts: `{len(approved)}/{len(reviews)}`",
            f"- Auto-reviewed and approved for bundled use: `{len(approved)}`",
            f"- High-risk findings requiring runtime guardrails: `{len(high_risk)}`",
            f"- Missing: `{len(missing)}`",
        ]
        headers = "| Expert | Bundle | Risk | Status | Findings |\n| --- | --- | --- | --- | --- |"
        notes = [
            "## Runtime Policy",
            "",
            "- Bundled expert skills may be invoked directly when Codex exposes them in the current session.",
            "- High-risk findings do not block use; they require normal Codex sandbox, approval, and verification guardrails.",
            "- If a current session was opened before installation, start a new Codex thread so the skill list refreshes.",
            "- Updates still go through company skill maintenance and security review; external hub updates are not auto-merged silently.",
        ]
    else:
        title = "公司专家依赖就绪报告"
        project = f"\n- 项目：`{project_path}`" if project_path else ""
        intro = "所有强依赖外部专家 skill 已随公司插件内置安装，用户不需要逐个对话安装。"
        summary = [
            f"- 生成时间：`{now}`",
            f"- 来源：`{SOURCE['repository']}`",
            f"- 观察上游版本：`{SOURCE['observed_version']}`",
            f"- 观察目录规模：`{SOURCE['observed_size']}`",
            f"- Vendored pin：`{SOURCE['vendored_pin']}`",
            f"- 已安装专家：`{len(approved)}/{len(reviews)}`",
            f"- 自动审查并批准随包使用：`{len(approved)}`",
            f"- 高风险发现，需运行时护栏：`{len(high_risk)}`",
            f"- 缺失：`{len(missing)}`",
        ]
        headers = "| Expert | Bundle | 风险 | 状态 | 发现 |\n| --- | --- | --- | --- | --- |"
        notes = [
            "## 运行策略",
            "",
            "- 内置专家 skill 在 Codex 当前会话暴露后可直接调用。",
            "- 高风险发现不阻止调用；执行时仍遵守 Codex sandbox、审批和验证护栏。",
            "- 如果当前会话早于安装动作创建，请新开 Codex 线程刷新 skill 列表。",
            "- 后续更新仍走公司技能维护和安全审查；不会静默合并外部 hub 更新。",
        ]

    rows = []
    for review in reviews:
        findings = ", ".join(review.findings)
        rows.append(f"| `{review.name}` | `{review.bundle}` | `{review.risk}` | `{review.status}` | {findings} |")

    body = [
        f"# {title}",
        "",
        intro,
        project,
        "",
        "## Summary" if lang == "en" else "## 摘要",
        "",
        *summary,
        "",
        "## Expert Table" if lang == "en" else "## 专家清单",
        "",
        headers,
        *rows,
        "",
        "## Source and License" if lang == "en" else "## 来源和许可",
        "",
        f"- URL: {SOURCE['url']}",
        f"- License: {SOURCE['license']}",
        "",
        *notes,
        "",
    ]
    return "\n".join(line for line in body if line is not None)


def write_json(reviews: list[ExpertReview], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "source": SOURCE,
        "experts": [review.__dict__ for review in reviews],
    }
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify bundled company expert dependencies.")
    parser.add_argument("command", choices=["review", "project-report"])
    parser.add_argument("--plugin-root", required=True)
    parser.add_argument("--project-path")
    parser.add_argument("--output")
    parser.add_argument("--json-output")
    parser.add_argument("--lang", choices=["zh", "en"], default="zh")
    args = parser.parse_args()

    plugin_root = Path(args.plugin_root).expanduser().resolve()
    reviews = collect_reviews(plugin_root)
    fail_if_missing_or_blocking(reviews)

    if args.command == "review":
        output = Path(args.output) if args.output else plugin_root / "EXPERT-READINESS.md"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(render_markdown(reviews, args.lang), encoding="utf-8")
        if args.json_output:
            write_json(reviews, Path(args.json_output))
        print(f"Expert dependency review passed: {len(reviews)}/{len(EXPERTS)} installed")
        print(f"Report: {output}")
        return

    project_path = Path(args.project_path or ".").expanduser().resolve()
    output = Path(args.output) if args.output else project_path / ".codex-workflow" / "EXPERT-READINESS.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_markdown(reviews, args.lang, project_path), encoding="utf-8")
    if args.json_output:
        write_json(reviews, Path(args.json_output))
    print(f"Expert readiness report written: {output}")


if __name__ == "__main__":
    main()
