# Tool 1: PyMuPDF rawdict + vector grid
import pymupdf, re, json, sys
PDF=sys.argv[1]; OUT=sys.argv[2]
NUM=re.compile(r'^\d{1,3}(\.\d{3})+$|^\d{1,3}$')
def merge(vals,tol=1.5):
    vals=sorted(vals); out=[]
    for v in vals:
        if out and v-out[-1][-1]<tol: out[-1].append(v)
        else: out.append([v])
    return [sum(g)/len(g) for g in out]
def grid(page):
    vx=[];hy=[];vseg=[];hseg=[]
    for d in page.get_drawings():
        for it in d['items']:
            if it[0]=='re':
                r=it[1]
                if r.width<2.5 and r.height>4: vseg.append(((r.x0+r.x1)/2,r.y0,r.y1))
                elif r.height<2.5 and r.width>4: hseg.append(((r.y0+r.y1)/2,r.x0,r.x1))
            elif it[0]=='l':
                p1,p2=it[1],it[2]
                if abs(p1.x-p2.x)<1 and abs(p1.y-p2.y)>4: vseg.append((p1.x,min(p1.y,p2.y),max(p1.y,p2.y)))
                elif abs(p1.y-p2.y)<1 and abs(p1.x-p2.x)>4: hseg.append((p1.y,min(p1.x,p2.x),max(p1.x,p2.x)))
    return vseg,hseg
def spans(page):
    out=[]
    raw=page.get_text('rawdict',flags=0)  # no clipping
    for b in raw['blocks']:
        for l in b.get('lines',[]):
            for s in l['spans']:
                chars=s['chars']
                # split runs at backward jumps or wide gaps
                cur=[]
                for c in chars:
                    if cur and (c['bbox'][0]<cur[-1]['bbox'][0]-0.5 or c['bbox'][0]-cur[-1]['bbox'][2]>6):
                        out.append(cur); cur=[]
                    cur.append(c)
                if cur: out.append(cur)
    res=[]
    for run in out:
        t=''.join(c['c'] for c in run)
        if not t.strip(): continue
        # split into words keeping bboxes
        words=[];w=[]
        for c in run:
            if c['c'].isspace():
                if w: words.append(w); w=[]
            else: w.append(c)
        if w: words.append(w)
        for w in words:
            res.append(dict(t=''.join(c['c'] for c in w),x0=w[0]['bbox'][0],x1=w[-1]['bbox'][2],
                            y0=min(c['bbox'][1] for c in w),y1=max(c['bbox'][3] for c in w)))
    return res
doc=pymupdf.open(PDF)
items=[];prev_cols=None;group=None
for pi,page in enumerate(doc):
    vseg,hseg=grid(page)
    words=spans(page)
    if not words: continue
    xs=merge([v[0] for v in vseg])
    ys=merge([h[0] for h in hseg])
    if len(xs)>=3: cols=xs
    else: cols=prev_cols
    if not cols: continue
    prev_cols=cols
    # header: words containing 'NAMA' line
    hdr=[w for w in words if w['t']=='NAMA']
    if not hdr: continue
    # handle multiple tables: each 'NAMA' header
    hdrs=sorted(hdr,key=lambda w:w['y0'])
    def colidx(x):
        for i in range(len(cols)-1):
            if cols[i]-0.5<=x<=cols[i+1]+0.5: return i
        return None
    # rows via horizontal lines
    ys_sorted=sorted(ys)
    for hi,h in enumerate(hdrs):
        ytop=h['y0']; ybot=hdrs[hi+1]['y0']-30 if hi+1<len(hdrs) else 1e9
        # header cell band: horizontal lines around header
        above=[y for y in ys_sorted if y<=ytop+0.5]; below=[y for y in ys_sorted if y>h['y1']]
        if not above or not below: continue
        hy0=above[-1]; hy1=below[0]
        hcells={}
        for w in words:
            if hy0<=w['y0'] and w['y1']<=hy1+1:
                ci=colidx(w['x0'])
                if ci is not None: hcells.setdefault(ci,[]).append(w)
        header={ci:' '.join(x['t'] for x in sorted(ws,key=lambda w:(round(w['y0']),w['x0']))) for ci,ws in hcells.items()}
        # title: nearest bold line above table
        title=' '.join(w['t'] for w in sorted([w for w in words if hy0-25<w['y1']<=hy0+0.5],key=lambda w:w['x0']))
        bands=[y for y in ys_sorted if hy1-0.5<=y<ybot]
        for a,b in zip(bands,bands[1:]):
            cell={}
            for w in words:
                yc=(w['y0']+w['y1'])/2
                if a<yc<b:
                    isnum=bool(re.fullmatch(r'\d{1,3}(\.\d{3})+',w['t']))
                    ci=colidx(w['x1'] if isnum else w['x0'])
                    if ci is not None: cell.setdefault(ci,[]).append(w)
            if not cell: continue
            txt={ci:' '.join(x['t'] for x in sorted(ws,key=lambda w:(round(w['y0']/3),w['x0']))) for ci,ws in cell.items()}
            # identify name col
            namec=[ci for ci,v in header.items() if 'NAMA' in v]
            kodec=[ci for ci,v in header.items() if 'KODE SAP'==v.strip() or v.startswith('KODE SAP')]
            noc=[ci for ci,v in header.items() if v.strip()=='NO']
            if not namec: continue
            nc=namec[0]
            kode=txt.get(kodec[0]) if kodec else None
            no=txt.get(noc[0]) if noc else None
            name=txt.get(nc)
            prices={header.get(ci,f'col{ci}'):txt.get(ci) for ci in header if ci>nc}
            if not any(prices.values()) and not (no and re.fullmatch(r'\d+',no)):
                group=name if (kode and re.fullmatch(r'[A-Z0-9]{10}',kode or '') and name) else ' '.join(x['t'] for ws in cell.values() for x in ws)
                group=' '.join(sorted(group.split(' '),key=lambda t:0)) if False else group
                items.append(dict(page=pi+1,type='group',text=txt,group=group))
                continue
            items.append(dict(page=pi+1,title=title,group=group,no=no,kode=kode,name=name,prices=prices,header=header))
json.dump(items,open(OUT,'w'),ensure_ascii=False,indent=0)
print(len([i for i in items if i.get('type')!='group']))
