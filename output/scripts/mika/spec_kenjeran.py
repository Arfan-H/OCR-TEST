"""Spec Mitra Keluarga Kenjeran (lihat spec_depok.py untuk format).
Buku ini punya kolom 'Rank' (tingkat dokter / lokasi) di antara nama dan tarif; Excel menggabungkan Rank ke nama."""
KEY = 'kenjeran'
SHEET = 'Mitra Keluarga Kenjeran'
PAGE_NOTE = 'hlm. = nomor halaman file PDF'
SRC = ("tanpa Effective Date di teks PDF; buku disahkan 'Surabaya, 26 November 2025' (hlm. 3); biaya administrasi rawat inap terpisah: ADMB000001 (hlm. 5) "
       "'8% dari Total Tagihan'; 'Harga dapat berubah sewaktu - waktu tanpa pemberitahuan terlebih dahulu'")
R = dict(role='Ragu')
def rk(v, **kw): return dict(rank='Rank', rv=v, **kw)
VT = 'Varian tingkat dokter (urutan kolom sama)'
U = {
 'Konsultasi Dokter Umum IGD': dict(
    nama='beda', use=[('KONA000002', 'Konsultasi Umum', 6, rk('IGD', alias='Konsultasi Umum IGD'))],
    p3="nama 'Konsultasi Umum' dipakai untuk dua baris berkode sama; versi IGD dibedakan oleh isi kolom 'Rank' ('IGD' vs 'Poli Umum')",
    p7="'Konsultasi Umum' Rank 'Poli Umum' (poli umum), 'Konsultasi Spesialis OnCall di IGD' dan versi (MN)/(OS) (spesialis di IGD), 'Konsultasi Dokter Umum MCU' (MCU), "
       "'Konsultasi Dokter Umum - Vaksin Covid' (vaksin), 'Telekonsultasi Dokter Umum' (telekonsultasi), 'Konsultasi Dokter Gigi Umum Oncall di IGD' (gigi)"),
 'Konsultasi Spesialis Rawat Inap': dict(
    nama='sama', use=[('KOND000001', 'Konsultasi Spesialis Rawat Inap', 8, rk('Spesialis', alias='Konsultasi Spesialis Rawat Inap Spesialis')),
                      ('KOND000001', 'Konsultasi Spesialis Rawat Inap', 8, rk('Konsultan', alias='Konsultasi Spesialis Rawat Inap Konsultan', role=VT)),
                      ('KOND000001', 'Konsultasi Spesialis Rawat Inap', 8, rk('Profesor', alias='Konsultasi Spesialis Rawat Inap Profesor', role=VT)),
                      ('KOND000004', 'Konsultasi Dokter Umum Rawat Inap', 8, rk('Dokter Jaga', alias='Konsultasi Dokter Umum Rawat Inap Dokter Jaga', role='Ragu'))],
    p3="'Konsultasi Dokter Umum Rawat Inap' (Rank 'Dokter Jaga') adalah visite dokter umum, bukan spesialis (padanan lemah)",
    p4="'Konsultasi Dokter Umum Rawat Inap' Kelas II = Kelas III, ODC 85.000 (sesuai PDF, dicek visual)",
    p7="'Konsultasi Intensive Care' (ICU), 'Konsultasi Spesialis' (rawat jalan, Rank 'Spesialis'/'Konsultan'/'Profesor' dan tarif per dokter hlm. 7), 'Konsultasi Spesialis via Telp' (telepon), "
       "'Konsultasi Spesialis OnCall di IGD' (IGD), 'Telekonsultasi Dokter Spesialis' (telekonsultasi), 'Konsultasi Dokter Spesialis MCU' (MCU)"),
 'Ruang Rawat': dict(
    nama='beda', row_labels={1: 'Varian bayi'},
    rows={'III': [('RUAA010008', 'Ruang Rawat - Kelas III', 9), ('RUAA040008', 'Ruang Rawat Bayi - Kelas III', 9)],
          'II': [('RUAA010007', 'Ruang Rawat - Kelas II', 9), ('RUAA040007', 'Ruang Rawat Bayi - Kelas II', 9)],
          'I & R. KHUSUS': [('RUAA010006', 'Ruang Rawat - Kelas I', 9), ('RUAA040006', 'Ruang Rawat Bayi - Kelas I', 9)]},
    p3="varian bayi dimasukkan sebagai varian umur; Excel memberi label \"UMUM/NON-KELAS\" untuk semua kamar sehingga kelas hanya terbaca dari nama item",
    p7="'Ruang Rawat - Suite', 'Ruang Rawat - Eksekutif' (di atas kelas I); 'Ruang Rawat - Isolasi', 'Ruang Rawat - Isolasi Radiasi', 'Ruang Rawat - ICU', 'Ruang Rawat - Intermediate', "
       "'Ruang Rawat - Perina', 'Ruang Rawat - NICU', 'Ruang Rawat - NINT' (ruang khusus); 'Ruang Rawat ODC - Kelas III' (one day care); 'Ruang Rawat Bayi - Suite', 'Ruang Rawat Bayi - Eksekutif'"),
 'Jasa Perawatan': dict(
    nama='sama', use=[('RUAA050004', 'Jasa Perawatan', 17)],
    p3="item berada di kelompok 'RUANG TINDAKAN' (bukan tabel kamar perawatan)",
    p7="'Jasa Perawat Pendamping Dalam Kota', 'Jasa Perawat Pendamping Luar Kota', 'Jasa Perawat Pendamping Luar Jatim', 'Jasa Perawat Pendamping Domestik', "
       "'Jasa Perawat Pendamping International' (pendampingan)"),
 'Pasang IV Line Access': dict(
    nama='beda', use=[('IGDJ000156', 'Pasang IV Line Acces', 86), ('PRWT000072', 'Pasang IV Line Acces', 91), ('TINJ000029', 'Vena Seksi', 87, R)],
    p3="'Vena Seksi' adalah akses vena dengan sayatan (cut-down), bukan IV line biasa",
    p4="ejaan 'Acces' sesuai PDF",
    p7="tidak ada item pasang infus dewasa/anak terpisah"),
 'Injeksi IM / IV': dict(
    nama='beda', use=[('IGDJ000078', 'Injeksi IM/IV', 83), ('TINJ000162', 'Injeksi IM/IV', 88), ('PRWT000029', 'Injeksi IM/ IV', 90)],
    p7="'Injeksi IM/IV' dan 'Injeksi IM/ IV' di tabel tindakan poli spesialis/poli gizi/kedokteran nuklir (rawat jalan per spesialis), "
       "'Pemberian Injeksi (IM, IV, SC, IC)' (homecare)"),
 'Hematologi Lengkap': dict(
    nama='beda', use=[('LABA100300', 'Darah Lengkap', 101)],
    p7="'Darah Rutin' (parameter lebih sedikit)"),
 'CRP Kuantitatif': dict(
    nama='sama', use=[('LABA320100', 'CRP Kuantitatif', 109), ('LABA321800', 'CRP Kuantitatif FIA', 110, dict(role='Varian metode')),
                      ('LABA321300', 'hs-CRP (R)', 110, R)],
    p3="'hs-CRP (R)' adalah CRP sensitivitas tinggi (pemeriksaan rujukan), bukan CRP kuantitatif standar; 'CRP Kuantitatif FIA' adalah CRP kuantitatif dengan metode FIA",
    p7="tidak ada CRP kualitatif/CRP tanpa keterangan"),
 'Thorax PA': dict(
    nama='beda', use=[('RADA030001', 'Thorax AP/PA', 124)],
    p3="satu item 'Thorax AP/PA' mencakup proyeksi AP atau PA (tidak ada item PA saja)",
    p7="'Thorax Lateral', 'Thorax RLD', 'Thorax LLD' (proyeksi lain), 'Thorax (AP/PA + Lat)' (kombinasi); tidak ada versi mobile"),
 'Infusion Pump / hari': dict(
    nama='sama', use=[('ALAD000003', 'Infusion Pump per Hari', 97)],
    p7="'Infusion Pump per Hari' kode ALAB000012 (kelompok 'Alat Ruang Khusus', hlm. 94) dan ALAC000097 (kelompok 'Alat OK', hlm. 96), tarif kelas sama; tidak ada versi < 6 jam"),
 'Syringe Pump / hari': dict(
    nama='sama', use=[('ALAD000012', 'Syringe Pump per Hari', 97)],
    p4="tarif 'Syringe Pump per Hari' sama persis dengan 'Infusion Pump per Hari' di semua kolom (sesuai PDF, dicek visual)",
    p7="'Syringe Pump per Hari' kode ALAB000024 (kelompok 'Alat Ruang Khusus', hlm. 94) dan ALAC000095 (kelompok 'Alat OK', hlm. 96), tarif kelas sama; tidak ada versi < 6 jam"),
 'O2 / Hari': dict(
    nama='sama', use=[('ALAE000001', 'O2 Per Hari', 98), ('ALAE000002', 'O2 <= 6 Jam', 98, R)],
    p3="'O2 <= 6 Jam' bersatuan <= 6 jam, bukan per hari",
    p7="'Incubator (Termasuk O2)' (inkubator); tidak ada O2 per jam"),
 'Nebulizer': dict(
    nama='beda', use=[('IGDJ000066', 'Tindakan Nebulizer', 83), ('TINJ000079', 'Tindakan Nebulizer', 87), ('PRWT000065', 'Tindakan Nebulizer', 91),
                      ('RHBB010011', 'Tindakan Nebulizer', 81), ('ALAD000029', 'Nebulizer', 97)],
    p3="'Nebulizer' adalah sewa alat, 'Tindakan Nebulizer' adalah tindakan (keduanya dimasukkan); versi 'Modalitas Fisioterapi' adalah layanan fisioterapi",
    p7="'Tindakan Nebulizer' kode HMCG010043 dan 'Homecare Nebulizer' (homecare, hanya kolom Rawat Jalan), 'Nebulizer' kode ALAB000029 (alat ruang khusus, tarif kelas sama), "
       "'Nebulizer, Clapping, Vibrasi' (paket)"),
 'Creatinin': dict(
    nama='sama', use=[('LABA210200', 'Creatinin', 104)],
    p4="tarif Kelas II = Kelas III, ODC 135.000 (sesuai PDF, dicek visual)",
    p7="'Creatinin Clearance', 'Creatinin Urin', 'Creatinin Urine Sewaktu' (clearance/urine), 'Albumin / Creatinin Urine Ratio (R)' (rasio urine)"),
 'Ureum': dict(
    nama='sama', use=[('LABA210100', 'Ureum', 104), ('LABA210900', 'BUN', 105, R)],
    p3="'BUN' (blood urea nitrogen) item terpisah dari ureum",
    p4="tarif Kelas II = Kelas III, ODC 135.000; 'BUN' bertarif sama persis dengan 'Ureum' (sesuai PDF, dicek visual)",
    p7="'Urea Breath Tes (UBT) (R)' (tes napas)"),
 'GDS': dict(
    nama='beda', use=[('LABA220300', 'Glukosa Darah Sewaktu', 105)],
    p7="'Glukosa Darah Puasa', 'Glukosa Darah PP', 'Glukosa Toleransi Test' (bukan sewaktu), 'Glukosa' (urinalisa)"),
 'Elektrolit (Na, K, Cl)': dict(
    nama='sama', use=[('LABA260100', 'Elektrolit (Na, K, Cl)', 106)],
    p7="'Natrium', 'Kalium', 'Chlorida' (item satuan; paket tersedia), 'Natrium Urin (R)', 'Kalium Urin (R)', 'Chlorida Urin (R)' (urine)"),
}
