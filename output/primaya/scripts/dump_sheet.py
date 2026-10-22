"""Tampilkan isi sheet RS: triplet per baris + alasan sekali per uraian. Usage: python3 dump_sheet.py OUT.xlsx SHEET"""
import sys, openpyxl
ws = openpyxl.load_workbook(sys.argv[1])[sys.argv[2]]
seen = set()
for r in range(2, ws.max_row + 1):
    u = ws.cell(r, 2).value
    v = [ws.cell(r, c).value for c in range(4, ws.max_column)]
    print(r, u, [x for x in v if x is not None])
    if u not in seen:
        seen.add(u); print('   >>', ws.cell(r, ws.max_column).value)
