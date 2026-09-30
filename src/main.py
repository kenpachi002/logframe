"""
ULPF CLI Entry Point

Usage (run from project root with PYTHONPATH=src):
  python -m src.main init-db
  python -m src.main ingest --demo
  python -m src.main ingest --file path/to/logs.log
  python -m src.main ingest --stdin
  python -m src.main verify --event-id <uuid>
  python -m src.main verify --batch-id <uuid>
  python -m src.main verify --chain
  python -m src.main export --output events.ndjson
  python -m src.main api
"""
from __future__ import annotations

import argparse
import json
import sys
import uuid
from pathlib import Path

# Ensure src/ is on the path when running as `python src/main.py`
sys.path.insert(0, str(Path(__file__).parent))


# ── Helpers ───────────────────────────────────────────────────────────────────

def _print_table(events: list[dict]) -> None:
    """Print a compact ASCII table summary of normalized events."""
    header = f"{'#':<4} {'Format':<8} {'Activity':<10} {'Severity':<12} {'Src IP':<18} {'Dst IP':<18} {'Proto':<8} Message"
    print("\n" + "=" * len(header))
    print(header)
    print("=" * len(header))
    for i, e in enumerate(events, 1):
        src_ip = (e.get("src_endpoint") or {}).get("ip") or "-"
        dst_ip = (e.get("dst_endpoint") or {}).get("ip") or "-"
        proto = (e.get("connection_info") or {}).get("protocol_name") or "-"
        fmt = (e.get("metadata") or {}).get("source_format", "-")
        activity = e.get("activity_name", "-")
        severity = e.get("severity", "-")
        msg = (e.get("message") or "-")[:40]
        print(f"{i:<4} {fmt:<8} {activity:<10} {severity:<12} {src_ip:<18} {dst_ip:<18} {proto:<8} {msg}")
    print("=" * len(header) + "\n")


def _run_ingest(args: argparse.Namespace) -> None:
    from config import Config
    from ingestion.reader import chunk, read_file, read_lines, read_stdin
    from integrity.blockchain import LocalHashchain
    from pipeline.processor import process_batch
    from storage.db import get_session

    blockchain = LocalHashchain(Config.BLOCKCHAIN_LEDGER_PATH)

    if args.demo:
        from sample.cef import SAMPLE_CEF_LOGS
        from sample.json_log import SAMPLE_JSON_LOGS
        from sample.syslog import SAMPLE_SYSLOGS

        all_lines = SAMPLE_SYSLOGS + SAMPLE_CEF_LOGS + SAMPLE_JSON_LOGS
        source_file = "demo"
        print(f"[ULPF] Demo mode — ingesting {len(all_lines)} sample log lines")
        lines_gen = read_lines(all_lines)
    elif args.file:
        source_file = args.file
        print(f"[ULPF] Ingesting from file: {source_file}")
        lines_gen = read_file(source_file)
    elif args.stdin:
        source_file = "stdin"
        print("[ULPF] Ingesting from stdin (Ctrl+D to finish)...")
        lines_gen = read_stdin()
    else:
        print("[ERROR] Specify --demo, --file <path>, or --stdin", file=sys.stderr)
        sys.exit(1)

    all_events: list[dict] = []
    batch_summaries: list[dict] = []

    for batch_lines in chunk(lines_gen, Config.BATCH_SIZE):
        with get_session() as session:
            summary = process_batch(
                raw_lines=batch_lines,
                source_file=source_file,
                session=session,
                blockchain=blockchain,
            )
            batch_summaries.append(summary)
            # Re-fetch events for display (session closed after context)
            from storage.normalized_event_repo import list_normalized_events
            evts = list_normalized_events(session, limit=len(batch_lines))
            all_events.extend([e.ocsf_json for e in evts])

    # Print summary
    total_events = sum(s["event_count"] for s in batch_summaries)
    total_blocks = len(batch_summaries)
    print(f"\n✅ Ingestion complete:")
    print(f"   Events stored : {total_events}")
    print(f"   Batches       : {total_blocks}")
    for s in batch_summaries:
        print(f"   Batch {s['batch_id'][:8]}... → block #{s['blockchain_block_index']} | merkle: {s['merkle_root'][:16]}...")
        if s["errors"]:
            for err in s["errors"]:
                print(f"   ⚠️  {err}")

    if args.demo and all_events:
        _print_table(all_events[:29])  # show up to 29 rows


