"""Spec Mitra Keluarga Waru (lihat spec_depok.py untuk format).
Tabel konsultasi rawat inap punya kolom 'RANK' (tingkat dokter); Excel menaruh tingkat dokter di kategori."""
KEY = 'waru'
SHEET = 'Mitra Keluarga Waru'
PAGE_NOTE = 'hlm. = nomor halaman file PDF, bukan nomor cetak (mis. hlm. 8 = cetak Hal 5)'
SRC = ("tanpa Effective Date di teks PDF (judul halaman hanya 'TAHUN 2026'); biaya administrasi rawat inap terpisah: ADMB000001 (hlm. 5) '8% dari Total Tagihan'; "
       "'Harga dapat berubah sewaktu-waktu tanpa pemberitahuan terlebih dahulu'")
R = dict(role='Ragu')
VT = 'Varian tingkat dokter (urutan kolom sama)'
SUBROW = ("kolom 'ICU, ICCU, NICU, PICU, UTAMA, NINT, INT, PERINA, ISOL, KELAS I' pada tabel konsultasi rawat inap memuat sub-baris "
          "'ICU ICCU NICU PICU NINT INT PERINA ISOLASI' bertarif lain (467.000 / 571.000 / 776.000); tarif baris utama (374.000 / 544.000 / 691.000) "
          "yang dipakai untuk kelas I (dicek visual)")
