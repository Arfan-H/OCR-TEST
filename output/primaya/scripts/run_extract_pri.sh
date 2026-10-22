#!/bin/bash
# Jalankan extract_pri.py (maks. 5 paralel, hemat memori) untuk PDF di pdf/ -> work/json/ ; argumen opsional: daftar key
cd "$(dirname "$0")/.."
keys="$@"; [ -z "$keys" ] && keys=$(ls pdf | sed 's/\.pdf$//')
for b in $keys; do echo $b; done | xargs -P 5 -I{} sh -c 'python3 scripts/extract_pri.py pdf/{}.pdf work/json/{}.json > work/json/{}.log 2>&1'
for b in $keys; do cat work/json/$b.log; done
