"""Spec Mitra Keluarga Cibubur (lihat spec_depok.py untuk format)."""
KEY = 'cibubur'
SHEET = 'Mitra Keluarga Cibubur'
PAGE_NOTE = 'hlm. = nomor halaman file PDF, bukan nomor cetak (mis. hlm. 7 = cetak 3)'
SRC = ("tanpa Effective Date di teks PDF (judul tabel 'TAHUN 2026'); 'Tarif diatas dapat berubah sewaktu-waktu tanpa pemberitahuan terlebih dahulu.'")
R = dict(role='Ragu')
FG = dict(grp='Fungsi Ginjal')      # nama kelompok melewati batas kolom di PDF sehingga ekstraksi memotongnya (dicek visual hlm. 10)
U = {
 'Konsultasi Dokter Umum IGD': dict(
    nama='beda', use=[('KONA000002', 'Konsultasi Umum (IGD)', 7)],
    p6="keterangan tabel: tarif belum termasuk tindakan medis",
    p7="'Konsultasi Umum (Poli Umum)' (kode KONA000002 yang sama: poli umum), 'Konsultasi Spesialis OnCall di IGD' dan versi (Konsultan)/(MN)/(OS) (spesialis di IGD), "
       "'Konsultasi Dokter Umum MCU' (MCU), 'Telekonsultasi Dokter Umum' (telekonsultasi)"),
 'Konsultasi Spesialis Rawat Inap': dict(
    nama='sama', use=[('KOND000001', 'Konsultasi Spesialis Rawat Inap', 7),
                      ('KOND000001', 'Konsultasi Spesialis Rawat Inap (Konsultan)', 7, dict(role='Varian tingkat dokter (urutan kolom sama)')),
                      ('KOND000004', 'Konsultasi Dokter Umum Rawat Inap', 7, R)],
    p3="'Konsultasi Dokter Umum Rawat Inap' adalah visite dokter umum, bukan spesialis (padanan lemah)",
    p6="keterangan tabel: tarif belum termasuk tindakan medis",
    p7="'Konsultasi Spesialis Neonatologi (NICU)' (hanya kolom NICU), 'Konsultasi Intensive Care' (hanya kolom ICU), 'Konsultasi Spesialis' dan "
       "'Konsultasi Spesialis (Konsultan)' (rawat jalan), konsultasi spesialis di IGD, 'Telekonsultasi Dokter Spesialis', 'Konsultasi Dokter Spesialis MCU'; "
       "kolom INT, ICU, PERINA, NICU (ruang intensif)"),
 'Ruang Rawat': dict(
    nama='beda', row_labels={1: 'Varian bayi'},
    rows={'III': [('RUAA010008', 'Ruang Rawat - Kelas III', 5), ('RUAA040008', 'Ruang Rawat Bayi - Kelas III', 5)],
          'II': [('RUAA010007', 'Ruang Rawat - Kelas II', 5), ('RUAA040007', 'Ruang Rawat Bayi - Kelas II', 5)],
          'I & R. KHUSUS': [('RUAA010006', 'Ruang Rawat - Kelas I', 5), ('RUAA040006', 'Ruang Rawat Bayi - Kelas I', 5)]},
    p3="varian bayi dimasukkan sebagai varian umur; Excel memberi label \"UMUM/NON-KELAS\" untuk semua kamar sehingga kelas hanya terbaca dari nama item",
    p4="'Ruang Rawat Bayi' bertarif sama 290.000 untuk semua kelas (sesuai PDF, dicek visual)",
    p7="'Ruang Rawat - Suite', 'Ruang Rawat - Eksekutif', 'Ruang Rawat - Utama A', 'Ruang Rawat - Utama B' (di atas kelas I); 'Ruang Rawat - Isolasi', "
       "'Ruang Rawat - ICU', 'Ruang Rawat - Intermediate', 'Ruang Rawat - Perina', 'Ruang Rawat - NICU' (ruang khusus); versi bayi Suite/Eksekutif/Utama; "
       "'Ruang Tambahan - Suite ( Non Pasien )' dkk. (non pasien), 'Recovery Room'"),
 'Jasa Perawatan': dict(
    nama='sama', use=[('RUAA050004', 'Jasa Perawatan', 5)],
    p7="'Jasa Perawat Pendamping Jabodetabek' dan 'Jasa Perawat Pendamping Luar Jabodetabek' (pendampingan)"),
 'Pasang IV Line Access': dict(
    nama='beda', use=[('PRWT000072', 'Pasang IV Line Acces', 36), ('TINJ000029', 'Vena Seksi', 37, R)],
    p3="'Vena Seksi' adalah akses vena dengan sayatan (cut-down), bukan IV line biasa",
    p4="ejaan 'Acces' sesuai PDF",
    p7="'AFF IV Line Acces' (pelepasan); tidak ada item pasang infus dewasa/anak terpisah"),
 'Injeksi IM / IV': dict(
    nama='beda', use=[('IGDJ000078', 'Injeksi IM/ IV', 33), ('PRWT000029', 'Injeksi IM/ IV', 35)],
    p7="'Injeksi IM/ IV' dan 'Injeksi IM/IV' di tabel tindakan poli spesialis (rawat jalan per spesialis), 'Pemberian Injeksi (IM, IV, SC, IC)' (homecare)"),
 'Hematologi Lengkap': dict(
    nama='beda', use=[('LABA100300', 'Darah Lengkap', 9)],
    p7="'Darah Rutin' (parameter lebih sedikit)"),
 'CRP Kuantitatif': dict(
    nama='sama', use=[('LABA320100', 'CRP Kuantitatif', 11, dict(grp='Protein Spesifik')), ('LABA321300', 'hs-CRP (R)', 16, R)],
    p3="'hs-CRP (R)' adalah CRP sensitivitas tinggi (pemeriksaan rujukan), bukan CRP kuantitatif standar",
    p7="tidak ada CRP kualitatif/CRP tanpa keterangan"),
 'Thorax PA': dict(
    nama='beda', use=[('RADA030001', 'Thorax AP/PA', 23)],
    p3="satu item 'Thorax AP/PA' mencakup proyeksi AP atau PA (tidak ada item PA saja)",
    p7="'Thorax Lateral', 'Thorax RLD', 'Thorax LLD', 'Thorax Top Lordotik' (proyeksi lain), 'Thorax (AP/PA + Lat)', 'Thorax AP/PA + RLD', 'Thorax AP/PA + LLD' (kombinasi); "
       "tidak ada versi mobile"),
 'Infusion Pump / hari': dict(
    nama='sama', use=[('ALAD000003', 'Infusion Pump per Hari', 82), ('ALAD000011', 'Infusion Pump < 6 Jam', 82, R)],
    p3="'Infusion Pump < 6 Jam' bersatuan < 6 jam, bukan per hari",
    p7="'Infusion Pump per Hari' kode ALAB000012 (kelompok 'Alat Ruang Khusus', hlm. 81) dan 'Infusion Pump < 6 Jam' kode ALAC000098 (kelompok 'Alat OK', hlm. 82), tarif sama"),
 'Syringe Pump / hari': dict(
    nama='sama', use=[('ALAD000012', 'Syringe Pump per Hari', 82), ('ALAD000013', 'Syringe Pump < 6 Jam', 82, R)],
    p3="'Syringe Pump < 6 Jam' bersatuan < 6 jam, bukan per hari",
    p4="tarif 'Syringe Pump per Hari' sama persis dengan 'Infusion Pump per Hari' (274.000 rata di semua kolom) (sesuai PDF, dicek visual)",
    p7="'Syringe Pump per Hari' kode ALAB000024 (kelompok 'Alat Ruang Khusus', hlm. 81) dan 'Syringe Pump < 6 Jam' kode ALAC000096 (kelompok 'Alat OK', hlm. 82), tarif sama"),
 'O2 / Hari': dict(
    nama='sama', use=[('ALAE000001', 'O2 per Hari', 82), ('ALAE000005', 'O2 per Jam', 82, R)],
    p3="'O2 per Jam' bersatuan per jam",
    p7="'Incubator (Termasuk O2)' (inkubator)"),
 'Nebulizer': dict(
    nama='beda', use=[('IGDJ000066', 'Tindakan Nebulizer', 33), ('RHBB010011', 'Tindakan Nebulizer', 77), ('ALAD000029', 'Nebulizer', 82)],
    p3="'Nebulizer' adalah sewa alat, 'Tindakan Nebulizer' adalah tindakan (keduanya dimasukkan); versi 'Modalitas FisioTerapi' adalah layanan fisioterapi",
    p7="'Nebulizer' kode ALAB000029 (kelompok 'Alat Ruang Khusus', hlm. 81, tarif sama), 'Nebulizer, Clapping, Vibrasi' (paket tindakan perawat)"),
 'Creatinin': dict(
    nama='sama', use=[('LABA210200', 'Creatinin', 10, FG)],
    p7="'Creatinin Clearance', 'Creatinin Urin' (clearance/urine), 'Albumin / Creatinin Urine Ratio (R)' (rasio urine)"),
 'Ureum': dict(
    nama='sama', use=[('LABA210100', 'Ureum', 10, FG), ('LABA210900', 'BUN', 10, dict(role='Ragu', grp='Fungsi Ginjal'))],
    p3="'BUN' (blood urea nitrogen) item terpisah dari ureum",
    p7="'Ureum Clearance', 'Ureum Urin' (clearance/urine), 'Urea Breath Tes (UBT) (R)' (tes napas)"),
 'GDS': dict(
    nama='beda', use=[('LABA220300', 'Glukosa Darah Sewaktu', 10)],
    p7="'Glukosa Darah Puasa', 'Glukosa Darah PP', 'Glukosa Toleransi Test' (bukan sewaktu), 'Glukosa' (urinalisa)"),
 'Elektrolit (Na, K, Cl)': dict(
    nama='sama', use=[('LABA260100', 'Elektrolit (Na, K, Cl)', 10)],
    p7="'Natrium', 'Kalium' (hlm. 10) dan 'Chlorida' (hlm. 11) (item satuan; paket tersedia)"),
}
