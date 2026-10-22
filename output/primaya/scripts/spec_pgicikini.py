"""Spec Primaya PGI Cikini (DRAF dibuat make_spec_pri.py, lalu ditinjau manual; format sama dengan spec MIKA)."""
KEY = 'pgicikini'
SHEET = 'Primaya PGI Cikini'
PAGE_NOTE = 'hlm. = nomor halaman file PDF (urutan halaman di file), bukan nomor cetak'
SRC = "biaya administrasi rawat inap terpisah: AD005 'Administrasi Rawat Inap' (hlm. 3) 7% dari total biaya perawatan"
U = {
 'Konsultasi Dokter Umum IGD': dict(
    nama='beda',
    use=[('DR004', 'Konsultasi Dokter UGD', 4)],
    p7="'Konsultasi Dokter Umum' (konsultasi dokter umum poliklinik, bukan UGD); 'Tele Konsultasi Dokter Umum' (telekonsultasi); 'Konsultasi Dokter Umum (Hari Libur)' (hari libur); 'Konsultasi Dokter Spesialis ke IGD', 'Konsultasi Dokter Sub Spesialis ke IGD' (dokter spesialis/subspesialis); 'Observasi di UGD < 6 jam', 'Observasi di UGD > 6 jam' (observasi di UGD, bukan konsultasi)",
 ),
 'Konsultasi Spesialis Rawat Inap': dict(
    nama='beda',
    use=[('DR005', 'Visite Dokter Spesialis', 6), ('DR006', 'Visite Dokter Sub Spesialis / Konsultan', 6, {'role': 'Varian tingkat dokter (urutan kolom sama)'}), ('DR007', 'Visite Dokter Umum', 6, {'role': 'Ragu'})],
    p3="'Visite Dokter Umum' adalah visite dokter umum, bukan spesialis (padanan lemah)",
    p7="'Konsultasi Dokter Spesialis', 'Konsultasi Dokter Sub Spesialis / Konsultan', 'Konsultasi Dokter Spesialis (Hari Libur)', 'Konsultasi Dokter Spesialis ke IGD', 'Konsultasi Dokter Sub Spesialis ke IGD', 'Konsultasi Dokter Sub Spesialis / Konsultan (Hari Libur)', 'Konsultasi Dokter Spesialis Jiwa < 30 menit', 'Konsultasi Dokter Spesialis Jiwa 30 - 60 menit' dkk. (konsultasi rawat jalan, bukan visite rawat inap); 'Visite On Call Dokter Spesialis (Audio Visual)', 'Visite On Call Dokter Spesialis (Audio)', 'Visite On Call Dokter Spesialis (Chat)', 'Visite On Call Dokter Sub Spesialis (Audio Visual)', 'Visite On Call Dokter Sub Spesialis (Audio)', 'Visite On Call Dokter Sub Spesialis (Chat)' (visite on call jarak jauh (audio/visual/chat)); 'Visite Laktasi' (laktasi); 'Visite Professor' (dokter tertentu/profesor); 'Visite Pasien CRRT/CVVH' (pasien CRRT/CVVH)",
 ),
 'Ruang Rawat': dict(
    nama='beda',
    rows={'III': [('KM001', 'Kelas III', 5), ('KM023', 'Bayi Sehat Kelas III', 5)], 'II': [('KM002', 'Kelas II', 5), ('KM024', 'Bayi Sehat Kelas II', 5)], 'I & R. KHUSUS': [('KM003', 'Kelas I', 5), ('KM025', 'Bayi Sehat Kelas I', 5)]}, row_labels={1: 'Varian bayi'},
    p3='varian bayi (bayi sehat) dimasukkan sebagai varian umur',
    p7="'Deluxe A', 'Suite', 'President Suite', 'Bayi Sehat Deluxe A', 'Bayi Sehat Suite', 'Bayi Sehat President Suite' (di atas kelas I); 'ICU', 'ICCU', 'NICU', 'PICU', 'PERINA', 'HCU' (ruang khusus); 'ISOLASI', 'Isolasi HCU Tekanan Negatif Tanpa Ventilator', 'Isolasi ICU Tekanan Negatif Tanpa Ventilator' (kamar isolasi); 'ODC' (one day care); 'VK Kelas III', 'VK Kelas II', 'VK Kelas I', 'VK Deluxe A', 'VK Suite', 'VK President Suite' (kamar bersalin (VK))",
 ),
 'Jasa Perawatan': dict(
    nama='sama',
    use=[('NB016', 'Jasa Perawatan', 52)],
    p7="'Jasa perawat Infus ICT/ SVF/ aaPRP' (perawat infus ICT/SVF); 'Jasa Perawat Pendamping Kemoterapi' (pendampingan)",
 ),
 'Pasang IV Line Access': dict(
    nama='beda',
    use=[('NB020', 'Pemasangan Infus', 52), ('DU065', 'Pemasangan Infus Dengan Penyulit', 45, {'role': 'Ragu'}), ('DU089', 'Venaseksi', 45, {'role': 'Ragu'})],
    p3="'Pemasangan Infus Dengan Penyulit' adalah pemasangan infus dengan penyulit oleh dokter umum; 'Venaseksi' adalah akses vena dengan sayatan (cut-down), bukan IV line biasa",
    p4="nama item DU065 di hlm. 45 terpotong batas sel pada tampilan PDF (yang terlihat hanya sampai «Dengan Peny»); teks lengkap 'Pemasangan Infus Dengan Penyulit' ada di lapisan teks PDF dan dipakai apa adanya",
    p7="'Drip Infus' (drip infus (pemberian), bukan pemasangan); 'Pemasangan Infus Intraosseus' (infus intraoseus); 'Infusion Pump 1 s/d 6 jam', 'Infusion Pump > 6 jam - 1 hari' (alat infusion pump); 'Saline Infusion Sonohysterography (SIS)' (tindakan kebidanan); 'Jasa perawat Infus ICT/ SVF/ aaPRP', 'Pemasangan Infus untuk Targeting Terapi' (infus terapi/estetik/onkologi)",
 ),
 'Injeksi IM / IV': dict(
    nama='beda',
    use=[('NB103', 'Injeksi Intramuskuler', 52), ('NB104', 'Injeksi Intravena', 52), ('DU103', 'Injeksi Intramuskuler', 45), ('DU104', 'Injeksi Intravena', 45)],
    p7="'Jasa Tindakan Injeksi Obat' (jasa tindakan injeksi obat (umum)); 'Injeksi Subkutan' (injeksi subkutan); 'Injeksi Intramuskular (USG Guidance) - Pain Manag' (injeksi dengan panduan USG (pain management))",
 ),
 'Hematologi Lengkap': dict(
    nama='sama',
    use=[('A1003', 'Hematologi Lengkap', 14)],
    p7="'Hematologi Rutin', 'Hematologi Rutin + Diff count' (parameter lebih sedikit)",
 ),
 'CRP Kuantitatif': dict(
    nama='sama',
    use=[('C2007', 'CRP Kuantitatif', 16), ('B5007', 'hsCRP', 15, {'role': 'Ragu'})],
    p3="'hsCRP' adalah CRP sensitivitas tinggi (fungsi jantung), bukan CRP kuantitatif standar",
    p7='tidak ada CRP kualitatif/CRP tanpa keterangan',
 ),
 'Thorax PA': dict(
    nama='sama',
    use=[('XR114', 'Thorax PA', 25)],
    p6="buku memuat tiga tabel radiologi: 'TARIF RADIOLOGI' (tarif total, dipakai), 'TARIF RADIOLOGI RS' (komponen RS) dan 'TARIF RADIOLOGI DOKTER' (jasa expertise)",
    p7="'Thorax PA' di tabel 'TARIF RADIOLOGI RS' (hlm. 30, komponen RS saja: III 327.000 / II 376.000 / I 406.000); 'Thorax PA - Jasa Expertise' di tabel 'TARIF RADIOLOGI DOKTER' (hlm. 36, jasa dokter saja); 'Thorax (AP + Lateral)', 'Thorax (AP + Lateral + Oblique)', 'Thorax (PA + Lateral)', 'Thorax (PA + Lateral + Oblique)' (kombinasi proyeksi); 'Thorax AP', 'Thorax Lateral', 'Thorax LLD', 'Thorax RLD', 'Thorax BED', 'Thorax Top Lordotic' (proyeksi lain)",
 ),
 'Infusion Pump / hari': dict(
    nama='beda',
    use=[('SA020', 'Infusion Pump > 6 jam - 1 hari', 58), ('SA035', 'Infusion Pump 1 s/d 6 jam', 58, {'role': 'Ragu'})],
    p3="'Infusion Pump 1 s/d 6 jam' bersatuan 1-6 jam, bukan per hari",
 ),
 'Syringe Pump / hari': dict(
    nama='beda',
    use=[('SA107', 'Syringe Pump > 6 jam - 1 hari', 58), ('SA059', 'Syringe Pump 1 s/d 6 jam', 58, {'role': 'Ragu'})],
    p3="'Syringe Pump 1 s/d 6 jam' bersatuan 1-6 jam, bukan per hari",
 ),
 'O2 / Hari': dict(
    nama='beda',
    use=[('OX002', 'Oksigen > 6 jam - 1 hari', 22), ('OX001', 'Oksigen / jam', 22, {'role': 'Ragu'})],
    p3="'Oksigen / jam' bersatuan per jam, bukan per hari",
 ),
 'Nebulizer': dict(
    nama='beda',
    use=[('NB203', 'Inhalasi/Nebulisasi Dewasa', 52), ('DU203', 'Inhalasi/Nebulisasi Dewasa', 45), ('RM058', 'Nebulizer', 42)],
    p3="'Inhalasi/Nebulisasi Dewasa' adalah tindakan nebulisasi; 'Nebulizer' di rehabilitasi medik adalah layanan fisioterapi",
    p7="'1 Modalitas, Nebulizer, Chest Physiotherapy', '2 Modalitas, Nebulizer, Chest Physiotherapy', '3 Modalitas, Nebulizer, Chest Physiotherapy', '4 Modalitas, Nebulizer, Chest Physiotherapy', '5 Modalitas, Nebulizer, Chest Physiotherapy' (paket modalitas fisioterapi); 'Nebulizer + CFT', 'Nebulizer + CFT + IRR' (kombinasi fisioterapi)",
 ),
 'Creatinin': dict(
    nama='beda',
    use=[('B2002', 'Kreatinin + eGFR', 15)],
    p3="satu item 'Kreatinin + eGFR' (kreatinin dengan perhitungan eGFR); tidak ada item kreatinin tanpa eGFR",
    p7="'Creatinin Clearence (CCT)' (clearance); 'Rasio Albumin-Kreatinin Urin', 'Kreatinin - Urine', 'Kreatinin Urine 24 Jam' (urine)",
 ),
 'Ureum': dict(
    nama='sama',
    use=[('B2006', 'Ureum', 15)],
    p7="'Phenylketon Urea (PKU)' (skrining neonatal); 'Urea Clearance Test (UCT)' (clearance); 'UBT (Urea Breath Test)' (tes napas); 'Ureum - Urine' (urine)",
 ),
 'GDS': dict(
    nama='beda',
    use=[('B3005', 'Glukosa Darah (Sewaktu)', 15), ('B3020', 'POCT Glukosa Darah (Sewaktu)', 15, {'role': 'Ragu'})],
    p3="'POCT Glukosa Darah (Sewaktu)' adalah pemeriksaan POCT (alat point-of-care), bukan analisa laboratorium",
    p7="'Glukosa Darah (2 Jam PP)', 'Glukosa Darah (Puasa)' (bukan sewaktu); 'POCT Glukosa Darah (Puasa)', 'POCT Glukosa Darah (2 Jam PP)' (POCT bukan sewaktu)",
 ),
 'Elektrolit (Na, K, Cl)': dict(
    nama='beda',
    use=[('B6008', 'Elektrolit Serum (Na, K, Cl)', 15)],
 ),
}
