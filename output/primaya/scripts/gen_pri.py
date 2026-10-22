"""Generator PRIMAYA (turunan gen_mika.py: kode boleh kosong -> 'tanpa kode'; kode ditulis di depan nama di PDF).
Generator: spec cabang + item PDF (alat 1) + Excel cabang -> SPEC sheet (triplet + alasan).
Usage (modul): from gen_pri import generate; SPEC, NTRIP, REVIEW = generate(spec_module, items_json, excel_path)
Spec cabang berisi pilihan item (kode, nama, hlm) dan catatan manual; tarif, label kolom, perbandingan Excel
dan penamaan dihitung di sini dari data, bukan diketik tangan."""
import re, json, collections, difflib
import openpyxl

KELAS = ('III', 'II', 'I & R. KHUSUS')
ws_ = lambda s: re.sub(r'\s+', ' ', str(s or '')).strip()
norm = lambda s: re.sub(r'[^A-Z0-9]', '', ws_(s).upper())
BUL = lambda s: re.sub(r'^- +', '', s or '')     # tanda daftar '- ' di depan nama (Cibubur) bukan bagian nama


def toint(v):
    v = re.sub(r'^Rp\.?\s*', '', ws_(v))
    v = re.sub(r'(?<=\d{3})[.,]00$', '', v) if re.fullmatch(r'\d{1,3}([.,]\d{3})+[.,]00', v) else v   # '693.000,00'
    if re.fullmatch(r'\d{1,3}([.,]\d{3})+|\d+', v): return int(re.sub(r'[.,]', '', v))
    return None


def rp(n): return f'{n:,}'.replace(',', '.') if isinstance(n, int) else n


TOKMAP = {'1': 'I', '2': 'II', '3': 'III', 'R': 'RUANG', 'ISO': 'ISOLASI', 'ISOL': 'ISOLASI', 'EXECUTIVE': 'EKSEKUTIF',
          'RJ': 'RAWAT JALAN', 'RAJAL': 'RAWAT JALAN', 'RANAP': 'RAWAT INAP', 'R.KHUSUS': 'RUANG KHUSUS', 'EKSEKUTI': 'EKSEKUTIF'}


def toks(lbl):
    out = set()
    for t in re.split(r'[,/&\s]+|(?<=R)\.', ws_(lbl).upper().replace('*', '')):
        t = t.strip('. ')
        if not t or t == 'KELAS': continue
        for x in TOKMAP.get(t, t).split(): out.add(x)
    return out


def cls_tok(lbl):
    """Token kelas reguler dalam label: {'III'}, {'II'}, {'I'} dst."""
    return toks(lbl) & {'I', 'II', 'III'}


WANT = {'III': 'III', 'II': 'II', 'I & R. KHUSUS': 'I'}


def class_col(header, kelas, override=None):
    if override and kelas in override:
        h = override[kelas]
        assert h in header, (h, header)
        return h
    m = [h for h in header if WANT[kelas] in cls_tok(h)]
    assert len(m) == 1, (kelas, header, m)
    return m[0]


class Excel:
    def __init__(self, path):
        ws = openpyxl.load_workbook(path, read_only=True).worksheets[0]
        it = ws.iter_rows(values_only=True); h = next(it)
        ix = {k: h.index(k) for k in ('kategori_harga', 'nama_layanan', 'kelas_kamar', 'tarif')}
        self.rows = []
        for r in it:
            if r[ix['nama_layanan']] is None: continue
            self.rows.append((ws_(r[ix['kategori_harga']]), ws_(r[ix['nama_layanan']]), ws_(r[ix['kelas_kamar']]), r[ix['tarif']]))

    def by_name(self, name, exact=True):
        if exact: return [r for r in self.rows if r[1] == name]
        return [r for r in self.rows if r[1].lower() == name.lower()]


