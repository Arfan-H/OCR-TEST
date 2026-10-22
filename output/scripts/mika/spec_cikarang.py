"""Spec Mitra Keluarga Cikarang (lihat spec_depok.py untuk format)."""
KEY = 'cikarang'
SHEET = 'Mitra Keluarga Cikarang'
PAGE_NOTE = 'hlm. = nomor halaman file PDF, bukan nomor cetak (mis. hlm. 9 = cetak 7)'
SRC = ("Effective Date per tabel 'PER 1 JANUARI 2026'; biaya administrasi rawat inap terpisah: ADMB000001 (hlm. 7) '5% dari Total Tagihan maksimal'; "
       "'Tarif diatas dapat berubah sewaktu-waktu tanpa pemberitahuan terlebih dahulu'")
R = dict(role='Ragu')
# hlm. 61 adalah lanjutan tabel hlm. 60 tanpa judul; ekstraksi membaca baris kelompok 'GAS MEDIS' sebagai judul dan memotong nama kelompok
# (dicek visual hlm. 60-61)
T61 = dict(ttl='TARIF PEMAKAIAN ALAT & GAS', grp='ALAT IGD/BANGSAL')
G61 = dict(ttl='TARIF PEMAKAIAN ALAT & GAS')
KIMIA = dict(grp='KIMIA')            # hlm. 80 melanjutkan kelompok 'KIMIA' dari hlm. 79 (dicek visual)
U = {
 'Konsultasi Dokter Umum IGD': dict(
    nama='beda', use=[('KONA000002', 'IGD', 9, dict(merged=True))],
    p3="nama item hanya 'IGD' di bawah sel kode KONA000002 yang digabung dengan 'Klinik Dokter Umum' (konsultasi dokter umum IGD)",
    p6="keterangan tabel: tarif belum termasuk tindakan medis",
    p7="'Klinik Dokter Umum' (poli umum, kode KONA000002 yang sama), 'Dokter Spesialis On Call IGD', 'Konsultasi Spesialis OnCall di IGD (MN)' dan '(OS)' (spesialis di IGD), "
       "'Konsultasi Dokter Umum MCU' (MCU), 'Konsultasi Dokter Umum - Vaksin Covid' (vaksin), 'Telekonsultasi Dokter Umum' (telekonsultasi)"),
 'Konsultasi Spesialis Rawat Inap': dict(
    nama='beda', use=[('KOND000001', 'Spesialis', 9),
                      ('KOND000001', 'Spesialis Bedah Syaraf', 9, dict(role='Varian spesialisasi (urutan kolom sama)')),
                      ('KOND000001', 'Sub Spesialis atau Konsulen', 9, dict(role='Varian tingkat dokter (urutan kolom sama)')),
                      ('KOND000004', 'Dokter Umum', 9, R)],
    p3="nama item di kelompok 'Jasa Visit Rawat Inap' hanya 'Spesialis' (visite spesialis rawat inap); 'Dokter Umum' (KOND000004) adalah visite dokter umum, bukan spesialis (padanan lemah)",
    p6="keterangan tabel: tarif belum termasuk tindakan medis",
    p7="'Dokter ICU/NICU' (hanya kolom ICU/NICU), kolom SUITE, EXECUTIVE (di atas kelas I), INT, ICU, PERINA, NICU, ISOLASI (ruang khusus) dan POLI; "
       "'Klinik Dokter Spesialis', 'Klinik Dokter Sub Spesialis' (rawat jalan), 'Telekonsultasi Dokter Spesialis', 'Konsultasi Dokter Spesialis MCU'"),
 'Ruang Rawat': dict(
    nama='beda', row_labels={1: 'Varian bayi'},
    rows={'III': [('RUAA010008', 'Ruang Rawat - Kelas III', 8), ('RUAA040008', 'Ruang Rawat Bayi - Kelas III', 8)],
          'II': [('RUAA010007', 'Ruang Rawat - Kelas II', 8), ('RUAA040007', 'Ruang Rawat Bayi - Kelas II', 8)],
          'I & R. KHUSUS': [('RUAA010006', 'Ruang Rawat - Kelas I', 8, dict(alias='Ruang Rawat - Kelas I PERAWATAN')),
                            ('RUAA040006', 'Ruang Rawat Bayi - Kelas I', 8, dict(alias='Ruang Rawat Bayi - Kelas I PERAWATAN'))]},
    p3="varian bayi dimasukkan sebagai varian umur; Excel memberi label \"UMUM/NON-KELAS\" untuk semua kamar sehingga kelas hanya terbaca dari nama item",
    p4="Excel menambahkan kata PERAWATAN (isi kolom 'JENIS KAMAR' yang digabung) ke nama kamar kelas I, tetapi tidak ke kelas II/III",
    p7="'Ruang Rawat - Suite', 'Ruang Rawat - Executive' (di atas kelas I); 'Ruang Rawat - Isolasi', 'Ruang Rawat - ICU', 'Ruang Rawat - Intermediate', "
       "'Ruang Rawat - Perina', 'Ruang Rawat - NICU' (ruang khusus); 'Ruang Rawat Bayi - Suite', 'Ruang Rawat Bayi - Executive'; "
       "'Ruang Rawat Bayi - Bayi Tinggal' (bayi tinggal, 328.000 rata per jenis kamar)"),
 'Jasa Perawatan': dict(
    nama='sama',
    rows={'III': [('RUAA050004', 'Jasa Perawatan', 8, dict(rank='JENIS KAMAR', rv='III', alias='Jasa Perawatan – III'))],
          'II': [('RUAA050004', 'Jasa Perawatan', 8, dict(rank='JENIS KAMAR', rv='II', alias='Jasa Perawatan – II'))],
          'I & R. KHUSUS': [('RUAA050004', 'Jasa Perawatan', 8, dict(rank='JENIS KAMAR', rv='I', alias='Jasa Perawatan - I'))]},
    p3="satu kode RUAA050004 dengan tarif berbeda per isi kolom 'JENIS KAMAR' (SUITE, EXECUTIVE, I, II, III); tiap kelas memakai baris jenis kamarnya",
    p7="baris 'JENIS KAMAR' SUITE dan EXECUTIVE; 'Jasa Perawat Pendamping' (IGDJ000056, PRWT000031) dan varian Jabodetabek/Luar Jabodetabek (pendampingan)"),
 'Pasang IV Line Access': dict(
    nama='beda', use=[('PRWT000072', 'Pasang IV Line Acces', 50), ('TINJ000029', 'Vena Seksi', 12, R)],
    p3="'Vena Seksi' adalah akses vena dengan sayatan (cut-down), bukan IV line biasa",
    p4="ejaan 'Acces' sesuai PDF",
    p7="tidak ada item pasang infus dewasa/anak terpisah"),
 'Injeksi IM / IV': dict(
    nama='beda', use=[('IGDJ000078', 'Injeksi IM/IV', 11), ('PRWT000029', 'Injeksi IM/ IV', 49)],
    p7="'Injeksi IM/IV' dan 'Injeksi IM/ IV' di tabel tindakan klinik spesialis (rawat jalan per spesialis), 'Pemberian Injeksi (IM, IV, SC, IC)' (homecare), "
       "'Memandikan Pasien dan Tindakan Suntik' (homecare)"),
 'Hematologi Lengkap': dict(
    nama='beda', use=[('LABA100300', 'Darah Lengkap', 79)],
    p7="'Darah Rutin' (parameter lebih sedikit)"),
 'CRP Kuantitatif': dict(
    nama='sama', use=[('LABA320100', 'CRP Kuantitatif', 80, dict(grp='IMMUNOSEROLOGI')), ('LABA321300', 'hs-CRP (R)', 86, R)],
    p3="'hs-CRP (R)' adalah CRP sensitivitas tinggi (pemeriksaan rujukan), bukan CRP kuantitatif standar",
    p7="tidak ada CRP kualitatif/CRP tanpa keterangan"),
 'Thorax PA': dict(
    nama='beda', use=[('RADA030001', 'Thorax AP/PA', 71, dict(grp='THORAX-ABDOMEN'))],
    p3="satu item 'Thorax AP/PA' mencakup proyeksi AP atau PA (tidak ada item PA saja)",
    p7="'Thorax Lateral', 'Thorax RLD', 'Thorax LLD', 'Thorax Top Lordotik' (proyeksi lain), 'Thorax (AP/PA + Lat)' (kombinasi); tidak ada versi mobile"),
 'Infusion Pump / hari': dict(
    nama='sama', use=[('ALAD000003', 'Infusion Pump per Hari', 61, T61), ('ALAD000011', 'Infusion Pump < 6 Jam', 61, dict(T61, role='Ragu'))],
    p3="'Infusion Pump < 6 Jam' bersatuan < 6 jam, bukan per hari",
    p7="'Infusion Pump per Hari' kode ALAB000012 (kelompok 'ALAT RUANG KHUSUS', hlm. 60) dan ALAC000097 (alkes ruang operasi, hlm. 63), tarif sama; "
       "versi '< 6 Jam' ALAB000044/ALAC000098"),
 'Syringe Pump / hari': dict(
    nama='sama', use=[('ALAD000012', 'Syringe Pump per Hari', 61, T61), ('ALAD000013', 'Syringe Pump < 6 Jam', 61, dict(T61, role='Ragu'))],
    p3="'Syringe Pump < 6 Jam' bersatuan < 6 jam, bukan per hari",
    p7="'Syringe Pump per Hari' kode ALAB000024 (kelompok 'ALAT RUANG KHUSUS', hlm. 60) dan ALAC000095 (alkes ruang operasi, hlm. 63), tarif sama; "
       "versi '< 6 Jam' ALAB000045/ALAC000096"),
 'O2 / Hari': dict(
    nama='sama', use=[('ALAE000001', 'O2 per Hari', 61, G61), ('ALAE000005', 'O2 per Jam', 61, dict(G61, role='Ragu'))],
    p3="'O2 per Jam' bersatuan per jam",
    p7="'Incubator (Termasuk O2)' (inkubator), 'N2O per 30 Menit', 'CO2 per 30 Menit' (gas lain)"),
 'Nebulizer': dict(
    nama='beda', use=[('IGDJ000066', 'Tindakan Nebulizer', 11), ('RHBB010011', 'Tindakan Nebulizer', 47), ('PRWT000065', 'Tindakan Nebulizer', 50),
                      ('ALAD000029', 'Nebulizer', 61, T61)],
    p3="'Nebulizer' adalah sewa alat, 'Tindakan Nebulizer' adalah tindakan (keduanya dimasukkan); versi 'TARIF FISIOTERAPI' adalah layanan fisioterapi",
    p7="'Nebulizer' kode ALAB000029 (kelompok 'ALAT RUANG KHUSUS', hlm. 60, 262.000), 'Nebulizer, Clapping, Vibrasi' (paket tindakan perawat)"),
 'Creatinin': dict(
    nama='sama', use=[('LABA210200', 'Creatinin', 79)],
    p7="'Creatinin Clearance', 'Creatinin Urine Sewaktu' (clearance/urine), 'Albumin / Creatinin Urine Ratio (R)' (rasio urine)"),
 'Ureum': dict(
    nama='sama', use=[('LABA210100', 'Ureum', 79), ('LABA210900', 'BUN', 80, dict(KIMIA, role='Ragu'))],
    p3="'BUN' (blood urea nitrogen) item terpisah dari ureum",
    p7="'Ureum Clearance' (clearance)"),
 'GDS': dict(
    nama='beda', use=[('LABA220300', 'Glukosa Darah Sewaktu', 80, KIMIA)],
    p7="'Glukosa Darah Puasa', 'Glukosa Darah PP', 'Glukosa Toleransi Test' (bukan sewaktu), 'Glukosa' (urinalisa)"),
 'Elektrolit (Na, K, Cl)': dict(
    nama='sama', use=[('LABA260100', 'Elektrolit (Na, K, Cl)', 80, KIMIA)],
    p7="'Natrium', 'Kalium', 'Chlorida' (item satuan; paket tersedia)"),
}
