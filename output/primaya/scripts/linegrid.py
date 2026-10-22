"""Pembaca tabel tarif berbasis posisi kata (tanpa garis tabel), untuk buku tarif Primaya.
Masukan: daftar kata (x0, top, x1, bottom, text) satu halaman. Kolom tarif = kelompok tepi kanan angka (angka rata kanan);
label kolom = kata header (baris yang memuat kata kelas) di atas kolom; item = baris berkode 'XX999 - Nama' (nama boleh
terlipat ke baris berikutnya) atau baris berangka tanpa kode. Halaman lanjutan tanpa header memakai kolom halaman sebelumnya
bila posisi kolomnya sama."""
import re

MONEY = re.compile(r'^\d{1,3}([.,]\d{3})+([.,]00)?$')
KNAME = re.compile(r'^([A-Z]{1,5}\d{2,8}[A-Z]?)\s*[-–]\s*(.*)$')   # nama boleh kosong di baris kode (nama terlipat ke baris bawah)
HDRW = re.compile(r'^(KELAS|III|II|I|RJ|RAWAT|JALAN|DEL[UI]XE|SUITE|PRESIDENT|GRAND|SIGNATURE|P|VIP|ICU|TARIF|TAIRF|ODC|ISOLASI|HCU|NICU|PERINA|ICCU|PICU|IMC|KAMAR|KHUSUS|UTAMA|EKSEKUTIF|EXECUTIVE)\W*$', re.I)
HDRX = re.compile(r'^(No\.?|Keterangan|Description|Deskripsi|Nama|Tindakan|Pelayanan|Layanan|Jenis|Uraian|Pemeriksaan|\(Rp\.?\)|Rp\.?|&|/|-|\d{1,2})$', re.I)
CLASSW = re.compile(r'^(20\d\d|KELAS|III|II|RJ|DEL[UI]XE|SUITE|VIP|ODC|TARIF|TAIRF|HARGA)\b', re.I)
ws_ = lambda s: re.sub(r'\s+', ' ', s or '').strip()


def lines_of(words, tol=2.5):
    ws = sorted(words, key=lambda w: ((w[1] + w[3]) / 2, w[0]))
    out = []
    for w in ws:
        yc = (w[1] + w[3]) / 2
        if out and abs(out[-1]['yc'] - yc) <= tol:
            out[-1]['w'].append(w); out[-1]['yc'] = (out[-1]['yc'] * (len(out[-1]['w']) - 1) + yc) / len(out[-1]['w'])
        else:
            out.append(dict(yc=yc, w=[w]))
    for l in out:
        l['w'].sort(key=lambda w: w[0]); l['top'] = min(w[1] for w in l['w']); l['bot'] = max(w[3] for w in l['w'])
    return out


def columns(lines):
    """tepi kanan angka uang -> pusat kolom (rata kanan)"""
    xs = sorted(w[2] for l in lines for w in l['w'] if MONEY.match(w[4]))
    cl = []
    for x in xs:
        if cl and x - cl[-1][-1] <= 6: cl[-1].append(x)
        else: cl.append([x])
    return [sum(c) / len(c) for c in cl if len(c) >= 2]


def fix_words(words):
    """gabung pecahan angka uang yang terpisah oleh jarak huruf: '3' + '57.000' -> '357.000', '1' + ',048,000' -> '1,048,000'"""
    ws = sorted(words, key=lambda w: (round((w[1] + w[3]) / 2), w[0])); out = []
    for w in ws:
        if out:
            p = out[-1]
            same = abs((p[1] + p[3]) / 2 - (w[1] + w[3]) / 2) < 2.5 and -1.5 <= w[0] - p[2] <= 4
            j = p[4] + w[4]
            if same and re.fullmatch(r'\d{1,3}', p[4]) and re.match(r'^[\d.,]', w[4]) and MONEY.match(j) and not MONEY.match(p[4]):
                out[-1] = (p[0], min(p[1], w[1]), w[2], max(p[3], w[3]), j); continue
            if same and re.fullmatch(r'\d{1,3}([.,]\d{1,3})*', p[4]) and re.fullmatch(r'\d{1,3}([.,]\d{3})*|[.,]\d{3}([.,]\d{3})*', w[4]) \
                    and MONEY.match(j) and not (MONEY.match(p[4]) and MONEY.match(w[4])):
                out[-1] = (p[0], min(p[1], w[1]), w[2], max(p[3], w[3]), j); continue
        out.append(tuple(w[:5]))
    return out


