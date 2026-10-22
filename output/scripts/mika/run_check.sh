#!/bin/bash
# Jalankan checker_mika.py untuk setiap cabang (paralel): run_check.sh key:"Sheet" ...
cd "$(dirname "$0")/.."
export CHK_CACHE=$PWD/work/cache
for a in "$@"; do k=${a%%:*}; sh=${a#*:}
  python3 scripts/checker_mika.py pdf/$k.pdf work/out.xlsx work/base.xlsx work/ex/$k.xlsx "$sh" > work/chk_$k.txt 2>&1 &
done
wait
for a in "$@"; do k=${a%%:*}; echo "== $k"; tail -4 work/chk_$k.txt; done
