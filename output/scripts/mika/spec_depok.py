"""Spec Mitra Keluarga Depok: pilihan item per uraian + catatan manual (ragu/janggal/tidak diambil).
Tarif, label kolom, perbandingan Excel dan penamaan dihitung gen_mika.py dari PDF/Excel."""
KEY = 'depok'
SHEET = 'Mitra Keluarga Depok'
PAGE_NOTE = 'hlm. = nomor halaman file PDF, bukan nomor cetak (mis. hlm. 9 = cetak 6)'
SRC = ("tanpa Effective Date di teks PDF; biaya administrasi rawat inap terpisah: ADMB000001 (hlm. 7) '5% dari Total Tagihan'; "
       "'Tarif diatas dapat berubah sewaktu-waktu tanpa pemberitahuan terlebih dahulu.'")
R = dict(role='Ragu')
U = {
 'Konsultasi Dokter Umum IGD': dict(
    nama='beda', use=[('KONA000002', 'Konsultasi Umum IGD', 9)],
    p6="keterangan tabel: jasa konsultasi belum termasuk tindakan medis",
    p7="'Konsultasi Umum' (kode KONA000002 yang sama, 170.000: poli umum), 'Konsultasi Spesialis OnCall di IGD' dan versi (MN)/(OS) (spesialis di IGD), "
       "'Konsultasi Dokter Umum MCU' (MCU), 'Telekonsultasi Dokter Umum' (telekonsultasi), 'Homecare Dokter Umum' (homecare)"),
 'Konsultasi Spesialis Rawat Inap': dict(
    nama='sama', use=[('KOND000001', 'Konsultasi Spesialis Rawat Inap', 9), ('KOND000001', 'Konsultasi Spesialis Rawat Inap', 9, dict(idx=1)),
                      ('KOND000004', 'Konsultasi Dokter Umum Rawat Inap', 9, R)],
    p3="'Konsultasi Spesialis Rawat Inap' tercantum 2x berturut-turut dengan kode sama KOND000001 dan tarif berbeda, tanpa keterangan tingkat dokter "
       "(kemungkinan spesialis vs subspesialis, bandingkan 'Konsultasi Spesialis (Subspesialis)' di rawat jalan) -> keduanya dimasukkan, mohon konfirmasi; "
       "'Konsultasi Dokter Umum Rawat Inap' adalah visite dokter umum, bukan spesialis (padanan lemah)",
    p4="nama dan kode baris 1 dan baris 2 identik di PDF (dicek visual)",
    p7="'Konsultasi Intensive Care ICU' dan 'Konsultasi Intensive Care NICU' (ICU/NICU), 'Konsultasi Spesialis' dan 'Konsultasi Spesialis (Subspesialis)' (rawat jalan), "
       "'Konsultasi Spesialis OnCall di IGD' (IGD), 'Telekonsultasi Spesialis' (telekonsultasi), 'Konsultasi Dokter Spesialis MCU' (MCU), "
       "'Homecare Dokter Spesialis' (homecare); kolom INT, ICU, PERINA, NICU (ruang intensif)"),
 'Ruang Rawat': dict(
    nama='beda', row_labels={1: 'Varian bayi'},
    rows={'III': [('RUAA010008', 'Ruang Rawat - Kelas III', 6), ('RUAA040008', 'Ruang Rawat Bayi - Kelas III', 6)],
          'II': [('RUAA010007', 'Ruang Rawat - Kelas II', 6), ('RUAA040007', 'Ruang Rawat Bayi - Kelas II', 6)],
          'I & R. KHUSUS': [('RUAA010006', 'Ruang Rawat - Kelas I', 6), ('RUAA040006', 'Ruang Rawat Bayi - Kelas I', 6)]},
    p3="varian bayi dimasukkan sebagai varian umur; Excel memberi label \"UMUM/NON-KELAS\" untuk semua kamar sehingga kelas hanya terbaca dari nama item",
    p4="'Ruang Rawat Bayi' bertarif sama 290.000 untuk semua kelas (Suite s.d. Kelas III) (sesuai PDF, dicek visual)",
    p7="'Ruang Rawat - Suite', 'Ruang Rawat - Eksekutif', 'Ruang Rawat - VIP', 'Ruang Rawat - Utama A', 'Ruang Rawat - Utama B' (di atas Kelas I); "
       "'Ruang Rawat - Isolasi', 'Ruang Rawat - ICU', 'Ruang Rawat - Intermediate', 'Ruang Rawat - Perina', 'Ruang Rawat - NICU' (ruang khusus); "
       "'Ruang Rawat Bayi - Bayi Tinggal' (bayi tinggal); ruang bayi di atas Kelas I; 'Ruang Tambahan' (non pasien)"),
 'Jasa Perawatan': dict(
    nama='sama', use=[('RUAA050004', 'Jasa Perawatan', 6)],
    p3="tabel 'TARIF KAMAR PERAWATAN' hanya mencantumkan satu tarif 'Jasa Perawatan' tanpa beda kelas",
    p7="'Jasa Perawat Pendamping' dan varian pendamping Jabodetabek/luar Jabodetabek/luar negeri (pendampingan); kelompok 'Homecare Keperawatan' (homecare)"),
 'Pasang IV Line Access': dict(
    nama='beda', use=[('PRWT000072', 'Pasang IV Line Acces', 107), ('TINJ000029', 'Vena Seksi', 63, R), ('BTKD000121', 'Vena Seksi', 23, R)],
    p3="'Vena Seksi' adalah akses vena dengan sayatan (cut-down), bukan IV line biasa; versi tabel 'TARIF TINDAKAN BEDAH THORAX' adalah tarif tindakan bedah",
    p4="'Vena Seksi' (TINJ000029) 5.949.000 sama di semua kolom, sedangkan versi bedah thorax 9.236.000-18.471.000 per kelas (sesuai PDF, dicek visual); ejaan 'Acces' sesuai PDF",
    p7="'Aff IV Line Acces' (lepas IV line), 'Memasang/ Melepas Infus' (homecare), 'Tindakan Infus Intra Osseus' (intraoseus, poli anak), "
       "'Infus dan Observasi Pemberian Stem Cell' (stem cell); tidak ada item pasang infus dewasa/anak terpisah"),
 'Injeksi IM / IV': dict(
    nama='beda', use=[('IGDJ000078', 'Injeksi IM/ IV', 10), ('PRWT000029', 'Injeksi IM/ IV', 106)],
    p7="'Injeksi IM/ IV' / 'Injeksi IM/IV' di tabel tindakan poliklinik spesialis (tindakan poli per spesialis; 215.000 rata, versi kode BONJ000014 116.000), "
       "'Injeksi IM/ IV/ SC' (poli bedah vaskuler), 'Pemberian Injeksi (IM, IV, SC, IC)' (homecare), 'Injeksi SCT' (stem cell), injeksi intraartikuler/lokal/keloid (bukan IM/IV)"),
 'Hematologi Lengkap': dict(
    nama='beda', use=[('LABA100300', 'Darah Lengkap', 42)],
    p7="'Darah Rutin' (parameter lebih sedikit)"),
 'CRP Kuantitatif': dict(
    nama='sama', use=[('LABA320100', 'CRP Kuantitatif', 44), ('LABA321300', 'hs-CRP (R)', 49, R)],
    p3="'hs-CRP (R)' adalah CRP sensitivitas tinggi (pemeriksaan rujukan), bukan CRP kuantitatif standar",
    p7="tidak ada CRP kualitatif/CRP tanpa keterangan"),
 'Thorax PA': dict(
    nama='beda', use=[('RADA030001', 'Thorax AP/PA', 54), ('RADA010099', 'Rontgen Thorax Mobile', 54, R)],
    p3="satu item 'Thorax AP/PA' mencakup proyeksi AP atau PA; 'Rontgen Thorax Mobile' 52.000 kemungkinan biaya tambahan pemeriksaan mobile, bukan tarif foto lengkap",
    p4="'Rontgen Thorax Mobile' tercantum di kelompok 'Konvensional Head' dan jauh lebih murah dari 'Thorax AP/PA' (sesuai PDF, dicek visual)",
    p7="'Thorax Lateral', 'Thorax Oblique', 'Thorax RLD', 'Thorax LLD', 'Thorax Top Lordotik' (proyeksi lain), 'Thorax (AP/PA + Lat)' dan 'Thorax (AP/PA + Oblique)' (kombinasi proyeksi)"),
 'Infusion Pump / hari': dict(
    nama='sama', use=[('ALAD000003', 'Infusion Pump per Hari', 65), ('ALAD000011', 'Infusion Pump < 6 Jam', 65, R)],
    p3="'Infusion Pump < 6 Jam' bersatuan < 6 jam, bukan per hari",
    p7="'Infusion Pump per Hari' kode ALAB000012 (kelompok 'Alat Ruang Khusus', hlm. 64) dan ALAC000097 (alat OK, hlm. 65), serta versi '< 6 Jam' ALAB000044/ALAC000098; tarif sama dengan yang dipakai"),
 'Syringe Pump / hari': dict(
    nama='sama', use=[('ALAD000012', 'Syringe Pump per Hari', 65), ('ALAD000013', 'Syringe Pump < 6 Jam', 65, R)],
    p3="'Syringe Pump < 6 Jam' bersatuan < 6 jam, bukan per hari",
    p4="tarif 'Syringe Pump per Hari' sama persis dengan 'Infusion Pump per Hari' (278.000 rata di semua kolom) (sesuai PDF, dicek visual)",
    p7="'Syringe Pump per Hari' kode ALAB000024 (kelompok 'Alat Ruang Khusus', hlm. 64) dan ALAC000095 (alat OK, hlm. 65), serta versi '< 6 Jam' ALAB000045/ALAC000096; tarif sama"),
 'O2 / Hari': dict(
    nama='sama', use=[('ALAE000001', 'O2 per Hari', 65), ('ALAE000005', 'O2 Per Jam', 65, R), ('ALAE000002', 'O2 <= 6 Jam', 65, R)],
    p3="'O2 Per Jam' bersatuan per jam dan 'O2 <= 6 Jam' bersatuan <= 6 jam, bukan per hari",
    p7="'Incubator (Termasuk O2)' (inkubator), 'Sarung O2' (barang umum)"),
 'Nebulizer': dict(
    nama='beda', use=[('PRWT000065', 'Tindakan Nebulizer', 107), ('RHBB010011', 'Nebulizer', 38), ('ALAD000029', 'Nebulizer', 65)],
    p3="'Nebulizer' di tabel sewa alat adalah sewa alat, 'Tindakan Nebulizer' adalah tindakan perawat, 'Nebulizer' di tabel fisioterapi adalah layanan fisioterapi (ketiganya dimasukkan)",
    p7="'Nebulizer' kode ALAB000029 (kelompok 'Alat Ruang Khusus', 220.000), 'Nebulizer, Clapping, Vibrasi' (paket), 'Exercise Nebulizer' (exercise), "
       "'Tindakan Nebulizer' kode ANKJ000012 (poli anak, 351.000)"),
 'Creatinin': dict(
    nama='sama', use=[('LABA210200', 'Creatinin', 43)],
    p7="'Creatinin Clearance', 'Creatinin Urin' (clearance/urine), 'Albumin / Creatinin Urine Ratio (R)' (rasio urine)"),
 'Ureum': dict(
    nama='sama', use=[('LABA210100', 'Ureum', 43), ('LABA210900', 'BUN', 43, R)],
    p3="'BUN' (blood urea nitrogen) item terpisah dari ureum",
    p4="'BUN' lebih mahal dari 'Ureum' (sesuai PDF, dicek visual)",
    p7="'Ureum Clearance', 'Ureum Urin' (clearance/urine), 'Urea Breat Tes (UBT) (R)' (tes napas)"),
 'GDS': dict(
    nama='beda', use=[('LABA220300', 'Glukosa Darah Sewaktu', 43)],
    p7="'Glukosa Darah Puasa', 'Glukosa Darah PP', 'Glukosa Toleransi Test' (bukan sewaktu), 'Glukosa' dan 'Glukosa Urine Kuantitatif' (urinalisa)"),
 'Elektrolit (Na, K, Cl)': dict(
    nama='sama', use=[('LABA260100', 'Elektrolit (Na, K, Cl)', 43)],
    p7="'Natrium', 'Kalium', 'Chlorida' (item satuan; paket tersedia), 'Natrium Urin (R)', 'Kalium Urin (R)', 'Chlorida Urin (R)' (urine)"),
}
