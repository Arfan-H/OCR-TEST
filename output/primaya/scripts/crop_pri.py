"""Cek visual (PRIMAYA): potong header tabel terdekat + baris setiap item yang dikutip di sheet, dengan keterangan
kutipan (nama, kode, halaman, tarif per label) dari kolom alasan, disusun jadi lembar PNG untuk dibandingkan mata.
Usage: python3 crop_pri.py PDF OUT.xlsx SHEET OUTDIR [per_sheet=8]"""
import sys, re, os
import pymupdf, openpyxl
from PIL import Image, ImageDraw

PDF, OUT, SHEET, OD = sys.argv[1:5]
PER = int(sys.argv[5]) if len(sys.argv) > 5 else 8
os.makedirs(OD, exist_ok=True)
ws = openpyxl.load_workbook(OUT)[SHEET]
AC = ws.max_column
CITE = re.compile(r"'([^']+)' \((?:kode ([A-Z0-9]+)|tanpa kode)( sel gabung)?((?:, (?:kelompok|tabel) '[^']+')*), hlm\. (\d+), ([^)]*)\)")
cites = []; texts = []
for r in range(2, ws.max_row + 1):
    t = ws.cell(r, AC).value or ''
    if t in texts: continue
    texts.append(t)
    ura = ws.cell(r, 2).value
    cites += [(ura,) + m for m in CITE.findall(t.split(' | ')[0])]
doc = pymupdf.open(PDF); Z = 2.0
FL = pymupdf.TEXTFLAGS_WORDS & ~pymupdf.TEXT_MEDIABOX_CLIP
HDR = re.compile(r'^(III|KELAS|TARIF|Tarif|Tairf|2026|RJ)\b')
tiles = []; seen = {}
nz = lambda s: re.sub(r'\s+', '', s)
for ura, name, kode, mg, extra, pg, vals in cites:
    page = doc[int(pg) - 1]
    words = page.get_text('words', flags=FL)
    k = (kode, name, pg); idx = seen.get(k, 0); seen[k] = idx + 1
    rows = []
    if kode:
        for w in words:
            if w[4] != kode: continue
            line = [x for x in words if abs((x[1] + x[3]) / 2 - (w[1] + w[3]) / 2) < 3 and x[0] > w[2] - 1]
            line.sort(key=lambda x: x[0])
            txt = nz(' '.join(x[4] for x in line if not re.fullmatch(r'\d{1,3}([.,]\d{3})+([.,]00)?', x[4])))
            txt = re.sub(r'^[-–]', '', txt)
            if nz(name).startswith(txt) or txt.startswith(nz(name)): rows.append(pymupdf.Rect(w[:4]))
    else:
        for r0 in page.search_for(name):   # baris yang teks non-angkanya persis nama (bukan judul kelompok yang memuat nama)
            line = [x for x in words if abs((x[1] + x[3]) / 2 - (r0.y0 + r0.y1) / 2) < 3]
            txt = nz(' '.join(x[4] for x in sorted(line, key=lambda x: x[0]) if not re.fullmatch(r'\d{1,3}([.,]\d{3})+([.,]00)?|\d{1,3}\.?|-', x[4])))
            if txt == nz(name): rows.append(r0)
    if not rows: print('TIDAK KETEMU', kode, name, pg); continue
    h = rows[min(idx, len(rows) - 1)]
    # header terdekat di atas baris: kata kelas/tarif
    lines = {}
    for w in words:
        if w[3] <= h.y0 + 1: lines.setdefault(round((w[1] + w[3]) / 4), []).append(w)
    HT = {'III', 'II', 'I', 'RJ', 'DELUXE', 'DELIXE', 'SUITE', 'TARIF', 'Tarif', 'Tairf', '2026', 'KELAS', 'VIP', 'ODC', 'III,', 'I,'}
    hl = [ln for ln in lines.values() if sum(w[4] in HT for w in ln) >= 2 or (len(ln) <= 3 and any(w[4] in ('TARIF', 'Tarif', 'Tairf', '2026') for w in ln))]
    hy = max((max(hl, key=lambda ln: max(w[3] for w in ln))), key=lambda w: w[3]) if hl else None
    rw = [w for w in words if h.y0 - 12 <= w[1] <= h.y1 + 12]
    x0 = max(0, min([w[0] for w in rw] + [h.x0]) - 30); x1 = min(page.rect.width, max(w[2] for w in rw) + 6)
    parts = []
    if hy is not None and h.y0 - hy[3] > 2:
        parts.append(page.get_pixmap(matrix=pymupdf.Matrix(Z, Z), clip=pymupdf.Rect(x0, hy[1] - 26, x1, hy[3] + 2)))
    parts.append(page.get_pixmap(matrix=pymupdf.Matrix(Z, Z), clip=pymupdf.Rect(x0, h.y0 - 12, x1, h.y1 + 14)))
    ims = [Image.frombytes('RGB', (p.width, p.height), p.samples) for p in parts]
    cap = f"{ura} | {kode or 'tanpa kode'} '{name}' hlm.{pg} | {vals}"
    W = max(max(i.width for i in ims), 900); H = sum(i.height for i in ims) + 22
    tile = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(tile)
    d.text((4, 4), cap[:170], fill=(200, 0, 0))
    y = 22
    for i in ims: tile.paste(i, (0, y)); y += i.height
    tiles.append(tile)
