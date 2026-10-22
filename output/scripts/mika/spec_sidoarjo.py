"""Spec Mitra Keluarga Sidoarjo (lihat spec_depok.py untuk format; tata letak buku sama dengan Pondok Tjandra)."""
KEY = 'sidoarjo'
SHEET = 'Mitra Keluarga Sidoarjo'
PAGE_NOTE = 'hlm. = nomor halaman file PDF, bukan nomor cetak'
SRC = ("tanpa Effective Date; buku disahkan 'Sidoarjo, 27 November 2025' (hlm. 3); biaya administrasi rawat inap terpisah: ADMB000001 (hlm. 4) "
       "'8% dari Total Tagihan Maksimal'; 'Harga dapat berubah sewaktu - waktu tanpa pemberitahuan terlebih dahulu' (hlm. 3)")
R = dict(role='Ragu')
VT = 'Varian tingkat dokter (urutan kolom sama)'
U = {
 'Konsultasi Dokter Umum IGD': dict(
    nama='beda', use=[('KONA000002', 'Konsultasi Umum (IGD)', 6)],
    p7="'Konsultasi Umum (Poli Umum)' (poli umum), 'Konsultasi Spesialis OnCall di IGD (Spesialis)', 'Konsultasi Spesialis OnCall di IGD (Konsultan)' dan "
       "'Konsultasi Spesialis Oncall IGD (MN)' (spesialis di IGD), 'Konsultasi Dokter Umum MCU' (MCU), 'Konsultasi Dokter Gigi Umum Oncall di IGD' (gigi)"),
 'Konsultasi Spesialis Rawat Inap': dict(
    nama='sama', use=[('KOND000001', 'Konsultasi Spesialis Rawat Inap', 7), ('KOND000001', 'Konsultasi Spesialis Rawat Inap (Konsultan)', 7, dict(role=VT)),
                      ('KOND000001', 'Konsultasi Spesialis Rawat Inap (Professor)', 7, dict(role=VT)),
                      ('KOND000001', 'Konsultasi Spesialis Rawat Inap (Konsultan ginjal)', 7, dict(role=VT)),
                      ('KOND000004', 'Konsultasi Dokter Umum', 7, R)],
    p3="'Konsultasi Dokter Umum' (tabel konsultasi rawat inap) adalah visite dokter umum, bukan spesialis (padanan lemah); kolom kelas 1 juga mencakup UTAMA/ISO/PERINA",
    p7="kolom 'ICU, ICCU, NICU, PICU, NINT, INT, IMC' (intensif); 'Konsultasi Spesialis' dan varian (Konsultan)/(Professor)/(Konsultan Ginjal) (rawat jalan); "
       "'Konsultasi Spesialis OnCall di IGD (Spesialis)' (IGD); 'Telekonsultasi Spesialis' (telekonsultasi); 'Konsultasi Dokter Spesialis MCU' (MCU)"),
 'Ruang Rawat': dict(
    nama='beda', row_labels={1: 'Varian bayi'},
    rows={'III': [('RUAA010008', 'Ruang Rawat - Kelas III', 8), ('RUAA040008', 'Ruang Rawat Bayi - Kelas III', 8)],
          'II': [('RUAA010007', 'Ruang Rawat - Kelas II', 8), ('RUAA040007', 'Ruang Rawat Bayi - Kelas II', 8)],
          'I & R. KHUSUS': [('RUAA010006', 'Ruang Rawat - Kelas I', 8), ('RUAA040006', 'Ruang Rawat Bayi - Kelas I', 8)]},
    p3="varian bayi dimasukkan sebagai varian umur; Excel memberi label \"UMUM/NON-KELAS\" untuk semua kamar sehingga kelas hanya terbaca dari nama item",
    p7="'Ruang Rawat - Suite', 'Ruang Rawat - Eksekutif' (di atas kelas I); 'Ruang Rawat - Isolasi', 'Ruang Rawat - ICU', 'Ruang Rawat - Intermediate', 'Ruang Rawat - Perina', "
       "'Ruang Rawat - NICU', 'Ruang Rawat - ICCU', 'Ruang Rawat - PICU', 'Ruang Rawat - NINT' (ruang khusus); 'Ruang Rawat ODC - Kelas III' (one day care); ruang bayi Suite/Eksekutif"),
 'Jasa Perawatan': dict(
    nama='sama', use=[('RUAA050004', 'Jasa Perawatan', 9)],
    p3="item berada di bawah kelompok 'KAMAR OPERASI' padahal berkode RUAA (keluarga kode ruang rawat); satuan (per hari/per tindakan) tidak tertulis",
    p7="'Jasa Perawat Pendamping Dalam Kota', 'Jasa Perawat Pendamping Luar Kota', 'Jasa Perawat Pendamping Luar Jatim' (pendampingan)"),
 'Pasang IV Line Access': dict(
    nama='beda', use=[('TINJ000065', 'Pasang IV Line Acces', 14), ('PRWT000072', 'Pasang IV Line Acces', 16), ('TINJ000029', 'Vena Seksi', 14, R)],
    p3="'Vena Seksi' adalah akses vena dengan sayatan (cut-down), bukan pemasangan IV line biasa",
    p4="ejaan 'Acces' sesuai PDF",
    p7="'Memasang / Melepas Infus' (homecare), 'Pasang CVC' (vena sentral); tidak ada item pasang infus anak/dewasa terpisah"),
 'Injeksi IM / IV': dict(
    nama='beda', use=[('TINJ000162', 'Injeksi IM/IV', 15), ('PRWT000029', 'Injeksi IM/ IV', 16)],
    p7="'Injeksi IM/IV' / 'Injeksi IM/ IV' di tabel tindakan poli spesialis (rawat jalan per spesialis), 'Pemberian Injeksi (IM, IV, SC, IC)' (homecare)"),
 'Hematologi Lengkap': dict(
    nama='beda', use=[('LABA100300', 'Darah Lengkap', 27)],
    p7="'Darah Rutin' (parameter lebih sedikit)"),
 'CRP Kuantitatif': dict(
    nama='sama', use=[('LABA320100', 'CRP Kuantitatif', 31), ('LABA321300', 'hs-CRP', 31, R)],
    p3="'hs-CRP' adalah CRP sensitivitas tinggi, bukan CRP kuantitatif standar",
    p7="tidak ada CRP kualitatif/CRP tanpa keterangan"),
 'Thorax PA': dict(
    nama='beda', use=[('RADA030001', 'Thorax AP/PA', 39)],
    p3="satu item 'Thorax AP/PA' mencakup proyeksi AP atau PA (tidak ada item PA saja)",
    p7="'Thorax Lateral', 'Thorax Oblique', 'Thorax RLD', 'Thorax LLD', 'Thorax Top Lordotik' (proyeksi lain), 'Thorax (AP/PA + Lat)' dan 'Thorax (AP/PA + Oblique)' (kombinasi); tidak ada versi mobile"),
 'Infusion Pump / hari': dict(
    nama='beda', use=[('ALAD000003', 'Infusion Pump', 24)],
    p3="nama PDF 'Infusion Pump' tanpa keterangan satuan per hari",
    p7="'Infusion Pump' kode ALAB000012 (kelompok 'ALAT RUANG KHUSUS', hlm. 22) dan ALAC000097 (alat OK, hlm. 23), tarif sama; tidak ada versi < 6 jam"),
 'Syringe Pump / hari': dict(
    nama='sama', use=[('ALAD000012', 'Syringe Pump per Hari', 24)],
    p4="tarif 'Syringe Pump per Hari' sama persis dengan 'Infusion Pump' di semua kolom (sesuai PDF, dicek visual)",
    p7="'Syringe Pump' kode ALAB000024 (kelompok 'ALAT RUANG KHUSUS', hlm. 22) dan ALAC000095 (alat OK, hlm. 23), tarif sama"),
 'O2 / Hari': dict(
    nama='sama', use=[('ALAE000001', 'O2 Per Hari', 24), ('ALAE000005', 'O2 Per Jam', 24, R)],
    p3="'O2 Per Jam' bersatuan per jam",
    p7="'Incubator ( Termasuk O2 )' (inkubator)"),
 'Nebulizer': dict(
    nama='beda', use=[('TINJ000079', 'Tindakan Nebulizer', 15, dict(grp='TARIF TINDAKAN MEDIS KHUSUS')), ('PRWT000065', 'Tindakan Nebulizer', 16),
                      ('RHBB010011', 'Tindakan Nebulizer', 19), ('ALAD000029', 'Nebulizer', 24)],
    p3="'Nebulizer' adalah sewa alat, 'Tindakan Nebulizer' adalah tindakan (alat vs tindakan, keduanya dimasukkan); versi 'Modalitas Fisoterapi' adalah layanan fisioterapi",
    p7="'Nebulizer' kode ALAB000029 (kelompok 'ALAT RUANG KHUSUS', tarif sama); obat nebulisasi (farmasi)"),
 'Creatinin': dict(
    nama='sama', use=[('LABA210200', 'Creatinin', 29)],
    p7="'Creatinin Clearance (R)', 'Creatinin Urine Sewaktu (R)' (clearance/urine), 'Albumin / Creatinin Urine Ratio (R)' (rasio urine)"),
 'Ureum': dict(
    nama='sama', use=[('LABA210100', 'Ureum', 29), ('LABA210900', 'BUN', 29, R)],
    p3="'BUN' (blood urea nitrogen) adalah parameter turunan ureum, item terpisah di buku",
    p4="'BUN' bertarif sama persis dengan 'Ureum' dan 'Creatinin' (sesuai PDF, dicek visual)",
    p7="'Ureum Clearance (R)' (clearance), 'Urea Breath Tes (UBT) (R)' (tes napas)"),
 'GDS': dict(
    nama='beda', use=[('LABA220300', 'Glukosa Darah Sewaktu', 29)],
    p7="'Glukosa Darah Puasa', 'Glukosa Darah PP', 'Glukosa Toleransi Test (R)' (bukan sewaktu), 'Glukosa' (urinalisa)"),
 'Elektrolit (Na, K, Cl)': dict(
    nama='sama', use=[('LABA260100', 'Elektrolit (Na, K, Cl)', 30)],
    p7="'Natrium', 'Kalium', 'Chlorida' (item satuan; paket tersedia), 'Natrium Urin (R)', 'Kalium Urin (R)', 'Chlorida Urin (R)' (urine)"),
}