def generate(S, items_path, excel_path):
    rows = json.load(open(items_path))
    EX = Excel(excel_path)
    count = collections.Counter(BUL(r['name']) for r in rows if any(toint(v) is not None for v in r['prices'].values()))
    SPEC = {}; REVIEW = []
    page_note = S.PAGE_NOTE

    def get(kode, name, page, idx=0, merged=False, rank=None, rv=None):
        m = [r for r in rows if r['kode'] == kode and BUL(r['name']) == name and r['page'] == page]
        if rank:
            # sub-baris tanpa kode & nama di bawah item (kode dan nama digabung/rowspan, pembeda di kolom rank, mis. JENIS KAMAR)
            for i, r in enumerate(rows):
                if r['kode'] == kode and BUL(r['name']) == name and r['page'] == page:
                    j = i + 1
                    while j < len(rows) and rows[j]['page'] == page and rows[j]['kode'] == '' and rows[j]['name'] == '':
                        m.append(dict(rows[j], kode=kode, name=r['name'], merged=True)); j += 1
            m = [r for r in m if r['prices'].get(rank) == rv]
        if merged and not m:
            # sel kode digabung (rowspan); kode dicek visual dan diverifikasi checker lewat posisi teks kode
            m = [dict(r, kode=kode, merged=True) for r in rows if r['kode'] == '' and BUL(r['name']) == name and r['page'] == page]
        assert len(m) > idx, ('item tidak ada di ekstraksi', kode, name, page, len(m))
        return m[idx]

    for ura, u in S.U.items():
        if u.get('notfound'):
            # item tidak ada di buku tarif cabang ini: satu triplet berisi '-' (dicek checker: istilah dicari tidak ada di PDF/Excel)
            pts = [f"1. Tidak ditemukan: {u['notfound']}",
                   "2. Pemetaan kelas & label: tidak ada item yang dipakai -> nama, label dan tarif diisi -"]
            if u.get('p3'): pts.append(f"3. Ragu: {u['p3']}")
            if u.get('p4'): pts.append(f"4. Janggal: {u['p4']}")
            pts.append(f"5. Excel vs sumber: {u['p5']}")
            pts.append(f"6. Catatan sumber: {S.SRC}{('; ' + u['p6']) if u.get('p6') else ''}")
            if u.get('p7'): pts.append(f"7. Tidak diambil: {u['p7']}")
            pts.append("8. Penamaan: tidak ada nama yang dipakai")
            SPEC[ura] = {'triplets': [{'name': '-', 'rows': {k: ('-', '-') for k in KELAS}}], 'alasan': ' | '.join(pts), 'per_row_names': False}
            REVIEW.append((ura, [])); continue
        uses = []
        per_row = 'rows' in u
        if per_row:
            n = len(u['rows']['III'])
            for t in range(n):
                for k in KELAS:
                    e = u['rows'][k][t]
                    uses.append(dict(kelas=k, t=t, **_norm_use(e)))
        else:
            for e in u['use']: uses.append(_norm_use(e))
        for x in uses:
            x['row'] = get(x['kode'], x['name'], x['page'], x.get('idx', 0), x.get('merged', False), x.get('rank'), x.get('rv'))
            if x.get('grp'): x['row'] = dict(x['row'], group=x['grp'])   # kelompok terputus di pergantian halaman (dicek visual)
            if x.get('ttl'): x['row'] = dict(x['row'], title=x['ttl'])   # judul tabel dari halaman sebelumnya (halaman lanjutan, dicek visual)
        # ---- penamaan (akhiran) ----
        incl = collections.Counter(x['name'] for x in uses) if not per_row else collections.Counter(x['name'] for x in uses)
        for x in uses:
            x['disp'] = x['name']
            if per_row and x.get('rank'):   # baris per kelas dari sub-baris: akhiran = isi kolom pembeda
                x['suffix'] = x['row']['prices'][x['rank']]; x['suffix_kind'] = f"isi kolom '{x['rank']}'"
                x['disp'] = f"{x['name']} - {x['suffix']}"
        if not per_row:
            for nm, c in incl.items():
                if c < 2: continue
                grp = [x for x in uses if x['name'] == nm]
                tit = [x['row']['title'] for x in grp]; gr = [x['row']['group'] for x in grp]
                rk = [x['row']['prices'].get(x['rank']) if x.get('rank') else None for x in grp]
                if all(rk) and len(set(rk)) == len(rk):
                    for x, v in zip(grp, rk): x['disp'] = f'{nm} - {v}'; x['suffix_kind'] = f"isi kolom '{x['rank']}'"; x['suffix'] = v
                    continue
                if all(t is None for t in rk) and len(set(tit)) == 1 and len(set(gr)) == 1 and len({x['page'] for x in grp}) == 1:
                    for i, x in enumerate(grp): x['disp'] = f'{nm} - baris {i + 1}'; x['suffix_kind'] = 'urutan baris'; x['suffix'] = f'baris {i + 1}'
                    continue
                # satu jenis akhiran untuk semua item bernama sama: judul tabel bila semua ada dan berbeda, lalu kelompok, lalu kode
                kd = [x['kode'] for x in grp]
                for vals_, kind in ((tit, 'judul tabel'), (gr, 'kelompok'), (kd, 'kode layanan')):
                    if all(vals_) and len(set(vals_)) == len(vals_): break
                else: raise AssertionError(('akhiran tidak bisa ditentukan', nm, tit, gr, kd))
                for x, v in zip(grp, vals_):
                    x['suffix'], x['suffix_kind'] = v, kind
                    x['disp'] = f"{nm} - {v}"
        # ---- triplet ----
        trip = []
        if per_row:
            for t in range(len(u['rows']['III'])):
                tr = {'rows': {}}
                for x in [y for y in uses if y['t'] == t]:
                    r = x['row']; v = [toint(val) for val in r['prices'].values()]
                    filled = [(h, toint(val)) for h, val in r['prices'].items() if toint(val) is not None]
                    assert len(filled) == 1, (x['name'], r['prices'])
                    lbl = _excel_label(EX, x['name'], filled[0][1], x.get('alias'))
                    x['label'] = lbl; x['tarif'] = filled[0][1]; x['col'] = filled[0][0]; x['nonkelas'] = True
                    tr['rows'][x['kelas']] = (x['disp'], lbl, filled[0][1])
                trip.append(tr)
        else:
            for x in uses:
                r = x['row']
                filled = [(h, toint(v)) for h, v in r['prices'].items() if toint(v) is not None]
                ccols = []
                if len(r['header']) > 1:
                    try: ccols = [class_col(r['header'], k, x.get('cls') or getattr(S, 'CLS_OVERRIDE', {}).get(r['page'])) for k in KELAS]
                    except AssertionError: ccols = []
                auto_nk = len(filled) == 1 and (not ccols or all(toint(r['prices'][h]) is None for h in ccols))
                if x.get('nonkelas') or len(r['header']) == 1 or auto_nk:
                    assert len(filled) == 1, (x['name'], r['prices'])
                    lbl = x.get('label') or _excel_label(EX, x['name'], filled[0][1], x.get('alias'))
                    x['nonkelas'] = True; x['col'] = filled[0][0]; x['label'] = lbl; x['tarif'] = filled[0][1]
                    rr = {k: (lbl, filled[0][1]) for k in KELAS}
                else:
                    rr = {}
                    x['cols'] = {}
                    for k in KELAS:
                        h = class_col(r['header'], k, x.get('cls') or getattr(S, 'CLS_OVERRIDE', {}).get(r['page']))
                        val = toint(r['prices'][h])
                        rr[k] = (h, val if val is not None else '-')
                        x['cols'][k] = h
                        if val is None: x.setdefault('dash', []).append(h)
                trip.append({'name': x['disp'], 'rows': rr})
        # ---- alasan ----
        pts = []
        pts.append(f"1. {u['p1'] if 'p1' in u else _p1(u, uses, per_row, page_note)}")
        pts.append(f"2. Pemetaan kelas & label: {u.get('p2') or _p2(S, u, uses, per_row)}")
        if u.get('p3'): pts.append(f"3. Ragu: {u['p3']}")
        if u.get('p4'): pts.append(f"4. Janggal: {u['p4']}")
        p5, rv = _p5(EX, u, uses)
        REVIEW.append((ura, rv))
        pts.append(f"5. Excel vs sumber: {p5}")
        pts.append(f"6. Catatan sumber: {S.SRC}{('; ' + u['p6']) if u.get('p6') else ''}")
        if u.get('p7'): pts.append(f"7. Tidak diambil: {u['p7']}")
        p8 = _p8(uses, count, per_row)
        if any(x['kode'] for x in uses):
            p8 += "; di PDF kode layanan tertulis di depan nama (format KODE - Nama), kode dipisah dari nama"
        if any(x['row']['name'] != x['name'] for x in uses):
            assert all(BUL(x['row']['name']) == x['name'] for x in uses)
            p8 += "; tanda daftar '- ' di depan nama item pada PDF tidak dimasukkan ke nama (Excel juga tanpa tanda itu)"
        pts.append(f"8. Penamaan: {p8}")
        SPEC[ura] = {'triplets': trip, 'alasan': ' | '.join(pts), 'per_row_names': per_row}
    NTRIP = max(len(v['triplets']) for v in SPEC.values())
    return SPEC, NTRIP, REVIEW


