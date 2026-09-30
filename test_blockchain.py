import sys, os, tempfile, json
sys.path.insert(0, 'src')

from integrity.hasher import sha256_hash, merkle_root
from integrity.blockchain import LocalHashchain

with tempfile.NamedTemporaryFile(suffix='.jsonl', delete=False, mode='w') as f:
    ledger_path = f.name

chain = LocalHashchain(ledger_path)

hashes0 = [sha256_hash('e' + str(i)) for i in range(10)]
hashes1 = [sha256_hash('e' + str(i)) for i in range(5)]
hashes2 = [sha256_hash('e' + str(i)) for i in range(20)]

b0 = chain.append_block('batch-001', 10, merkle_root(hashes0))
b1 = chain.append_block('batch-002', 5,  merkle_root(hashes1))
b2 = chain.append_block('batch-003', 20, merkle_root(hashes2))

print('Block 0 index=' + str(b0['block_index']) + '  hash=' + b0['block_hash'][:16] + '...')
print('Block 1 index=' + str(b1['block_index']) + '  hash=' + b1['block_hash'][:16] + '...')
print('Block 2 index=' + str(b2['block_index']) + '  hash=' + b2['block_hash'][:16] + '...')

ok, detail = chain.verify_chain()
assert ok, 'Clean chain failed: ' + detail
print('Clean chain: ' + detail)

# Tamper block 1
with open(ledger_path, 'r') as f:
    lines = f.readlines()
block1_data = json.loads(lines[1])
block1_data['merkle_root'] = 'a' * 64
lines[1] = json.dumps(block1_data) + '\n'
with open(ledger_path, 'w') as f:
    f.writelines(lines)

ok, detail = chain.verify_chain()
assert not ok, 'Tampered chain should fail verification'
print('Tampered chain detected: ' + detail)

os.unlink(ledger_path)
print()
print('=== BLOCKCHAIN CHECKPOINT PASSED ===')
