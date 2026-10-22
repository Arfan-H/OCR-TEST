"""Kandidat item per uraian Normalisasi di JSON extract_pri.py. Usage: python3 search_pri.py ITEMS.json [key ...]"""
import sys, json, re, collections
rows = json.load(open(sys.argv[1]))
Q = {
 'igd': r'(ugd|igd|gawat darurat)',
 'ranap': r'visite|visit',
 'kamar': r'^(kamar|ruang) (perawatan|rawat|kelas)|^kelas (i|ii|iii|1|2|3)\b|^kamar$',
 'jasa': r'jasa (perawat|keperawatan|perawatan)|asuhan kep|askep',
 'iv': r'infus|iv line|vena ?seksi|venaseksi|venasectie|abocath',
 'inj': r'injeksi|suntik',
 'dl': r'darah lengkap|hematologi (lengkap|rutin)|darah rutin|complete blood',
 'crp': r'crp',
 'thorax': r'thorax|thoraks|toraks|dada',
 'pump': r'pump|syring',
 'o2': r'\bo2\b|oksigen|oxygen',
 'neb': r'nebul',
 'cr': r'creat|kreat',
 'ur': r'ureum|\bbun\b|urea',
 'gds': r'glukosa|gula darah|\bgds\b',
 'el': r'elektrolit|electrolyt',
}
keys = sys.argv[2:] or list(Q)
H = {}
for k in keys:
    print(f'##### {k}')
    rx = re.compile(Q[k], re.I); n = 0
    for r in rows:
        if not rx.search(r['name'] or ''): continue
        n += 1
        if n > 40: continue
        hid = H.setdefault(tuple(r['header']), len(H))
        pv = '/'.join(v or '_' for v in r['prices'].values())
        print(f"p{r['page']}|{r['title']}|{r['group']}|{r['kode']}|{r['name']}|H{hid}|{pv}")
    if n > 40: print(f'  ... {n} total')
print('##### HEADERS')
for h, i in H.items(): print(f'H{i}', h)
