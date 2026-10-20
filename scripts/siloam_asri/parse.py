import json,re,sys
COLS=['ED','OPD','OPD ODC DELUXE','BASIC','STANDARD','DELUXE','VIP','VIP DELUXE','VVIP','EXECUTIVE SUITE']
d=json.load(open('work/raw.json'))
out=[]; bad=[]
sub=None; lastkey=None
for x in d['items']:
    c=x['cells']
    if x['page']==3: continue
    if x['ncols']==12: c=c[1:]
    if len(c)!=11: bad.append(x); continue
    key=(x['page'],x['table_top'])
    if key!=lastkey: lastkey=key; hdr=0
    joined=' '.join(c)
    if 'BASIC' in c or c[0] in ('DESCRIPTION','ROOM','OPERATING THEATRE','LDS OBSERVATION','') and all(v in ('','DELUXE','SUITE','ODC DELUXE','OPD','VIP','EXECUTIVE','ODC') for v in c[1:]):
        if c[0] and c[0] not in('DESCRIPTION',''): x['hdr0']=c[0]
        continue
    vals=dict(zip(COLS,c[1:]))
    if all(v=='' for v in c[1:]):
        sub=c[0]; out.append({'page':x['page'],'section':x['section'],'kind':'sub','name':c[0],'y':x['y']}); continue
    out.append({'page':x['page'],'section':x['section'],'kind':'item','name':c[0],'vals':vals,'y':x['y'],'y1':x['y1'],'xs':x['xs'][-11:] if x['xs'] else None,'sub':sub,'row':x['row'],'table_top':x['table_top']})
json.dump(out,open('work/items.json','w'),ensure_ascii=False)
print(len(out),'bad',len(bad))
for b in bad[:10]: print(b['page'],b['cells'])
import collections
print(collections.Counter(o['kind'] for o in out))
subs=[o for o in out if o['kind']=='sub']
for s in subs: print('SUB',s['page'],s['section'],s['name'])
print([o['name'] for o in out if o['kind']=='item' and '  ' in o['name']][:20])
# non numeric values
nn=collections.Counter(v for o in out if o['kind']=='item' for v in o['vals'].values() if not re.fullmatch(r'\d{1,3}(\.\d{3})*|-|',v))
print(nn.most_common(40))
