import json,subprocess,sys,re
from PIL import Image
it=[o for o in json.load(open('work/items.json')) if o['kind']=='item']
names=json.load(open(sys.argv[1]))
R=110; s=R/72
done=[]
for i,(nm,pg) in enumerate(names):
    rows=[o for o in it if o['name']==nm and o['page']==pg]
    assert rows,(nm,pg)
    o=rows[0]
    # header: top of table
    top=o['table_top']; 
    out=f'crops/c{i:02d}'
    subprocess.run(['pdftoppm','-r',str(R),'-png','-f',str(pg),'-l',str(pg),'-singlefile','src/asri.pdf',out],check=True)
    im=Image.open(out+'.png')
    W=im.width
    hdr=im.crop((0,int(top*s)-2,W,int((top+28)*s)))
    row=im.crop((0,int(o['y']*s)-2,W,int(o['y1']*s)+2))
    new=Image.new('RGB',(W,hdr.height+row.height+4),'white'); new.paste(hdr,(0,0)); new.paste(row,(0,hdr.height+4))
    new.save(out+'.png'); done.append(out+'.png')
# stack into sheets of 6
from math import ceil
for k in range(ceil(len(done)/6)):
    ims=[Image.open(p) for p in done[k*6:(k+1)*6]]
    H=sum(i.height+10 for i in ims); W=max(i.width for i in ims)
    sh=Image.new('RGB',(W,H),'white'); y=0
    for i in ims: sh.paste(i,(0,y)); y+=i.height+10
    sh.save(f'crops/sheet{k}.png')
print(len(done))
