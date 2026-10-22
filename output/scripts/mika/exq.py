"""Tampilkan baris Excel RS yang namanya cocok regex. Usage: python3 exq.py EXCEL.xlsx REGEX [REGEX ...]"""
import sys, re, openpyxl, collections
ws = openpyxl.load_workbook(sys.argv[1], read_only=True).worksheets[0]
it = ws.iter_rows(values_only=True)
h = next(it)
ix = {k: h.index(k) for k in ('kategori_harga', 'nama_layanan', 'kelas_kamar', 'tarif')}
rows = [r for r in it if r[ix['nama_layanan']] is not None]
for q in sys.argv[2:]:
    rx = re.compile(q, re.I)
    g = collections.OrderedDict()
    for r in rows:
        n = re.sub(r'\s+', ' ', str(r[ix['nama_layanan']])).strip()
        if rx.search(n):
            g.setdefault((n, r[ix['kategori_harga']]), []).append(f"{r[ix['kelas_kamar']]}={r[ix['tarif']]}")
    print(f'## {q}')
    for (n, k), v in g.items(): print(f'  "{n}" [{k}] ' + ' | '.join(v))