# judul tabel/kelompok yang tercetak di halaman sebelumnya: potongan judul di hlm. N + bagian atas tiap halaman sampai hlm. M
CAR = re.compile(r"(judul tabel|kelompok) '([^']+)' tercetak di hlm\. (\d+) \(tabel berlanjut ke hlm\. (\d+)\)")
done = set()
for t in texts:
    for kind, ttl, a, b in CAR.findall(t):
        if (ttl, a, b) in done: continue
        done.add((ttl, a, b)); a, b = int(a), int(b)
        ims = []
        pa = doc[a - 1]; hit = pa.search_for(ttl)
        if hit:
            r0 = hit[-1]; ims.append(pa.get_pixmap(matrix=pymupdf.Matrix(1.2, 1.2), clip=pymupdf.Rect(0, r0.y0 - 8, pa.rect.width, r0.y1 + 70)))
        for pn in range(a + 1, b + 1):
            pg = doc[pn - 1]; ws_ = pg.get_text('words', flags=FL)
            codes = [w for w in ws_ if re.fullmatch(r'[A-Z]{1,5}\d{2,8}[A-Z]?', w[4])]
            y1 = min(w[3] for w in codes) + 4 if codes else pg.rect.height * 0.3
            ims.append(pg.get_pixmap(matrix=pymupdf.Matrix(1.2, 1.2), clip=pymupdf.Rect(0, 0, pg.rect.width, y1)))
        ims = [Image.frombytes('RGB', (p.width, p.height), p.samples) for p in ims]
        W = max(max(i.width for i in ims), 900); H = sum(i.height + 4 for i in ims) + 22
        tile = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(tile)
        d.text((4, 4), f"CEK BERLANJUT: {kind} '{ttl}' hlm.{a} -> hlm.{b} (atas tiap halaman {a + 1}..{b})", fill=(0, 0, 200))
        y = 22
        for i in ims: tile.paste(i, (0, y)); y += i.height + 4
        tiles.append(tile)
for n in range(0, len(tiles), PER):
    grp = tiles[n:n + PER]
    W = max(t.width for t in grp); H = sum(t.height + 6 for t in grp)
    sheet = Image.new('RGB', (W, H), (230, 230, 230)); y = 0
    for t in grp: sheet.paste(t, (0, y)); y += t.height + 6
    sheet.save(os.path.join(OD, f'{SHEET.replace(" ", "_")}_{n // PER + 1}.png'))
print(SHEET, 'kutipan', len(cites), 'potongan', len(tiles))
