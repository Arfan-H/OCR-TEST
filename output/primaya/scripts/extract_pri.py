"""Alat 1 (pdfplumber): ekstrak semua baris tabel buku tarif PRIMAYA ke JSON (turunan extract_mika.py).
Usage: python3 extract_pri.py PDF OUT.json
Beda dengan MIKA: kode layanan tertulis di depan nama dalam satu sel ('DR004 - Konsultasi Dokter UGD') dan dipisah;
item tanpa kode (mis. tabel kamar) diberi kode ''; tidak ada pewarisan kode sel gabung; judul tabel hanya dari teks
di atas tabel pada halaman yang sama (banyak buku Primaya menaruh judul sebagai gambar -> judul None, tidak ditebak).
Tiap baris: page, title, group, kode, name, prices {header: nilai}, header, ncols, rowi (urutan baris data di halaman)."""
import sys, re, json
import pdfplumber
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from linegrid import read_page

PDF, OUT = sys.argv[1:3]
ws_ = lambda s: re.sub(r'\s+', ' ', s or '').strip()
KODE = re.compile(r'^[A-Z]{1,5}\d{2,8}[A-Z]?$')
KNAME = re.compile(r'^([A-Z]{1,5}\d{2,8}[A-Z]?)\s*[-–]\s*(\S.*)$')
MONEY = re.compile(r'^(Rp\.?\s*)?\d{1,3}([.,]\d{3})+([.,]00)?$')
HEAD = re.compile(r'^([A-Z]{1,2}\d*|[IVX]+)\.\s')
SKIP_TITLE = re.compile(r'^(RUMAH SAKIT|RS |PRIMAYA|TARIF \d|TAHUN 20\d\d|20\d\d$|\d+$|No\. Dokumen|Tanggal|Revisi|Halaman|Hal\.? \d+|BUKU TARIF|Buku Tarif)'
                        r'|^PER \d*\s*[A-Z]+ 20\d\d$|^TARIF\s*\(Rp\.?\)$|^(NO\.?\s+)?(KETERANGAN|DESKRIPSI|DESCRIPTION)?\s*(TARIF|TAIRF)?$|^\d{1,2}\s+[A-Za-z]+\s+20\d\d(\s+\d+)?$|^TRF/[A-Z]+/\d+|^-\s*\d+\s*-$|^\(\d+\)$|^Keterangan\s*:?$|Primaya Hospital|PRIMAYA HOSPITAL|Rumah Sakit', re.I)


def fixnum(x):
    """'3 57.000' (huruf angka terpisah oleh pdfplumber) -> '357.000'; sel berisi beberapa angka penuh dibiarkan"""
    if re.fullmatch(r'[\d\s.,]+', x) and re.search(r'\d', x) and ' ' in x:
        parts = x.split()
        if all(not re.search(r'[.,]', p) for p in parts[:-1]):
            y = ''.join(parts)
            if MONEY.match(y): return y
    return x


def is_header(c):
    if sum(1 for x in c if x) < 2: return False
    t = ' '.join(c).upper()
    if any(KNAME.match(x) for x in c): return False
    if any(MONEY.match(x) for x in c): return False
    return bool(re.search(r'\bKETERANGAN\b|\bNAMA\b|\bTINDAKAN\b|\bPELAYANAN\b|\bPEMERIKSAAN\b|\bLAYANAN\b|\bJENIS\b|\bURAIAN\b|\bDESCRIPTION\b|\bDESKRIPSI\b', t)) and \
        bool(re.search(r'KELAS|\bIII\b|\bII\b|\bRJ\b|TARIF|DELUXE|SUITE|RAWAT|VIP|HARGA|\b20\d\d\b|\bI\b', t))


