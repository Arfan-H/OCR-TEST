"""Judul tabel/kelompok/header untuk item yang dipakai spec. Usage: used_ctx.py key [key ...]"""
import json, importlib, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for k in sys.argv[1:]:
    S = importlib.import_module('spec_' + k); rows = json.load(open(f'{ROOT}/work/json/{k}.json'))
    for ura, u in S.U.items():
        uses = u.get('use') or [x for v in (u.get('rows') or {}).values() for x in v]
        for e in uses:
            m = [r for r in rows if r['kode'] == e[0] and r['name'] == e[1] and r['page'] == e[2]]
            if not m: print(k, 'TIDAK ADA', e); continue
            r = m[0]
            print(k, r['page'], r['kode'], r['name'][:28], '| T:', r['title'], '| G:', r['group'], '|', r.get('via'), '| H:', ' ; '.join(r['header']))
