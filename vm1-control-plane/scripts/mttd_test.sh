#!/bin/bash
cd ~/zt-prototype/blockchain-audit

echo "🔍 MTTD (Mean Time To Detect) Test"
echo "=================================="

cp audit_chain.json audit_chain_backup.json

# Start timing
START=$(date +%s%N)

# Tamper
python3 << 'PYEOF'
import json
with open('audit_chain.json', 'r') as f:
    chain = json.load(f)
chain[1]['event']['result'] = 'CLEAN'
with open('audit_chain.json', 'w') as f:
    json.dump(chain, f, indent=2)
PYEOF

# Detect
./audit_chain.py verify 2>&1
RESULT=$?

END=$(date +%s%N)

# Calculate
MTTD=$(echo "scale=3; ($END - $START) / 1000000" | bc)
echo ""
echo "⏱️  MTTD: $MTTD milliseconds"

mv audit_chain_backup.json audit_chain.json

if [ $RESULT -ne 0 ]; then
    echo "✅ Tamper detected!"
else
    echo "❌ Detection failed"
fi
