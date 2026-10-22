#!/bin/bash
# Jalankan extract_mika.py paralel untuk semua PDF di pdf/ -> work/json/
cd "$(dirname "$0")/.."
for f in pdf/*.pdf; do b=$(basename $f .pdf); python3 scripts/extract_mika.py $f work/json/$b.json > work/json/$b.log 2>&1 & done
wait; cat work/json/*.log
