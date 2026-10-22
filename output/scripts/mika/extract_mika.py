"""Alat 1 (pdfplumber): ekstrak semua baris tabel buku tarif MIKA ke JSON.
Usage: python3 extract_mika.py PDF OUT.json
Tiap baris: page, title (judul tabel di atas tabel), group (baris kelompok terakhir), kode, name, prices {header: nilai}."""
import sys, re, json
import pdfplumber

PDF, OUT = sys.argv[1:3]
ws_ = lambda s: re.sub(r'\s+', ' ', s or '').strip()
KODE = re.compile(r'^[A-Z]{4}\d{6}$')
NUM = re.compile(r'^(Rp\.?\s*)?\d{1,3}([.,]\d{3})+$|^\d{1,3}$|^-$')
SKIP_TITLE = re.compile(r'^(MITRA KELUARGA|TAHUN 20\d\d|RS MITRA|RUMAH SAKIT|\d+|# Internal|Internal|Hal\.? \d+)\b|^Keterangan\s*:?$'
                        r'|^PER \d*\s*[A-Z]+ 20\d\d$|^-\s*\d+\s*-$|^\(\d+\)$|^[A-Z]{3,4}[A-Z0-9]?\d{5,6}\b', re.I)
GENERIC = re.compile(r'^(TARIF MITRA KELUARGA|BUKU TARIF)\b', re.I)


def is_header(c):
    if sum(1 for x in c if x) < 2: return False   # baris satu sel = judul/kelompok, bukan header
    t = ' '.join(c).upper()
    if any(KODE.match(x) for x in c): return False
    if any(re.fullmatch(r'\d{1,3}([.,]\d{3})+', x) for x in c): return False
    return bool(re.search(r'\bKODE\b|\bSERVICE\b|\bKETERANGAN\b|\bNAMA\b|\bTINDAKAN\b|\bPELAYANAN\b|\bPEMERIKSAAN\b|\bLAYANAN\b', t)) and \
        bool(re.search(r'KELAS|\bIII\b|\bII\b|\bRJ\b|TARIF|EKSEKUTIF|EXECUTIVE|VIP|SUITE|RAWAT', t))


