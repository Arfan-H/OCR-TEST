"""Buat DRAF spec_<key>.py Primaya dari JSON ekstraksi (pola kode layanan Primaya seragam antar cabang).
Usage: python3 make_spec_pri.py KEY "Nama Sheet" [--force]
Draf ditinjau manual (nama, halaman, ragu/janggal) dan dicek checker + visual; tidak menimpa spec yang sudah ada tanpa --force."""
import sys, os, re, json, collections
import pymupdf

KEY, SHEET = sys.argv[1:3]
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
OUTP = os.path.join(HERE, f'spec_{KEY}.py')
if os.path.exists(OUTP) and '--force' not in sys.argv: sys.exit(f'{OUTP} sudah ada (pakai --force)')
rows = json.load(open(os.path.join(ROOT, 'work', 'json', KEY + '.json')))
doc = pymupdf.open(os.path.join(ROOT, 'pdf', KEY + '.pdf'))
MONEY = re.compile(r'^\d{1,3}([.,]\d{3})+([.,]00)?$')
has_price = lambda r: any(MONEY.match(v or '') for v in r['prices'].values())
byk = collections.defaultdict(list)
for r in rows:
    if r['kode'] and has_price(r): byk[r['kode']].append(r)
REPORT = []


def item(code, role=None, name=None, opts=None):
    rs = byk.get(code, [])
    if name: rs = [r for r in rs if r['name'] == name] or rs
    if not rs: REPORT.append(f'TIDAK ADA kode {code}'); return None
    if len(rs) > 1: REPORT.append(f'kode {code} muncul {len(rs)}x: ' + ', '.join(f"hlm.{r['page']} {r['name']}" for r in rs))
    r = rs[0]; o = dict(opts or {})
    if role: o['role'] = role
    return (code, r['name'], r['page'], o) if o else (code, r['name'], r['page'])


def by_name(rx):
    return [r for r in rows if re.search(rx, r['name'], re.I) and has_price(r)]


def other(rx, used, reasons, skip=r'^(HC|KL|GB|GA)'):
    """daftar 'tidak diambil': nama unik dari PDF yang cocok rx, selain yang dipakai, dengan alasan per pola"""
    usedn = {(u[0], u[1]) for u in used if u}
    seen = collections.OrderedDict()
    for r in by_name(rx):
        if (r['kode'], r['name']) in usedn or re.match(skip, r['kode'] or ''): continue
        why = next((w for p, w in reasons if re.search(p, r['name'], re.I)), 'bukan padanan langsung')
        seen.setdefault(why, [])
        if r['name'] not in seen[why] and r['name'] not in [u[1] for u in used if u]: seen[why].append(r['name'])
    parts = []
    for why, ns in seen.items():
        if not ns: continue
        q = ', '.join(f"'{n}'" for n in ns[:8]) + (' dkk.' if len(ns) > 8 else '')
        parts.append(f'{q} ({why})')
    return '; '.join(parts)


R = 'Ragu'
U = collections.OrderedDict()
# 1. konsultasi dokter umum IGD
use = [item('DR004')]
U['Konsultasi Dokter Umum IGD'] = dict(nama='beda', use=use, p7=other(r'ugd|igd|konsultasi dokter umum', use, [
    (r'observasi', 'observasi di UGD, bukan konsultasi'), (r'tele', 'telekonsultasi'), (r'isolasi', 'kamar isolasi'),
    (r'spesialis', 'dokter spesialis/subspesialis'), (r'IPS', 'IPS'), (r'libur', 'hari libur'), (r'klinik', 'klinik'),
    (r'konsultasi dokter umum$', 'konsultasi dokter umum poliklinik, bukan UGD')]))
# 2. visite spesialis rawat inap
use = [item('DR005'), item('DR006', 'Varian tingkat dokter (urutan kolom sama)'), item('DR007', R)]
U['Konsultasi Spesialis Rawat Inap'] = dict(nama='beda', use=use,
    p3="'Visite Dokter Umum' adalah visite dokter umum, bukan spesialis (padanan lemah)",
    p7=other(r'^visite|^konsultasi dokter (spesialis|sub)', use, [
        (r'on call', 'visite on call jarak jauh (audio/visual/chat)'), (r'laktasi', 'laktasi'), (r'professor|dr\.|dr ', 'dokter tertentu/profesor'),
        (r'crrt|cvvh', 'pasien CRRT/CVVH'), (r'^konsultasi', 'konsultasi rawat jalan, bukan visite rawat inap')]))
