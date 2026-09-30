"""
Full pipeline dry-run test (no database required).
Tests: dispatch -> normalize -> validate -> hash -> merkle -> blockchain
"""
import sys, os, tempfile, uuid
sys.path.insert(0, 'src')

from parser import dispatch
from normalizer.normalizer import normalize
from schema.universal_event import UniversalEvent
from integrity.hasher import sha256_hash, merkle_root
from integrity.blockchain import LocalHashchain
from sample.cef import SAMPLE_CEF_LOGS
from sample.syslog import SAMPLE_SYSLOGS
from sample.json_log import SAMPLE_JSON_LOGS

all_logs = SAMPLE_SYSLOGS + SAMPLE_CEF_LOGS + SAMPLE_JSON_LOGS
print('Testing full pipeline (no DB) with ' + str(len(all_logs)) + ' logs...\n')

# Simulate pipeline
raw_hashes = []
ocsf_events = []
errors = []

for log in all_logs:
    try:
        fmt, parsed = dispatch(log)
        uid = str(uuid.uuid4())
        raw_uid = str(uuid.uuid4())
        ocsf = normalize(fmt, parsed, uid, raw_uid)
        UniversalEvent.model_validate(ocsf)
        raw_hash = sha256_hash(log)
        raw_hashes.append(raw_hash)
        ocsf_events.append(ocsf)
    except Exception as e:
        errors.append(str(e))

print('Processed: ' + str(len(ocsf_events)) + ' events')
print('Errors: ' + str(len(errors)))
if errors:
    for e in errors:
        print('  ERROR: ' + e)

# Merkle + blockchain
with tempfile.NamedTemporaryFile(suffix='.jsonl', delete=False, mode='w') as f:
    ledger_path = f.name

chain = LocalHashchain(ledger_path)
root = merkle_root(raw_hashes)
block = chain.append_block('test-batch-001', len(raw_hashes), root)

print()
print('Merkle root: ' + root[:32] + '...')
print('Block index: ' + str(block['block_index']))
print('Block hash:  ' + block['block_hash'][:32] + '...')
print('Prev hash:   ' + block['prev_block_hash'][:32] + '...')

ok, detail = chain.verify_chain()
assert ok, 'Chain verification failed: ' + detail
print('Chain verified: ' + detail)

# Show sample normalized output
print()
print('--- Sample CEF event (OCSF normalized) ---')
import json
cef_event = next(e for e in ocsf_events if e['metadata']['source_format'] == 'cef')
display = {k: v for k, v in cef_event.items() if k not in ('raw_data', 'unmapped')}
print(json.dumps(display, indent=2, default=str))

os.unlink(ledger_path)
print()
print('=== FULL PIPELINE DRY-RUN PASSED ===')
