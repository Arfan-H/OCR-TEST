"""Cek klaim manual ('tidak ada X', daftar item tidak diambil) terhadap item PDF hasil ekstraksi.
Usage: python3 claims.py ITEMS.json REGEX [REGEX ...]  -> semua baris yang namanya cocok (hlm, kode, nama, tarif)"""
import sys, json, re
rows = json.load(open(sys.argv[1]))
for q in sys.argv[2:]:
    print('##', q)
    for x in rows:
        if re.search(q, x['name'] or '', re.I):
            print(f"   p{x['page']} {x['kode']} {x['name']!r} [{x['group']}] " + '/'.join(v or '_' for v in x['prices'].values())[:90])