def _norm_use(e):
    if isinstance(e, dict): return dict(e)
    d = dict(kode=e[0], name=e[1], page=e[2])
    if len(e) > 3: d.update(e[3])
    return d


def _excel_label(EX, name, tarif, alias=None):
    ex = EX.by_name(alias or name) or EX.by_name(alias or name, exact=False)
    lb = sorted({r[2] for r in ex if r[3] == tarif})
    return lb[0] if len(lb) == 1 else 'UMUM/NON-KELAS'


def _vals(x):
    if x.get('nonkelas'): return f"{x['col']} {rp(x['tarif'])}"
    r = x['row']
    return ' / '.join(rp(toint(r['prices'][x['cols'][k]]) if toint(r['prices'][x['cols'][k]]) is not None else '-') for k in KELAS)


def _cite(x, full):
    r = x['row']; s = (f"'{x['name']}' (kode {x['kode']}" if x['kode'] else f"'{x['name']}' (tanpa kode") + (' sel gabung' if r.get('merged') else '')
    if full or x.get('suffix'):
        if r['group'] and x.get('suffix_kind') != 'judul tabel' and x.get('show_group', True):
            s += f", kelompok '{r['group']}'"; x['_shown_group'] = True
        if r['title']: s += f", tabel '{r['title']}'"; x['_shown_title'] = True
    if x.get('rank'): s += f", {x['rank']} '{r['prices'][x['rank']]}'"
    s += f", hlm. {r['page']}, "
    if x.get('nonkelas'): s += f"{x['col']} {rp(x['tarif'])})"
    elif full: s += ' / '.join(f"{x['cols'][k]} {rp(toint(r['prices'][x['cols'][k]])) if toint(r['prices'][x['cols'][k]]) is not None else '-'}" for k in KELAS) + ')'
    else: s += _vals(x) + ')'
    return s


