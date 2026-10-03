from __future__ import annotations

import argparse
import json
import sys
import time
import uuid
from collections import Counter, defaultdict
from dataclasses import asdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

if __package__:
    from .case import KNOWN_XFAILS, Case, Verdict, dotted_get
    from .error_gen import generate_error_cases
    from .fuzzer import generate_fuzz_cases
    from .valid_gen import generate_valid_cases
else:
    from case import KNOWN_XFAILS, Case, Verdict, dotted_get
    from error_gen import generate_error_cases
    from fuzzer import generate_fuzz_cases
    from valid_gen import generate_valid_cases

from config import Config
from normalizer.normalizer import normalize
from parser import UnknownFormatError, dispatch
from schema.universal_event import UniversalEvent


def _normalize(fmt: str, parsed: dict[str, Any]) -> dict[str, Any]:
    return normalize(
        fmt,
        parsed,
        str(uuid.uuid4()),
        str(uuid.uuid4()),
        Config.LOG_TIMEZONE,
    )


def _actual_verdict(case: Case) -> tuple[Verdict, str, str | None]:
    try:
        fmt, parsed = dispatch(case.line)
    except UnknownFormatError as exc:
        verdict = Verdict.PASS_NO if case.expect in ("reject", "fuzz") else Verdict.FAIL
        return verdict, str(exc), None

    if case.expect == "reject":
        if "error_message" in parsed:
            return Verdict.PASS_NO, str(parsed["error_message"]), fmt
        try:
            event = _normalize(fmt, parsed)
            UniversalEvent.model_validate(event)
        except Exception as exc:
            return Verdict.PASS_NO, f"Strict event validation rejected input: {exc}", fmt
        return Verdict.FAIL, "Input was parsed and produced a schema-valid event.", fmt

    if "error_message" in parsed:
        verdict = Verdict.PASS_NO if case.expect == "fuzz" else Verdict.FAIL
        return verdict, str(parsed["error_message"]), fmt

    try:
        event = _normalize(fmt, parsed)
        UniversalEvent.model_validate(event)
    except Exception as exc:
        verdict = Verdict.PASS_NO if case.expect == "fuzz" else Verdict.FAIL
        return verdict, f"Strict event validation failed: {exc}", fmt

    if case.expect == "fuzz":
        return Verdict.PASS_YES, "Mutation parsed and normalized without an exception.", fmt

    if case.want_format and fmt != case.want_format:
        return Verdict.FAIL, f"Expected format {case.want_format!r}; detected {fmt!r}.", fmt

    for path, expected in case.want.items():
        exists, actual = dotted_get(event, path)
        if not exists:
            return Verdict.FAIL, f"Expected field {path!r} is missing.", fmt
        if actual != expected:
            return Verdict.FAIL, f"Field {path!r}: expected {expected!r}, got {actual!r}.", fmt

    for path in case.forbid:
        exists, _ = dotted_get(event, path)
        if exists:
            return Verdict.FAIL, f"Forbidden field {path!r} is present.", fmt

    if "_validation_warning" in event:
        return Verdict.WARN, str(event["_validation_warning"]), fmt
    return Verdict.PASS_YES, "Parsed, normalized, and strictly validated.", fmt


def run_case(case: Case, time_budget_ms: float) -> dict[str, Any]:
    started = time.perf_counter()
    try:
        verdict, reason, actual_format = _actual_verdict(case)
    except Exception as exc:
        verdict, reason, actual_format = Verdict.CRASH, f"{type(exc).__name__}: {exc}", None

    elapsed_ms = (time.perf_counter() - started) * 1000
    if elapsed_ms > time_budget_ms and verdict not in (Verdict.CRASH,):
        verdict = Verdict.FAIL
        reason = f"Exceeded {time_budget_ms:g} ms budget ({elapsed_ms:.2f} ms). {reason}"

    if case.xfail:
        if verdict in (Verdict.FAIL, Verdict.CRASH, Verdict.WARN):
            reason = f"{case.xfail}: {reason}"
            verdict = Verdict.XFAIL
        elif verdict in (Verdict.PASS_YES, Verdict.PASS_NO):
            reason = f"Known defect not reproduced ({case.xfail}). {reason}"
            verdict = Verdict.XPASS

    return {
        "id": case.id,
        "expect": case.expect,
        "format": actual_format or case.want_format,
        "verdict": verdict.value,
        "reason": reason,
        "elapsed_ms": round(elapsed_ms, 3),
        "xfail": case.xfail,
        "note": case.note,
        "line": case.line,
    }


