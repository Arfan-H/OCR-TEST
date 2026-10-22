"""Spec Primaya Betang Pambelum (DRAF dibuat make_spec_pri.py, lalu ditinjau manual; format sama dengan spec MIKA)."""
KEY = 'betang'
SHEET = 'Primaya Betang Pambelum'
PAGE_NOTE = 'hlm. = nomor halaman file PDF (urutan halaman di file), bukan nomor cetak'
SRC = "berlaku: 'mulai berlaku sejak 01 Januari 2026' (hlm. 4); biaya administrasi rawat inap terpisah: AD005 'Administrasi Rawat Inap' (hlm. 6) 7% dari total biaya perawatan"
U = {
 'Konsultasi Dokter Umum IGD': dict(
    nama='beda',
    use=[('DR004', 'Konsultasi Dokter UGD', 7)],
    p7="'Konsultasi Dokter Umum' (konsultasi dokter umum poliklinik, bukan UGD); 'Tele Konsultasi Dokter Umum' (telekonsultasi); 'Konsultasi Dokter Spesialis ke IGD', 'Konsultasi Dokter Sub Spesialis ke IGD' (dokter spesialis/subspesialis); 'Observasi di UGD < 6 jam', 'Observasi di UGD > 6 jam' (observasi di UGD, bukan konsultasi)",
 ),
 'Konsultasi Spesialis Rawat Inap': dict(
    nama='beda',
    use=[('DR005', 'Visite Dokter Spesialis', 31), ('DR006', 'Visite Dokter Sub Spesialis / Konsultan', 31, {'role': 'Varian tingkat dokter (urutan kolom sama)'}), ('DR007', 'Visite Dokter Umum', 31, {'role': 'Ragu'})],
    p3="'Visite Dokter Umum' adalah visite dokter umum, bukan spesialis (padanan lemah)",
    p7="'Konsultasi Dokter Spesialis', 'Konsultasi Dokter Spesialis ke IGD', 'Konsultasi Dokter Sub Spesialis / Konsultan', 'Konsultasi Dokter Sub Spesialis ke IGD', 'Konsultasi Dokter Spesialis Jiwa < 30 menit', 'Konsultasi Dokter Spesialis Jiwa 30 - 60 menit', 'Konsultasi Dokter Spesialis Jiwa 60 - 90 menit', 'Konsultasi Dokter Spesialis Jiwa > 90 menit' (konsultasi rawat jalan, bukan visite rawat inap); 'Visite On Call Dokter Spesialis (Audio Visual)', 'Visite On Call Dokter Spesialis (Audio)', 'Visite On Call Dokter Spesialis (Chat)', 'Visite On Call Dokter Sub Spesialis (Audio Visual)', 'Visite On Call Dokter Sub Spesialis (Audio)', 'Visite On Call Dokter Sub Spesialis (Chat)' (visite on call jarak jauh (audio/visual/chat))",
 ),
 'Ruang Rawat': dict(
    nama='beda',
    rows={'III': [('KM001', 'Kelas III', 30), ('KM023', 'Bayi Sehat Kelas III', 30)], 'II': [('KM002', 'Kelas II', 30), ('KM024', 'Bayi Sehat Kelas II', 30)], 'I & R. KHUSUS': [('KM003', 'Kelas I', 30), ('KM025', 'Bayi Sehat Kelas I', 30)]}, row_labels={1: 'Varian bayi'},
    p3='varian bayi (bayi sehat) dimasukkan sebagai varian umur',
    p7="'Deluxe A', 'Deluxe B', 'Suite', 'President Suite', 'Bayi Sehat Deluxe A', 'Bayi Sehat Deluxe B', 'Bayi Sehat Suite', 'Bayi Sehat President Suite' (di atas kelas I); 'ICU', 'ICCU', 'NICU', 'PICU', 'PERINA', 'HCU' (ruang khusus); 'ISOLASI', 'Isolasi Suite Tekanan Negatif' (kamar isolasi); 'ODC' (one day care); 'VK Kelas III', 'VK Kelas II', 'VK Kelas I', 'VK Deluxe A', 'VK Deluxe B', 'VK Suite', 'VK President Suite' (kamar bersalin (VK))",
 ),
 'Jasa Perawatan': dict(
    nama='sama',
    use=[('NB016', 'Jasa Perawatan', 32)],
 ),
 'Pasang IV Line Access': dict(
    nama='beda',
    use=[('NB020', 'Pemasangan Infus', 32), ('DU065', 'Pemasangan Infus Dengan Penyulit', 39, {'role': 'Ragu'}), ('DU089', 'Venaseksi', 40, {'role': 'Ragu'})],
    p3="'Pemasangan Infus Dengan Penyulit' adalah pemasangan infus dengan penyulit oleh dokter umum; 'Venaseksi' adalah akses vena dengan sayatan (cut-down), bukan IV line biasa",
    p7="'Saline Infusion Sonohysterography (SIS)' (tindakan kebidanan); 'Drip Infus' (drip infus (pemberian), bukan pemasangan); 'Infusion Pump 1 s/d 6 jam', 'Infusion Pump > 6 jam - 1 hari' (alat infusion pump); 'Pemasangan Infus Intraosseus' (infus intraoseus)",
 ),
 'Injeksi IM / IV': dict(
    nama='beda',
    use=[('NB103', 'Injeksi Intramuskuler', 32), ('NB104', 'Injeksi Intravena', 32), ('DU103', 'Injeksi Intramuskuler', 40), ('DU104', 'Injeksi Intravena', 40)],
    p7="'Injeksi Subkutan' (injeksi subkutan); 'Jasa Tindakan Injeksi Obat' (jasa tindakan injeksi obat (umum)); 'Injeksi Intramuskular (USG Guidance) - Pain Management' (injeksi dengan panduan USG (pain management))",
 ),
 'Hematologi Lengkap': dict(
    nama='sama',
    use=[('A1003', 'Hematologi Lengkap', 50)],
    p7="'Hematologi Rutin', 'Hematologi Rutin + Diff count' (parameter lebih sedikit)",
 ),
 'CRP Kuantitatif': dict(
    nama='sama',
    use=[('C2007', 'CRP Kuantitatif', 54), ('B5007', 'hsCRP', 53, {'role': 'Ragu'})],
    p3="'hsCRP' adalah CRP sensitivitas tinggi (fungsi jantung), bukan CRP kuantitatif standar",
    p7='tidak ada CRP kualitatif/CRP tanpa keterangan',
 ),
 'Thorax PA': dict(
    nama='sama',
    use=[('XR114', 'Thorax PA', 67)],
    p7="'Thorax (AP + Lateral)', 'Thorax (AP + Lateral + Oblique)', 'Thorax (PA + Lateral)', 'Thorax (PA + Lateral + Oblique)' (kombinasi proyeksi); 'Thorax AP', 'Thorax Lateral', 'Thorax LLD', 'Thorax RLD', 'Thorax BED', 'Thorax Top Lordotic' (proyeksi lain)",
 ),
 'Infusion Pump / hari': dict(
    nama='beda',
    use=[('SA020', 'Infusion Pump > 6 jam - 1 hari', 34), ('SA035', 'Infusion Pump 1 s/d 6 jam', 34, {'role': 'Ragu'})],
    p3="'Infusion Pump 1 s/d 6 jam' bersatuan 1-6 jam, bukan per hari",
 ),
 'Syringe Pump / hari': dict(
    nama='beda',
    use=[('SA107', 'Syringe Pump > 6 jam - 1 hari', 35), ('SA059', 'Syringe Pump 1 s/d 6 jam', 35, {'role': 'Ragu'})],
    p3="'Syringe Pump 1 s/d 6 jam' bersatuan 1-6 jam, bukan per hari",
 ),
 'O2 / Hari': dict(
    nama='beda',
    use=[('OX002', 'Oksigen > 6 jam - 1 hari', 33), ('OX001', 'Oksigen / jam', 33, {'role': 'Ragu'})],
    p3="'Oksigen / jam' bersatuan per jam, bukan per hari",
 ),
 'Nebulizer': dict(
    nama='beda',
    use=[('NB203', 'Inhalasi/Nebulisasi Dewasa', 32), ('DU203', 'Inhalasi/Nebulisasi Dewasa', 40), ('RM058', 'Nebulizer', 26)],
    p3="'Inhalasi/Nebulisasi Dewasa' adalah tindakan nebulisasi; 'Nebulizer' di rehabilitasi medik adalah layanan fisioterapi",
    p7="'1 Modalitas, Nebulizer, Chest Physiotherapy', '2 Modalitas, Nebulizer, Chest Physiotherapy', '3 Modalitas, Nebulizer, Chest Physiotherapy', '4 Modalitas, Nebulizer, Chest Physiotherapy', '5 Modalitas, Nebulizer, Chest Physiotherapy' (paket modalitas fisioterapi); 'Nebulizer + CFT', 'Nebulizer + CFT +' (kombinasi fisioterapi)",
 ),
 'Creatinin': dict(
    nama='beda',
    use=[('B2002', 'Kreatinin + eGFR', 52)],
    p3="satu item 'Kreatinin + eGFR' (kreatinin dengan perhitungan eGFR); tidak ada item kreatinin tanpa eGFR",
    p7="'Creatinin Clearence (CCT)' (clearance); 'Rasio Albumin-Kreatinin Urin', 'Kreatinin - Urine', 'Kreatinin Urine 24 Jam' (urine)",
 ),
 'Ureum': dict(
    nama='sama',
    use=[('B2006', 'Ureum', 52)],
    p7="'Phenylketon Urea (PKU)' (skrining neonatal); 'Urea Clearance Test (UCT)' (clearance); 'UBT (Urea Breath Test)' (tes napas); 'Ureum - Urine' (urine)",
 ),
 'GDS': dict(
    nama='beda',
    use=[('B3005', 'Glukosa Darah (Sewaktu)', 52), ('B3020', 'POCT Glukosa Darah (Sewaktu)', 52, {'role': 'Ragu'})],
    p3="'POCT Glukosa Darah (Sewaktu)' adalah pemeriksaan POCT (alat point-of-care), bukan analisa laboratorium",
    p7="'Glukosa Darah (2 Jam PP)', 'Glukosa Darah (Puasa)' (bukan sewaktu); 'POCT Glukosa Darah (Puasa)', 'POCT Glukosa Darah (2 Jam PP)' (POCT bukan sewaktu)",
 ),
 'Elektrolit (Na, K, Cl)': dict(
    nama='beda',
    use=[('B6008', 'Elektrolit Serum (Na, K, Cl)', 53)],
 ),
}
