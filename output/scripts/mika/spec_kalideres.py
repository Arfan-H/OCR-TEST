"""Spec Mitra Keluarga Kalideres (lihat spec_depok.py untuk format)."""
KEY = 'kalideres'
SHEET = 'Mitra Keluarga Kalideres'
PAGE_NOTE = 'hlm. = nomor halaman file PDF, bukan nomor cetak (mis. hlm. 7 = cetak 4)'
SRC = ("tanpa Effective Date di teks PDF; buku disahkan 'Jakarta, 27 November 2025' (hlm. 3); biaya administrasi rawat inap terpisah: "
       "'Administrasi (5%)' (ADMB000001, hlm. 6) '5% dari Total Tagihan Maksimal'")
R = dict(role='Ragu')
U = {
 'Konsultasi Dokter Umum IGD': dict(
    nama='beda', use=[('KONA000002', 'Konsultasi IGD', 7)],
    p3="'Konsultasi IGD' tidak menyebut dokter umum; sel kode KONA000002 digabung dengan 'Konsultasi Poli Umum'",
    p7="'Konsultasi Poli Umum' (poli umum), 'Konsultasi Spesialis OnCall di IGD', 'Konsultasi Subspesialis OnCall di IGD' dan versi (MN)/(OS) (spesialis di IGD), "
       "'Konsultasi Spesialis via Telp di IGD' (telepon), 'Konsultasi Dokter Umum MCU' (MCU), 'Telekonsultasi Dokter Umum Mika Apps' (telekonsultasi)"),
 'Konsultasi Spesialis Rawat Inap': dict(
    nama='sama', use=[('KOND000001', 'Konsultasi Spesialis Rawat Inap', 7),
                      ('KOND000001', 'Konsultasi Subspesialis Rawat Inap', 7, dict(role='Varian tingkat dokter (urutan kolom sama)'))],
    p7="'Konsultasi Intensive Care' (ICU), 'Konsultasi Spesialis' dan 'Konsultasi Subspesialis' (rawat jalan), konsultasi spesialis di IGD, 'Telekonsultasi Spesialis'; "
       "tidak ada visite dokter umum rawat inap; kolom 'EKSEKUTIF / VIP' dan 'RJ'"),
 'Ruang Rawat': dict(
    nama='beda', row_labels={1: 'Varian bayi'},
    rows={'III': [('RUAA010008', 'RUANG RAWAT - III', 4), ('RUAA040008', 'RUANG RAWAT BAYI - III', 5)],
          'II': [('RUAA010007', 'RUANG RAWAT - II', 4), ('RUAA040007', 'RUANG RAWAT BAYI - II', 5)],
          'I & R. KHUSUS': [('RUAA010006', 'RUANG RAWAT - I', 4), ('RUAA040006', 'RUANG RAWAT BAYI - I', 5)]},
    p3="varian bayi dimasukkan sebagai varian umur; Excel memberi label \"UMUM/NON-KELAS\" untuk semua kamar sehingga kelas hanya terbaca dari nama item",
    p7="'RUANG RAWAT - EKSEKUTIF', 'RUANG RAWAT - VIP' (di atas kelas I); 'RUANG RAWAT - ISOLASI', 'RUANG RAWAT - ICU', 'RUANG RAWAT - INTERMEDIATE', 'RUANG RAWAT - PERINA', "
       "'RUANG RAWAT - NICU', 'RUANG RAWAT - ICCU', 'RUANG RAWAT - PICU' (ruang khusus); 'RUANG RAWAT BAYI - Eksekutif', 'RUANG RAWAT BAYI - VIP', 'RUANG RAWAT BAYI - Bayi Tinggal'"),
 'Jasa Perawatan': dict(
    nama='beda', use=[('RUAA050004', 'Jasa keperawatan', 6)],
    p7="'Jasa Dokter Pendamping' dan 'Jasa Pendampingan Anestesi' (jasa dokter, bukan jasa perawatan)"),
 'Pasang IV Line Access': dict(
    nama='beda', use=[('TINJ000065', 'Pasang IV Line Acces', 46), ('PRWT000072', 'Pasang IV Line Acess', 48),
                      ('IGDJ000082', 'Vena Seksi', 45, R), ('TINJ000029', 'Vena Seksi', 46, R)],
    p3="'Vena Seksi' adalah akses vena dengan sayatan (cut-down), bukan IV line biasa",
    p4="ejaan berbeda di dua tabel: 'Pasang IV Line Acces' (TINJ000065) dan 'Pasang IV Line Acess' (PRWT000072), sesuai PDF (dicek visual)",
    p7="'Pemberian injeksi (IV,IM,SC)' (homecare); tidak ada item pasang infus dewasa/anak terpisah"),
 'Injeksi IM / IV': dict(
    nama='beda', use=[('IGDJ000078', 'Injeksi IM / IV / SC', 45), ('PRWT000029', 'Injeksi IM / IV / SC', 48)],
    p3="item PDF mencakup juga injeksi SC (subkutan)",
    p7="'Injeksi IM/IV' dan 'Injeksi IM / IV /SC' di tabel tindakan poli spesialis (rawat jalan per spesialis), 'Pemberian injeksi (IV,IM,SC)' (homecare)"),
 'Hematologi Lengkap': dict(
    nama='beda', use=[('LABA100300', 'Darah Lengkap', 50)],
    p7="'Darah Rutin' (parameter lebih sedikit)"),
 'CRP Kuantitatif': dict(
    nama='sama', use=[('LABA320100', 'CRP Kuantitatif', 54), ('LABA321300', 'hs-CRP', 54, R)],
    p3="'hs-CRP' adalah CRP sensitivitas tinggi, bukan CRP kuantitatif standar",
    p7="tidak ada CRP kualitatif/CRP tanpa keterangan"),
 'Thorax PA': dict(
    nama='beda', use=[('RADA030001', 'Thorax AP/PA', 62), ('RADA010099', 'Rontgen Thorax Mobile', 62, R)],
    p3="satu item 'Thorax AP/PA' mencakup proyeksi AP atau PA; 'Rontgen Thorax Mobile' hanya bertarif di kolom 'RJ' 20.000 (kemungkinan biaya tambahan mobile)",
    p4="'Rontgen Thorax Mobile' tercantum di kelompok 'KONVENSIONAL HEAD' (sesuai PDF, dicek visual)",
    p7="'Thorax Lateral', 'Thorax Oblique', 'Thorax RLD', 'Thorax LLD', 'Thorax Top Lordotik' (proyeksi lain), 'Thorax (AP/PA + Lat)' dan kombinasi AP/PA lainnya, "
       "'Thorax AP/PA External' (hanya kolom RJ, film luar)"),
 'Infusion Pump / hari': dict(
    nama='sama', use=[('ALAD000003', 'Infusion Pump per Hari', 79), ('ALAD000011', 'Infusion Pump < 6 jam', 79, R)],
    p3="'Infusion Pump < 6 jam' bersatuan < 6 jam, bukan per hari",
    p7="'Infusion Pump per Hari' kode ALAB000012 dan 'Infusion Pump < 6 Jam' ALAB000044 (kelompok 'ALAT RUANG KHUSUS', hlm. 78), tarif sama"),
 'Syringe Pump / hari': dict(
    nama='sama', use=[('ALAD000012', 'Syringe Pump per Hari', 79), ('ALAD000013', 'Syringe Pump < 6 jam', 79, R)],
    p3="'Syringe Pump < 6 jam' bersatuan < 6 jam, bukan per hari",
    p4="tarif 'Syringe Pump per Hari' sama persis dengan 'Infusion Pump per Hari' (281.000 rata di semua kolom) (sesuai PDF, dicek visual)",
    p7="kode ALAB000024/ALAB000045 (kelompok 'ALAT RUANG KHUSUS', hlm. 78) dan ALAC000095/ALAC000096 (kelompok 'ALAT OK', hlm. 79), tarif sama"),
 'O2 / Hari': dict(
    nama='sama', use=[('ALAE000001', 'O2 Per Hari', 80), ('ALAE000005', 'O2 Per Jam', 80, R)],
    p3="'O2 Per Jam' bersatuan per jam",
    p4="'O2 Per Hari' 630.000 rata di semua kolom kelas (sesuai PDF, dicek visual)"),
 'Nebulizer': dict(
    nama='beda', use=[('IGDJ000066', 'Tindakan Nebulizer', 44), ('TINJ000079', 'Tindakan Nebulizer', 47), ('PRWT000065', 'Tindakan Nebulizer', 48),
                      ('RHBB010011', 'Tindakan Nebulizer', 12)],
    p3="versi 'MODALITAS FISIOTERAPI' adalah layanan rehabilitasi medik; tidak ada item sewa alat nebulizer",
    p7="'Tindakan Nebulizer' di tabel tindakan poli paru, penyakit dalam dan anak (rawat jalan per spesialis), 'Paket Nebulizer 5 x' (paket)"),
 'Creatinin': dict(
    nama='sama', use=[('LABA210200', 'Creatinin', 52)],
    p7="'Creatinin Clearance', 'Creatinin Urin' (clearance/urine), 'Albumin / Creatinin Urine Ratio' (rasio urine)"),
 'Ureum': dict(
    nama='sama', use=[('LABA210100', 'Ureum', 52), ('LABA210900', 'BUN', 52, R)],
    p3="'BUN' (blood urea nitrogen) item terpisah dari ureum",
    p4="'BUN' lebih mahal dari 'Ureum' di kelas III/RJ tetapi lebih murah di kelas I dan EKSEKUTIF/ VIP (sesuai PDF, dicek visual)",
    p7="'Ureum Clearance', 'Ureum Urin' (clearance/urine), 'Urea Breat Tes (UBT)' (tes napas)"),
 'GDS': dict(
    nama='beda', use=[('LABA220300', 'Glukosa Darah Sewaktu', 52)],
    p7="'Glukosa Darah Puasa', 'Glukosa Darah PP', 'Glukosa Toleransi Test' (bukan sewaktu)"),
 'Elektrolit (Na, K, Cl)': dict(
    nama='sama', use=[('LABA260100', 'Elektrolit (Na, K, Cl)', 53)],
    p7="'Natrium', 'Kalium', 'Chlorida' (item satuan; paket tersedia), 'Natrium Urin', 'Kalium Urin', 'Chlorida Urin' (urine)"),
}