# 3. kamar
km = {c: item(c) for c in ('KM001', 'KM002', 'KM003', 'KM023', 'KM024', 'KM025')}
if all(km[c] for c in ('KM001', 'KM002', 'KM003')):
    rws = {'III': [km['KM001']], 'II': [km['KM002']], 'I & R. KHUSUS': [km['KM003']]}
    lab = {}
    if all(km[c] for c in ('KM023', 'KM024', 'KM025')):
        rws['III'].append(km['KM023']); rws['II'].append(km['KM024']); rws['I & R. KHUSUS'].append(km['KM025']); lab = {1: 'Varian bayi'}
    U['Ruang Rawat'] = dict(nama='beda', rows=rws, row_labels=lab,
        p3="varian bayi (bayi sehat) dimasukkan sebagai varian umur" if lab else None,
        p7=other(r'^(kelas|deluxe|suite|president|icu|iccu|nicu|picu|perina|isolasi|hcu|odc|vk|bayi sehat)', [x for v in rws.values() for x in v], [
            (r'^vk', 'kamar bersalin (VK)'), (r'isolasi', 'kamar isolasi'), (r'^(icu|iccu|nicu|picu|perina|hcu)', 'ruang khusus'),
            (r'deluxe|suite|president', 'di atas kelas I'), (r'odc', 'one day care')]))
else:
    kp = [r for r in by_name(r'^kamar perawatan$')]
    bs = [r for r in by_name(r'^kamar bayi sehat$')]
    use = [(r['kode'], r['name'], r['page']) for r in kp[:1]] + [(r['kode'], r['name'], r['page'], {'role': 'Varian bayi'}) for r in bs[:1]]
    if not kp: REPORT.append('TIDAK ADA kamar (KM001-3 / Kamar Perawatan)')
    U['Ruang Rawat'] = dict(nama='beda', use=use, p7=other(r'^kamar', use, [
        (r'icu|iccu|nicu|picu|perina|hcu', 'ruang khusus'), (r'isolasi', 'kamar isolasi'), (r'odc', 'one day care'), (r'vk|bersalin', 'kamar bersalin'),
        (r'sewa|extra', 'sewa kamar/extra bed')]))
# 4. jasa perawatan
jp = [r for r in by_name(r'^jasa perawatan$')]
use = [(r['kode'], r['name'], r['page']) for r in jp[:1]]
if not jp: REPORT.append('TIDAK ADA Jasa Perawatan')
U['Jasa Perawatan'] = dict(nama='sama', use=use, p7=other(r'jasa perawat', use, [(r'pendamping', 'pendampingan'), (r'infus', 'perawat infus ICT/SVF')]))
# 5. pasang infus
use = [item('NB020'), item('DU065', R), item('DU089', R)]
U['Pasang IV Line Access'] = dict(nama='beda', use=use,
    p3="'Pemasangan Infus Dengan Penyulit' adalah pemasangan infus dengan penyulit oleh dokter umum; 'Venaseksi' adalah akses vena dengan sayatan (cut-down), bukan IV line biasa",
    p7=other(r'infus|venaseksi|vena seksi', use, [(r'pump', 'alat infusion pump'), (r'drip', 'drip infus (pemberian), bukan pemasangan'),
        (r'intraosseus', 'infus intraoseus'), (r'sonohyster', 'tindakan kebidanan'), (r'vitamin|whitening|glowing|oxy|ict|svf|targeting', 'infus terapi/estetik/onkologi'),
        (r'penyulit|venaseksi', 'versi dokter spesialis'), (r'pemasangan infus', 'versi lain')]))
# 6. injeksi
use = [item('NB103'), item('NB104'), item('DU103'), item('DU104')]
U['Injeksi IM / IV'] = dict(nama='beda', use=use,
    p7=other(r'^injeksi (intramusk|intraven|subkut)|injeksi obat', use, [(r'usg', 'injeksi dengan panduan USG (pain management)'),
        (r'subkutan', 'injeksi subkutan'), (r'jasa tindakan injeksi obat', 'jasa tindakan injeksi obat (umum)'), (r'iv/im', 'homecare'),
        (r'intramusk|intraven', 'versi dokter spesialis')]))