def _segment(L, prev, title):
    """satu blok tabel (header + baris data) -> (items, info)"""
    cols = columns(L)
    if not cols: return [], prev
    lefts = []
    for j, x in enumerate(cols):
        mx = min((w[0] for l in L for w in l['w'] if MONEY.match(w[4]) and abs(w[2] - x) <= 6), default=x - 40)
        lefts.append(mx - 4 if j == 0 else max(cols[j - 1] + 2, mx - 30))
    span = lambda j: (lefts[j], cols[j] + 4)
    def colof(w, hdr=False):
        xc = (w[0] + w[2]) / 2
        for j in range(len(cols)):
            a, b = span(j)
            if hdr and len(cols) == 1: a -= 60    # tabel satu kolom tarif: label boleh di tengah kolom lebar (angka rata kanan)
            if hdr and j > 0: a = min(a, cols[j - 1] + 4)   # label header di tengah kolom lebar: mulai dari tepi kanan kolom sebelumnya
            if a <= xc <= b or (MONEY.match(w[4]) and abs(w[2] - cols[j]) <= 6): return j
        return None
    first_price = next((i for i, l in enumerate(L) if any(MONEY.match(w[4]) for w in l['w'])), None)
    if first_price is None: return [], prev
    # header: baris di atas baris tarif pertama yang memuat kata kelas, + baris tetangga dekat (label multi-baris)
    hi = [i for i in range(first_price) if any(CLASSW.match(w[4]) for w in L[i]['w'] if colof(w, True) is not None)]
    labels = None
    if hi:
        a = b = hi[-1]   # baris header terdekat di atas data; baris atasnya ikut bila rapat dan hanya berisi kata header
        hw = lambda t: all(not p or HDRW.match(p) or re.fullmatch(r'[A-Z]{1,4}', p) for p in re.split(r'[,/&\s]+', t))   # pecahan kata header ('NIC'+'U')
        # baris rapat di atas: ikut bila kata di kolom tarif hanya kata header; baris yang hanya berisi teks kolom nama
        # (mis. judul kolom 'SEWA ALAT' di tengah sel header bertingkat) dilewati bila baris di atasnya masih label kolom
        k = a
        while k - 1 >= 0 and L[k]['top'] - L[k - 1]['bot'] < 4 and all(hw(w[4]) for w in L[k - 1]['w'] if colof(w, True) is not None):
            k -= 1
            if any(colof(w, True) is not None for w in L[k]['w']): a = k
        while b + 1 < first_price and L[b + 1]['top'] - L[b]['bot'] < 4 and all(colof(w, True) is not None and hw(w[4]) for w in L[b + 1]['w']): b += 1
        lab = [[] for _ in cols]
        for l in L[a:b + 1]:
            for w in l['w']:
                j = colof(w, True)
                if j is not None: lab[j].append(w)
        # kata 'TARIF (Rp)' di atas beberapa kolom (judul rentang) dibuang bila kolom punya label lain
        drop = lambda c: [w for w in c if not re.fullmatch(r'TARIF|\(Rp\)|Rp\.?', w[4], re.I)] or c
        lab = [drop(c) if len(cols) > 1 else c for c in lab]
        labels = [ws_(' '.join(w[4] for w in sorted(c, key=lambda w: (round(w[1] / 3), w[0])))) for c in lab]
        if not all(labels): labels = None
        hdr_end = L[b]['bot']; hdr_top = L[a]['top']
    else:
        hdr_end = -1; hdr_top = None
    if labels is None:
        if prev and len(prev['cols']) == len(cols) and all(abs(a - b) <= 8 for a, b in zip(prev['cols'], cols)):
            labels = prev['labels']
        else:
            return [], prev
    info = dict(cols=cols, labels=labels, hdr_top=hdr_top, title=title)
    items = []; cur = None; group = None; gbot = None
    # kolom nomor urut: angka murni di kiri posisi kode layanan (bisa sejajar baris lipatan nama)
    kx = [w[0] for l in L for w in l['w'] if re.fullmatch(r'[A-Z]{1,5}\d{2,8}[A-Z]?', w[4])]
    code_x0 = min(kx) if len(kx) >= 2 else None
    for l in L:
        if l['top'] <= hdr_end: continue
        name_w = [w for w in l['w'] if w[2] <= lefts[0] + 2 and not MONEY.match(w[4])
                  and not (code_x0 is not None and w[2] < code_x0 - 1 and re.fullmatch(r'\d{1,4}\.?', w[4]))]
        price_w = [w for w in l['w'] if colof(w) is not None and (MONEY.match(w[4]) or w[4] in ('-', '–'))]
        if not price_w and name_w:   # baris tanpa tarif (judul kelompok bisa melebar ke area kolom tarif)
            name_w = [w for w in l['w'] if not MONEY.match(w[4])
                      and not (code_x0 is not None and w[2] < code_x0 - 1 and re.fullmatch(r'\d{1,4}\.?', w[4]))]
        if not name_w and not price_w: continue
        txt = ws_(' '.join(w[4] for w in name_w))
        if code_x0 is None:   # tanpa kolom kode: nomor urut di awal baris
            txt = re.sub(r'^\d{1,4}\.?\s+(?=\S)', '', txt) if re.match(r'^\d{1,4}\.?\s+[A-Za-z]', txt) else txt
            if re.fullmatch(r'\d{1,4}\.?', txt): txt = ''
        m = KNAME.match(txt)
        if not (txt and not price_w): gbot = None
        if m or (price_w and not txt and cur is None):
            cur = dict(kode=m.group(1) if m else '', name=m.group(2) if m else txt, prices={}, group=group, yc=l['yc'], cell=txt, nl=1, bot=l['bot'])
            items.append(cur)
        elif txt and not price_w:
            if cur is not None and not cur['prices'] and cur['nl'] < 4:
                cur['name'] += ' ' + txt; cur['cell'] += ' ' + txt; cur['nl'] += 1      # nama terlipat, tarif di baris bawah
            elif cur is not None and cur['prices'] and l['top'] - cur['bot'] < 3 and not re.match(r'^[IVX]+\.|^[A-Z]\d*\.\s|^\*', txt) \
                    and (not txt.isupper() or txt.startswith('(') or cur['name'].count('(') > cur['name'].count(')') or re.search(r'[/,&+\-]$', cur['name'])):
                cur['name'] += ' ' + txt; cur['cell'] += ' ' + txt; cur['nl'] += 1      # lanjutan nama di bawah baris tarif
            elif txt.startswith('*') or re.match(r'^[A-Z]{1,5}\d{2,8}[A-Z]?\b', txt):
                cur = None   # catatan kaki ('*tarif dapat berubah ...') / potongan baris item berkode -> bukan judul kelompok
            else:
                # judul kelompok bernomor yang terlipat ke baris berikut ('A. Pemeriksaan Radiologi X-Ray' + 'Konvensional Tanpa Kontras')
                if gbot is not None and l['top'] - gbot < 3 and group and re.match(r'^([A-Z]{1,2}\d*|[IVX]+)\.\s', group) \
                        and not re.match(r'^([A-Z]{1,2}\d*|[IVX]+)\.\s', txt):
                    group += ' ' + txt
                else:
                    group = txt
                cur = None; gbot = l['bot']
                continue
            if cur is not None: cur['bot'] = l['bot']
            continue
        elif txt and price_w and not m:
            if cur is not None and not cur['prices']:
                cur['name'] += ' ' + txt; cur['cell'] += ' ' + txt; cur['nl'] += 1
            else:
                cur = dict(kode='', name=txt, prices={}, group=group, yc=l['yc'], cell=txt, nl=1, bot=l['bot']); items.append(cur)
        if cur is None or not price_w: continue   # baris hanya nomor urut / sisa teks
        for w in price_w:
            j = colof(w)
            if labels[j] in cur['prices'] and cur['prices'][labels[j]]: continue
            cur['prices'][labels[j]] = w[4]
        cur['bot'] = l['bot']
    out = []
    for it in items:
        if not any(MONEY.match(v or '') for v in it['prices'].values()): continue
        it['prices'] = {lb: it['prices'].get(lb, '') for lb in labels}
        it['labels'] = labels; it['title'] = title; it['name'] = ws_(it['name']); it['cell'] = ws_(it['cell'])
        out.append(it)
    return out, info


