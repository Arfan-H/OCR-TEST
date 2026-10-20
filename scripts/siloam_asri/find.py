import json,re,sys
it=[o for o in json.load(open('work/items.json')) if o['kind']=='item' and o['name']]
pat=re.compile(sys.argv[1],re.I)
for o in it:
    if pat.search(o['name']):
        v=o['vals']
        print(o['page'],'|',o['section'],'|',repr(o['name']),'| ED',v['ED'],'OPD',v['OPD'],'ODC',v['OPD ODC DELUXE'],'| B',v['BASIC'],'S',v['STANDARD'],'D',v['DELUXE'],'| VIP',v['VIP'],v['VIP DELUXE'],v['VVIP'],v['EXECUTIVE SUITE'])