# 7-17. penunjang & alat
use = [item('A1003')]
U['Hematologi Lengkap'] = dict(nama='sama', use=use, p7=other(r'^hematologi (rutin|lengkap)', use, [(r'rutin', 'parameter lebih sedikit')]))
use = [item('C2007'), item('B5007', R)]
U['CRP Kuantitatif'] = dict(nama='sama', use=use, p3="'hsCRP' adalah CRP sensitivitas tinggi (fungsi jantung), bukan CRP kuantitatif standar",
    p7='tidak ada CRP kualitatif/CRP tanpa keterangan')
use = [item('XR114')]
U['Thorax PA'] = dict(nama='sama', use=use, p7=other(r'^thorax', use, [(r'expertise', 'jasa expertise saja'), (r'\+', 'kombinasi proyeksi'),
    (r'ap$|lateral$|lld$|rld$|lordotic$|bed$', 'proyeksi lain')]))
use = [item('SA020'), item('SA035', R)]
U['Infusion Pump / hari'] = dict(nama='beda', use=use, p3="'Infusion Pump 1 s/d 6 jam' bersatuan 1-6 jam, bukan per hari")
use = [item('SA107'), item('SA059', R)]
U['Syringe Pump / hari'] = dict(nama='beda', use=use, p3="'Syringe Pump 1 s/d 6 jam' bersatuan 1-6 jam, bukan per hari")
use = [item('OX002'), item('OX001', R)]
U['O2 / Hari'] = dict(nama='beda', use=use, p3="'Oksigen / jam' bersatuan per jam, bukan per hari")
use = [item('NB203'), item('DU203'), item('RM058')]
U['Nebulizer'] = dict(nama='beda', use=use,
    p3="'Inhalasi/Nebulisasi Dewasa' adalah tindakan nebulisasi; 'Nebulizer' di rehabilitasi medik adalah layanan fisioterapi",
    p7=other(r'nebul', use, [(r'modalitas', 'paket modalitas fisioterapi'), (r'\+', 'kombinasi fisioterapi'), (r'pemakaian', 'homecare')], skip=r'^$'))
use = [item('B2002')]
U['Creatinin'] = dict(nama='beda', use=use, p3="satu item 'Kreatinin + eGFR' (kreatinin dengan perhitungan eGFR); tidak ada item kreatinin tanpa eGFR",
    p7=other(r'kreatinin|creatinin', use, [(r'clearence|clearance', 'clearance'), (r'urin', 'urine')]))
use = [item('B2006')]
U['Ureum'] = dict(nama='sama', use=use, p7=other(r'ureum|urea', use, [(r'clearance', 'clearance'), (r'urin', 'urine'), (r'breath|ubt', 'tes napas'),
    (r'phenyl', 'skrining neonatal')]))
use = [item('B3005'), item('B3020', R)]
U['GDS'] = dict(nama='beda', use=use, p3="'POCT Glukosa Darah (Sewaktu)' adalah pemeriksaan POCT (alat point-of-care), bukan analisa laboratorium",
    p7=other(r'glukosa darah', use, [(r'poct', 'POCT bukan sewaktu'), (r'puasa|pp|jam', 'bukan sewaktu')]))
use = [item('B6008')]
U['Elektrolit (Na, K, Cl)'] = dict(nama='beda', use=use)

# ---- tulis draf ----
def fmt_use(u):
    return repr(u)
L = [f'"""Spec {SHEET} (DRAF dibuat make_spec_pri.py, lalu ditinjau manual; format sama dengan spec MIKA)."""',
     f'KEY = {KEY!r}', f'SHEET = {SHEET!r}',
     "PAGE_NOTE = 'hlm. = nomor halaman file PDF (urutan halaman di file), bukan nomor cetak'",
     'SRC = None   # diisi manual', 'U = {']
for ura, d in U.items():
    L.append(f' {ura!r}: dict(')
    L.append(f"    nama={d['nama']!r},")
    if 'rows' in d:
        L.append(f"    rows={d['rows']!r}, row_labels={d['row_labels']!r},")
    else:
        L.append(f"    use={[u for u in d['use'] if u]!r},")
    for k in ('p3', 'p4', 'p7'):
        if d.get(k): L.append(f'    {k}={d[k]!r},')
    L.append(' ),')
L.append('}')
open(OUTP, 'w').write('\n'.join(L) + '\n')
print('\n'.join(REPORT) or 'semua kode ada'); print('ditulis', OUTP)