def _carried(uses):
    """judul tabel/kelompok yang dikutip tetapi tercetak di halaman sebelumnya (tabel berlanjut ke halaman berikut)"""
    out = []
    for x in uses:
        r = x['row']
        for key, lab in (('title', 'judul tabel'), ('group', 'kelompok')):
            pg = r.get(key + '_pg')
            if x.get('_shown_' + key) and pg and pg != r['page']:
                t = f"{lab} '{r[key]}' tercetak di hlm. {pg} (tabel berlanjut ke hlm. {r['page']})"
                if t not in out: out.append(t)
    return ('; ' + '; '.join(out)) if out else ''


def _p1(u, uses, per_row, page_note):
    head = 'Nama sama' if u.get('nama') == 'sama' else 'Nama beda'
    if per_row:
        groups = collections.OrderedDict()
        for x in uses: groups.setdefault(x['t'], []).append(x)
        parts = []
        for t, xs in groups.items():
            lab = (u.get('row_labels') or {}).get(t)
            txt = ', '.join(_cite(x, i == 0 and t == 0) for i, x in enumerate(xs))
            parts.append((f'{lab}: ' if lab else '') + txt)
        return f"{head}: Dipakai " + '. '.join(parts) + f"; {page_note}" + _carried(uses)
    main = [x for x in uses if not x.get('role')]
    rest = collections.OrderedDict()
    for x in uses:
        if x.get('role'): rest.setdefault(x['role'], []).append(x)
    first = True; out = []
    for x in main:
        out.append(_cite(x, first)); first = False
    s = f"{head}: Dipakai " + _join(out)
    for role, xs in rest.items():
        cs = []
        for x in xs: cs.append(_cite(x, first)); first = False
        s += f". {role}: " + _join(cs)
    return s + f"; {page_note}" + _carried(uses)


def _q(x):
    return f"'{x['name']}'" + (f' (akhiran " - {x["suffix"]}")' if x.get('suffix') else '')


def _join(xs):
    return xs[0] if len(xs) == 1 else ', '.join(xs[:-1]) + ' dan ' + xs[-1]


