"""Ringkas sheet untuk review: triplet baris pertama per uraian + poin alasan terpilih. Usage: review.py OUT.xlsx SHEET [poin...]"""
import sys, openpyxl
ws = openpyxl.load_workbook(sys.argv[1])[sys.argv[2]]
keep = sys.argv[3:] or ['1', '2', '5', '8']
seen = set()
for r in range(2, ws.max_row + 1):
    u = ws.cell(r, 2).value
    trip = [ws.cell(r, c).value for c in range(6, ws.max_column - 1)]
    print(f"r{r} {ws.cell(r,4).value:>13} | " + ' ; '.join(f'{trip[i]} [{trip[i+1]}] {trip[i+2]}' for i in range(0, len(trip), 3) if trip[i]) + f" | flag={ws.cell(r, ws.max_column-1).value}")
    if u in seen: continue
    seen.add(u)
    for p in (ws.cell(r, ws.max_column).value or '').split(' | '):
        if p.split('.')[0] in keep: print('     ', p)
