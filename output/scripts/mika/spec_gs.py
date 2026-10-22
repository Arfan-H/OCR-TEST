"""Spec Mitra Keluarga Gading Serpong (lihat spec_depok.py untuk format).
Banyak tabel satu kolom 'TARIF' (non-kelas) dan kolom 'KETERANGAN' sebagai pembeda baris bernama sama."""
KEY = 'gs'
SHEET = 'Mitra Keluarga Gading Serpong'
PAGE_NOTE = 'hlm. = nomor halaman file PDF, bukan nomor cetak (mis. hlm. 9 = cetak 6)'
SRC = ("Effective Date per tabel 'PER 1 JANUARI 2026' (mis. hlm. 9 dan 18); 'Tarif tersebut di atas dapat berubah sewaktu-waktu tanpa pemberitahuan terlebih dahulu'")
R = dict(role='Ragu')
def kt(v, **kw): return dict(rank='KETERANGAN', rv=v, **kw)
U = {
 'Konsultasi Dokter Umum IGD': dict(
    nama='beda', use=[('KONA000002', 'Konsultasi Umum', 18, kt('DOKTER UMUM IGD'))],
    p3="nama 'Konsultasi Umum' dipakai untuk dua baris berkode sama; versi IGD dibedakan oleh kolom 'KETERANGAN' ('DOKTER UMUM IGD' vs 'DOKTER UMUM POLI UMUM')",
    p5="Excel \"Konsultasi Umum\" punya dua tarif \"UMUM/NON-KELAS\" (160.000 dan 225.000) tanpa pembeda Poli/IGD",
    p7="'Konsultasi Umum' KETERANGAN 'DOKTER UMUM POLI UMUM' (poli umum, 160.000), 'Konsultasi Spesialis OnCall di IGD' dan varian (MN)/(OS)/SubSpesialis (spesialis di IGD)"),
 'Konsultasi Spesialis Rawat Inap': dict(
    nama='sama', use=[('KOND000001', 'Konsultasi Spesialis Rawat Inap', 18, kt('SPESIALIS')),
                      ('KOND000001', 'Konsultasi Spesialis Rawat Inap', 18, kt('SUBSPESIALIS', role='Varian tingkat dokter (urutan kolom sama)')),
                      ('KOND000004', 'Konsultasi Dokter Umum', 18, kt('DOKTER UMUM', role='Ragu'))],
    p3="'Konsultasi Dokter Umum' (KETERANGAN 'DOKTER UMUM', tabel visit rawat inap) adalah visite dokter umum, bukan spesialis (padanan lemah)",
    p4="tabel visit rawat inap memisahkan kolom 'UTAMA' dan 'KELAS I/IMC/ISO PERINA' dengan tarif sama (sesuai PDF, dicek visual)",
    p7="'Konsultasi Intensive Care' (ICU), 'Konsultasi Spesialis' (rawat jalan: DOKTER SPESIALIS/SUBPESIALIS/RADIOLOGI INTERVENSI), 'Konsultasi Spesialis via Telp', "
       "'Telekonsultasi Spesialis', konsultasi spesialis OnCall di IGD; kolom 'UTAMA', 'ICU', 'NICU/PICU' (di atas kelas I/intensif)"),
 'Ruang Rawat': dict(
    nama='beda', row_labels={1: 'Varian bayi'},
    rows={'III': [('RUAA010008', 'Ruang Rawat - Kelas III', 9), ('RUAA040008', 'Ruang Rawat Bayi - Kelas III', 9)],
          'II': [('RUAA010007', 'Ruang Rawat - Kelas II', 9), ('RUAA040007', 'Ruang Rawat Bayi - Kelas II', 9)],
          'I & R. KHUSUS': [('RUAA010006', 'Ruang Rawat - Kelas I', 9), ('RUAA040006', 'Ruang Rawat Bayi - Kelas I', 9)]},
    p3="varian bayi dimasukkan sebagai varian umur; Excel memberi label \"UMUM/NON-KELAS\" untuk semua kamar sehingga kelas hanya terbaca dari nama item",
    p7="'Ruang Rawat - Suite', 'Ruang Rawat - Eksekutif', 'Ruang Rawat - VIP', 'Ruang Rawat - Utama A' (di atas kelas I); 'Ruang Rawat - Isolasi', 'Ruang Rawat - ICU', "
       "'Ruang Rawat - Intermediate', 'Ruang Rawat - Perina', 'Ruang Rawat - NICU', 'Ruang Rawat - PICU' (ruang khusus); 'Ruang Rawat ODC - Kelas III' dkk. (one day care); "
       "ruang bayi di atas kelas I"),
 'Jasa Perawatan': dict(
    nama='sama', use=[('RUAA050004', 'Jasa Perawatan', 9)],
    p3="item berada di tabel 'KAMAR KHUSUS' dengan satu tarif tanpa beda kelas",
    p7="'Jasa Perawat Pendamping' dan varian pendamping (Jabodetabek, luar kota, luar negeri; pendampingan)"),
 'Pasang IV Line Access': dict(
    nama='beda', use=[('PRWT000072', 'Pasang IV Line Acces', 91), ('ANKJ000052', 'Pasang IV Line Acces', 65, dict(role='Varian anak')),
                      ('TINJ000029', 'Vena Seksi', 10, R)],
    p3="versi tabel 'TARIF TINDAKAN ANAK' dimasukkan sebagai varian anak; 'Vena Seksi' adalah akses vena dengan sayatan (cut-down), bukan IV line biasa",
    p4="versi anak 400.000 jauh lebih mahal dari versi perawat 230.000 (sesuai PDF, dicek visual)",
    p7="tidak ada item pasang infus dewasa/anak lain"),
 'Injeksi IM / IV': dict(
    nama='beda', use=[('PRWT000029', 'Injeksi IM/ IV', 89)],
    p7="'Injeksi IM/ IV' kode ANKJ000001 (tabel tindakan anak) dan 'Injeksi IM/IV' / 'Injeksi IM/ IV' di tabel poliklinik spesialis (rawat jalan per spesialis, tarif sama 100.000), "
       "'Pemberian Injeksi (IM, IV, SC, IC)' (homecare)"),
 'Hematologi Lengkap': dict(
    nama='beda', use=[('LABA100300', 'Darah Lengkap', 48)],
    p7="'Darah Rutin' (parameter lebih sedikit)"),
 'CRP Kuantitatif': dict(
    nama='sama', use=[('LABA320100', 'CRP Kuantitatif', 49), ('LABA321300', 'hs-CRP (R)', 52, R)],
    p3="'hs-CRP (R)' adalah CRP sensitivitas tinggi (pemeriksaan rujukan), bukan CRP kuantitatif standar",
    p7="tidak ada CRP kualitatif/CRP tanpa keterangan"),
 'Thorax PA': dict(
    nama='beda', use=[('RADA030001', 'Thorax AP/PA', 37), ('RADA010099', 'Rontgen Thorax Mobile', 37, R)],
    p3="satu item 'Thorax AP/PA' mencakup proyeksi AP atau PA; 'Rontgen Thorax Mobile' tercantum di kelompok 'Konvensional Head' dengan tarif rata 373.000",
    p4="'Thorax AP/PA' kelas III 373.000 sama dengan 'Rontgen Thorax Mobile' (sesuai PDF, dicek visual)",
    p7="'Thorax Lateral', 'Thorax Oblique', 'Thorax RLD', 'Thorax LLD', 'Thorax Top Lordotik' (proyeksi lain), 'Thorax (AP/PA + Lat)' dan kombinasi AP/PA lainnya"),
 'Infusion Pump / hari': dict(
    nama='sama', use=[('ALAD000003', 'Infusion Pump per Hari', 12), ('ALAD000011', 'Infusion Pump < 6 Jam', 12, R)],
    p3="'Infusion Pump < 6 Jam' bersatuan < 6 jam, bukan per hari",
    p7="kode ALAB000012/ALAB000044 (ruang khusus, tarif sama) dan ALAC000097/ALAC000098 (alat OK, 205.000/167.000)"),
 'Syringe Pump / hari': dict(
    nama='sama', use=[('ALAD000012', 'Syringe Pump per Hari', 12), ('ALAD000013', 'Syringe Pump < 6 Jam', 12, R)],
    p3="'Syringe Pump < 6 Jam' bersatuan < 6 jam, bukan per hari",
    p7="kode ALAB000024/ALAB000045 (ruang khusus, tarif sama) dan ALAC000095/ALAC000096 (alat OK, 205.000/167.000)"),
 'O2 / Hari': dict(
    nama='sama', use=[('ALAE000001', 'O2 per Hari', 11), ('ALAE000005', 'O2 per Jam', 11, R)],
    p3="'O2 per Jam' bersatuan per jam",
    p4="'O2 per Hari' berketerangan 'OKSIGEN ≥ 3 JAM' (berlaku mulai 3 jam, bukan 24 jam) (sesuai PDF, dicek visual)",
    p7="'Incubator (Termasuk O2)' (inkubator), 'N2O per Hari', 'CO2 per 30 Menit' (gas lain)"),
 'Nebulizer': dict(
    nama='beda', use=[('PRWT000065', 'Tindakan Nebulizer', 91), ('RHBB010011', 'Nebulizer', 59), ('ALAB000029', 'Nebulizer', 13, R)],
    p3="'Nebulizer' di tabel fisioterapi adalah layanan fisioterapi; sewa alat 'Nebulizer' hanya tercantum di tabel ruang khusus (tidak ada versi IGD/bangsal)",
    p7="'Tindakan Nebulizer' kode ANKJ000012 (tabel tindakan anak) dan versi poli penyakit dalam, 'Nebulizer, Clapping, Vibrasi' (gabungan), 'Paket Nebulizer 5x' dan paket modalitas fisioterapi (paket)"),
 'Creatinin': dict(
    nama='sama', use=[('LABA210200', 'Creatinin', 48)],
    p7="'Creatinin Clearance (R)', 'Creatinin Urin (R)', 'Creatinin Urine Sewaktu (R)' (clearance/urine), 'Albumin / Creatinin Urine Ratio (R)' (rasio urine)"),
 'Ureum': dict(
    nama='sama', use=[('LABA210100', 'Ureum', 48), ('LABA210900', 'BUN (R)', 50, R)],
    p3="'BUN (R)' (blood urea nitrogen, pemeriksaan rujukan) item terpisah dari ureum",
    p4="'BUN (R)' lebih mahal dari 'Ureum' (sesuai PDF, dicek visual)",
    p7="'Ureum Clearance (R)', 'Ureum Urin (R)' (clearance/urine), 'Urea Breath Tes (UBT) (R)' (tes napas)"),
 'GDS': dict(
    nama='beda', use=[('LABA220300', 'Glukosa Darah Sewaktu', 48)],
    p7="'Glukosa Darah Puasa', 'Glukosa Darah PP', 'Glukosa Toleransi Test' (bukan sewaktu)"),
 'Elektrolit (Na, K, Cl)': dict(
    nama='sama', use=[('LABA260100', '"Elektrolit (Na, K, Cl)"', 49)],
    p4="nama item di PDF diapit tanda kutip ganda (ditulis persis sesuai PDF, dicek visual)",
    p7="'Natrium', 'Kalium', 'Chlorida' (item satuan; paket tersedia), 'Natrium Urin (R)', 'Kalium Urin (R)', 'Chlorida Urin (R)' (urine), 'Fraksi Ekskresi Kalium (R)' (perhitungan)"),
}
