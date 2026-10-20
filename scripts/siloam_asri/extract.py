import pdfplumber, json, sys, re, collections
COLS=['ED','OPD','OPD ODC DELUXE','BASIC','STANDARD','DELUXE','VIP','VIP DELUXE','VVIP','EXECUTIVE SUITE']
SNAP={'snap_tolerance':6,'join_tolerance':6,'intersection_tolerance':6}
def text_of(chars, gaplog=None):
    if not chars: return ''
    chars=sorted(chars,key=lambda c:(round(c['top']),c['x0']))
    lines=[]
    for c in sorted(chars,key=lambda c:c['top']):
        for L in lines:
            if abs(L[0]-c['top'])<2.5: L[1].append(c); break
        else: lines.append([c['top'],[c]])
    out=[]
    for top,cs in sorted(lines,key=lambda L:L[0]):
        cs.sort(key=lambda c:c['x0'])
        s=''; prev=None
        for c in cs:
            if prev is not None and c['text']!=' ' and prev['text']!=' ' and c['x0']-prev['x1']>0.3*c['size']:
                s+=' '
                if gaplog is not None: gaplog.append((s,c['text']))
            s+=c['text']; prev=c
        out.append(s.strip())
    return ' '.join(x for x in out if x)
def main(path,out):
    pdf=pdfplumber.open(path)
    items=[]; texts=[]; section=None; title=None; gaps=[]
    for pi,p in enumerate(pdf.pages,1):
        tabs=p.find_tables()
        snaps=p.find_tables(SNAP)
        inside=lambda c,bb: bb[0]-1<=c['x0'] and c['x1']<=bb[2]+1 and bb[1]-1<=c['top'] and c['bottom']<=bb[3]+1
        # free text lines (outside tables)
        free=[c for c in p.chars if not any(inside(c,t.bbox) for t in tabs)]
        freelines=collections.defaultdict(list)
        for c in free: freelines[round(c['top']/3)].append(c)
        fl=[]
        for k in sorted(freelines):
            cs=freelines[k]; t=text_of(cs)
            if t: fl.append((min(c['top'] for c in cs),t,max(c['size'] for c in cs)))
        texts.append({'page':pi,'free':[x[1] for x in fl]})
        events=[('text',y,t,sz) for y,t,sz in fl]+[('table',t.bbox[1],t,None) for t in tabs]
        events.sort(key=lambda e:e[1])
        for ev in events:
            if ev[0]=='text':
                y,t,sz=ev[1],ev[2],ev[3]
                if re.fullmatch(r'\d{1,3}',t): continue
                if re.match(r'^[A-K]\. ',t) and sz>=13: section=t; title=t
                elif sz>=12 and t not in ('TABLE OF CONTENTS',): title=t
                continue
            t=ev[2]
            # find snapped table overlapping
            sn=[s for s in snaps if not (s.bbox[2]<t.bbox[0] or s.bbox[0]>t.bbox[2] or s.bbox[3]<t.bbox[1] or s.bbox[1]>t.bbox[3])]
            xs=None
            if sn:
                s=sn[0]
                best=max(s.rows,key=lambda r:sum(1 for c in r.cells if c))
                xs=[(c[0],c[2]) for c in best.cells if c]
            rows=t.rows
            header=None; sub=None
            for ri,r in enumerate(rows):
                y0,y1=r.bbox[1],r.bbox[3]
                rc=[c for c in p.chars if t.bbox[0]-1<=c['x0']<=t.bbox[2]+1 and y0-0.5<=(c['top']+c['bottom'])/2<=y1+0.5]
                if xs is None or len(xs)<2:
                    cells=[text_of([c for c in rc if x0<= (c['x0']+c['x1'])/2 <=x1]) for (x0,x1) in [(cc[0],cc[2]) for cc in r.cells if cc]]
                else:
                    cells=[text_of([c for c in rc if x0-0.5<=(c['x0']+c['x1'])/2<=x1+0.5],gaps) for (x0,x1) in xs]
                bold=all('Bold' in c['fontname'] for c in rc if c['text'].strip()) and rc
                items.append({'page':pi,'section':section,'title':title,'table_top':round(t.bbox[1],1),'row':ri,'y':round(y0,1),'y1':round(y1,1),'cells':cells,'bold':bool(bold),'ncols':len(xs) if xs else None,'xs':xs})
    json.dump({'items':items,'texts':texts,'gaps':gaps[:200],'ngaps':len(gaps)},open(out,'w'),ensure_ascii=False)
main(sys.argv[1],sys.argv[2])
