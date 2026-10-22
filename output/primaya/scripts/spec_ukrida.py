"""Spec UKRIDA Primaya (DRAF dibuat make_spec_pri.py, lalu ditinjau manual; format sama dengan spec MIKA)."""
KEY = 'ukrida'
SHEET = 'UKRIDA Primaya'
PAGE_NOTE = 'hlm. = nomor halaman file PDF (urutan halaman di file), bukan nomor cetak'
SRC = "biaya administrasi rawat inap terpisah: AD005 'Administrasi Rawat Inap' (hlm. 4) 7% dari ... (teks di sel PDF terpotong)"
U = {
 'Konsultasi Dokter Umum IGD': dict(
    nama='beda',
    use=[('DR004', 'Konsultasi Dokter UGD', 4)],
    p7="'Isolasi UGD Tekanan Negatif tanpa Ventilator' (kamar isolasi); 'Konsultasi Dokter Umum' (konsultasi dokter umum poliklinik, bukan UGD); 'Konsultasi Dokter Spesialis ke IGD', 'Konsultasi Dokter Sub Spesialis ke IGD' (dokter spesialis/subspesialis); 'Observasi di UGD < 6 jam', 'Observasi di UGD > 6 jam' (observasi di UGD, bukan konsultasi)",
 ),
 'Konsultasi Spesialis Rawat Inap': dict(
    nama='beda',
    use=[('DR005', 'Visite Dokter Spesialis', 4), ('DR006', 'Visite Dokter Sub Spesialis / Konsultan', 4, {'role': 'Varian tingkat dokter (urutan kolom sama)'}), ('DR007', 'Visite Dokter Umum', 4, {'role': 'Ragu'})],
    p3="'Visite Dokter Umum' adalah visite dokter umum, bukan spesialis (padanan lemah)",
    p7="'Konsultasi Dokter Spesialis', 'Konsultasi Dokter Sub Spesialis / Konsultan', 'Konsultasi Dokter Spesialis ke IGD', 'Konsultasi Dokter Sub Spesialis ke IGD' (konsultasi rawat jalan, bukan visite rawat inap)",
 ),
 'Ruang Rawat': dict(
    nama='beda',
    rows={'III': [('KM001', 'Kelas III', 4), ('KM023', 'Bayi Sehat Kelas III', 4)], 'II': [('KM002', 'Kelas II', 4), ('KM024', 'Bayi Sehat Kelas II', 4)], 'I & R. KHUSUS': [('KM003', 'Kelas I', 4), ('KM025', 'Bayi Sehat Kelas I', 4)]}, row_labels={1: 'Varian bayi'},
    p3='varian bayi (bayi sehat) dimasukkan sebagai varian umur',
    p4="Excel memberi label \"RJ\" (rawat jalan) untuk tarif kamar rawat inap 'Kelas III', 'Kelas II', 'Kelas I' dan varian bayi sehat; di PDF kolom tarifnya berlabel 'Tairf' (hlm. 4). Label tetap mengikuti Excel sesuai keputusan user, mohon konfirmasi",
    p7="'Deluxe A', 'Suite', 'President Suite', 'Bayi Sehat Deluxe A', 'Bayi Sehat Suite', 'Bayi Sehat President Suite' (di atas kelas I); 'ICU', 'ICCU', 'NICU', 'PICU', 'PERINA', 'HCU' (ruang khusus); 'ISOLASI', 'Isolasi Suite Tekanan Negatif', 'Isolasi ICU/ICCU/PICU Tekanan Negatif Tanpa Ventilator', 'Isolasi HCU Tekanan Negatif Tanpa Ventilator', 'Isolasi Tekanan Negatif Tanpa Ventilator', 'Isolasi UGD Tekanan Negatif tanpa Ventilator', 'Isolasi President Suite Tekanan Negatif', 'Isolasi Deluxe Tekanan Negatif' dkk. (kamar isolasi); 'ODC' (one day care); 'VK Kelas III', 'VK Kelas II', 'VK Kelas I', 'VK Deluxe A', 'VK Suite', 'VK President Suite' (kamar bersalin (VK))",
 ),
 'Jasa Perawatan': dict(
    nama='sama',
    use=[('NB016', 'Jasa Perawatan', 25)],
    p7="'Jasa perawat Infus ICT/ SVF/ aaPRP' (perawat infus ICT/SVF)",
 ),
 'Pasang IV Line Access': dict(
    nama='beda',
    use=[('NB020', 'Pemasangan Infus', 25), ('DU065', 'Pemasangan Infus Dengan Penyulit', 19, {'role': 'Ragu'}), ('DU089', 'Venaseksi', 19, {'role': 'Ragu'})],
    p3="'Pemasangan Infus Dengan Penyulit' adalah pemasangan infus dengan penyulit oleh dokter umum; 'Venaseksi' adalah akses vena dengan sayatan (cut-down), bukan IV line biasa",
    p7="'Drip Infus' (drip infus (pemberian), bukan pemasangan); 'Pemasangan Infus Intraosseus' (infus intraoseus); 'Saline Infusion Sonohysterography (SIS)' (tindakan kebidanan); 'Jasa perawat Infus ICT/ SVF/ aaPRP' (infus terapi/estetik/onkologi)",
 ),
 'Injeksi IM / IV': dict(
    nama='beda',
    use=[('NB103', 'Injeksi Intramuskuler', 25), ('NB104', 'Injeksi Intravena', 25), ('DU103', 'Injeksi Intramuskuler', 20), ('DU104', 'Injeksi Intravena', 20)],
    p7="'Jasa Tindakan Injeksi Obat' (jasa tindakan injeksi obat (umum)); 'Injeksi Subkutan' (injeksi subkutan); 'Injeksi Intramuskular (USG Guidance) - Pain Management' (injeksi dengan panduan USG (pain management))",
 ),
 'Hematologi Lengkap': dict(
    nama='sama',
    use=[('A1003', 'Hematologi Lengkap', 5)],
    p7="'Hematologi Rutin', 'Hematologi Rutin + Diff count' (parameter lebih sedikit)",
 ),
 'CRP Kuantitatif': dict(
    nama='sama',
    use=[('C2007', 'CRP Kuantitatif', 7), ('B5007', 'hsCRP', 6, {'role': 'Ragu'})],
    p3="'hsCRP' adalah CRP sensitivitas tinggi (fungsi jantung), bukan CRP kuantitatif standar",
    p7='tidak ada CRP kualitatif/CRP tanpa keterangan',
 ),
 'Thorax PA': dict(
    nama='sama',
    use=[('XR114', 'Thorax PA', 14)],
    p7="'Thorax (AP + Lateral)', 'Thorax (AP + Lateral + Oblique)', 'Thorax (PA + Lateral)', 'Thorax (PA + Lateral + Oblique)' (kombinasi proyeksi); 'Thorax AP', 'Thorax Lateral', 'Thorax LLD', 'Thorax RLD', 'Thorax BED', 'Thorax Top Lordotic' (proyeksi lain)",
 ),
 'Infusion Pump / hari': dict(
    notfound="tidak ada teks «infusion pump» di PDF; buku tarif cabang ini tidak memuat bagian tarif pemakaian alat (daftar isi hlm. 3 tanpa bagian alat)",
    p5="Excel tidak memuat nama berisi «infusion pump» (sama dengan PDF)",
    p7="'Aff IABP (Intra Aortic Ballon Pump)', 'Pemasangan Intra-Aortic Ballon Pump' (pompa balon intra-aorta, bukan pompa infus/syringe)",
 ),
 'Syringe Pump / hari': dict(
    notfound="tidak ada teks «syringe» di PDF; buku tarif cabang ini tidak memuat bagian tarif pemakaian alat (daftar isi hlm. 3 tanpa bagian alat)",
    p5="Excel tidak memuat nama berisi «syringe» (sama dengan PDF)",
    p7="'Aff IABP (Intra Aortic Ballon Pump)', 'Pemasangan Intra-Aortic Ballon Pump' (pompa balon intra-aorta, bukan pompa infus/syringe)",
 ),
 'O2 / Hari': dict(
    nama='beda',
    use=[('OX002', 'Oksigen > 6 jam - 1 hari', 11), ('OX001', 'Oksigen / jam', 11, {'role': 'Ragu'})],
    p3="'Oksigen / jam' bersatuan per jam, bukan per hari",
    p4="di tabel 'F. GAS' (hlm. 11) oksigen hanya bertarif di kolom 'RJ'; kolom III, II, I, DELUXE, SUITE, P SUITE bertanda '-' (tidak ada tarif rawat inap tertulis). Sesuai aturan item satu tarif, tarif RJ dipakai di ketiga baris kelas dengan label Excel, mohon konfirmasi",
 ),
 'Nebulizer': dict(
    nama='beda',
    use=[('NB203', 'Inhalasi/Nebulisasi Dewasa', 25), ('DU203', 'Inhalasi/Nebulisasi Dewasa', 20), ('RM058', 'Nebulizer', 18)],
    p3="'Inhalasi/Nebulisasi Dewasa' adalah tindakan nebulisasi; 'Nebulizer' di rehabilitasi medik adalah layanan fisioterapi",
    p7="'1 Modalitas, Nebulizer, Chest Physiotherapy', '2 Modalitas, Nebulizer, Chest Physiotherapy', '3 Modalitas, Nebulizer, Chest Physiotherapy', '4 Modalitas, Nebulizer, Chest Physiotherapy', '5 Modalitas, Nebulizer, Chest Physiotherapy' (paket modalitas fisioterapi); 'Nebulizer + CFT', 'Nebulizer + CFT + IRR' (kombinasi fisioterapi)",
 ),
 'Creatinin': dict(
    nama='beda',
    use=[('B2002', 'Kreatinin + eGFR', 6)],
    p3="satu item 'Kreatinin + eGFR' (kreatinin dengan perhitungan eGFR); tidak ada item kreatinin tanpa eGFR",
    p7="'Creatinin Clearence (CCT)' (clearance); 'Rasio Albumin-Kreatinin Urin', 'Kreatinin - Urine', 'Kreatinin Urine 24 Jam' (urine)",
 ),
 'Ureum': dict(
    nama='sama',
    use=[('B2006', 'Ureum', 6)],
    p7="'Phenylketon Urea (PKU)' (skrining neonatal); 'Urea Clearance Test (UCT)' (clearance); 'UBT (Urea Breath Test)' (tes napas); 'Ureum - Urine' (urine)",
 ),
 'GDS': dict(
    nama='beda',
    use=[('B3005', 'Glukosa Darah (Sewaktu)', 6), ('B3020', 'POCT Glukosa Darah (Sewaktu)', 6, {'role': 'Ragu'})],
    p3="'POCT Glukosa Darah (Sewaktu)' adalah pemeriksaan POCT (alat point-of-care), bukan analisa laboratorium",
    p7="'Glukosa Darah (2 Jam PP)', 'Glukosa Darah (Puasa)' (bukan sewaktu); 'POCT Glukosa Darah (Puasa)', 'POCT Glukosa Darah (2 Jam PP)' (POCT bukan sewaktu)",
 ),
 'Elektrolit (Na, K, Cl)': dict(
    nama='beda',
    use=[('B6008', 'Elektrolit Serum (Na, K, Cl)', 6)],
 ),
}
