<div align="center">

# ULPF — Universal Log Pre-processing Framework

**Enterprise-grade multi-vendor log ingestion · OCSF 1.9.0 normalization · Cryptographic blockchain integrity**

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![OCSF](https://img.shields.io/badge/OCSF-1.9.0-6366f1?style=flat-square)](https://schema.ocsf.io)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)
[![Formats](https://img.shields.io/badge/Formats-CEF·Syslog·JSON·XML·CSV·LEEF-f59e0b?style=flat-square)]()

</div>

---

ULPF solves a real enterprise problem: logs from hundreds of different vendors — firewalls, IDS, cloud services, operating systems — all speak different languages. ULPF ingests them all, maps every field to a single canonical **OCSF 1.9.0** schema, and anchors every batch to a **SHA-256 Merkle hashchain ledger** that makes log tampering instantly detectable.

```
Cisco ASA (CEF)   ─┐
Juniper SRX (CEF) ─┤                         ┌─ OCSF Normalized JSON
IBM QRadar (LEEF) ─┤──► Parser Dispatcher ──►─┤─ SHA-256 + Merkle Chain
Linux Syslog      ─┤                         └─ Blockchain Block Ledger
Windows XML Event ─┤
Fortinet CSV       ─┘
```

---

## Features at a Glance

| Capability | Detail |
|---|---|
| **6 Zero-Dependency Parsers** | CEF, Syslog (RFC 3164/5424), JSON, XML, CSV, LEEF 1.0/2.0 |
| **OCSF 1.9.0 Normalization** | Canonical `Network Activity` schema, class_uid 4001 |
| **Merkle Hashchain Ledger** | SHA-256 per event → Merkle root per batch → Blockchain block |
| **Tamper Detection** | Re-hash raw bytes on demand; flags any modification instantly |
| **Rate Limiting** | 60 req/min on ingest, 120 req/min global (configurable) |
| **Payload Protection** | 2 MB hard cap + 500 line batch cap — DoS-resistant |
| **OWASP Headers** | `X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection` |
| **Optional API Key Auth** | Guard all endpoints via `X-API-Key` header |
| **Zero External Runtime** | No Kafka, no Redis, no ML models — just Python + SQLite/PostgreSQL |
| **Interactive UI** | Live parser playground, blockchain ledger viewer, event history |
| **Test Lab** | 60+ real-vendor log samples across all 6 formats, copy-to-parser in one click |

---

## Quick Start — Local Python (Recommended)

**Requirements:** Python 3.12+

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/ulpf.git
cd ulpf

# 2. Create a virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set PYTHONPATH (required — all source lives under src/)
# Windows PowerShell
$env:PYTHONPATH="src"

# Windows CMD
set PYTHONPATH=src

# macOS / Linux
export PYTHONPATH=src

# 5. Start the server (auto-opens browser)
python -m main api
```

That's it. The browser opens at **http://localhost:8000** automatically.

> **Tip:** No `.env` file needed for local development. ULPF uses SQLite by default with zero configuration.

---

## Quick Start — Docker

```bash
# Start everything (PostgreSQL + ULPF API)
docker compose up --build

# Open the UI
open http://localhost:8000

# Open Swagger
open http://localhost:8000/docs
```

---

## How to Use the UI

1. **Open** → http://localhost:8000
2. **Paste** any raw log into the input panel (or click **Load Sample** to auto-fill)
3. **Click** `Parse & Normalize` — the system auto-detects the format
4. **See** the normalized OCSF event, field breakdown, SHA-256 hash, and blockchain block on the right
5. **Explore** the **Blockchain Ledger** tab to see all anchored batches
6. **Browse** the **Event History** tab to query all past normalized events

Need sample logs? Click **🧪 Test Lab Samples** in the footer for 60+ real vendor examples across all 6 formats.

---

## Pages

| URL | Description |
|---|---|
| `/` | Live parser playground + blockchain ledger + event history |
| `/examples` | Test Lab — 60+ real-vendor samples, copy-to-parser in one click |
| `/roadmap` | Architecture diagram, implementation roadmap, compliance mapping |
| `/docs` | Interactive Swagger API documentation |
| `/redoc` | ReDoc API reference |

---

## Supported Log Formats

| Format | Standards / Vendors |
|---|---|
| **CEF** | Cisco ASA, Palo Alto PAN-OS, Fortinet FortiGate, Juniper SRX, Check Point |
| **Syslog** | RFC 3164 + RFC 5424 — Linux, routers, any syslog-enabled device |
| **JSON** | Flat + nested JSON — application logs, cloud tools, API logs |
| **XML** | Windows Event Log, vendor syslog-over-XML, IDS/IPS alert exports |
| **CSV** | Fortinet traffic CSV, pfSense firewall logs, Cisco Meraki, generic IDS export |
| **LEEF** | IBM QRadar LEEF 1.0 + 2.0, Juniper SA, Check Point Firewall |

All parsers are **zero-dependency** — pure Python standard library, no third-party parsing packages.

---

## REST API

| Method | Path | Rate Limit | Description |
|---|---|---|---|
| `GET` | `/api/health` | 120/min | System health + DB status + blockchain block count |
| `POST` | `/api/ingest` | **60/min** | Full pipeline — parse → normalize → store → hashchain |
| `GET` | `/api/events` | 120/min | List normalized events (filterable by format, severity) |
| `GET` | `/api/events/{id}` | 120/min | Single normalized event |
| `GET` | `/api/events/{id}/raw` | 120/min | Trace normalized → raw event |
| `GET` | `/api/raw/{id}` | 120/min | Raw event by ID |
| `GET` | `/api/raw/batch/{batch_id}` | 120/min | All raw events in a batch |
| `POST` | `/api/verify/event` | 120/min | Re-hash raw event, compare to stored hash |
| `POST` | `/api/verify/chain` | 120/min | Verify full blockchain chain integrity |
| `GET` | `/api/blockchain/blocks` | 120/min | List all blockchain blocks |
| `GET` | `/api/formats` | 120/min | Supported parser formats + capabilities |
| `GET` | `/api/samples/{format}` | 120/min | Sample logs for a given format |

Full interactive documentation at **`/docs`** (Swagger UI) and **`/redoc`**.

---

## Security & Rate Limiting

ULPF is hardened against common web attack vectors out of the box:

```
✓ Rate limiting         60 req/min (ingest) · 120 req/min (all others)
✓ Payload size cap      2 MB per request (HTTP 413 on violation)
✓ Batch line cap        500 lines per ingest request (HTTP 413 on violation)
✓ OWASP headers         X-Content-Type-Options · X-Frame-Options · X-XSS-Protection
✓ Input sanitization    All raw log text stripped of control characters
✓ API Key auth          Optional ULPF_API_KEY — header or query param
✓ Error sanitization    500 errors never expose stack traces or DB credentials
✓ CORS                  Configurable (open for demo, restrict for production)
```

All security settings are controlled via environment variables — no code changes needed.

---

## Environment Variables

Copy `.env.example` to `.env` and adjust as needed:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | *(empty)* | Full SQLAlchemy URL (Supabase, Railway, etc.) — overrides all DB_* vars |
| `DB_HOST` | *(empty)* | PostgreSQL host |
| `DB_PORT` | `5432` | PostgreSQL port |
| `DB_NAME` | `ulpf` | Database name |
| `DB_USER` | *(empty)* | Database user |
| `DB_PASSWORD` | *(empty)* | Database password |
| `ULPF_API_KEY` | *(empty)* | Optional API key — if empty, all endpoints are open |
| `RATE_LIMIT_DEFAULT` | `120/minute` | Global rate limit |
| `RATE_LIMIT_INGEST` | `60/minute` | Ingest endpoint rate limit |
| `MAX_REQUEST_SIZE_BYTES` | `2097152` | Max request body size (2 MB) |
| `BATCH_SIZE` | `50` | Base batch size; hard cap is 10× this (500 lines) |
| `LOG_TIMEZONE` | `Asia/Kolkata` | Timezone for timestamp normalization |
| `API_HOST` | `0.0.0.0` | Bind host |
| `API_PORT` | `8000` | Bind port |

---

## Architecture

```
┌─────────────────── Ingestion Layer ───────────────────────┐
│  UI Form  ·  REST POST /api/ingest  ·  CLI stdin/file     │
└───────────────────────┬───────────────────────────────────┘
                        │
              ┌─────────▼──────────┐
              │  Format Dispatcher  │  (heuristic auto-detection)
              └─────────┬──────────┘
          ┌─────────────┼──────────────┐
          ▼             ▼              ▼              ...
       CEF Parser   Syslog Parser  JSON Parser   XML · CSV · LEEF
          └─────────────┴──────────────┘
                        │
              ┌─────────▼──────────┐
              │   OCSF Normalizer   │  → class_uid 4001 Network Activity
              └─────────┬──────────┘
                        │
          ┌─────────────┴──────────────┐
          ▼                            ▼
   raw_events table            normalized_events table
   (raw_data + SHA-256)        (OCSF JSON, FK → raw)
          │
          ▼
   Merkle Root (per batch)
          │
          ▼
   Blockchain Block Ledger
   (blockchain_ledger/chain.jsonl)
   [block_index | merkle_root | prev_hash | block_hash]
          │
          ▼
   Tamper Detection API
   (re-hash raw_data → compare)
```

---

## Project Structure

```
ulpf/
├── src/
│   ├── main.py              ← CLI entry point
│   ├── config.py            ← Environment config (no code changes needed)
│   ├── parser/              ← 6 parsers + auto-dispatch registry
│   │   ├── __init__.py      ← dispatch() entry point
│   │   ├── cef.py
│   │   ├── syslog.py
│   │   ├── json_log.py
│   │   ├── xml_log.py
│   │   ├── csv_log.py
│   │   └── leef.py
│   ├── normalizer/          ← OCSF 1.9.0 normalization
│   ├── schema/              ← Pydantic UniversalEvent model
│   ├── pipeline/            ← Batch orchestrator + tamper detection
│   ├── storage/             ← SQLAlchemy models + repositories
│   ├── integrity/           ← SHA-256 hasher + Merkle chain ledger
│   ├── sample/              ← 60+ real-vendor sample logs (6 formats)
│   └── api/
│       ├── app.py           ← FastAPI application factory
│       ├── security.py      ← Rate limiter + auth + OWASP middleware
│       └── routes/          ← health · ingest · events · raw · integrity
├── frontend/
│   ├── index.html           ← Live parser UI (pure HTML/CSS/JS)
│   ├── examples.html        ← Test Lab — 60+ sample logs
│   └── roadmap.html         ← Architecture & implementation roadmap
├── migrations/              ← PostgreSQL DDL scripts
├── blockchain_ledger/       ← Append-only hashchain (gitignored)
├── .env.example             ← Configuration template
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

## CLI Reference

```bash
# Set PYTHONPATH first
$env:PYTHONPATH="src"   # PowerShell
export PYTHONPATH=src   # bash

# Start the API server (auto-opens browser)
python -m main api

# Initialize the database schema
python -m main init-db

# Ingest built-in demo logs (6 formats, 30+ samples)
python -m main ingest --demo

# Ingest from a log file
python -m main ingest --file /var/log/cisco.log

# Ingest from stdin (pipe)
cat /var/log/syslog | python -m main ingest --stdin

# Verify a single event's integrity
python -m main verify --event-id <uuid>

# Verify entire blockchain chain
python -m main verify --chain

# Export all normalized events as NDJSON
python -m main export --output events.ndjson
```

---

## Verifying Tamper Detection

```bash
# 1. Ingest some logs
python -m main ingest --demo

# 2. Note any raw_event_id from the API
curl http://localhost:8000/api/events | python -m json.tool

# 3. Verify integrity — should show VERIFIED
curl -X POST http://localhost:8000/api/verify/event \
     -H "Content-Type: application/json" \
     -d '{"raw_event_id": "<id>"}'
# → {"is_tampered": false, "stored_hash": "...", "computed_hash": "..."}

# 4. Tamper with the raw event (SQLite example)
python -c "
import sqlite3; c = sqlite3.connect('ulpf.db')
c.execute(\"UPDATE raw_events SET raw_data='INJECTED' WHERE id='<id>'\")
c.commit()
"

# 5. Re-verify — tamper is instantly detected
curl -X POST http://localhost:8000/api/verify/event \
     -H "Content-Type: application/json" \
     -d '{"raw_event_id": "<id>"}'
# → {"is_tampered": true, "stored_hash": "abc...", "computed_hash": "xyz..."}
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI 0.111+ |
| ASGI Server | Uvicorn (with standard extras) |
| Rate Limiting | SlowAPI (token-bucket, per-IP) |
| Database | SQLite (default) · PostgreSQL (production) |
| ORM | SQLAlchemy 2.0 |
| Schema Validation | Pydantic v2 |
| Cryptography | `hashlib` (SHA-256) — stdlib only |
| Frontend | Vanilla HTML + CSS + JavaScript — no framework |
| Deployment | Docker + docker-compose |

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-parser`)
3. Commit changes (`git commit -m 'feat: add Palo Alto NGFW parser'`)
4. Push to branch (`git push origin feature/new-parser`)
5. Open a Pull Request

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

<div align="center">

Built with precision · OCSF 1.9.0 · Zero external parsing dependencies

</div>
