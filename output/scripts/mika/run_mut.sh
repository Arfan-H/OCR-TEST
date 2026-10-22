#!/bin/bash
# Uji mutasi paralel: run_mut.sh key:"Sheet" ...  -> work/mut_<key>.txt
cd "$(dirname "$0")/.."
export CHK_CACHE=$PWD/work/cache
for a in "$@"; do k=${a%%:*}; sh=${a#*:}
  python3 scripts/mutate_mika.py work/out.xlsx work/base.xlsx pdf/$k.pdf work/ex/$k.xlsx "$sh" work/mut/$k > work/mut_$k.txt 2>&1 &
done
wait
for a in "$@"; do k=${a%%:*}; echo "== $k"; tail -3 work/mut_$k.txt; done