U = {
 'Konsultasi Dokter Umum IGD': dict(
    nama='beda', use=[('KONA000002', 'Konsultasi Umum', 7, dict(rank='KETERANGAN', rv='IGD', alias='Konsultasi Umum IGD'))],
    p3="nama 'Konsultasi Umum' dipakai untuk dua baris berkode sama; versi IGD dibedakan oleh isi kolom 'KETERANGAN' ('IGD' vs 'POLI UMUM')",
    p7="'Konsultasi Umum' KETERANGAN 'POLI UMUM' (poli umum), 'Konsultasi Spesialis OnCall di IGD' dan versi (MN) (spesialis di IGD), 'Konsultasi Dokter Umum MCU' (MCU)"),
 'Konsultasi Spesialis Rawat Inap': dict(
    nama='sama', use=[('KOND000001', 'Konsultasi Spesialis Rawat Inap', 8, dict(rank='RANK', rv='SPESIALIS')),
                      ('KOND000001', 'Konsultasi Spesialis Rawat Inap', 8, dict(rank='RANK', rv='KONSULTAN', role=VT)),
                      ('KOND000001', 'Konsultasi Spesialis Rawat Inap', 8, dict(rank='RANK', rv='PROFESSOR', role=VT)),
                      ('KOND000004', 'Konsultasi Dokter Umum Rawat Inap', 8, R)],
    p3="'Konsultasi Dokter Umum Rawat Inap' adalah visite dokter umum, bukan spesialis (padanan lemah); " + SUBROW,
    p5="Excel menaruh tingkat dokter di kategori (\"KONSULTASI RAWAT INAP - SPESIALIS\", \"KONSULTASI RAWAT INAP - KONSULTAN\", \"KONSULTASI RAWAT INAP - PROFESSOR\") "
       "dan mencatat sub-baris ICU dkk. sebagai label \"ICU/ICCU/NICU/PICU/NINT/INT/PERINA/ISOLASI\"",
    p7="'Konsultasi Intensive Care' (ICU), 'Konsultasi Spesialis' (rawat jalan), 'Konsultasi Spesialis Rawat Jalan' dan 'Konsultasi Spesialis Rawat Inap' tarif khusus per dokter (hlm. 9), "
       "'Konsultasi Spesialis via Telp', 'Telekonsultasi Spesialis', 'Konsultasi Spesialis OnCall di IGD'"),
 'Ruang Rawat': dict(
    nama='beda', row_labels={1: 'Varian bayi'},
    rows={'III': [('RUAA010008', 'Ruang Rawat - Kelas III', 20), ('RUAA040008', 'Ruang Rawat Bayi - Kelas III', 20)],
          'II': [('RUAA010007', 'Ruang Rawat - Kelas II', 20), ('RUAA040007', 'Ruang Rawat Bayi - Kelas II', 20)],
          'I & R. KHUSUS': [('RUAA010006', 'Ruang Rawat - Kelas I', 20), ('RUAA040006', 'Ruang Rawat Bayi - Kelas I', 20)]},
    p3="varian bayi dimasukkan sebagai varian umur; Excel memberi label \"UMUM/NON-KELAS\" untuk semua kamar sehingga kelas hanya terbaca dari nama item",
    p7="'Ruang Rawat - Suite', 'Ruang Rawat - Eksekutif', 'Ruang Rawat - Utama A', 'Ruang Rawat - Utama B' (di atas kelas I); 'Ruang Rawat - Isolasi', 'Ruang Rawat - ICU', "
       "'Ruang Rawat - Intermediate', 'Ruang Rawat - Perina', 'Ruang Rawat - NICU', 'Ruang Rawat - PICU', 'Ruang Rawat - NINT' (ruang khusus); 'Ruang Rawat ODC - Kelas III' (one day care); "
       "ruang bayi di atas kelas I"),
 'Jasa Perawatan': dict(
    nama='sama', use=[('RUAA050004', 'Jasa Perawatan', 16)],
    p3="item berada di kelompok 'Pemakaian Ruang Tindakan' (bukan tabel kamar perawatan)",
    p7="'Jasa Perawat Pendamping Dalam Kota', 'Jasa Perawat Pendamping Luar Kota', 'Jasa Perawat Pendamping Luar Jatim' (pendampingan)"),
 'Pasang IV Line Access': dict(
    nama='beda', use=[('PRWT000072', 'Pasang IV Line Acces', 80), ('IGDJ000082', 'Vena Seksi', 83, R), ('TINJ000029', 'Vena Seksi', 85, R)],
    p3="'Vena Seksi' adalah akses vena dengan sayatan (cut-down), bukan IV line biasa",
    p4="ejaan 'Acces' sesuai PDF; 'Vena Seksi' versi IGD dan tindakan medis khusus bertarif sama di kolom kelas",
    p7="'Aff IV Line Acces' (lepas IV line); tidak ada item pasang infus dewasa/anak terpisah"),
 'Injeksi IM / IV': dict(
    nama='beda', use=[('PRWT000029', 'Injeksi IM/ IV', 79)],
    p7="'Injeksi IM/IV' dan 'Injeksi IM/ IV' di tabel tindakan dokter spesialis/poli (rawat jalan per spesialis, tarif sama), 'Pemberian Injeksi (IM, IV, SC, IC)' "
       "dan 'Suntikan melalui Surflo' (homecare); tidak ada injeksi IM/IV di tabel tindakan IGD"),
 'Hematologi Lengkap': dict(
    nama='beda', use=[('LABA100300', 'Darah Lengkap', 117), ('LABA111800', 'Darah Lengkap + IPF', 117, R), ('LABA112100', 'Darah Lengkap - CBC Plus', 117, R),
                      ('LABA112200', 'Darah Lengkap + Neu GI-RI', 117, R), ('LABA112300', 'Darah Lengkap + Lymp As-Re', 117, R)],
    p3="varian 'Darah Lengkap + IPF', 'Darah Lengkap - CBC Plus', 'Darah Lengkap + Neu GI-RI', 'Darah Lengkap + Lymp As-Re' adalah darah lengkap dengan parameter tambahan (dimasukkan sebagai varian nama)",
    p7="'Darah Rutin' (parameter lebih sedikit)"),
 'CRP Kuantitatif': dict(
    nama='sama', use=[('LABA320100', 'CRP Kuantitatif', 124), ('LABA321300', 'hs-CRP', 125, R)],
    p3="'hs-CRP' adalah CRP sensitivitas tinggi, bukan CRP kuantitatif standar",
    p7="tidak ada CRP kualitatif/CRP tanpa keterangan"),
 'Thorax PA': dict(
    nama='beda', use=[('RADA030001', 'Thorax AP/PA', 106)],
    p3="satu item 'Thorax AP/PA' mencakup proyeksi AP atau PA (tidak ada item PA saja)",
    p7="'Thorax Lateral', 'Thorax Oblique', 'Thorax RLD', 'Thorax LLD', 'Thorax Top Lordotik' (proyeksi lain), 'Thorax (AP/PA + Lat)' (kombinasi); tidak ada versi mobile"),
 'Infusion Pump / hari': dict(
    nama='sama', use=[('ALAD000003', 'Infusion Pump per Hari', 97)],
    p7="'Infusion Pump per Hari' kode ALAB000012 (kelompok 'Alat Ruang Khusus', hlm. 93) dan ALAC000097 (kelompok 'Alat OK', hlm. 95), tarif kelas sama; tidak ada versi < 6 jam"),
 'Syringe Pump / hari': dict(
    nama='sama', use=[('ALAD000012', 'Syringe Pump per Hari', 97)],
    p7="'Syringe Pump per Hari' kode ALAB000024 (kelompok 'Alat Ruang Khusus', hlm. 93) dan ALAC000095 (kelompok 'Alat OK', hlm. 95), tarif kelas sama; "
       "'Syringe Pump < 6 Jam' hanya ada di kelompok 'Alat OK' (kamar operasi)"),
 'O2 / Hari': dict(
    nama='sama', use=[('ALAE000001', 'O2 Per Hari', 98), ('ALAE000005', 'O2 Per Jam', 98, R)],
    p3="'O2 Per Jam' bersatuan per jam",
    p7="'Incubator (Termasuk O2)' (inkubator)"),
 'Nebulizer': dict(
    nama='beda', use=[('PRWT000065', 'Tindakan Nebulizer', 80), ('TINJ000079', 'Tindakan Nebulizer', 86), ('RHBB010011', 'Tindakan Nebulizer', 89),
                      ('ALAD000029', 'Nebulizer', 97)],
    p3="'Nebulizer' adalah sewa alat, 'Tindakan Nebulizer' adalah tindakan (keduanya dimasukkan); versi rehabilitasi medik adalah layanan fisioterapi",
    p4="'Tindakan Nebulizer' bertarif sama di tabel keperawatan, tindakan medis khusus dan fisioterapi (sesuai PDF, dicek visual)",
    p7="'Tindakan Nebulizer' kode ANKJ000012 dan PDMJ000020 (poli spesialis), 'Nebulizer' kode ALAB000029 dan ALAC000143 (alat ruang khusus/OK, tarif kelas sama), "
       "'Nebulizer, Clapping, Vibrasi' (IGD, gabungan), 'Nebulizer 2 Sesi' dan 'Nebulizer 2 Sesi + Clapping + Vibrasi' (paket)"),
 'Creatinin': dict(
    nama='sama', use=[('LABA210200', 'Creatinin', 120)],
    p7="'Creatinin Clearance', 'Creatinin Urin (R)', 'Creatinin Urine Sewaktu' (clearance/urine), 'Ratio Total Protein/ Creatinin Urin (R)' dan 'Albumin / Creatinin Urine Ratio' (rasio urine)"),
 'Ureum': dict(
    nama='sama', use=[('LABA210100', 'Ureum', 120), ('LABA210900', 'BUN', 120, R)],
    p3="'BUN' (blood urea nitrogen) item terpisah dari ureum",
    p4="'BUN' bertarif sama persis dengan 'Ureum' dan 'Creatinin' (sesuai PDF, dicek visual)",
    p7="'Ureum Clearance', 'Ureum Urin (R)' (clearance/urine), 'Urea Breath Tes (UBT)' (tes napas)"),
 'GDS': dict(
    nama='beda', use=[('LABA220300', 'Glukosa Darah Sewaktu', 121)],
    p7="'Glukosa Darah Puasa', 'Glukosa Darah PP', 'Glukosa Toleransi Test' (bukan sewaktu), 'Glukosa' (urinalisa)"),
 'Elektrolit (Na, K, Cl)': dict(
    nama='sama', use=[('LABA260100', 'Elektrolit (Na, K, Cl)', 122)],
    p7="'Natrium', 'Kalium', 'Chlorida' (item satuan; paket tersedia), 'Natrium Urin (R)', 'Kalium Urin (R)', 'Chlorida Urin (R)' (urine), 'Fraksi Ekskresi Natrium (R)' (perhitungan)"),
}