def _p2(S, u, uses, per_row):
    if per_row:
        lbls = []
        for x in uses:
            if f'"{x["label"]}"' not in lbls: lbls.append(f'"{x["label"]}"')
        col = uses[0]['col']
        nk = ' (label non-kelas)' if any(x['label'] == 'UMUM/NON-KELAS' for x in uses) else ''
        rk = {x.get('rank') for x in uses}
        where = (f"kelas tertulis di kolom '{uses[0]['rank']}' (sub-baris di bawah kode dan nama yang digabung); nama diberi akhiran isi kolom itu"
                 if rk == {uses[0].get('rank')} and uses[0].get('rank') else "kelas tertulis di nama item")
        tb = 'tabel' if uses[0].get('rank') else 'tabel kamar'
        return (f"{tb} hanya punya satu kolom '{col}' dan {where}, jadi tiap baris memakai item kelasnya sendiri "
                f"dengan label mengikuti Excel ({', '.join(lbls)}{nk}; keputusan user). Nama triplet berbeda per baris (pengecualian aturan daftar triplet sama)")
    out = []
    maps = collections.OrderedDict()
    for x in uses:
        if x.get('nonkelas'): continue
        key = tuple(x['cols'][k] for k in KELAS)
        maps.setdefault(key, []).append(x)
    for key, xs in maps.items():
        h1 = key[2]
        extra = re.sub(r'(?i)\bkelas\s*(i|1)\b|(?<![A-Za-z0-9])(i|1)(?![A-Za-z0-9.])', ' ', h1)
        extra = re.sub(r'\s*([,/&])\s*(?:[,/&]\s*)*', r'\1 ', extra).strip(' ,/&')
        extra = re.sub(r'\s+', ' ', extra)
        s = f"III = '{key[0]}', II = '{key[1]}', I & R. KHUSUS = '{h1}'"
        if extra: s += f" (satu-satunya kolom yang memuat kelas I; di PDF digabung dengan {extra} sehingga tarif kelas I = tarif kolom gabungan; dipakai sesuai keputusan user)"
        else: s += " (kolom kelas I tersendiri)"
        others = [h for h in xs[0]['row']['header'] if h not in key and h and h not in ('Rank', 'FASILITAS', 'JENIS KAMAR', 'KELAS')]
        if others: s += '. Tidak dipakai: ' + ', '.join(f"'{h}'" for h in others)
        if len(maps) > 1: s = f"untuk {', '.join(_q(x) for x in xs)}: " + s
        out.append(s)
    nk = [x for x in uses if x.get('nonkelas')]
    if nk:
        lbls = sorted({x['label'] for x in nk})
        out.append(f"{', '.join(_q(x) for x in nk)} hanya bertarif di satu kolom ('{nk[0]['col']}') -> label non-kelas mengikuti Excel "
                   + ', '.join(f'"{l}"' for l in lbls) + " (keputusan user), tarif sama di ketiga baris")
    dash = [x for x in uses if x.get('dash')]
    for x in dash:
        out.append(f"sel {', '.join(chr(39) + h + chr(39) for h in x['dash'])} untuk {_q(x)} kosong/'-' di PDF -> tarif diisi -")
    return '; '.join(out)


