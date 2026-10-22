"""debug: baris yang dibaca checker (linegrid + kata PyMuPDF, halaman berurutan). Usage: chkview.py PDF PAGE REGEX"""
import sys, re, pymupdf
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from linegrid import read_page
d = pymupdf.open(sys.argv[1]); pg = int(sys.argv[2]); rx = re.compile(sys.argv[3], re.I); prev = None
for pn in range(1, pg + 1):
    items, prev = read_page([w[:5] for w in d[pn - 1].get_text('words', flags=pymupdf.TEXTFLAGS_WORDS & ~pymupdf.TEXT_MEDIABOX_CLIP)], prev)
    if pn == pg:
        print('items', len(items))
        for it in items:
            if rx.search(it['kode'] + ' ' + it['name']): print(repr(it['kode']), repr(it['name']), it['prices'])