def _markdown_report(results: list[dict[str, Any]], summary: Counter[str]) -> str:
    by_format: dict[str, Counter[str]] = defaultdict(Counter)
    for result in results:
        by_format[result["format"] or "unknown"][result["verdict"]] += 1

    lines = [
        "# ULPF QA Report",
        "",
        f"Cases: **{len(results)}**",
        "",
        "| Verdict | Count |",
        "|---|---:|",
    ]
    for verdict in Verdict:
        lines.append(f"| {verdict.value} | {summary[verdict.value]} |")

    lines.extend(["", "## By Format", "", "| Format | " + " | ".join(v.value for v in Verdict) + " |", "|---|" + "---:|" * len(Verdict)])
    for fmt, counts in sorted(by_format.items()):
        lines.append(f"| {fmt} | " + " | ".join(str(counts[v.value]) for v in Verdict) + " |")

    lines.extend(["", "## Cases", "", "| ID | Format | Expected | Verdict | Time (ms) | Reason |", "|---|---|---|---|---:|---|"])
    for result in results:
        reason = str(result["reason"]).replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| {result['id']} | {result['format'] or '-'} | {result['expect']} "
            f"| {result['verdict']} | {result['elapsed_ms']:.3f} | {reason} |"
        )
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run offline ULPF parser and normalizer QA cases.")
    parser.add_argument("--json", dest="json_path", type=Path, default=ROOT / "qa" / "qa_report.json")
    parser.add_argument("--md", dest="md_path", type=Path, default=ROOT / "qa" / "qa_report.md")
    parser.add_argument("--filter", help="Run only cases whose ID or expected format contains this text.")
    parser.add_argument("--seed", type=int, default=20261003)
    parser.add_argument("--fuzz-count", type=int, default=300)
    parser.add_argument("--no-fuzz", action="store_true", help="Skip seeded mutation cases.")
    parser.add_argument("--time-budget-ms", type=float, default=500.0)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.fuzz_count < 0 or args.time_budget_ms <= 0:
        build_parser().error("--fuzz-count must be non-negative and --time-budget-ms must be positive")

    valid = generate_valid_cases()
    cases = valid + generate_error_cases()
    if not args.no_fuzz:
        cases.extend(generate_fuzz_cases(valid, count=args.fuzz_count, seed=args.seed))

    if args.filter:
        needle = args.filter.casefold()
        cases = [
            case for case in cases
            if needle in case.id.casefold() or needle in (case.want_format or "").casefold()
        ]

    results = [run_case(case, args.time_budget_ms) for case in cases]
    summary = Counter(result["verdict"] for result in results)

    payload = {
        "seed": args.seed,
        "time_budget_ms": args.time_budget_ms,
        "case_count": len(results),
        "summary": {verdict.value: summary[verdict.value] for verdict in Verdict},
        "known_xfails": KNOWN_XFAILS,
        "results": results,
    }
    args.json_path.parent.mkdir(parents=True, exist_ok=True)
    args.md_path.parent.mkdir(parents=True, exist_ok=True)
    args.json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.md_path.write_text(_markdown_report(results, summary), encoding="utf-8")

    print(" | ".join(f"{verdict.value} {summary[verdict.value]}" for verdict in Verdict))
    print(f"Reports: {args.json_path} and {args.md_path}")
    failures = summary[Verdict.FAIL.value] + summary[Verdict.CRASH.value] + summary[Verdict.WARN.value]
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())