def _run_verify(args: argparse.Namespace) -> None:
    from config import Config
    from integrity.blockchain import LocalHashchain
    from pipeline.processor import verify_event_integrity
    from storage.db import get_session

    if args.chain:
        chain = LocalHashchain(Config.BLOCKCHAIN_LEDGER_PATH)
        ok, detail = chain.verify_chain()
        icon = "✅" if ok else "❌"
        print(f"{icon} Chain verification: {detail}")
        sys.exit(0 if ok else 1)

    if args.event_id:
        with get_session() as session:
            result = verify_event_integrity(
                raw_event_id=args.event_id,
                session=session,
                blockchain=LocalHashchain(Config.BLOCKCHAIN_LEDGER_PATH),
            )
        if "error" in result:
            print(f"❌ {result['error']}", file=sys.stderr)
            sys.exit(1)
        icon = "❌ TAMPERED" if result["is_tampered"] else "✅ VERIFIED"
        print(f"\n{icon}")
        print(f"  raw_event_id    : {result['raw_event_id']}")
        print(f"  stored_hash     : {result['stored_hash']}")
        print(f"  recomputed_hash : {result['recomputed_hash']}")
        print(f"  block_index     : {result['blockchain_block_index']}")
        print(f"  detail          : {result['detail']}")
        sys.exit(1 if result["is_tampered"] else 0)

    if args.batch_id:
        print(f"[ULPF] Verifying all events in batch {args.batch_id}...")
        from storage.db import get_session
        from storage.raw_event_repo import get_raw_events_by_batch
        from integrity.blockchain import LocalHashchain
        chain = LocalHashchain(Config.BLOCKCHAIN_LEDGER_PATH)
        tampered_count = 0
        with get_session() as session:
            raws = get_raw_events_by_batch(session, args.batch_id)
            for r in raws:
                result = verify_event_integrity(str(r.id), session, chain)
                icon = "❌" if result.get("is_tampered") else "✅"
                print(f"  {icon} {str(r.id)[:8]}... {result.get('detail','')}")
                if result.get("is_tampered"):
                    tampered_count += 1
        print(f"\nResult: {len(raws)} events checked, {tampered_count} tampered.")
        sys.exit(1 if tampered_count else 0)

    print("[ERROR] Specify --event-id, --batch-id, or --chain", file=sys.stderr)
    sys.exit(1)


def _run_export(args: argparse.Namespace) -> None:
    from storage.db import get_session
    from storage.normalized_event_repo import list_normalized_events

    output = args.output or "ulpf_events.ndjson"
    count = 0
    with get_session() as session:
        with open(output, "w", encoding="utf-8") as f:
            offset = 0
            while True:
                batch = list_normalized_events(session, limit=500, offset=offset)
                if not batch:
                    break
                for evt in batch:
                    f.write(json.dumps(evt.ocsf_json, default=str) + "\n")
                    count += 1
                offset += len(batch)
    print(f"✅ Exported {count} events to {output}")


def _run_api(_args: argparse.Namespace) -> None:
    import uvicorn
    from api.app import create_app
    from config import Config

    app = create_app()
    print(f"[ULPF] Starting API on http://{Config.API_HOST}:{Config.API_PORT}")
    print(f"[ULPF] Swagger UI -> http://{Config.API_HOST}:{Config.API_PORT}/docs")
    uvicorn.run(app, host=Config.API_HOST, port=Config.API_PORT)


def _run_init_db(_args: argparse.Namespace) -> None:
    from storage.db import init_db
    init_db()


# ── CLI definition ────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="ulpf",
        description="Universal Log Pre-processing Framework (ULPF) — SIH Project",
    )
    sub = p.add_subparsers(dest="command", required=True)

    # init-db
    sub.add_parser("init-db", help="Initialize the PostgreSQL schema")

    # ingest
    ing = sub.add_parser("ingest", help="Ingest log lines through the full pipeline")
    src = ing.add_mutually_exclusive_group(required=True)
    src.add_argument("--demo",  action="store_true", help="Use built-in sample logs")
    src.add_argument("--file",  metavar="PATH",      help="Read from a log file")
    src.add_argument("--stdin", action="store_true",  help="Read from stdin")

    # verify
    ver = sub.add_parser("verify", help="Verify event or chain integrity")
    vg = ver.add_mutually_exclusive_group(required=True)
    vg.add_argument("--event-id",  metavar="UUID", help="Verify a single raw event")
    vg.add_argument("--batch-id",  metavar="UUID", help="Verify all events in a batch")
    vg.add_argument("--chain",     action="store_true", help="Verify entire blockchain")

    # export
    exp = sub.add_parser("export", help="Export normalized events as NDJSON")
    exp.add_argument("--output", metavar="FILE", default="ulpf_events.ndjson")

    # api
    sub.add_parser("api", help="Start the FastAPI REST server")

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    dispatch = {
        "init-db": _run_init_db,
        "ingest":  _run_ingest,
        "verify":  _run_verify,
        "export":  _run_export,
        "api":     _run_api,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
