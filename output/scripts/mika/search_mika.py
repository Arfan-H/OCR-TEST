"""Cari kandidat item per uraian Normalisasi di JSON hasil extract_mika.py.
Usage: python3 search_mika.py ITEMS.json [uraian-key ...]
Baris dari tabel poli spesialis diringkas (jumlah + kode) supaya daftar tetap terbaca."""
import sys, json, re, collections
rows = json.load(open(sys.argv[1]))
Q = {
 'igd': r'konsul.*(umum|igd)|dokter umum.*(igd|rawat inap)|\bigd\b.*konsul',
 'ranap': r'konsul.*(rawat inap|ranap|spesialis|visit)|visit',
 'kamar': r'^(ruang rawat|ruang perawatan|kamar perawatan|kelas)\b|^(kelas )?(i|ii|iii|1|2|3)$',
 'jasa': r'jasa .*rawat|keperawatan|jasa perawat',
 'iv': r'iv line|pasang infus|infus (dewasa|anak|bayi)|vena ?seksi|abocath|venflon|^infus$',
 'inj': r'injeksi.*\b(im|iv)\b|suntik',
 'dl': r'darah lengkap|hematologi lengkap|darah rutin|complete blood|^hematologi',
 'crp': r'crp',
 'thorax': r'^(foto |rontgen |x-?ray )?(thorax|thoraks|toraks)',
 'ipump': r'infus(ion)? ?pump',
 'spump': r'syring',
 'o2': r'\bo2\b|oksigen|oxygen',
 'neb': r'nebul',
 'cr': r'creat|kreat',
 'ur': r'ureum|\bbun\b|urea',
 'gds': r'glukosa|gula darah|\bgds\b',
 'el': r'elektrolit|electrolyt',
}
POLI = re.compile(r'POLI|KLINIK', re.I)
keys = sys.argv[2:] or list(Q)
hdrs = {}
for k in keys:
    print(f'##### {k}')
    rx = re.compile(Q[k], re.I)
    poli = collections.defaultdict(list)
    for r in rows:
        if not rx.search(r['name'] or ''): continue
        h = tuple(r['header'])
        hid = hdrs.setdefault(h, len(hdrs))
        pv = '/'.join(v or '_' for v in r['prices'].values())
        line = f"p{r['page']}|{r['title']}|{r['group']}|{r['kode']}|{r['name']}|H{hid}|{pv}"
        if k in ('inj', 'iv', 'neb') and POLI.search(r['title'] or ''):
            poli[(r['name'], pv)].append(f"{r['kode']}@p{r['page']}"); continue
        print(line)
    for (n, pv), ks in poli.items():
        print(f"  [poli x{len(ks)}] {n} | {pv} | {', '.join(ks[:6])}{' ...' if len(ks) > 6 else ''}")
print('##### HEADERS')
for h, i in hdrs.items(): print(f'H{i}', h)
