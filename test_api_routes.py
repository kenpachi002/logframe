import urllib.request
import json
import sys

BASE_URL = "http://localhost:8000"

def log(msg, success=True):
    symbol = "[PASS]" if success else "[FAIL]"
    print(f"{symbol} {msg}")

def get(path):
    req = urllib.request.Request(f"{BASE_URL}{path}")
    with urllib.request.urlopen(req, timeout=10) as r:
        return r.status, r.read().decode("utf-8")

def post(path, data):
    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=body,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return r.status, r.read().decode("utf-8")

def run_tests():
    all_ok = True
    print("\n--- Testing ULPF API & Frontend Endpoints ---")
    
    # 1. Frontend UI root
    try:
        status, html = get("/")
        assert status == 200 and "Universal Log Pre-processing Framework" in html
        log(f"GET / (Frontend UI loads HTML, length={len(html)})")
    except Exception as e:
        log(f"GET / failed: {e}", False)
        all_ok = False

    # 2. Health
    try:
        status, text = get("/api/health")
        data = json.loads(text)
        assert status == 200 and data.get("status") == "ok"
        log(f"GET /api/health -> status={data['status']}, db_type={data.get('db_type')}, db_ok={data.get('db_ok')}, blocks={data.get('blockchain_blocks')}")
    except Exception as e:
        log(f"GET /api/health failed: {e}", False)
        all_ok = False

    # 3. Formats
    try:
        status, text = get("/api/formats")
        data = json.loads(text)
        assert status == 200 and len(data.get("formats", [])) >= 3
        log(f"GET /api/formats -> supported formats: {[f['id'] for f in data['formats']]}")
    except Exception as e:
        log(f"GET /api/formats failed: {e}", False)
        all_ok = False

    # 4. Samples for CEF, Syslog, JSON
    for fmt in ["cef", "syslog", "json"]:
        try:
            status, text = get(f"/api/samples/{fmt}")
            data = json.loads(text)
            assert status == 200 and len(data.get("lines", [])) > 0
            log(f"GET /api/samples/{fmt} -> returned {len(data['lines'])} sample lines")
        except Exception as e:
            log(f"GET /api/samples/{fmt} failed: {e}", False)
            all_ok = False

    # 5. POST /api/ingest
    sample_raw = "CEF:0|Cisco|ASA|9.1|106023|Deny Inbound TCP|5|src=192.168.1.10 dst=8.8.8.8 spt=54321 dpt=443 proto=tcp act=deny"
    try:
        status, text = post("/api/ingest", {"logs": sample_raw, "source_hint": "auto"})
        data = json.loads(text)
        assert status == 200 and data.get("event_count") >= 1
        log(f"POST /api/ingest -> batch_id={data.get('batch_id')}, count={data.get('event_count')}, merkle_root={data.get('merkle_root')[:16]}..., block_hash={data.get('blockchain_block_hash')[:16]}...")
    except Exception as e:
        log(f"POST /api/ingest failed: {e}", False)
        all_ok = False

    # 6. GET /api/events
    try:
        status, text = get("/api/events?limit=5")
        data = json.loads(text)
        assert status == 200 and "events" in data
        log(f"GET /api/events?limit=5 -> retrieved {len(data['events'])} events (total={data.get('total')})")
    except Exception as e:
        log(f"GET /api/events failed: {e}", False)
        all_ok = False

    # 7. GET /api/blockchain/blocks
    try:
        status, text = get("/api/blockchain/blocks")
        data = json.loads(text)
        assert status == 200 and "blocks" in data
        log(f"GET /api/blockchain/blocks -> block_count={data.get('block_count')}")
    except Exception as e:
        log(f"GET /api/blockchain/blocks failed: {e}", False)
        all_ok = False

    # 8. POST /api/verify/chain
    try:
        status, text = post("/api/verify/chain", {})
        data = json.loads(text)
        assert status == 200 and data.get("is_valid") is True
        log(f"POST /api/verify/chain -> is_valid={data['is_valid']}, block_count={data.get('block_count')}, detail='{data.get('detail')}'")
    except Exception as e:
        log(f"POST /api/verify/chain failed: {e}", False)
        all_ok = False

    # 9. GET /api/integrity/batches
    try:
        status, text = get("/api/integrity/batches")
        data = json.loads(text)
        assert status == 200 and "batches" in data
        log(f"GET /api/integrity/batches -> batch_count={data.get('count')}")
    except Exception as e:
        log(f"GET /api/integrity/batches failed: {e}", False)
        all_ok = False

    # 10. Swagger Docs
    try:
        status, html = get("/docs")
        assert status == 200
        log("GET /docs -> Swagger UI loaded (200 OK)")
    except Exception as e:
        log(f"GET /docs failed: {e}", False)
        all_ok = False

    print("\n--- Summary ---")
    if all_ok:
        print("[SUCCESS] ALL ENDPOINTS ARE FULLY OPERATIONAL AND VERIFIED!\n")
    else:
        print("[WARNING] Some tests failed. Please review above.\n")
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
