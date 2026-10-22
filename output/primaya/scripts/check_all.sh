#!/bin/bash
# checker untuk ke-15 sheet Primaya -> work/chk_<key>.txt, ringkasan ke stdout
cd "$(dirname "$0")/.."
bash scripts/run_check_pri.sh "bekasitimur:Primaya Bekasi Timur" "evasari:Primaya Evasari" "bhaktiwara:Primaya Bhaktiwara" "karawang:Primaya Karawang" \
  "depok:Primaya Depok" "betang:Primaya Betang Pambelum" "hertasning:Primaya Hertasning" "kelapagading:Primaya Kelapa Gading" >/dev/null
bash scripts/run_check_pri.sh "makassar:Primaya Makassar" "sukabumi:Primaya Sukabumi" "tangerang:Primaya Tangerang" "semarang:Primaya Semarang" \
  "pgicikini:Primaya PGI Cikini" "ukrida:UKRIDA Primaya" "pasarkemis:Primaya Pasar Kemis" >/dev/null
for k in bekasitimur evasari bhaktiwara karawang depok betang hertasning kelapagading makassar sukabumi tangerang semarang pgicikini ukrida pasarkemis; do head -30 work/chk_$k.txt; done
