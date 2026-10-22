"""debug: tampilkan tabel grid_tables per halaman. Usage: dbg_grid.py PDF PAGE [maxrows]"""
import sys, re
src = open(__file__.replace('dbg_grid.py', 'checker_mika.py')).read()
src = src[src.index('class _Row'):src.index('# ---------- PDF (PyMuPDF) ----------')]
import pymupdf
exec(src)
d = pymupdf.open(sys.argv[1]); p = d[int(sys.argv[2]) - 1]; mx = int(sys.argv[3]) if len(sys.argv) > 3 else 8
words = [w for w in p.get_text('words') if w[3] - w[1] < 25]
for t in grid_tables(p):
    print('TAB', len(t.rows), t.rows[0].bbox)
    for r in t.rows[:mx]:
        out = []
        for bb in r.cells:
            if bb is None: out.append(None); continue
            x0, y0, x1, y1 = bb
            out.append(' '.join(w[4] for w in words if x0 <= (w[0] + w[2]) / 2 <= x1 and y0 <= (w[1] + w[3]) / 2 <= y1))
        print(out)
