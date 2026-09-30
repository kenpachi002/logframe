# ULPF — Universal Log Pre-processing Framework

**SIH 2025 | Theme: Blockchain & Security**

A framework that ingests heterogeneous network/security device logs, normalizes them into a common OCSF 1.9.0 schema, anchors integrity on a blockchain ledger, and detects tampered events.

---

## Quick Start (with Docker)

```bash
# 1. Clone and enter the project
git clone <repo-url> && cd py

# 2. Start PostgreSQL + ULPF API
docker compose up --build

# 3. Run the demo (in a new terminal)
docker compose exec ulpf python -m main ingest --demo

# 4. Open Swagger UI
# → http://localhost:8000/docs
```

## Quick Start (local Python)

**Prerequisites:** Python 3.12+, PostgreSQL 16 running locally

```bash
# Install dependencies
pip install -r requirements.txt

# Copy and edit environment
cp .env.example .env

# Set PYTHONPATH
export PYTHONPATH=src        # Linux/macOS
set PYTHONPATH=src           # Windows CMD
$env:PYTHONPATH="src"        # Windows PowerShell

# Initialize the database
python -m main init-db

# Run demo ingestion (29 sample logs from Cisco, Palo Alto, Fortinet, Juniper, Check Point)
python -m main ingest --demo

# Start the REST API
python -m main api
# → http://localhost:8000/docs
```

---

## CLI Commands

| Command | Description |
|---|---|
| `python -m main init-db` | Create PostgreSQL tables |
| `python -m main ingest --demo` | Ingest 30 built-in sample logs |
| `python -m main ingest --file logs.log` | Ingest from a log file |
| `python -m main ingest --stdin` | Ingest from stdin (pipe) |
| `python -m main verify --chain` | Verify entire blockchain integrity |
| `python -m main verify --event-id <uuid>` | Verify a single raw event |
| `python -m main verify --batch-id <uuid>` | Verify all events in a batch |
| `python -m main export --output out.ndjson` | Export normalized events as NDJSON |
| `python -m main api` | Start FastAPI REST server |

---

## REST API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/events` | List normalized events (filterable) |
| GET | `/api/events/{id}` | Get single normalized event |
| GET | `/api/events/{id}/raw` | Get the raw event linked to a normalized event |
| GET | `/api/raw/{id}` | Get raw event by ID |
| GET | `/api/raw/batch/{batch_id}` | Get all raw events in a batch |
| POST | `/api/verify/event` | Verify integrity of a raw event |
| POST | `/api/verify/chain` | Verify entire blockchain chain |
| GET | `/api/blockchain/blocks` | List all blockchain blocks |
| GET | `/api/blockchain/blocks/{n}` | Get block at index n |
| GET | `/api/integrity/batches` | List integrity batches |

---

## Architecture

```
Heterogeneous Logs (Syslog RFC3164/5424, CEF, JSON)
        │
        ▼
Ingestion Layer (file / stdin / demo)
        │
        ▼
Parser Registry (plug-and-play dispatcher)
  ├── CEF parser     (Cisco, Palo Alto, Fortinet, Juniper, Check Point)
  ├── Syslog parser  (RFC 3164 + RFC 5424)
  └── JSON parser
        │
        ▼
ULPF Normalizer → OCSF 1.9.0 Network Activity Schema
        │
        ├──→ PostgreSQL: raw_events (raw_data + SHA-256 hash)
        └──→ PostgreSQL: normalized_events (OCSF JSON, FK → raw_events)
                │
                ▼
        SHA-256 hash per event
        Merkle root per batch
                │
                ▼
        Local Hashchain Ledger (blockchain_ledger/chain.jsonl)
        [block_index | batch_id | merkle_root | prev_hash | block_hash]
                │
                ▼
        Tamper Detection: re-hash raw_data → compare to stored hash
```

---

## Supported Log Formats

| Format | Standards | Vendors |
|---|---|---|
| Syslog | RFC 3164, RFC 5424 | Linux firewalls, routers, any syslog-enabled device |
| CEF | Common Event Format | Cisco ASA, Palo Alto PAN-OS, Fortinet FortiGate, Juniper SRX, Check Point |
| JSON | Any JSON object | Application logs, cloud security tools |

---

## SIH Demo Script (9 steps)

```bash
# Step 1: Ingest diverse vendor logs
python -m main ingest --demo

# Step 2: Query normalized events (unified schema)
curl http://localhost:8000/api/events | python -m json.tool

# Step 3: View a specific event
curl http://localhost:8000/api/events/<event_id>

# Step 4: Trace normalized → raw (traceability)
curl http://localhost:8000/api/events/<event_id>/raw

# Step 5: Verify event integrity (should be VERIFIED)
curl -X POST http://localhost:8000/api/verify/event \
     -H "Content-Type: application/json" \
     -d '{"raw_event_id": "<raw_event_id>"}'

# Step 6: View blockchain blocks
curl http://localhost:8000/api/blockchain/blocks

# Step 7: Tamper with the database (simulate attack)
psql -U ulpf_user -d ulpf -c "UPDATE raw_events SET raw_data='TAMPERED' WHERE id='<id>';"

# Step 8: Detect the tamper
curl -X POST http://localhost:8000/api/verify/event \
     -H "Content-Type: application/json" \
     -d '{"raw_event_id": "<raw_event_id>"}'
# → { "is_tampered": true, ... }

# Step 9: Verify full chain integrity
curl -X POST http://localhost:8000/api/verify/chain
```

---

## Project Structure

```
py/
├── src/
│   ├── main.py              ← CLI entry point
│   ├── config.py            ← Environment config
│   ├── parser/              ← CEF, Syslog, JSON parsers + registry
│   ├── normalizer/          ← OCSF normalization logic
│   ├── schema/              ← Pydantic OCSF model (validation)
│   ├── ingestion/           ← File/stdin/in-memory reader
│   ├── pipeline/            ← Orchestrator + tamper detection
│   ├── storage/             ← SQLAlchemy models + DB repos
│   ├── integrity/           ← SHA-256 hasher + hashchain
│   ├── api/                 ← FastAPI app + routes
│   └── sample/              ← 30 real-vendor sample logs
├── migrations/              ← PostgreSQL DDL
├── blockchain_ledger/       ← Hashchain file (append-only)
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```
