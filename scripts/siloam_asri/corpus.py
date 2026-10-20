import pdfplumber,json
pdf=pdfplumber.open('src/asri.pdf')
parts=[]
for p in pdf.pages:
    parts.append(p.extract_text() or '')
d=json.load(open('work/raw.json'))
for x in d['items']: parts.extend(x['cells'])
for t in d['texts']: parts.extend(t['free'])
open('work/corpus.txt','w').write('\n'.join(parts))
