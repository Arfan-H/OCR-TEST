import json,re,openpyxl,collections
it=[o for o in json.load(open('work/items.json')) if o['kind']=='item' and o['name']]
wb=openpyxl.load_workbook('in/1bdd2f48-RS_Siloam_ASRI_normalized_notDuplicate.xlsx',read_only=True)
ex=[r for r in wb.active.iter_rows(min_row=2,values_only=True)]
N=lambda s:re.sub(r'\s+',' ',(s or '')).strip().lower()
exset=collections.defaultdict(set)   # (name,col)->tarifs
for r in ex: exset[(N(r[1]),r[2])].add(r[3])
exnames=collections.defaultdict(list)
for r in ex: exnames[N(r[1])].append(r)
def num(v):
    v=v.replace(' ','')
    if re.fullmatch(r'\d{1,3}(\.\d{3})*',v): return int(v.replace('.',''))
    if re.fullmatch(r'\d+',v): return int(v)
    return None
tot=ok=okf=0; miss=[]
# fuzzy index by tarif triple
bytar=collections.defaultdict(list)
for r in ex: bytar[(r[2],r[3])].append(N(r[1]))
for o in it:
    for col,v in o['vals'].items():
        n=num(v)
        if n is None: continue
        tot+=1
        if n in exset.get((N(o['name']),col),()): ok+=1; continue
        cands=bytar.get((col,n),[])
        if any(N(o['name']) in c or c in N(o['name']) for c in cands if c): okf+=1; continue
        miss.append((o['page'],o['name'],col,n))
print('total cells',tot,'exact',ok,round(ok/tot*100,2),'fuzzy',okf,'combined',round((ok+okf)/tot*100,2),'miss',len(miss))
c=collections.Counter((m[0],m[1]) for m in miss)
for k,v in list(c.items())[:80]: print(k,v)
json.dump(miss,open('work/miss.json','w'))
