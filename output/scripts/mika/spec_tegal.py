"""Spec Mitra Keluarga Tegal (lihat spec_depok.py untuk format)."""
KEY = 'tegal'
SHEET = 'Mitra Keluarga Tegal'
PAGE_NOTE = 'hlm. = nomor halaman file PDF, bukan nomor cetak (mis. hlm. 6 = cetak 4)'
SRC = ("Effective Date per tabel, mis. 'MITRA KELUARGA TEGAL PER JANUARI 2026' (tabel konsultasi, hlm. 6) dan 'MITRA KELUARGA TEGAL PER 1 MEI 2026' "
       "(tabel keperawatan, hlm. 78); biaya administrasi rawat inap terpisah: ADMB000001 (hlm. 6) '7% Dari Total Tagihan Maksimal'")
R = dict(role='Ragu')
NG = dict(show_group=False)          # sub-judul tabel hlm. 78 terbaca sebagai kelompok; tidak dikutip
U = {
 'Konsultasi Dokter Umum IGD': dict(
    nama='beda', use=[('KONA000002', 'Konsultasi Umum IGD', 6, dict(merged=True))],
    p7="'Konsultasi Umum Poli Umum' (poli umum), 'Konsultasi Akupuntur', 'Konsultasi Spesialis OnCall di IGD' dan 'Konsultasi Spesialis On Call di IGD Hari Libur' "
       "(spesialis di IGD), 'Konsultasi Spesialis via Telp di IGD' (telepon), 'Konsultasi Dokter Umum MCU' (MCU), 'Telekonsultasi Dokter Umum' (telekonsultasi)"),
 'Konsultasi Spesialis Rawat Inap': dict(
    nama='sama', use=[('KOND000001', 'Konsultasi Spesialis Rawat Inap', 6), ('KOND000004', 'Konsultasi Dokter Umum Rawat Inap', 6, R)],
    p3="'Konsultasi Dokter Umum Rawat Inap' adalah visite dokter umum, bukan spesialis (padanan lemah); tidak ada tarif subspesialis/konsultan rawat inap",
    p4="tabel 'TARIF JASA KONSULTASI & ADMINISTRASI' tercantum dua kali (hlm. 6 dan hlm. 7) dengan tarif 'Konsultasi Spesialis Rawat Inap' yang sama; "
       "versi hlm. 7 tidak memuat 'Konsultasi Dokter Umum Rawat Inap' (sesuai PDF, dicek visual)",
    p7="'Konsultasi Intensive Care' (ICU/IMC), 'Konsultasi Spesialis', 'Konsultasi SubSpesialis', 'Konsultasi Spesialis Hari Minggu', 'Konsultasi Spesialis Pasien Covid' (rawat jalan), "
       "'Telekonsultasi Spesialis'; kolom PERINA, NICU, IMC, ICU (ruang khusus)"),
 'Ruang Rawat': dict(
    nama='beda', row_labels={1: 'Nama lain di tabel fasilitas', 2: 'Varian bayi'},
    rows={'III': [('RUAA010008', 'Ruang Rawat - Kelas III', 5), ('RUAA010008', 'KELAS III', 3), ('RUAA040008', 'Ruang Rawat Bayi - Kelas III', 5)],
          'II': [('RUAA010007', 'Ruang Rawat - Kelas II', 5), ('RUAA010007', 'KELAS II', 3), ('RUAA040007', 'Ruang Rawat Bayi - Kelas II', 5)],
          'I & R. KHUSUS': [('RUAA010006', 'Ruang Rawat - Kelas I', 5), ('RUAA010006', 'KELAS I', 3), ('RUAA040006', 'Ruang Rawat Bayi - Kelas I', 5)]},
    p3="kamar dewasa tercantum dua kali dengan nama berbeda (kode dan tarif sama): 'Ruang Rawat - Kelas III' dst. di tabel 'TARIF KAMAR PERAWATAN' dan 'KELAS III' dst. "
       "di tabel 'FASILITAS & TARIF KAMAR PERAWATAN' -> keduanya dimasukkan; varian bayi dimasukkan sebagai varian umur",
    p7="'Ruang Rawat - Suite', 'Ruang Rawat - VIP' (di atas kelas I); 'Ruang Rawat - Isolasi', 'Ruang Rawat - Isolasi VIP', 'Ruang Rawat - ICU', 'Ruang Rawat - Intermediate', "
       "'Ruang Rawat - Perina', 'Ruang Rawat - NICU', 'Ruang Rawat - ICCU', 'Ruang Rawat - PICU' (ruang khusus); 'Ruang Rawat Bayi - Suite', 'Ruang Rawat Bayi - VIP'; "
       "'Ruang Rawat ODC - Kelas III' dkk. (one day care)"),
 'Jasa Perawatan': dict(
    nama='sama', use=[('RUAA050004', 'Jasa Perawatan', 5)],
    p7="'Jasa Perawat Pendamping Dalam Kota' dan 'Jasa Perawat Pendamping Luar Kota' (pendampingan)"),
 'Pasang IV Line Access': dict(
    nama='beda', use=[('PRWT000072', 'Pasang IV Line Acces', 78, NG), ('IGDJ000082', 'Vena Seksi', 8, R), ('TINJ000029', 'Vena Seksi', 46, R)],
    p3="'Vena Seksi' adalah akses vena dengan sayatan (cut-down), bukan IV line biasa",
    p4="ejaan 'Acces' sesuai PDF",
    p7="tidak ada item pasang infus dewasa/anak terpisah"),
 'Injeksi IM / IV': dict(
    nama='beda', use=[('IGDJ000078', 'Injeksi IM/IV', 8), ('PRWT000029', 'Injeksi IM/ IV', 78, NG)],
    p7="'Injeksi IM/IV' dan 'Injeksi IM/ IV' di tabel tindakan poli spesialis (rawat jalan per spesialis), 'Pemberian Injeksi (IM, IV, SC, IC)' (homecare), "
       "'Suntik Intra Konka' (poli THT)"),
 'Hematologi Lengkap': dict(
    nama='beda', use=[('LABA100300', 'Darah Lengkap', 50)],
    p7="'Darah Rutin' (parameter lebih sedikit)"),
 'CRP Kuantitatif': dict(
    nama='sama', use=[('LABA320100', 'CRP Kuantitatif', 51), ('LABA321300', 'hs-CRP (R)', 54, R)],
    p3="'hs-CRP (R)' adalah CRP sensitivitas tinggi (pemeriksaan rujukan), bukan CRP kuantitatif standar",
    p7="tidak ada CRP kualitatif/CRP tanpa keterangan"),
 'Thorax PA': dict(
    nama='beda', use=[('RADA030001', 'Thorax AP/PA', 59)],
    p3="satu item 'Thorax AP/PA' mencakup proyeksi AP atau PA (tidak ada item PA saja)",
    p7="'Thorax Lateral', 'Thorax RLD', 'Thorax LLD', 'Thorax Top Lordotik' (proyeksi lain), 'Thorax (AP/PA + Lat)' dan 'Thorax (AP/PA + Oblique)' (kombinasi); tidak ada versi mobile"),
 'Infusion Pump / hari': dict(
    nama='sama', use=[('ALAD000003', 'Infusion Pump per Hari', 34), ('ALAD000011', 'Infusion Pump < 6 Jam', 34, R)],
    p3="'Infusion Pump < 6 Jam' bersatuan < 6 jam, bukan per hari",
    p7="'Infusion Pump' kode ALAB000012 (kelompok 'Alat Ruang Khusus', hlm. 35, tarif lebih rendah) dan 'Infusion Pump per Hari' kode ALAC000097 (kelompok 'Alat OK', hlm. 36, tarif sama); "
       "versi '< 6 Jam' ALAB000044/ALAC000098"),
 'Syringe Pump / hari': dict(
    nama='sama', use=[('ALAD000012', 'Syringe Pump per Hari', 34), ('ALAD000013', 'Syringe Pump < 6 Jam', 34, R)],
    p3="'Syringe Pump < 6 Jam' bersatuan < 6 jam, bukan per hari",
    p4="tarif 'Syringe Pump per Hari' sama persis dengan 'Infusion Pump per Hari' di semua kolom (sesuai PDF, dicek visual)",
    p7="'Syringe Pump' kode ALAB000024 (kelompok 'Alat Ruang Khusus', hlm. 35) dan ALAC000095 (kelompok 'Alat OK', hlm. 36), tarif berbeda; versi '< 6 Jam' ALAB000045/ALAC000096"),
 'O2 / Hari': dict(
    nama='sama', use=[('ALAE000001', 'O2 Per Hari', 38), ('ALAE000005', 'O2 Per Jam', 38, R)],
    p3="'O2 Per Jam' bersatuan per jam",
    p7="'O2 Per 1.5 M3' (hanya kolom RJ, satuan volume), 'Incubator (Termasuk O2)' (inkubator)"),
 'Nebulizer': dict(
    nama='beda', use=[('IGDJ000066', 'Tindakan Nebulizer', 8), ('RHBB010011', 'Tindakan Nebulizer', 10), ('TINJ000079', 'Tindakan Nebulizer', 46),
                      ('PRWT000065', 'Tindakan Nebulizer', 78, NG), ('ALAD000029', 'Nebulizer', 34)],
    p3="'Nebulizer' adalah sewa alat, 'Tindakan Nebulizer' adalah tindakan (keduanya dimasukkan); versi 'Modalitas Fisioterapi' adalah layanan fisioterapi",
    p7="'Nebulizer' kode ALAB000029 dan ALAC000143 (alat ruang khusus/OK, tarif sama), 'Nebulizer, Clapping, Vibrasi' (paket), 'Exercise Nebulizer' (exercise), "
       "'Paket Nebulizer 1' dan 'Paket Nebulizer 2' (paket rawat jalan), 'Nebulizer' kode PARJ000048, 'Tindakan Nebulezer' kode PDMJ000020 dan 'Tindakan Nebulizer' kode ANKJ000012 (poli spesialis)"),
 'Creatinin': dict(
    nama='sama', use=[('LABA210200', 'Creatinin', 50)],
    p7="'Creatinin Clearance (R)', 'Creatinin Urin (R)' (clearance/urine), 'Albumin / Creatinin Urine Ratio (R)' (rasio urine)"),
 'Ureum': dict(
    nama='sama', use=[('LABA210100', 'Ureum', 50)],
    p7="'Ureum Clearance (R)', 'Ureum Urin (R)' (clearance/urine), 'Urea Breath Tes (UBT) (R)' (tes napas); tidak ada item BUN"),
 'GDS': dict(
    nama='beda', use=[('LABA220300', 'Gula Darah Sewaktu', 50)],
    p7="'Gula Darah Puasa', 'Gula Darah PP' (bukan sewaktu)"),
 'Elektrolit (Na, K, Cl)': dict(
    nama='sama', use=[('LABA260100', 'Elektrolit (Na, K, Cl)', 51)],
    p7="'Natrium', 'Kalium', 'Chlorida' (item satuan; paket tersedia), 'Natrium Urin (R)', 'Kalium Urin (R)', 'Chlorida Urin (R)' (urine)"),
}
