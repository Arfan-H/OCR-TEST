"""Cek visual: potong header tabel + baris setiap item yang dikutip di sheet, susun jadi lembar PNG.
Usage: python3 crop_mika.py PDF OUT.xlsx SHEET OUTDIR [per_sheet=7]"""
import sys, re, os
import pymupdf, openpyxl
from PIL import Image, ImageDraw

PDF, OUT, SHEET, OD = sys.argv[1:5]
PER = int(sys.argv[5]) if len(sys.argv) > 5 else 7
os.makedirs(OD, exist_ok=True)
ws = openpyxl.load_workbook(OUT)[SHEET]
AC = ws.max_column
CITE = re.compile(r"'([^']+)' \(kode ([A-Z0-9]{10})(?: sel gabung)?((?:, (?:kelompok|tabel|Rank|RANK|KETERANGAN|JENIS KAMAR|KELAS) '[^']+')*), hlm\. (\d+)")
cites = []; texts = []
for r in range(2, ws.max_row + 1):
    t = ws.cell(r, AC).value or ''
    if t in texts: continue          # alasan sama di 3 baris kelas -> ambil sekali per uraian
    texts.append(t); cites += CITE.findall(t)
doc = pymupdf.open(PDF); Z = 2.0
tiles = []
seen = {}
for name, kode, extra, pg in cites:
    rkm = re.search(r"(?:Rank|RANK|KETERANGAN|JENIS KAMAR|KELAS) '([^']+)'", extra)
    page = doc[int(pg) - 1]
    k = (kode, name, pg, extra); idx = seen.get(k, 0); seen[k] = idx + 1
    hits = [h for h in page.search_for(kode)]
    nz = re.sub(r'\s+', '', name)
    rows = []
    for h in hits:
        band = pymupdf.Rect(0, h.y0 - 1, page.rect.width, h.y1 + 1)
        ws = [w for w in page.get_text('words', clip=band) if w[0] > h.x1 - 1 and h.y0 <= (w[1] + w[3]) / 2 <= h.y1 and w[3] - w[1] < 25]
        txt = ''.join(w[4] for w in ws if not re.fullmatch(r'\d{1,3}([.,]\d{3})+|\d{4,}|-', w[4]))
        if txt.startswith('-') and not nz.startswith('-'): txt = txt[1:]   # tanda daftar '- '
        rest = txt[len(nz):] if txt.startswith(nz) else None
        if rest is None: continue
        if rkm:
            rz = re.sub(r'\s+', '', rkm.group(1))
            if rest.startswith(rz) and not re.match(r'[A-Za-z(]', rest[len(rz):]): rows.append(h)
        elif rest == '' or not re.match(r'[A-Za-z(]', rest): rows.append(h)
    # sel kode gabung: cari baris bernama sama di bawah kode
    if not rows:
        for b in page.search_for(name):
            rows.append(pymupdf.Rect(b.x0, b.y0, b.x1, b.y1))
    if not rows: print('TIDAK KETEMU', kode, name, pg); continue
    h = rows[min(idx, len(rows) - 1)]
    tab = None
    for t in page.find_tables().tables:
        if t.bbox[1] - 2 <= h.y0 <= t.bbox[3] + 2: tab = t; break
    hb = None
    if tab is not None:
        for rw in tab.rows:
            bb = pymupdf.Rect(rw.bbox)
            tx = page.get_text('text', clip=bb).upper()
            if len(tx.split()) >= 2 and re.search(r'\bKODE\b|\bSERVICE\b|^\s*NO\.', tx): hb = bb; break
    x0 = tab.bbox[0] - 2 if tab else 0; x1 = tab.bbox[2] + 2 if tab else page.rect.width
    parts = []
    if hb is not None and hb.height > 2:
        parts.append(page.get_pixmap(matrix=pymupdf.Matrix(Z, Z), clip=pymupdf.Rect(x0, hb.y0 - 1, x1, hb.y1 + 1)))
    parts.append(page.get_pixmap(matrix=pymupdf.Matrix(Z, Z), clip=pymupdf.Rect(x0, h.y0 - 3, x1, h.y1 + 3)))
    ims = [Image.frombytes('RGB', (p.width, p.height), p.samples) for p in parts]
    W = max(i.width for i in ims); H = sum(i.height for i in ims) + 18
    tile = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(tile)
    d.text((2, 2), f'hlm. {pg} | {kode} | {name}', fill=(200, 0, 0))
    y = 16
    for i in ims: tile.paste(i, (0, y)); y += i.height
    tiles.append(tile)
n = 0
for k in range(0, len(tiles), PER):
    grp = tiles[k:k + PER]
    W = max(t.width for t in grp); H = sum(t.height + 8 for t in grp)
    sh = Image.new('RGB', (W, H), (235, 235, 235)); y = 0
    for t in grp: sh.paste(t, (0, y)); y += t.height + 8
    if W > 1600: sh = sh.resize((1600, int(H * 1600 / W)))
    sh.save(os.path.join(OD, f'{SHEET.replace(" ", "_")}_{n}.png')); n += 1
print(len(tiles), 'tile', n, 'lembar')