def _p5(EX, u, uses):
    diffs = []; rv = []; same_tarif = True; katd = {}
    for x in uses:
        nm = x.get('alias') or x['name']
        ex = EX.by_name(nm)
        if not ex:
            exi = EX.by_name(nm, exact=False)
            if exi:
                en = exi[0][1]
                if f'Excel menulis "{en}"' not in ' '.join(diffs):
                    diffs.append(f"Excel menulis \"{en}\" (PDF '{x['name']}')")
                ex = exi
            else:
                diffs.append(f"'{x['name']}' tidak ada di Excel"); rv.append((x['name'], 'TIDAK ADA')); continue
        elif x.get('alias'):
            diffs.append(f"Excel menamai item ini \"{x['alias']}\" (PDF '{x['name']}'" + (f" {x['rank']} '{x['rv']}')" if x.get('rank') else ')'))
        r = x['row']
        if x.get('nonkelas'):
            ok = any(e[2] == x['label'] and e[3] == x['tarif'] for e in ex)
            if not ok:
                same_tarif = False; diffs.append(f"Excel tidak punya tarif {rp(x['tarif'])} untuk \"{ex[0][1]}\"")
            cand = [e for e in ex if e[3] == x['tarif']]
        else:
            cand = []; miss = []
            for k in KELAS:
                h = x['cols'][k]; v = toint(r['prices'][h])
                if v is None: continue
                m = [e for e in ex if e[3] == v and WANT[k] in cls_tok(e[2])]
                if not m:
                    # label Excel kehilangan token kelas tetapi tarif sama (token label Excel subset header PDF)
                    lm = [e for e in ex if e[3] == v and toks(e[2]) and toks(e[2]) < toks(h)]
                    if lm:
                        el = toks(lm[0][2])
                        miss = [ws_(w) for w in re.split(r'[,/]+', h) if ws_(w) and not toks(w) <= el]
                        t = f"Excel memberi label \"{lm[0][2]}\" untuk kolom '{h}' (tanpa {', '.join(miss)})"
                        if t not in diffs: diffs.append(t)
                        cand += lm
                        continue
                    same_tarif = False
                    have = [f'{e[2]}={rp(e[3])}' for e in ex if WANT[k] in cls_tok(e[2])]
                    if have:
                        diffs.append(f"Excel \"{ex[0][1]}\" kolom kelas {WANT[k]} bertarif {', '.join(have)} (PDF '{h}' {rp(v)})")
                    else:
                        miss.append((WANT[k], h, v))
                    continue
                cand += m
                lbs = {e[2] for e in m}
                if not any(toks(l) == toks(h) for l in lbs):
                    l0 = sorted(lbs)[0]
                    t = f"Excel memberi label \"{l0}\" untuk kolom '{h}'"
                    if t not in diffs: diffs.append(t)
            if miss:   # kelas yang sama sekali tidak ada di Excel: satu pernyataan per item
                diffs.append(f"Excel \"{ex[0][1]}\" tidak punya tarif kelas " + '/'.join(m[0] for m in miss) + " (PDF "
                             + ' / '.join(f"'{m[1]}' {rp(m[2])}" for m in miss) + "); Excel hanya memuat "
                             + ', '.join(f'{e[2]}={rp(e[3])}' for e in ex))
        # kategori
        kat = sorted({e[0] for e in cand})
        # kategori Excel dibandingkan dengan judul tabel PDF saja (kata >= 3 huruf, tanpa awalan bagian 'C. ' dan kata umum
        # 'TARIF'; salah ketik ringan ditoleransi). Kelompok/sub-bagian tidak dibandingkan: hierarki bagian buku Primaya
        # (mis. 'C. SEROLOGI - IMUNOLOGI' > 'C2. PROTEIN SPESIFIK') tidak selalu terbaca utuh. Tanpa judul tabel: tidak dibandingkan.
        GP = lambda t: re.sub(r'^\s*(?:[A-Z]{1,2}\d*|[IVX]+|\d+)\s*[.)]\s*', '', t or '')
        KTOK = lambda t: {w for w in re.findall(r'[A-Z]{3,}', GP(t).upper()) if w not in ('TARIF', 'DAN', 'DENGAN', 'UNTUK', 'UTK', 'YANG')}
        def kat_ok(c):
            tt = KTOK(r['title'])
            if not tt: return True
            return any(difflib.SequenceMatcher(None, a, b).ratio() >= 0.85 for a in KTOK(c) for b in tt)
        if kat and not any(kat_ok(c) for c in kat):
            if not x.get('kat_ok'):
                pdesc = f"tabel '{r['title']}'"
                katd.setdefault((kat[0], pdesc), []).append(cand[0][1])
        rv.append((x['disp'], kat))
    for (k, pdesc), names in katd.items():
        diffs.append(f"kategori Excel \"{k}\" untuk " + ', '.join(f'\"{n}\"' for n in dict.fromkeys(names)) + f" (PDF {pdesc})")
    if u.get('p5'): diffs.append(u['p5'])
    if not diffs: return 'label dan tarif sama dengan Excel', rv
    return 'selisih - ' + '; '.join(diffs) + ('. Tarif sama' if same_tarif else ''), rv


def _p8(uses, count, per_row):
    names = []
    for x in uses:
        if x['name'] not in names: names.append(x['name'])
    sufs = [x for x in uses if x.get('suffix')]
    out = []
    if sufs:
        byn = collections.OrderedDict()
        for x in sufs: byn.setdefault(x['name'], []).append(x)
        for nm, xs in byn.items():
            kinds = ' / '.join(dict.fromkeys(x['suffix_kind'] for x in xs))
            out.append(f"'{nm}' dimasukkan {len(xs)}x -> akhiran = {kinds} di PDF (" + ', '.join(f'" - {x["suffix"]}"' for x in xs) + ')')
    rest = [n for n in names if n not in {x['name'] for x in sufs}]
    multi = [n for n in rest if count[n] > 1]
    if multi:
        out.append('; '.join(f"'{n}' muncul {count[n]}x di buku tetapi hanya satu yang dimasukkan" for n in multi) + ' -> tanpa akhiran')
    if len(multi) < len(rest):
        out.append('Nama unik di buku -> tanpa akhiran' if not out else 'nama lain unik -> tanpa akhiran')
    return '; '.join(out)
