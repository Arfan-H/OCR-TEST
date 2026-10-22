"""Spec Mitra Keluarga Kemayoran (lihat spec_depok.py untuk format).
Buku ini bertanda air 'CONTROLLED COPY' (dibuang saat ekstraksi); banyak tabel satu kolom 'TARIF' (non-kelas)."""
KEY = 'kemayoran'
SHEET = 'Mitra Keluarga Kemayoran'
PAGE_NOTE = 'hlm. = nomor halaman file PDF, bukan nomor cetak (mis. hlm. 8 = cetak 5)'
SRC = ("Effective Date per tabel 'PER 1 JANUARI 2026'; biaya administrasi rawat inap terpisah: ADMB000001 (hlm. 4) '7% dari total tagihan'; "
       "'Tarif di atas dapat berubah sewaktu-waktu tanpa pemberitahuan terlebih dahulu.'")
R = dict(role='Ragu')
VT = 'Varian tingkat dokter (urutan kolom sama)'
U = {
 'Konsultasi Dokter Umum IGD': dict(
    nama='beda', use=[('KONA000002', 'Konsultasi Umum (IGD)', 10)],
    p7="'Konsultasi Umum (Poli Umum)' (poli umum), 'Konsultasi Spesialis Oncall IGD (MN)' dan '(OS)' (spesialis di IGD), 'Konsultasi Dokter Umum MCU' (MCU)"),
 'Konsultasi Spesialis Rawat Inap': dict(
    nama='beda', use=[('KOND000001', 'Konsultasi Rawat Inap (Spesialis)', 11), ('KOND000001', 'Konsultasi Rawat Inap (Konsultan)', 11, dict(role=VT)),
                      ('KOND000001', 'Konsultasi Rawat Inap (Subspesialis)', 11, dict(role=VT))],
    p3="tidak ada visite dokter umum rawat inap; nama PDF tersusun 'Konsultasi Rawat Inap (Spesialis)' (urutan kata berbeda dari uraian)",
    p7="'Konsultasi Intensive Care' dan 'Konsultasi NICU' (ICU/NICU); tabel 'TARIF KONSULTASI RAWAT INAP DOKTER KHUSUS' (tarif per nama dokter); 'Konsultasi Spesialis', 'Konsultasi Spesialis (Konsultan)', 'Konsultasi Spesialis (Subspesialis)' "
       "(rawat jalan); 'Konsultasi Spesialis via Telp', 'Telekonsultasi Dokter Spesialis'; kolom 'PRESIDENT SUITE', 'SUITE', 'EXECUTIVE'"),
 'Ruang Rawat': dict(
    nama='beda', row_labels={1: 'Varian bayi'},
    rows={'III': [('RUAA010008', 'Ruang Rawat - Kelas III', 8), ('RUAA040008', 'Ruang Rawat Bayi - Kelas III', 8)],
          'II': [('RUAA010007', 'Ruang Rawat - Kelas II', 8), ('RUAA040007', 'Ruang Rawat Bayi - Kelas II', 8)],
          'I & R. KHUSUS': [('RUAA010006', 'Ruang Rawat - Kelas I', 8), ('RUAA040006', 'Ruang Rawat Bayi - Kelas I', 8)]},
    p3="varian bayi dimasukkan sebagai varian umur; Excel memberi label \"UMUM/NON-KELAS\" untuk semua kamar sehingga kelas hanya terbaca dari nama item",
    p7="'Ruang Rawat - President Suite', 'Ruang Rawat - Suite', 'Ruang Rawat - Executive' (di atas kelas I); 'Ruang Rawat - Isolasi', 'Ruang Rawat - ICU', 'Ruang Rawat - Intermediate', "
       "'Ruang Rawat - Perina', 'Ruang Rawat - NICU' (ruang khusus); ruang bayi di atas kelas I; 'Ruang Tambahan' (non pasien)"),
 'Jasa Perawatan': dict(
    nama='beda',
    rows={'III': [('RUAA050004', 'Jasa Perawatan - Kelas III', 8)], 'II': [('RUAA050004', 'Jasa Perawatan - Kelas II', 8)],
          'I & R. KHUSUS': [('RUAA050004', 'Jasa Perawatan - Kelas I', 8)]},
    p7="'Jasa Perawatan - President Suite', 'Jasa Perawatan - Suite', 'Jasa Perawatan - Executive' (di atas kelas I); 'Jasa Perawat Pendamping' dan varian pendamping (pendampingan)"),
 'Pasang IV Line Access': dict(
    nama='beda', use=[('TINJ000065', 'Pasang IV Line Acces', 65), ('PRWT000072', 'Pasang IV Line Acces', 69), ('TINJ000029', 'Vena Seksi', 64, R)],
    p3="'Vena Seksi' adalah akses vena dengan sayatan (cut-down), bukan IV line biasa",
    p4="ejaan 'Acces' sesuai PDF; tarif satu kolom tanpa beda kelas",
    p7="'Vena Seksi' kode BDAJ000018 (poli bedah anak); tidak ada item pasang infus dewasa/anak terpisah"),
 'Injeksi IM / IV': dict(
    nama='beda', use=[('IGDJ000078', 'Injeksi IM/IV', 13), ('PRWT000029', 'Injeksi IM/ IV', 68)],
    p7="'Injeksi IM/IV' / 'Injeksi IM/ IV' di tabel tindakan poli spesialis (rawat jalan per spesialis), 'Pemberian Injeksi (IM, IV, SC, IC)' (homecare), 'Suntik Intra Konka' (poli THT)"),
 'Hematologi Lengkap': dict(
    nama='beda', use=[('LABA100300', 'Darah lengkap', 89), ('LABA111800', 'Darah Lengkap + IPF', 89, R)],
    p3="'Darah Lengkap + IPF' adalah darah lengkap dengan parameter tambahan (dimasukkan sebagai varian nama)",
    p4="'Darah lengkap' ditulis dengan huruf kecil pada kata lengkap di PDF",
    p7="'Darah Rutin' (parameter lebih sedikit)"),
 'CRP Kuantitatif': dict(
    nama='sama', use=[('LABA320100', 'CRP Kuantitatif', 92), ('LABA321300', 'hs-CRP', 93, R)],
    p3="'hs-CRP' adalah CRP sensitivitas tinggi, bukan CRP kuantitatif standar",
    p4="tarif 'CRP Kuantitatif' sama persis dengan 'Darah Lengkap + IPF' (hlm. 89) di semua kolom (sesuai PDF, dicek visual)",
    p7="tidak ada CRP kualitatif/CRP tanpa keterangan"),
 'Thorax PA': dict(
    nama='beda', use=[('RADA030001', 'Thorax AP/PA', 100)],
    p3="satu item 'Thorax AP/PA' mencakup proyeksi AP atau PA (tidak ada item PA saja)",
    p7="'Thorax Lateral', 'Thorax RLD', 'Thorax LLD', 'Thorax Top Lordotik' (proyeksi lain), 'Thorax (AP/PA + Lat)' dan kombinasi AP/PA lainnya; tidak ada versi mobile"),
 'Infusion Pump / hari': dict(
    nama='beda', use=[('ALAD000003', 'Pemakaian Infus/ Syringe Pump', 85), ('ALAD000011', 'Infusion Pump < 6 Jam', 85, R)],
    p3="di tabel alat IGD/bangsal tidak ada item infusion pump per hari; yang ada 'Pemakaian Infus/ Syringe Pump' (gabungan infus/syringe pump, satuan tidak tertulis) dan "
       "'Infusion Pump < 6 Jam' (satuan < 6 jam)",
    p7="'Infusion Pump' kode ALAB000012 (kelompok 'Alat Ruang Khusus', hlm. 81) dan ALAC000097 (alat OK, hlm. 83), tarif sama 276.000"),
 'Syringe Pump / hari': dict(
    nama='sama', use=[('ALAD000012', 'Syringe Pump per Hari', 85), ('ALAD000013', 'Syringe Pump < 6 Jam', 85, R), ('ALAD000003', 'Pemakaian Infus/ Syringe Pump', 85, R)],
    p3="'Syringe Pump < 6 Jam' bersatuan < 6 jam; 'Pemakaian Infus/ Syringe Pump' adalah item gabungan infus/syringe pump",
    p4="'Syringe Pump per Hari' dan 'Pemakaian Infus/ Syringe Pump' bertarif sama 276.000 (sesuai PDF, dicek visual)",
    p7="'Syringe Pump' kode ALAB000024 (ruang khusus) dan ALAC000095 (alat OK), tarif sama"),
 'O2 / Hari': dict(
    nama='sama', use=[('ALAE000001', 'O2 Per Hari', 86), ('ALAE000005', 'O2 Per Jam', 86, R), ('ALAE000002', 'O2 <= 6 Jam', 86, R)],
    p3="'O2 Per Jam' bersatuan per jam dan 'O2 <= 6 Jam' bersatuan <= 6 jam, bukan per hari",
    p7="'Incubator per Hari', 'Incubator < 6 Jam', 'Incubator Transpot Rujuk' (inkubator)"),
 'Nebulizer': dict(
    nama='beda', use=[('IGDJ000066', 'Tindakan Nebulizer', 13), ('TINJ000079', 'Tindakan Nebulizer', 65), ('PRWT000065', 'Tindakan Nebulizer', 69),
                      ('RHBB010011', 'Tindakan Nebulizer', 70), ('ALAD000029', 'Nebulizer', 86)],
    p3="'Nebulizer' adalah sewa alat, 'Tindakan Nebulizer' adalah tindakan (keduanya dimasukkan); versi 'MODALITAS FISIOTERAPI' adalah layanan fisioterapi",
    p7="'Tindakan Nebulizer' kode PARJ000048 (poli paru), 'Nebulizer' kode ALAB000029 dan ALAC000143 (alat ruang khusus/OK, tarif sama), 'Nebulizer, Clapping, Vibrasi' (gabungan), "
       "'Exercise Nebulizer', 'Paket Nebulizer 5x' dan paket modalitas (paket), 'Home Care Nebulizer' (homecare)"),
 'Creatinin': dict(
    nama='sama', use=[('LABA210200', 'Creatinin', 90)],
    p7="'Creatinin Clearance', 'Creatinin Urin', 'Creatinin Urine Sewaktu' (clearance/urine), 'Albumin / Creatinin Urine Ratio' (rasio urine)"),
 'Ureum': dict(
    nama='sama', use=[('LABA210100', 'Ureum', 90), ('LABA210900', 'BUN', 90, R)],
    p3="'BUN' (blood urea nitrogen) item terpisah dari ureum",
    p4="'BUN' lebih mahal dari 'Ureum' (sesuai PDF, dicek visual)",
    p7="'Ureum Clearance', 'Ureum Urin', 'Ureum urin sewaktu' (clearance/urine), 'Urea Breat Tes (UBT)' dan 'Urea Breath Tes (UBT) (R)' (tes napas)"),
 'GDS': dict(
    nama='beda', use=[('LABA220300', 'Gula Darah Sewaktu', 91)],
    p7="'Gula Darah Puasa', 'Gula Darah PP' (bukan sewaktu), glukosa cairan tubuh/LCS/pleura"),
 'Elektrolit (Na, K, Cl)': dict(
    nama='sama', use=[('LABA260100', 'Elektrolit (Na, K, Cl)', 91), ('LABA261800', 'Elektrolit (Na, K, Cl) Urin', 91, R)],
    p3="'Elektrolit (Na, K, Cl) Urin' adalah pemeriksaan elektrolit pada sampel urine (dimasukkan sebagai varian nama)",
    p7="'Natrium', 'Kalium', 'Chlorida' (item satuan; paket tersedia), 'Natrium Urin', 'Kalium Urin', 'Chlorida Urin' (urine satuan), 'Chlorida (cairan LCS)' (cairan tubuh)"),
}