def words_from_chars(page):
    """kata dari karakter (dipakai bila extract_words memecah teks per huruf, mis. matriks teks sedikit miring)"""
    ch = sorted((c for c in page.chars if c['text'].strip() or c['text'] == ' '), key=lambda c: (round(c['top']), c['x0']))
    out = []; cur = None
    for c in ch:
        if c['text'] == ' ':
            cur = None; continue
        if cur and abs(c['top'] - cur['top']) < 1.5 and 0 - 0.5 <= c['x0'] - cur['x1'] < 1.2:
            cur['text'] += c['text']; cur['x1'] = c['x1']; cur['bottom'] = max(cur['bottom'], c['bottom'])
        else:
            cur = dict(text=c['text'], x0=c['x0'], x1=c['x1'], top=c['top'], bottom=c['bottom']); out.append(cur)
    return out


rows = []; AGREE = []
with pdfplumber.open(PDF) as pdf:
    prev_hdr = None; lg_prev = None
    for pn, page in enumerate(pdf.pages, 1):
        words = page.extract_words(keep_blank_chars=False, use_text_flow=False)
        if words and sum(1 for w in words if len(w['text']) == 1) > 0.5 * len(words):
            words = words_from_chars(page)
        # cadangan berbasis posisi kata (linegrid) untuk halaman yang tabelnya tidak terbaca utuh
        lg_items, lg_prev = read_page([(w['x0'], w['top'], w['x1'], w['bottom'], w['text']) for w in words], lg_prev)
        n_money = sum(1 for w in words if MONEY.match(w['text']))
        start = len(rows)
        tables = page.find_tables(); rowi = 0
        for ti, tb in enumerate(tables):
            data = tb.extract()
            top = tb.bbox[1]
            ptop = tables[ti - 1].bbox[3] if ti else 0
            lines = {}
            for w in words:
                if ptop - 1 <= w['top'] and w['top'] < top - 1 and w['bottom'] <= top + 6:
                    lines.setdefault(round(w['top']), []).append(w)
            tl = [ws_(' '.join(x['text'] for x in sorted(v, key=lambda w: w['x0']))) for k, v in sorted(lines.items())]
            tl = [t for t in tl if t and not SKIP_TITLE.search(t) and re.search(r'[A-Za-z]{3}', t)]
            title = tl[-1] if tl else None
            hdr = None; sub_ok = False; group = None; prev_grp = False
            hi = next((i for i, rw in enumerate(data) if is_header([ws_(x) for x in rw])), None)
            if title is None and hi:   # judul tabel sebagai baris pertama tabel (di atas baris header)
                ok = lambda t: t and not SKIP_TITLE.search(t) and re.search(r'[A-Za-z]{3}', t)
                pre = [[ws_(l) for x in rw if x for l in x.split('\n') if ok(ws_(l))] for rw in data[:hi]
                       if not is_header([ws_(x) for x in rw])]   # sel bisa 2 baris: judul + tanggal
                pre = [ls for ls in pre if ls]
                title = pre[-1][0] if pre else None
            for r in (data[hi:] if hi is not None else data):
                c = [fixnum(ws_(x)) for x in r]
                if not any(c): continue
                if is_header(c):
                    hdr = c; sub_ok = True; continue
                if hdr is not None and sub_ok and sum(1 for x in c if x) >= 2 and not any(re.search(r'\d{3}', x) for x in c) and len(c) == len(hdr) \
                        and re.search(r'KELAS|SUITE|VIP|DELUXE|ICU|\bIII\b|\bII\b|\bRJ\b|RAWAT JALAN', ' '.join(c).upper()):
                    hdr = [b if b else a for a, b in zip(hdr, c)]; continue
                sub_ok = False
                if hdr is None and prev_hdr is not None and len(prev_hdr) == len(c):
                    hdr = prev_hdr
                if hdr is None: continue
                ni = None
                for pat in (r'NAMA|DESKRIPSI|DESCRIPTION|URAIAN', r'TINDAKAN|PELAYANAN|PEMERIKSAAN|LAYANAN|JENIS', r'KETERANGAN'):
                    ni = next((i for i, h in enumerate(hdr) if re.search(pat, h.upper())), None)
                    if ni is not None: break
                if ni is None: continue
                pcols = [i for i in range(ni + 1, len(hdr))]
                vals = {hdr[i] or f'col{i}': (c[i] if i < len(c) else '') for i in pcols}
                cell = c[ni] if ni < len(c) else ''
                # nama yang meluber ke sel tarif pertama (teks PDF utuh, tampilan sel memotong): 'Peny' + 'ul i t 253,000'
                if pcols and pcols[0] < len(c):
                    mo = re.match(r'^([A-Za-z][A-Za-z ]*?)\s+(\d{1,3}(?:[.,]\d{3})+(?:[.,]00)?)$', c[pcols[0]])
                    if mo and cell:
                        cell += mo.group(1).replace(' ', ''); vals[hdr[pcols[0]] or f'col{pcols[0]}'] = mo.group(2)
                m = KNAME.match(cell)
                kode, name = (m.group(1), m.group(2)) if m else ('', cell)
                if not m and not any(MONEY.match(v or '') or re.fullmatch(r'[-–]', v or '') for v in vals.values()):
                    # baris judul kelompok (tanpa tarif dan tanpa kode); teks bisa berada di kolom lain (sel gabung)
                    if any(re.fullmatch(r'(RJ|III|II|I|DELUXE|SUITE|P\.? ?SUITE|VIP|KELAS.*|TARIF.*|\(Rp\.?\)|To Be)(\s*,.*)?', v or '', re.I)
                           for v in vals.values()):
                        continue   # sisa baris header (label kelas di kolom tarif), bukan judul kelompok
                    lines = [ws_(t) for x in r if x for t in x.split('\n')]
                    lines = [t for t in lines if t and not re.fullmatch(r'\d+\.?|[IVX]+\.?', t)]
                    if lines and re.match(r'^(NO|No\.?)$', lines[0]): lines = []   # sisa header ('NO', 'To Be')
                    if lines and re.match(r'^[A-Z]{1,5}\d{2,8}[A-Z]?\b', lines[0]): lines = []   # baris item yang terpecah, bukan judul kelompok
                    if lines:
                        hix = [i for i, t in enumerate(lines) if HEAD.match(t)]
                        if hix and hix[-1] > 0: lines = lines[hix[-1]:]   # 'A. HEMATOLOGI - KOAGULASI' + 'A1. HEMATOLOGI' -> sub kelompok
                        txt = re.sub(r'(\s+\d+(?:[.,]\d+)?\s*%)+$', '', ' '.join(lines))   # persen di sel gabung judul
                        # judul kelompok bernomor yang terlipat ke baris berikut ('B3. KIMIA - METABOLISME' + 'KARBOHIDRAT')
                        group = (group + ' ' + txt) if (prev_grp and group and HEAD.match(group) and not HEAD.match(txt) and len(txt.split()) <= 3) else txt
                        prev_grp = True
                    continue
                prev_grp = False
                rowi += 1
                rows.append(dict(page=pn, title=title, group=group, kode=kode, merged=False, name=name, prices=vals,
                                 header=[hdr[i] for i in pcols], ncols=len(c), rowi=rowi, cell=cell))
            if hdr is not None: prev_hdr = hdr
        got = sum(1 for r in rows[start:] for v in r['prices'].values() if MONEY.match(v or ''))
        lg_got = sum(1 for it in lg_items for v in it['prices'].values() if MONEY.match(v or ''))
        # tabel pdfplumber dianggap rusak bila ada tarif di kolom tanpa label header atau baris bertarif tanpa nama
        bad = sum(1 for r in rows[start:] for h, v in r['prices'].items() if MONEY.match(v or '') and (not h or re.fullmatch(r'col\d+', h))) \
            + sum(1 for r in rows[start:] if not r['name'] and any(MONEY.match(v or '') for v in r['prices'].values()))
        # kecocokan dua metode (untuk evaluasi): item sama (kode, nama) -> tarif per label sama?
        W = lambda t: re.sub(r'\s+', '', t or '')
        lgm = {(it['kode'], W(it['name'])): {W(k): v for k, v in it['prices'].items() if v} for it in lg_items}
        same = diff = 0; dl = []
        for r in rows[start:]:
            k = (r['kode'], W(r['name']))
            if k in lgm:
                tp = {W(h): v for h, v in r['prices'].items() if v}
                if tp == lgm[k]: same += 1
                else: diff += 1; dl.append(r['kode'] or r['name'])
        AGREE.append((pn, got, lg_got, bad, n_money, same, diff, dl[:5]))
        if n_money >= 3 and lg_got >= 0.9 * n_money and (got < 0.9 * n_money or bad) or (n_money >= 3 and got < 0.9 * n_money and lg_got > got):
            del rows[start:]
            top = lg_prev.get('hdr_top') if lg_prev else None
            tl = []
            if top is not None:
                lines = {}
                for w in words:
                    if w['bottom'] <= top + 1: lines.setdefault(round(w['top']), []).append(w)
                tl = [ws_(' '.join(x['text'] for x in sorted(v, key=lambda w: w['x0']))) for k, v in sorted(lines.items())]
                tl = [t for t in tl if t and not SKIP_TITLE.search(t) and re.search(r'[A-Za-z]{3}', t)]
            title = tl[-1] if tl else None
            for i, it in enumerate(lg_items, 1):
                # judul per blok tabel (satu halaman bisa memuat beberapa bagian, mis. 'B. ROOM RATE' dan 'C. CONSULTATION')
                st = [t for t in it.get('tlines') or [] if t and not SKIP_TITLE.search(t) and re.search(r'[A-Za-z]{3}', t)]
                rows.append(dict(page=pn, title=st[-1] if st else title, group=it['group'], kode=it['kode'], merged=False, name=it['name'], prices=it['prices'],
                                 header=it['labels'], ncols=len(it['labels']) + 1, rowi=i, cell=it['cell'], via='linegrid'))
