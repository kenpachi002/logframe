# ULPF — Universal Log Pre-processing Framework
## Architecture Document · v0.1.0

---

## 1. System Overview

ULPF is a prototype framework that ingests heterogeneous security device logs, parses and normalises them to a common schema, and anchors their integrity in a cryptographic hashchain. It targets the *current scope* defined in SIH 2026: **perimeter network device logs** (firewalls, IDS/IPS, routers) in the six most prevalent formats.

```
+-------------------------- Ingestion Layer ----------------------------+
|  Browser UI (Playground)  .  REST POST /api/ingest  .  CLI stdin     |
+-----------------------------------+----------------------------------+
                                    | raw log text (preserved as submitted)
                         +----------v----------+
                         |  Format Dispatcher  |  heuristic auto-detection
                         |  parser/__init__.py |  order: CEF->LEEF->Syslog->XML->JSON->CSV
                         +----------+----------+
           +-----------+-----------+-----------+-----------+----------+
           v           v           v           v           v          v
        cef.py     leef.py    syslog.py   xml_log.py  json_log   csv_log
           +-----------+-----------+-----------+-----------+----------+
                                    | parsed flat dict
                         +----------v----------+
                         |  OCSF Normalizer    |  -> Network Activity class_uid 4001
                         |  normalizer.py      |     OCSF 1.9.0 schema
                         +----------+----------+
                                    | ocsf_event dict
                         +----------v----------+
                         |  Schema Validator   |  Pydantic UniversalEvent
                         |  schema/            |  warnings logged; pipeline never aborted
                         +----------+----------+
                +------------------+-----------------+
                v                                    v
     raw_events table                   normalized_events table
     . raw_data TEXT (exact text)        . ocsf_json JSONB/TEXT
     . sha256_hash CHAR(64)              . FK -> raw_events.id
     . source_format, batch_id           . denorm cols: src_ip, severity_id
     raw_batch_payloads table
     . full decoded submitted text
     . sha256_hash included in batch Merkle root
                |
                v
     Merkle root (SHA-256 per event -> tree root per batch)
                |
                v
     blockchain_ledger/chain.jsonl  (append-only JSONL)
     [block_index | batch_id | event_count | merkle_root | prev_hash | block_hash]
                |
                v
     Tamper Detection API  POST /api/verify/event
     re-hash raw_data -> compare sha256_hash -> flag divergence
```

---

## 2. Component Design

| Component | Location | Role |
|---|---|---|
| **Parser Registry** | `src/parser/__init__.py` | Ordered dispatcher; each parser is a pure function `parse_X(src: str) -> dict`. New formats: add detect_X + parse_X + registry entry. |
| **OCSF Normalizer** | `src/normalizer/normalizer.py` | Maps parser output to OCSF 1.9.0 Network Activity fields. Preserves unmapped fields in `unmapped{}`. Stores original text in `raw_data`. |
| **Schema / Validator** | `src/schema/universal_event.py` | Pydantic v2 model matching OCSF Base Event + Network Activity subset. |
| **Pipeline Processor** | `src/pipeline/processor.py` | Orchestrates per-line and per-batch flow. Event text and optional full API batch text are stored separately; parsers receive a trimmed copy. |
| **Integrity Layer** | `src/integrity/` | `hasher.py` — SHA-256 + Merkle root. `blockchain.py` — append-only JSONL chain with chained block hashes. |
| **Storage** | `src/storage/` | SQLAlchemy 2.0. RawEvent + NormalizedEvent + IntegrityBatch + TamperCheck models. SQLite (zero-config) or PostgreSQL. |
| **REST API** | `src/api/` | FastAPI. Routes: ingest, events, raw, integrity, blockchain, health, samples. Rate-limited (SlowAPI). Optional API-key auth. |
| **Frontend UI** | `frontend/index.html` | Pure HTML/CSS/JS (no framework). Playground, Blockchain Ledger, Event History with raw-event download. Light/dark theme. |

---

## 3. Raw-Data Preservation Contract

**Guarantee:** For API submissions, the complete decoded `logs` text is stored in
`raw_batch_payloads.raw_payload`, including whitespace, blank lines, and line endings.
Its SHA-256 digest is included as an additional leaf in the batch Merkle root. Each
non-blank event line is also stored and hashed independently in `raw_events`; the
normalized event's `raw_data` contains the same event-line text. Batch `.txt` download
retrieves the persisted submission. Per-event raw download retrieves its event line.

The request is JSON-decoded text, so the original HTTP wire bytes and original character
encoding are not retained. CLI batches currently store event lines but do not have a
single original multi-line submission payload. Older batches without a saved API payload
cannot provide a full-batch download.

---

## 4. Normalised Schema (OCSF 1.9.0 subset)

```json
{
  "time": "<ms epoch>",
  "class_uid": 4001,
  "category_uid": 4,
  "activity_id": "<1-7: Open/Close/Reset/Fail/Refuse/Traffic/Listen>",
  "severity_id": "<1-5>",
  "src_endpoint": { "ip": "", "port": 0, "hostname": "" },
  "dst_endpoint": { "ip": "", "port": 0, "hostname": "" },
  "connection_info": { "direction_id": 0, "protocol_name": "", "protocol_num": 0 },
  "metadata": { "version": "1.9.0", "source_format": "cef|syslog|json|xml|csv|leef" },
  "raw_data": "<original log line — preservation field>",
  "unmapped": {},
  "ulpf_event_id": "<uuid — normalised event>",
  "ulpf_raw_event_id": "<uuid — raw event FK>"
}
```

---

## 5. Deployment

| Mode | Command | Notes |
|---|---|---|
| **Local dev (SQLite)** | `.\run.bat` or `.\start.ps1` | Zero configuration; ulpf.db in project root |
| **Docker (PostgreSQL)** | `docker compose up --build` | Compose starts Postgres + API; env vars in .env |
| **Air-gap (prepare online)** | `docker pull postgres:16-alpine`<br>`docker compose build ulpf`<br>`docker image save -o ulpf-images.tar ulpf:local postgres:16-alpine` | Transfer the image archive, Compose file, and required configuration to the offline host |
| **Air-gap (run offline)** | `docker image load -i ulpf-images.tar`<br>`docker compose up --no-build` | Uses the preloaded app and database images; this procedure is documented but not yet validated on a disconnected host |
| **Cloud (Render/Railway)** | Set `DATABASE_URL` env var | Supabase or Railway PostgreSQL URL |

---

## 6. Scope and Honest Boundaries

| Capability | Status |
|---|---|
| Parse CEF, Syslog, JSON, XML, CSV, LEEF | Implemented and tested |
| OCSF 1.9.0 Network Activity normalisation | Implemented (MVP subset) |
| SHA-256 + Merkle hashchain integrity | Implemented |
| Tamper detection via re-hash | Implemented |
| REST API + Interactive UI | Implemented |
| Container deployment | Docker + Compose |
| Full submitted API batch text preservation and download | Implemented for API-ingested batches |
| SIEM/data-lake integration | API and NDJSON export available; outbound connectors are future scope |
| Air-gapped installation | Container preparation procedure documented; disconnected deployment unverified |
| Developer parser extension | Static parser registry; each parser requires code and registry changes |
| Billion-event/day throughput | Out of scope (future: Kafka + worker pool) |
| AI/ML analytics pipeline | Out of scope (structured output can be consumed downstream) |
| Automated/plugin-based parser onboarding | Future scope |
| Full OCSF event taxonomy (auth, endpoint…) | Future scope; currently Network Activity only |
