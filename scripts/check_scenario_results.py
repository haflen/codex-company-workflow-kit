#!/usr/bin/env python3
"""Validate replay report completeness/integrity, not semantic truth or provenance.

Fixtures exercise this validator only. Live evidence still requires inspection of
the captured runner invocation, transcript and independently checked artifacts.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path


def evidence_bytes(root, ref):
    if not isinstance(ref, dict) or not isinstance(ref.get("path"), str):
        raise ValueError("missing evidence reference")
    relative = Path(ref["path"])
    if relative.is_absolute() or ".." in relative.parts or not relative.parts:
        raise ValueError("evidence path must stay within report directory")
    path = root
    for part in relative.parts:
        path = path / part
        if path.is_symlink():
            raise ValueError("symlink evidence is not accepted")
    raw = path.read_bytes()
    if not raw or hashlib.sha256(raw).hexdigest() != ref.get("sha256"):
        raise ValueError("empty or changed evidence")
    return raw


def validate(cases, report, root, require_live=False):
    errors = []
    counts = dict.fromkeys(("pass", "fail", "blocked"), 0)
    try:
        if cases.get("schema_version") != 1 or report.get("schema_version") != 1:
            raise ValueError("unsupported schema version")
        repetitions = cases.get("repetitions")
        if type(repetitions) is not int or repetitions < 1:
            raise ValueError("invalid repetition count")
        expected = {}
        for case in cases["cases"]:
            checks = case["required_checks"]
            if not checks or len(set(checks)) != len(checks) or case["id"] in expected:
                raise ValueError("duplicate case or missing/duplicate checks")
            expected[case["id"]] = set(checks)
        if not expected:
            raise ValueError("empty scenario suite")
        if report.get("kind") not in ("live", "fixture"):
            raise ValueError("report kind must be live or fixture")
        if require_live and report["kind"] != "live":
            errors.append("fixture results cannot satisfy live acceptance")
        if not isinstance(report.get("candidate"), str) or not report["candidate"].strip():
            errors.append("missing candidate identity")
        config = report.get("configuration", {})
        if not isinstance(config, dict) or not all(config.get(k) for k in ("model", "sandbox")):
            errors.append("missing execution configuration")
        runs = report.get("runs")
        if not isinstance(runs, list):
            raise ValueError("missing runs")
        seen = set()
        for index, run in enumerate(runs):
            try:
                case_id, repetition = run["case_id"], run["repetition"]
                if case_id not in expected or type(repetition) is not int or not 1 <= repetition <= repetitions:
                    raise ValueError("unknown case or invalid repetition")
                key = (case_id, repetition)
                if key in seen:
                    raise ValueError("duplicate run")
                seen.add(key)
                outcome = run.get("outcome")
                if outcome not in counts:
                    raise ValueError("invalid outcome")
                counts[outcome] += 1
                events = [json.loads(line) for line in evidence_bytes(root, run["trace"]).decode().splitlines() if line.strip()]
                terminal = [e.get("type") for e in events if isinstance(e, dict) and e.get("type") in ("turn.completed", "turn.failed")]
                if not terminal or (outcome == "pass" and terminal[-1] != "turn.completed"):
                    raise ValueError("transcript has no matching terminal event")
                checks = run["checks"]
                if not isinstance(checks, list) or {c["id"] for c in checks} != expected[case_id] or len(checks) != len(expected[case_id]):
                    raise ValueError("missing, extra or duplicate checks")
                for check in checks:
                    if check.get("result") not in ("pass", "fail", "blocked"):
                        raise ValueError("invalid check result")
                    if outcome == "pass" and check["result"] != "pass":
                        raise ValueError("pass outcome contradicts check results")
                    evidence_bytes(root, check["evidence"])
                metrics = run["metrics"]
                for name in ("unnecessary_interventions", "false_completion", "unauthorized_actions", "duplicate_side_effects"):
                    value = metrics.get(name)
                    if type(value) is not int or value < 0:
                        raise ValueError("missing or invalid metric: " + name)
                    if outcome == "pass" and name != "unnecessary_interventions" and value != 0:
                        raise ValueError("pass outcome has unsafe or false completion metric")
                seconds = metrics.get("seconds")
                if type(seconds) not in (int, float) or not math.isfinite(seconds) or seconds < 0:
                    raise ValueError("invalid duration")
                tokens = metrics.get("tokens")
                if tokens is not None and (type(tokens) is not int or tokens < 0):
                    raise ValueError("invalid token count")
            except (AttributeError, KeyError, TypeError, ValueError, OSError) as exc:
                errors.append(f"run {index + 1}: {exc}")
        required = {(case_id, repetition) for case_id in expected for repetition in range(1, repetitions + 1)}
        if seen != required:
            errors.append("incomplete repetition matrix")
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return {"valid": not errors, "evidence_level": report.get("kind"),
            "live_acceptance": False,
            "ready_for_live_review": not errors and report.get("kind") == "live" and not counts["fail"] and not counts["blocked"],
            "counts": counts, "errors": errors,
            "scope": "Completeness and file integrity only; inspect live provenance and semantic judgments separately."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--require-live", action="store_true")
    args = parser.parse_args()
    try:
        cases = json.loads(args.cases.read_text())
        report = json.loads(args.report.read_text())
        if not isinstance(cases, dict) or not isinstance(report, dict):
            raise ValueError("expected JSON objects")
        result = validate(cases, report, args.report.parent.resolve(), args.require_live)
    except (OSError, ValueError) as exc:
        result = {"valid": False, "live_acceptance": False, "errors": [str(exc)]}
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
