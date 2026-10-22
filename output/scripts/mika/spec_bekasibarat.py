"""Spec Mitra Keluarga Bekasi Barat (lihat spec_depok.py untuk format).
PDF/Excel cabang ini ditandatangani sebagai 'MITRA KELUARGA BEKASI' (sumber: file bekasi barat di folder input)."""
KEY = 'bekasibarat'
SHEET = 'Mitra Keluarga Bekasi Barat'
PAGE_NOTE = 'hlm. = nomor halaman file PDF, bukan nomor cetak (mis. hlm. 44 = cetak 43)'
SRC = ("Effective Date per tabel 'PER 1 JANUARI 2026'; biaya administrasi rawat inap terpisah: ADMB000001 (hlm. 43) '5% dari total Tagihan'")
R = dict(role='Ragu')
# hlm. 45: baris kelompok 'KAMAR PERAWATAN'/'KAMAR BERSALIN' terbaca sebagai judul tabel; judul asli 'TARIF KAMAR' (dicek visual)
KP = dict(ttl='TARIF KAMAR', grp='KAMAR PERAWATAN')
KB = dict(ttl='TARIF KAMAR', grp='KAMAR BERSALIN')
# hlm. 58: sub-judul 'ALAT RUANG KHUSUS' terbaca sebagai judul tabel dan nama kelompok terpotong; judul asli 'TARIF SEWA ALAT' (dicek visual)
T58 = dict(ttl='TARIF SEWA ALAT', grp='ALAT IGD/BANGSAL')
# hlm. 57: sub-judul 'Gas Medis' terbaca sebagai judul tabel; judul asli 'TARIF PEMAKAIAN CSSD DAN GAS MEDIS' (dicek visual)
G57 = dict(ttl='TARIF PEMAKAIAN CSSD DAN GAS MEDIS', grp='Gas Medis')


def sp(name, rv, alias, **kw):
    return ('KOND000001', name, 44, dict(rank='KELAS', rv=rv, alias=alias, **kw))


