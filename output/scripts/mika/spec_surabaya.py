"""Spec Mitra Keluarga Surabaya (lihat spec_depok.py untuk format)."""
KEY = 'surabaya'
SHEET = 'Mitra Keluarga Surabaya'
PAGE_NOTE = 'hlm. = nomor halaman file PDF, bukan nomor cetak (mis. hlm. 11 = cetak Page 7)'
SRC = ("tanpa Effective Date di teks PDF (judul tabel memuat tahun 2026); biaya administrasi rawat inap terpisah: ADMB000001 (hlm. 4) '8% dari Total Tagihan'; "
       "'Harga dapat berubah sewaktu-waktu tanpa ada pemberitahuan terlebih dahulu'")
R = dict(role='Ragu')
U = {
 'Konsultasi Dokter Umum IGD': dict(
    nama='beda', use=[('KONA000002', 'Dokter Umum I G D', 11)],
    p4="kata IGD ditulis berspasi 'I G D' di PDF (sesuai PDF, dicek visual)",
    p7="'Dokter Umum' (kode KONA000002 yang sama, 128.000: poli umum), 'Dokter Spesialis Rank 1 (Konsultasi Spesialis OnCall di IGD)' dst. dan 'IGD Midnight on call' "
       "(spesialis di IGD), 'Dokter Umum MCU' (MCU)"),
 'Konsultasi Spesialis Rawat Inap': dict(
    nama='beda', use=[('KOND000001', 'Konsultasi Dokter Spesialis', 13),
                      ('KOND000001', 'Konsultasi Dokter Spesialis Konsultan', 13, dict(role='Varian tingkat dokter (urutan kolom sama)')),
                      ('KOND000001', 'Konsultasi Profesor', 13, dict(role='Varian tingkat dokter (urutan kolom sama)')),
                      ('KOND000004', 'Dokter Umum Ruang Khusus', 13, R)],
    p3="'Dokter Umum Ruang Khusus' adalah visite dokter umum, bukan spesialis (padanan lemah)",
    p7="'Dokter Konsultan Intensive Care' (hanya kolom ICU), kolom 'Suite', 'Eksekutif' (di atas kelas I) dan 'ICU, ICCU, NICU, NINT, IMC' (ruang intensif); "
       "'Dokter Spesialis Rank 1' dst. (rawat jalan)"),
 'Ruang Rawat': dict(
    nama='beda', row_labels={1: 'Varian bayi'},
    rows={'III': [('RUAA010008', 'Ruang Rawat - Kelas III', 6), ('RUAA040008', 'Ruang Rawat Bayi - Kelas III', 6)],
          'II': [('RUAA010007', 'Ruang Rawat - Kelas II', 6), ('RUAA040007', 'Ruang Rawat Bayi - Kelas II', 6)],
          'I & R. KHUSUS': [('RUAA010006', 'Ruang Rawat - Kelas I', 6), ('RUAA040006', 'Ruang Rawat Bayi - Kelas I', 6)]},
    p3="varian bayi dimasukkan sebagai varian umur; Excel memberi label \"UMUM/NON-KELAS\" untuk semua kamar sehingga kelas hanya terbaca dari nama item",
    p7="'Ruang Rawat - Suite', 'Ruang Rawat - Eksekutif' (di atas kelas I); 'Ruang Rawat - Isolasi', 'Ruang Rawat - ICU', 'Ruang Rawat - Intermediate', 'Ruang Rawat - Perina', "
       "'Ruang Rawat - NICU', 'Ruang Rawat - ICCU', 'Ruang Rawat - NINT' (ruang khusus); versi bayi Suite/Eksekutif; 'Ruang Tambahan - Suite ( Non Pasien )' dkk."),
 'Jasa Perawatan': dict(
    nama='sama', use=[('RUAA050004', 'Jasa Perawatan', 7)],
    p4="'Jasa Perawatan' tercantum di tabel 'RUANG TINDAKAN' kelompok 'RUANG TINDAKAN OPERASI', bukan di tabel ruang perawatan (sesuai PDF, dicek visual)",
    p7="'Jasa Perawat Pendamping' (IGDJ000056, PRWT000031) dan varian Dalam Kota/Luar Kota/Luar Jatim/Domestik/International (pendampingan)"),
 'Pasang IV Line Access': dict(
    nama='beda', use=[('PRWT000072', 'Pasang IV Line Acces', 19), ('IGDJ000082', 'Vena Seksi', 17, R), ('TINJ000029', 'Vena Seksi', 80, R)],
    p3="'Vena Seksi' adalah akses vena dengan sayatan (cut-down), bukan IV line biasa",
    p4="ejaan 'Acces' sesuai PDF",
    p7="'Suntikan Melalui Surflo' (homecare); tidak ada item pasang infus dewasa/anak terpisah"),
 'Injeksi IM / IV': dict(
    nama='beda', use=[('IGDJ000078', 'Injeksi IM/IV', 17), ('PRWT000029', 'Injeksi IM/ IV', 18)],
    p7="'Injeksi IM/IV' dan 'Injeksi IM/ IV' di tabel tindakan poli spesialis (rawat jalan per spesialis), 'Pemberian Injeksi (IM IV SC IC)' (homecare)"),
 'Hematologi Lengkap': dict(
    nama='beda', use=[('LABA100300', 'Darah Lengkap', 105), ('LABA111800', 'Darah Lengkap + IPF', 105, R)],
    p3="'Darah Lengkap + IPF' adalah darah lengkap dengan parameter tambahan (dimasukkan sebagai varian nama)",
    p7="'Darah Rutin' (parameter lebih sedikit)"),
 'CRP Kuantitatif': dict(
    nama='sama', use=[('LABA320100', 'CRP Kuantitatif', 112), ('LABA321300', 'hs-CRP', 112, R)],
    p3="'hs-CRP' adalah CRP sensitivitas tinggi, bukan CRP kuantitatif standar",
    p7="tidak ada CRP kualitatif/CRP tanpa keterangan"),
 'Thorax PA': dict(
    nama='beda', use=[('RADA030001', 'Thorax AP/PA', 125)],
    p3="satu item 'Thorax AP/PA' mencakup proyeksi AP atau PA (tidak ada item PA saja)",
    p7="'Thorax Lateral', 'Thorax Oblique', 'Thorax RLD', 'Thorax LLD', 'Thorax Top Lordotik' (proyeksi lain), 'Thorax (AP/PA + Lat)', 'Thorax (AP/PA + Oblique)' "
       "(kombinasi); tidak ada versi mobile"),
 'Infusion Pump / hari': dict(
    nama='sama', use=[('ALAD000003', 'Infusion Pump per Hari', 101), ('ALAD000011', 'Infusion Pump < 6 Jam', 101, R)],
    p3="'Infusion Pump < 6 Jam' bersatuan < 6 jam, bukan per hari",
    p7="'Infusion Pump per Hari' kode ALAB000012 (kelompok 'Alat Ruang Khusus', hlm. 99) dan ALAC000097 (kelompok 'Alat OK', hlm. 100), tarif lebih tinggi; "
       "versi '< 6 Jam' ALAB000044/ALAC000098"),
 'Syringe Pump / hari': dict(
    nama='sama', use=[('ALAD000012', 'Syringe Pump per Hari', 101), ('ALAD000013', 'Syringe Pump < 6 Jam', 101, R)],
    p3="'Syringe Pump < 6 Jam' bersatuan < 6 jam, bukan per hari",
    p4="tarif 'Syringe Pump per Hari' sama persis dengan 'Infusion Pump per Hari' kode ALAD000003 (sesuai PDF, dicek visual)",
    p7="'Syringe Pump per Hari' kode ALAB000024 (kelompok 'Alat Ruang Khusus', hlm. 99) dan ALAC000095 (kelompok 'Alat OK', hlm. 100), tarif sama; versi '< 6 Jam' ALAB000045/ALAC000096"),
 'O2 / Hari': dict(
    nama='sama', use=[('ALAE000001', 'O2 Per Hari', 102), ('ALAE000005', 'O2 Per Jam', 102, R)],
    p3="'O2 Per Jam' bersatuan per jam",
    p7="'Incubator (Termasuk O2)' (inkubator)"),
 'Nebulizer': dict(
    nama='beda', use=[('IGDJ000066', 'Tindakan Nebulizer', 17), ('PRWT000065', 'Tindakan Nebulizer', 19), ('RHBB010011', 'Tindakan Nebulizer', 77),
                      ('ALAD000029', 'Nebulizer', 102)],
    p3="'Nebulizer' adalah sewa alat, 'Tindakan Nebulizer' adalah tindakan (keduanya dimasukkan); versi fisioterapi adalah layanan rehabilitasi medik",
    p7="'Nebulizer' kode ALAB000029 (kelompok 'Alat Ruang Khusus', hlm. 99), 'Nebulizer Clapping Vibrasi' (paket), 'Exercise Nebulizer' (exercise), "
       "'Tindakan Nebulizer' kode PDMJ000020 (poli penyakit dalam)"),
 'Creatinin': dict(
    nama='sama', use=[('LABA210200', 'Creatinin', 108)],
    p7="'Creatinin Clearance', 'Creatinin Urine Sewaktu' (clearance/urine), 'Albumin / Creatinin Urine Ratio (R)' (rasio urine)"),
 'Ureum': dict(
    nama='sama', use=[('LABA210100', 'Ureum', 108)],
    p7="'Urea Breath Tes (UBT) (R)' (tes napas); tidak ada item BUN"),
 'GDS': dict(
    nama='beda', use=[('LABA220300', 'Glukosa Darah Sewaktu', 108)],
    p7="'Glukosa Darah Puasa', 'Glukosa Darah PP', 'Glukosa Toleransi Test' (bukan sewaktu), 'Glukosa (Cairan LCS)', 'Glukosa (Cairan Tubuh)' (cairan tubuh)"),
 'Elektrolit (Na, K, Cl)': dict(
    nama='sama', use=[('LABA260100', 'Elektrolit (Na, K, Cl)', 109)],
    p7="'Elektrolit (Na, K, Cl) Urin (R)' (urine, rujukan)"),
}