rows = []
with pdfplumber.open(PDF) as pdf:
    prev_hdr = None; prev_group = None; prev_title = None
    for pn, page in enumerate(pdf.pages, 1):
        # buang watermark (mis. 'CONTROLLED COPY' Kemayoran: huruf besar >30pt, miring)
        page = page.filter(lambda o: not (o.get('object_type') == 'char' and o.get('size', 0) > 30))
        words = page.extract_words(keep_blank_chars=False, use_text_flow=False)
        tables = page.find_tables(); last_title = None
        for ti, tb in enumerate(tables):
            data = tb.extract()
            top = tb.bbox[1]
            # tabel berbingkai bisa memuat judul di dalam kotak: batas bawah judul = baris header pertama
            for ri, rw in enumerate(data):
                if is_header([ws_(x) for x in rw]) and ri < len(tb.rows):
                    top = tb.rows[ri].bbox[1]; break
            # judul: baris teks di atas tabel (setelah tabel sebelumnya pada halaman yang sama)
            ptop = tables[ti - 1].bbox[3] if ti else 0
            lines = {}
            for w in words:
                if ptop - 1 <= w['top'] and w['top'] < top - 1 and w['bottom'] <= top + 6:
                    lines.setdefault(round(w['top']), []).append(w)
            tl = [ws_(' '.join(x['text'] for x in sorted(v, key=lambda w: w['x0']))) for k, v in sorted(lines.items())]
            tl = [t for t in tl if t and not SKIP_TITLE.match(t)]
            if not tl:
                # judul di dalam bingkai tabel: baris satu-sel sebelum header
                for rw in data:
                    if is_header([ws_(x) for x in rw]): break
                    cells = [x for x in rw if x and x.strip()]
                    if len(cells) == 1:
                        t0 = ws_(cells[0].split('\n')[0])
                        if t0 and not SKIP_TITLE.match(t0): tl = [t0]; break
            # judul = baris non-generik terdekat di atas tabel; judul generik 'TARIF MITRA KELUARGA X' hanya cadangan
            spec_t = [t for t in tl if not GENERIC.match(t)]
            tl = spec_t[-1:] or tl[:1]
            cont = not tl and ti == 0 and prev_title is not None   # halaman lanjutan tanpa judul: warisi judul tabel sebelumnya
            title = tl[0] if tl else (last_title if ti else (prev_title if cont else None))
            last_title = title
            hdr = None; last_kode = None; sub_ok = False
            # kelompok berlanjut dari tabel sebelumnya hanya jika judul tabelnya sama
            hi = next((i for i, rw in enumerate(data) if is_header([ws_(x) for x in rw])), None)
            # kelompok hanya berlanjut ke tabel lanjutan tanpa header sendiri dengan judul sama
            group = prev_group if ((hi is None or cont) and title and title == prev_title) else None
            for r in (data[hi:] if hi is not None else data):   # baris sebelum header = judul/sub-judul
                c = [ws_(x) for x in r]
                if not any(c): continue
                if is_header(c):
                    hdr = c; sub_ok = True; continue
                # sub-header (header dua tingkat): baris >=2 sel tanpa kode/angka langsung setelah header
                if hdr is not None and sub_ok and sum(1 for x in c if x) >= 2 and not any(KODE.match(x) for x in c) \
                        and not any(re.search(r'\d', x) for x in c) and len(c) == len(hdr) \
                        and re.search(r'KELAS|SUITE|VIP|EKSEKUTIF|EXECUTIVE|UTAMA|ICU|\bIII\b|\bII\b|\bRJ\b|RAWAT JALAN', ' '.join(c).upper()):
                    hdr = [b if b else a for a, b in zip(hdr, c)]; continue   # sub-header menimpa label rentang ('TARIF')
                sub_ok = False
                if hdr is None and prev_hdr is not None and len(prev_hdr) == len(c):
                    hdr = prev_hdr
                if hdr is None: continue
                ki = next((i for i, x in enumerate(c) if KODE.match(x)), None)
                # kolom nama: kolom header pertama non-KODE berisi teks
                kc = next((i for i, h in enumerate(hdr) if re.search(r'KODE|SERVICE', h.upper())), None)
                ni = None   # kolom nama: prioritas NAMA/DESKRIPSI, KETERANGAN paling akhir (bisa berisi kategori sel gabung)
                for pat in (r'NAMA|DESKRIPSI|DESCRIPTION', r'TINDAKAN|PELAYANAN|PEMERIKSAAN|LAYANAN|JENIS', r'KETERANGAN'):
                    ni = next((i for i, h in enumerate(hdr) if i != kc and re.search(pat, h.upper()) and not re.search(r'^KODE', h.upper())), None)
                    if ni is not None: break
                if ni is None: ni = (kc + 1) if kc is not None else 0
                pcols = [i for i in range(ni + 1, len(hdr))]
                vals = {hdr[i] or f'col{i}': (c[i] if i < len(c) else '') for i in pcols}
                name = c[ni] if ni < len(c) else ''
                kode = c[kc] if kc is not None and kc < len(c) else (c[ki] if ki is not None else '')
                if not any(v for v in vals.values()):
                    group = (name if KODE.match(kode or '') else ' '.join(x for x in c if x)) or name; last_kode = None; continue
                merged = False
                if not kode and last_kode and name:
                    kode = last_kode; merged = True   # sel kode digabung (rowspan) dengan baris di atasnya
                if KODE.match(kode or ''): last_kode = kode if not merged else last_kode
                rows.append(dict(page=pn, title=title, group=group, kode=kode, merged=merged, name=name, prices=vals,
                                 header=[hdr[i] for i in pcols], ncols=len(c)))
            if hdr is not None: prev_hdr = hdr
            prev_group, prev_title = group, title
json.dump(rows, open(OUT, 'w'), ensure_ascii=False, indent=0)
print(PDF, len(rows))