U = {
 'Konsultasi Dokter Umum IGD': dict(
    nama='beda', use=[('KONA000002', 'IGD', 44, dict(merged=True))],
    p3="nama item hanya 'IGD' di bawah sel kode KONA000002 yang digabung dengan 'Klinik Dokter Umum' (konsultasi dokter umum IGD)",
    p7="'Klinik Dokter Umum' (poli umum, kode KONA000002 yang sama), 'Konsultasi Spesialis OnCall di IGD (MN)' dan '(OS)' serta versi anestesi (spesialis di IGD), "
       "'Konsultasi Dokter Gigi Umum Oncall di IGD' (gigi), 'Konsultasi Dokter Umum MCU' (MCU), 'Telekonsultasi Umum' (telekonsultasi)"),
 'Konsultasi Spesialis Rawat Inap': dict(
    nama='beda', row_labels={1: 'Varian tingkat dokter'},
    rows={'III': [sp('Spesialis', 'III', 'Jasa Visit Rawat Inap - Spesialis - III'),
                  sp('SubSpesialis/Konsultan', 'III', 'Jasa Visit Rawat Inap - SubSpesialis/Konsultan - III')],
          'II': [sp('Spesialis', 'II', 'Jasa Visit Rawat Inap - Spesialis - II'),
                 sp('SubSpesialis/Konsultan', 'II', 'Jasa Visit Rawat Inap - Spesialis - II')],
          'I & R. KHUSUS': [sp('Spesialis', 'I/ISOLASI', 'Jasa Visit Rawat Inap - Spesialis - I/ISOLASI'),
                            sp('SubSpesialis/Konsultan', 'I/ISOLASI', 'Jasa Visit Rawat Inap - Spesialis - I/ISOLASI')]},
    p3="nama item di kelompok 'Jasa Visit Rawat Inap' hanya 'Spesialis' dan 'SubSpesialis/Konsultan'; tarif per kelas ada di sub-baris kolom 'KELAS' "
       "('I/ISOLASI' memuat kelas I)",
    p5="Excel menaruh tarif 'SubSpesialis/Konsultan' untuk SUITE, EXECUTIVE, I/ISOLASI dan II di bawah nama Spesialis "
       "(\"Jasa Visit Rawat Inap - Spesialis - II\" punya dua tarif 315000 dan 390000), hanya III, ICU, INT, NICU, PERINA yang memakai nama SubSpesialis/Konsultan",
    p7="'Dr. ICU Intensive' (dokter ICU), sub-baris 'KELAS' SUITE, EXECUTIVE (di atas kelas I), ICU, INT, NICU, PERINA (ruang khusus); 'Klinik Dokter Spesialis', "
       "'Klinik Dokter SubSpesialis' (rawat jalan), 'Telekonsultasi Spesialis'; tidak ada visite dokter umum rawat inap"),
 'Ruang Rawat': dict(
    nama='beda', row_labels={1: 'Varian bayi'},
    rows={'III': [('RUAA010008', 'Ruang Rawat - Kelas III', 45, KP), ('RUAA040008', 'Ruang Rawat Bayi - Kelas III', 45, KP)],
          'II': [('RUAA010007', 'Ruang Rawat - Kelas II', 45, KP), ('RUAA040007', 'Ruang Rawat Bayi - Kelas II', 45, KP)],
          'I & R. KHUSUS': [('RUAA010006', 'Ruang Rawat - Kelas I', 45, KP), ('RUAA040006', 'Ruang Rawat Bayi - Kelas I', 45, KP)]},
    p3="varian bayi dimasukkan sebagai varian umur; Excel memberi label \"UMUM/NON-KELAS\" untuk semua kamar sehingga kelas hanya terbaca dari nama item",
    p7="'Ruang Rawat - Suite', 'Ruang Rawat - Eksekutif' (di atas kelas I); 'Ruang Rawat - Isolasi', 'Ruang Rawat - ICU', 'Ruang Rawat - Intermediate', 'Ruang Rawat - Perina', "
       "'Ruang Rawat - NICU' (ruang khusus); versi bayi Suite/Eksekutif; 'Kamar Bersalin - Suite' dkk. (kamar bersalin)"),
 'Jasa Perawatan': dict(
    nama='beda',
    rows={'III': [('RUAA050004', 'Jasa Perawatan - KelasIII', 45, KB)],
          'II': [('RUAA050004', 'Jasa Perawatan - Kelas II', 45, KB)],
          'I & R. KHUSUS': [('RUAA050004', 'Jasa Perawatan - KelasI / Ruang Khusus*', 45, KB)]},
    p4="baris 'Jasa Perawatan' (keterangan 'Jasa Perawatan') berada di bawah baris kelompok 'KAMAR BERSALIN' pada tabel kamar; ejaan 'KelasIII' dan 'KelasI' "
       "tanpa spasi sesuai PDF (dicek visual)",
    p7="'Jasa Perawatan - Suite', 'Jasa Perawatan - Eksekutif' (di atas kelas I); 'Jasa Perawat Pendamping Jabodetabek dengan Ventilator' dkk. (pendampingan)"),
 'Pasang IV Line Access': dict(
    nama='beda', use=[('PRWT000072', 'Pasang IV Line Acces', 101), ('IGDJ000082', 'Vena Seksi', 100, R), ('TINJ000029', 'Vena Seksi', 54, R)],
    p3="'Vena Seksi' adalah akses vena dengan sayatan (cut-down), bukan IV line biasa",
    p4="ejaan 'Acces' sesuai PDF",
    p7="'Aff IV Line Acces' (pelepasan); tidak ada item pasang infus dewasa/anak terpisah"),
 'Injeksi IM / IV': dict(
    nama='beda', use=[('IGDJ000078', 'Injeksi IM/ IV', 99), ('PRWT000029', 'Injeksi IM/ IV', 101)],
    p7="'Injeksi IM/ IV', 'Injeksi IM/IV' dan 'INJEKSI IM/IV' di tabel tindakan poli spesialis/tumbuh kembang (rawat jalan per spesialis), "
       "'Pemberian Injeksi (IM, IV, SC, IC)' (homecare)"),
 'Hematologi Lengkap': dict(
    nama='beda', use=[('LABA100300', 'Darah Lengkap', 109)],
    p7="'Darah Rutin' (parameter lebih sedikit)"),
 'CRP Kuantitatif': dict(
    nama='sama', use=[('LABA320100', 'CRP Kuantitatif', 110, dict(grp='IMMUNOSEROLOGI')), ('LABA321300', 'hs-CRP (R)', 114, R)],
    p3="'hs-CRP (R)' adalah CRP sensitivitas tinggi (pemeriksaan rujukan), bukan CRP kuantitatif standar",
    p7="tidak ada CRP kualitatif/CRP tanpa keterangan"),
 'Thorax PA': dict(
    nama='beda', use=[('RADA030001', 'Thorax AP/PA', 103)],
    p3="satu item 'Thorax AP/PA' mencakup proyeksi AP atau PA (tidak ada item PA saja)",
    p7="'Thorax Lateral', 'Thorax RLD', 'Thorax LLD', 'Thorax Top Lordotik' (proyeksi lain), 'Thorax (AP/PA + Lat)' dan kombinasi AP/PA lainnya; tidak ada versi mobile"),
 'Infusion Pump / hari': dict(
    nama='sama', use=[('ALAD000003', 'Infusion Pump per Hari', 58, T58), ('ALAD000011', 'Infusion Pump < 6 Jam', 58, dict(T58, role='Ragu'))],
    p3="'Infusion Pump < 6 Jam' bersatuan < 6 jam, bukan per hari",
    p7="'Infusion Pump per Hari' kode ALAB000012 (kelompok 'ALAT RUANG KHUSUS', hlm. 58) dan ALAC000097 (sewa alat OK, hlm. 59), tarif sama; versi '< 6 Jam' ALAB000044/ALAC000098"),
 'Syringe Pump / hari': dict(
    nama='sama', use=[('ALAD000012', 'Syringe Pump per Hari', 58, T58), ('ALAD000013', 'Syringe Pump < 6 Jam', 58, dict(T58, role='Ragu'))],
    p3="'Syringe Pump < 6 Jam' bersatuan < 6 jam, bukan per hari",
    p4="tarif 'Syringe Pump per Hari' sama persis dengan 'Infusion Pump per Hari' (375.000 rata di semua kolom) (sesuai PDF, dicek visual)",
    p7="'Syringe Pump per Hari' kode ALAB000024 (kelompok 'ALAT RUANG KHUSUS', hlm. 58) dan ALAC000095 (sewa alat OK, hlm. 59), tarif sama; versi '< 6 Jam' ALAB000045/ALAC000096"),
 'O2 / Hari': dict(
    nama='sama', use=[('ALAE000001', 'O2 Per Hari', 57, G57), ('ALAE000005', 'O2 Per Jam', 57, dict(G57, role='Ragu')),
                      ('ALAE000002', 'O2 <= 6 Jam', 57, dict(G57, role='Ragu'))],
    p3="'O2 Per Jam' bersatuan per jam dan 'O2 <= 6 Jam' bersatuan <= 6 jam, bukan per hari",
    p4="'O2 Per Hari' bertarif sama 900.000 di SUITE dan EXECUTIVE (sesuai PDF, dicek visual)",
    p7="'C - PAP Mask ( O2 + UT )' dan versi per jam (C-PAP), 'O2 Saturasi' (laboratorium)"),
 'Nebulizer': dict(
    nama='beda', use=[('IGDJ000066', 'Tindakan Nebulizer', 99), ('PRWT000065', 'Tindakan Nebulizer', 101),
                      ('RHBB010011', 'Tindakan Nebulizer', 126, dict(ttl='TARIF FISIOTERAPI', grp='PELAYANAN DI LUAR KOMBINASI / PAKET')),
                      ('ALAD000029', 'Nebulizer', 58, T58)],
    p3="'Nebulizer' adalah sewa alat, 'Tindakan Nebulizer' adalah tindakan (keduanya dimasukkan); versi 'TARIF FISIOTERAPI' adalah layanan fisioterapi",
    p7="'Paket Nebulizer' (paket fisioterapi), 'Tindakan Nebulizer' kode ANKJ000012 dan ANPJ000018 (poli anak)"),
 'Creatinin': dict(
    nama='sama', use=[('LABA210200', 'Creatinin', 109)],
    p7="'Creatinin Clearance', 'Creatinin Urin', 'Creatinin Urine Sewaktu' (clearance/urine), 'Albumin / Creatinin Urine Ratio' (rasio urine)"),
 'Ureum': dict(
    nama='sama', use=[('LABA210100', 'Ureum', 109), ('LABA210900', 'BUN', 109, R)],
    p3="'BUN' (blood urea nitrogen) item terpisah dari ureum",
    p7="'Ureum Clearance', 'Ureum Urin', 'Ureum urin sewaktu' (clearance/urine), 'Urea Breat Tes (UBT) (R)' dan 'Urea Breath Tes (UBT) (R)' (tes napas)"),
 'GDS': dict(
    nama='beda', use=[('LABA220300', 'Glukosa Darah Sewaktu', 110)],
    p7="'Glukosa Darah Puasa', 'Glukosa Darah PP', 'Glukosa Toleransi Test' (bukan sewaktu), 'Glukosa' (urinalisa), 'Glukosa (Cairan LCS)' dkk. (cairan tubuh)"),
 'Elektrolit (Na, K, Cl)': dict(
    nama='sama', use=[('LABA260100', 'Elektrolit (Na, K, Cl)', 110)],
    p7="'Natrium', 'Kalium', 'Chlorida' (item satuan; paket tersedia)"),
}
