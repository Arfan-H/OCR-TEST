"""Spec Mitra Keluarga Slawi (lihat spec_depok.py untuk format; struktur buku sama dengan Tegal)."""
KEY = 'slawi'
SHEET = 'Mitra Keluarga Slawi'
PAGE_NOTE = 'hlm. = nomor halaman file PDF, bukan nomor cetak'
SRC = ("tanpa Effective Date di teks PDF; biaya administrasi rawat inap terpisah: ADMB000001 (hlm. 6) '7% dari total tagihan maksimal'; "
       "'Tarif diatas dapat berubah sewaktu-waktu tanpa pemberitahuan terlebih dahulu.'")
R = dict(role='Ragu')
U = {
 'Konsultasi Dokter Umum IGD': dict(
    nama='beda', use=[('KONA000002', 'Konsultasi Umum (IGD)', 6)],
    p7="'Konsultasi Umum (Poli Umum)' (poli umum), 'Konsultasi Umum (Akupuntur)' (akupuntur), 'Konsultasi Spesialis OnCall di IGD' dan versi (MN) (spesialis di IGD), "
       "'Konsultasi Dokter Umum MCU' (MCU), 'Telekonsultasi Dokter Umum' (telekonsultasi)"),
 'Konsultasi Spesialis Rawat Inap': dict(
    nama='sama', use=[('KOND000001', 'Konsultasi Spesialis Rawat Inap', 6), ('KOND000004', 'Konsultasi Dokter Umum Rawat Inap', 6, R)],
    p3="'Konsultasi Dokter Umum Rawat Inap' adalah visite dokter umum, bukan spesialis (padanan lemah); tidak ada tarif subspesialis/konsultan rawat inap",
    p7="'Konsultasi Intensive Care' (ICU), 'Konsultasi Spesialis', 'Konsultasi Spesialis (Hari Minggu)', 'Konsultasi Spesialis Pasien Covid' (rawat jalan), 'Konsultasi Spesialis via Telp', "
       "'Telekonsultasi Spesialis'; kolom 'VIP' dan 'RJ'"),
 'Ruang Rawat': dict(
    nama='beda', row_labels={1: 'Nama lain di tabel fasilitas', 2: 'Varian bayi'},
    rows={'III': [('RUAA010008', 'Ruang Rawat - Kelas III', 5), ('RUAA010008', 'KELAS III', 3), ('RUAA040008', 'Ruang Rawat Bayi - Kelas III', 5)],
          'II': [('RUAA010007', 'Ruang Rawat - Kelas II', 5), ('RUAA010007', 'KELAS II', 3), ('RUAA040007', 'Ruang Rawat Bayi - Kelas II', 5)],
          'I & R. KHUSUS': [('RUAA010006', 'Ruang Rawat - Kelas I', 5), ('RUAA010006', 'KELAS I', 3), ('RUAA040006', 'Ruang Rawat Bayi - Kelas I', 5)]},
    p3="kamar dewasa tercantum dua kali dengan nama berbeda (kode dan tarif sama): 'Ruang Rawat - Kelas III' dst. di tabel 'TARIF KAMAR PERAWATAN' dan 'KELAS III' dst. "
       "di tabel 'FASILITAS & TARIF KAMAR PERAWATAN' -> keduanya dimasukkan; varian bayi dimasukkan sebagai varian umur",
    p7="'Ruang Rawat - VIP' (di atas kelas I); 'Ruang Rawat - Isolasi', 'Ruang Rawat - Isolasi VIP', 'Ruang Rawat - ICU', 'Ruang Rawat - Intermediate', 'Ruang Rawat - Perina', "
       "'Ruang Rawat - NICU', 'Ruang Rawat - ICCU', 'Ruang Rawat - PICU' (ruang khusus); 'Ruang Rawat Bayi - VIP'; 'Ruang Rawat ODC - Kelas III' dkk. (one day care)"),
 'Jasa Perawatan': dict(
    nama='sama', use=[('RUAA050004', 'Jasa Perawatan', 5)],
    p7="'Jasa Perawat Pendamping Dalam Kota' dan 'Jasa Perawat Pendamping Luar Kota' (pendampingan)"),
 'Pasang IV Line Access': dict(
    nama='beda', use=[('PRWT000072', 'Pasang IV Line Acces', 56), ('IGDJ000082', 'Vena Seksi', 8, R), ('TINJ000029', 'Vena Seksi', 50, R)],
    p3="'Vena Seksi' adalah akses vena dengan sayatan (cut-down), bukan IV line biasa",
    p4="ejaan 'Acces' sesuai PDF",
    p7="tidak ada item pasang infus dewasa/anak terpisah"),
 'Injeksi IM / IV': dict(
    nama='beda', use=[('IGDJ000078', 'Injeksi IM/ IV', 8), ('TINJ000162', 'Injeksi IM/IV', 51), ('PRWT000029', 'Injeksi IM/ IV', 55)],
    p7="'Injeksi IM/IV' dan 'Injeksi IM/ IV' di tabel tindakan poli spesialis (rawat jalan per spesialis), 'Pemberian Injeksi (IM, IV, SC, IC)' dan "
       "'Memandikan Pasien, Suntik, Perawatan Luka' (homecare)"),
 'Hematologi Lengkap': dict(
    nama='beda', use=[('LABA100300', 'Darah Lengkap', 57)],
    p7="'Darah Rutin' (parameter lebih sedikit)"),
 'CRP Kuantitatif': dict(
    nama='sama', use=[('LABA320100', 'CRP Kuantitatif', 58), ('LABA321300', 'hs-CRP (R)', 62, R)],
    p3="'hs-CRP (R)' adalah CRP sensitivitas tinggi (pemeriksaan rujukan), bukan CRP kuantitatif standar",
    p7="tidak ada CRP kualitatif/CRP tanpa keterangan"),
 'Thorax PA': dict(
    nama='beda', use=[('RADA030001', 'Thorax AP/PA', 68)],
    p3="satu item 'Thorax AP/PA' mencakup proyeksi AP atau PA (tidak ada item PA saja)",
    p7="'Thorax Lateral', 'Thorax RLD', 'Thorax LLD', 'Thorax Top Lordotik' (proyeksi lain), 'Thorax (AP/PA + Lat)' dan kombinasi AP/PA lainnya; tidak ada versi mobile"),
 'Infusion Pump / hari': dict(
    nama='sama', use=[('ALAD000003', 'Infusion Pump per Hari', 37), ('ALAD000011', 'Infusion Pump < 6 Jam', 37, R)],
    p3="'Infusion Pump < 6 Jam' bersatuan < 6 jam, bukan per hari",
    p7="'Infusion Pump per Hari' kode ALAB000012 (kelompok 'Alat Ruang Khusus', hlm. 39, tarif lebih rendah)"),
 'Syringe Pump / hari': dict(
    nama='sama', use=[('ALAD000012', 'Syringe Pump per Hari', 37), ('ALAD000013', 'Syringe Pump < 6 Jam', 37, R)],
    p3="'Syringe Pump < 6 Jam' bersatuan < 6 jam, bukan per hari",
    p4="tarif 'Syringe Pump per Hari' sama persis dengan 'Infusion Pump per Hari' di semua kolom (sesuai PDF, dicek visual)",
    p7="kode ALAB000024/ALAB000045 (kelompok 'Alat Ruang Khusus', hlm. 39) dan ALAC000095/ALAC000096 (kelompok 'Alat OK', hlm. 41), tarif berbeda"),
 'O2 / Hari': dict(
    nama='sama', use=[('ALAE000001', 'O2 per Hari', 40), ('ALAE000005', 'O2 per Jam', 40, R)],
    p3="'O2 per Jam' bersatuan per jam",
    p7="'O2 per 1.5 M3' (hanya kolom RJ, satuan volume), 'Incubator (Termasuk O2)' (inkubator)"),
 'Nebulizer': dict(
    nama='beda', use=[('IGDJ000066', 'Tindakan Nebulizer', 8), ('RHBB010011', 'Tindakan Nebulizer', 10), ('TINJ000079', 'Tindakan Nebulizer', 50),
                      ('PRWT000065', 'Tindakan Nebulizer', 56), ('ALAD000029', 'Nebulizer', 37)],
    p3="'Nebulizer' adalah sewa alat, 'Tindakan Nebulizer' adalah tindakan (keduanya dimasukkan); versi 'Modalitas Fisioterapi' adalah layanan fisioterapi",
    p7="'Nebulizer' kode ALAB000029 dan ALAC000143 (alat ruang khusus/OK, tarif sama), 'Nebulizer, Clapping, Vibrasi' (gabungan), 'Exercise Nebulizer' (exercise), "
       "'Tindakan Nebulizer' di tabel poli spesialis"),
 'Creatinin': dict(
    nama='sama', use=[('LABA210200', 'Creatinin', 57)],
    p7="'Creatinin Clearance (R)', 'Creatinin Urin (R)' (clearance/urine)"),
 'Ureum': dict(
    nama='sama', use=[('LABA210100', 'Ureum', 57)],
    p7="'Ureum Clearance (R)', 'Ureum Urin (R)' (clearance/urine), 'Urea Breat Tes (UBT) (R)' (tes napas); tidak ada item BUN"),
 'GDS': dict(
    nama='beda', use=[('LABA220300', 'Glukosa Darah Sewaktu', 57)],
    p7="'Glukosa Darah Puasa', 'Glukosa Darah PP', 'Glukosa Toleransi Test' (bukan sewaktu)"),
 'Elektrolit (Na, K, Cl)': dict(
    nama='sama', use=[('LABA260100', 'Elektrolit (Na, K, Cl)', 58)],
    p7="'Natrium', 'Kalium', 'Chlorida' (item satuan; paket tersedia), 'Natrium Urin (R)', 'Kalium Urin (R)', 'Chlorida Urin (R)' (urine)"),
}