def read_page(words, prev=None):
    """-> (items, info). Halaman dipecah per blok header (satu halaman bisa memuat beberapa tabel dengan kolom berbeda).
    items: dict(kode, name, prices{label: teks}, labels, group, title, yc, cell)"""
    L = lines_of(fix_words(words))
    isM = lambda l: any(MONEY.match(w[4]) for w in l['w'])
    # calon header: memuat kata kelas dan sebagian besar katanya kata header (baris nama 'Luka Bakar Derajat II' bukan header)
    HT = lambda t: bool(CLASSW.match(t) or HDRW.match(t) or HDRX.match(t))
    cand = [i for i, l in enumerate(L) if not isM(l) and any(CLASSW.match(w[4]) for w in l['w'])
            and not KNAME.match(ws_(' '.join(w[4] for w in l['w'])))
            and sum(HT(w[4]) for w in l['w']) > len(l['w']) / 2]
    # header = calon yang diikuti baris bertarif sebelum calon berikutnya; calon berurutan rapat = satu header multi-baris
    starts = []
    for i in cand:
        if starts and i - starts[-1][1] <= 1 and L[i]['top'] - L[starts[-1][1]]['bot'] < 4: starts[-1][1] = i; continue
        starts.append([i, i])
    hw = lambda t: all(not p or HDRW.match(p) or re.fullmatch(r'[A-Z]{1,4}', p) for p in re.split(r'[,/&\s]+', t))   # pecahan kata header ('NIC'+'U')
    for st in starts:   # baris label di atas (mis. 'PRESIDENT' di atas 'SUITE') ikut header
        while st[0] - 1 >= 0 and L[st[0]]['top'] - L[st[0] - 1]['bot'] < 4 and not isM(L[st[0] - 1]) \
                and all(hw(w[4]) for w in L[st[0] - 1]['w']): st[0] -= 1
    bounds = [s[0] for s in starts]
    segs = []; last = 0; carry = None
    for k, (a, b) in enumerate(starts):
        end = bounds[k + 1] if k + 1 < len(bounds) else len(L)
        if carry is not None: a = carry; carry = None
        if not any(isM(l) for l in L[b + 1:end]):
            # calon header tanpa baris tarif (mis. 'TARIF (Rp)' di atas label kelas bertingkat): bila baris-baris sampai calon
            # berikutnya rapat, ikut header berikutnya (label kolom yang terlipat ke atas tidak terpotong)
            if k + 1 < len(bounds) and all(L[i + 1]['top'] - L[i]['bot'] < 4 for i in range(b, end)): carry = a
            continue
        segs.append((a, end))
    out = []; info = prev
    first = segs[0][0] if segs else len(L)
    if any(isM(l) for l in L[:first]):        # lanjutan tabel halaman sebelumnya (tanpa header)
        it, inf = _segment(L[:first], info, None)
        out += it; info = inf if it else info
    prev_end = first if segs else len(L)
    for k, (a, end) in enumerate(segs):
        # judul blok: baris teks tanpa angka tepat di atas header (setelah blok sebelumnya)
        lo = segs[k - 1][1] if k else 0
        tl = [ws_(' '.join(w[4] for w in l['w'])) for l in L[lo:a] if not isM(l)]
        title = tl[-1] if tl else None
        tlines = tl
        # segmen dimulai tepat setelah baris bertarif terakhir sebelumnya: baris label header yang terlipat ke atas
        # (bercampur teks kolom nama) tetap terlihat oleh _segment; baris di atas header tidak dibaca sebagai data
        lo2 = max([i + 1 for i in range(a) if isM(L[i])], default=0)
        it, inf = _segment(L[lo2:end], info, title)
        ht = inf.get('hdr_top') if it and inf is not info else None
        if ht is not None:   # baris judul = baris teks di atas blok header (bukan potongan label header)
            tlines = [ws_(' '.join(w[4] for w in l['w'])) for l in L[lo2:end] if not isM(l) and l['bot'] <= ht + 1]
        for x in it: x['tlines'] = tlines
        out += it
        if it: info = inf
    return out, info
