#!/bin/bash
# Jalankan checker_pri.py paralel: run_check_pri.sh key:"Sheet" ...  -> work/chk_<key>.txt
cd "$(dirname "$0")/.."
export CHK_CACHE=$PWD/work/cache
for a in "$@"; do k=${a%%:*}; sh=${a#*:}
  python3 scripts/checker_pri.py pdf/$k.pdf work/out.xlsx work/base.xlsx work/ex/$k.xlsx "$sh" > work/chk_$k.txt 2>&1 &
done
wait
for a in "$@"; do k=${a%%:*}; echo "== $k"; head -40 work/chk_$k.txt; done
