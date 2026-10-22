#!/bin/bash
# Uji mutasi paralel (maks. 5): run_mut_pri.sh key:"Sheet" ...  -> work/mut_<key>.txt
cd "$(dirname "$0")/.."
export CHK_CACHE=$PWD/work/cache
for a in "$@"; do echo "$a"; done | xargs -P 5 -I{} sh -c 'a="{}"; k=${a%%:*}; s=${a#*:}; python3 scripts/mutate_pri.py work/out.xlsx work/base.xlsx pdf/$k.pdf work/ex/$k.xlsx "$s" work/mut_tmp_$k > work/mut_$k.txt 2>&1'
for a in "$@"; do k=${a%%:*}; tail -1 work/mut_$k.txt; done
