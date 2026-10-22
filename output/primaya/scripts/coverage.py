"""Cakupan ekstraksi: per halaman, jumlah angka uang di teks PDF (PyMuPDF) vs nilai tarif yang terekstrak.
Usage: python3 coverage.py PDF JSON [detail]"""
import sys, re, json, collections, pymupdf
d = pymupdf.open(sys.argv[1]); rows = json.load(open(sys.argv[2]))
MONEY = re.compile(r'^\d{1,3}([.,]\d{3})+([.,]00)?$')
got = collections.Counter()
for r in rows:
    got[r['page']] += sum(1 for v in r['prices'].values() if MONEY.match(v or ''))
tot = 0; miss = []
for i, p in enumerate(d, 1):
    n = sum(1 for w in p.get_text('words') if MONEY.match(w[4]))
    tot += n
    if n >= 5 and got[i] < 0.8 * n: miss.append((i, n, got[i]))
print(sys.argv[1], 'uang di teks', tot, 'terekstrak', sum(got.values()), 'halaman kurang:', len(miss), miss[:25] if len(sys.argv) > 3 else miss[:8])
