"""Tulis sheet RS ke workbook Normalisasi (gaya sama dengan build2.py).
Usage: python3 build_mika.py BASE.xlsx OUT.xlsx WORKDIR spec_a [spec_b ...]
WORKDIR berisi json/<PDFKEY>.json (alat 1) dan ex/<PDFKEY>.xlsx. Sheet yang sudah ada di BASE diganti di posisi yang sama,
sheet baru ditambahkan di akhir. SPEC hasil generator disimpan ke WORKDIR/spec_out/<sheet>.json."""
import sys, os, copy, json, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter as L
from gen_mika import generate

FLAG_KEYS = ['3. Ragu', '4. Janggal', 'Tidak ditemukan', 'selisih', 'non-kelas', 'mohon konfirmasi', 'tarif diisi -']


def write_sheet(wb, SHEET, SPEC, NTRIP):
    tpl = wb['Normalisasi']
    pos = None
    if SHEET in wb.sheetnames:
        pos = wb.sheetnames.index(SHEET); del wb[SHEET]
    ws = wb.create_sheet(SHEET, pos) if pos is not None else wb.create_sheet(SHEET)
    for r in range(1, tpl.max_row + 1):
        for c in range(1, 6):
            s = tpl.cell(r, c); d = ws.cell(r, c, s.value)
            if s.has_style:
                d.font = copy.copy(s.font); d.fill = copy.copy(s.fill); d.border = copy.copy(s.border)
                d.alignment = copy.copy(s.alignment); d.number_format = s.number_format; d.protection = copy.copy(s.protection)
        if tpl.row_dimensions[r].height is not None:
            ws.row_dimensions[r].height = tpl.row_dimensions[r].height
    for col in 'ABCDE':
        if col in tpl.column_dimensions:
            ws.column_dimensions[col].width = tpl.column_dimensions[col].width
    hfill = PatternFill('solid', fgColor='FCE4D6'); ffill = PatternFill('solid', fgColor='FFC7CE')
    col = 6
    for n in range(1, NTRIP + 1):
        for name, w in ((f'nama_layanan_{n}', 42), (f'kelas_kamar_{n}', 24), (f'tarif_{n}', 11)):
            c = ws.cell(1, col, name); c.font = Font(bold=True); c.fill = hfill
            ws.column_dimensions[L(col)].width = w
            col += 1
    FLAGC, ALC = col, col + 1
    for cc, name, w in ((FLAGC, 'flag_mencurigakan', 18), (ALC, 'alasan_mencurigakan', 120)):
        c = ws.cell(1, cc, name); c.font = Font(bold=True); c.fill = ffill
        ws.column_dimensions[L(cc)].width = w
    seen = set()
    for r in range(2, tpl.max_row + 1):
        uraian = tpl.cell(r, 2).value; kelas = tpl.cell(r, 4).value
        sp = SPEC[uraian]; seen.add(uraian)
        col = 6
        for t in sp['triplets']:
            row = t['rows'][kelas]
            name, label, tarif = row if sp['per_row_names'] else (t['name'],) + tuple(row)
            ws.cell(r, col, name); ws.cell(r, col + 1, label)
            c = ws.cell(r, col + 2, tarif)
            if isinstance(tarif, int): c.number_format = '#,##0'
            col += 3
        txt = sp['alasan']
        if any(k in txt for k in FLAG_KEYS):
            c = ws.cell(r, FLAGC, 'YA'); c.font = Font(bold=True, color='9C0006')
        a = ws.cell(r, ALC, txt); a.alignment = Alignment(wrap_text=True, vertical='top')
    assert seen == set(SPEC), set(SPEC) ^ seen
    ws.freeze_panes = 'F2'


if __name__ == '__main__':
    BASE, OUT, WD = sys.argv[1:4]
    wb = openpyxl.load_workbook(BASE)
    os.makedirs(os.path.join(WD, 'spec_out'), exist_ok=True)
    for mod in sys.argv[4:]:
        S = importlib.import_module(mod)
        SPEC, NTRIP, REVIEW = generate(S, os.path.join(WD, 'json', S.KEY + '.json'), os.path.join(WD, 'ex', S.KEY + '.xlsx'))
        write_sheet(wb, S.SHEET, SPEC, NTRIP)
        json.dump(dict(SPEC=SPEC, NTRIP=NTRIP, REVIEW=REVIEW), open(os.path.join(WD, 'spec_out', S.KEY + '.json'), 'w'), ensure_ascii=False, indent=1)
        print('sheet', S.SHEET, 'NTRIP', NTRIP)
    wb.save(OUT)
    print('saved', OUT, wb.sheetnames)