# tabel yang berlanjut ke halaman berikut (header sama, halaman berurutan) tanpa judul/kelompok tercetak ulang:
# judul dan kelompok dibawa dari halaman sebelumnya; halaman tempat judul/kelompok tercetak disimpan (title_pg/group_pg)
for key in ('title', 'group'):
    pr = None
    for r in rows:
        if r[key]: r.setdefault(key + '_pg', r['page']); pr = r
        elif pr and r['header'] == pr['header'] and r['page'] - pr['page'] <= 1 and \
                (key == 'title' or (r['title'] and r['title'] == pr['title'] and r.get('title_pg') == pr.get('title_pg'))):
            r[key], r[key + '_pg'] = pr[key], pr[key + '_pg']; pr = r   # kelompok hanya dibawa di dalam tabel berjudul yang sama
        else: pr = None
# label kolom berupa daftar (mis. 'I,ICU,ICCU, HCU, NICU' yang terlipat beberapa baris): spasi dibuang agar seragam
# label huruf kecil yang dipecah per huruf oleh pdfplumber ('I / I C U / H C U'): spasi di dalam tiap bagian '/' dibuang
NL = lambda h: re.sub(r'\s+', '', h) if ',' in h else \
    (' / '.join(re.sub(r'\s+', '', x) for x in h.split('/')) if '/' in h and len(re.findall(r'\b[A-Z]\b', h)) >= 3 else h)
for r in rows:
    r['prices'] = {NL(h): v for h, v in r['prices'].items()}; r['header'] = [NL(h) for h in r['header']]
json.dump(rows, open(OUT, 'w'), ensure_ascii=False, indent=0)
json.dump(AGREE, open(OUT.replace('.json', '.pages.json'), 'w'))
print(PDF, len(rows))
