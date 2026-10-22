"""Spec Primaya Kelapa Gading (DRAF dibuat make_spec_pri.py, lalu ditinjau manual; format sama dengan spec MIKA)."""
KEY = 'kelapagading'
SHEET = 'Primaya Kelapa Gading'
PAGE_NOTE = 'hlm. = nomor halaman file PDF (urutan halaman di file), bukan nomor cetak'
SRC = "Effective Date per tabel 'PER 01 JANUARI 2026' (hlm. 3); biaya administrasi rawat inap terpisah: AD005 'Administrasi Rawat Inap' (hlm. 3) 7% dari total billing"
U = {
 'Konsultasi Dokter Umum IGD': dict(
    nama='beda',
    use=[('DR004', 'Konsultasi Dokter UGD', 4)],
    p7="'Konsultasi Dokter Umum' (konsultasi dokter umum poliklinik, bukan UGD); 'Tele Konsultasi Dokter Umum' (telekonsultasi); 'Konsultasi Dokter Spesialis ke IGD', 'Konsultasi Dokter Sub Spesialis ke IGD', 'Konsultasi Dokter Sub Spesialis dr. Suwito SpPD KGEH hadir di IGD', 'Konsultasi Dokter Sub Spesialis / Konsultan Professor hadir di IGD' (dokter spesialis/subspesialis); 'Observasi di UGD < 6 jam', 'Observasi di UGD > 6 jam' (observasi di UGD, bukan konsultasi)",
 ),
 'Konsultasi Spesialis Rawat Inap': dict(
    nama='beda',
    use=[('DR005', 'Visite Dokter Spesialis', 6), ('DR006', 'Visite Dokter Sub Spesialis / Konsultan', 6, {'role': 'Varian tingkat dokter (urutan kolom sama)'}), ('DR007', 'Visite Dokter Umum', 6, {'role': 'Ragu'})],
    p3="'Visite Dokter Umum' adalah visite dokter umum, bukan spesialis (padanan lemah)",
    p7="'Konsultasi Dokter Spesialis', 'Konsultasi Dokter Spesialis (Hari Libur)', 'Konsultasi Dokter Spesialis Jiwa < 30 menit', 'Konsultasi Dokter Spesialis Jiwa 30 - 60 menit', 'Konsultasi Dokter Spesialis Jiwa 60 - 90 menit', 'Konsultasi Dokter Spesialis Jiwa > 90 menit', 'Konsultasi Dokter Spesialis ke IGD', 'Konsultasi Dokter Sub Spesialis / Konsultan' dkk. (konsultasi rawat jalan, bukan visite rawat inap); 'Konsultasi Dokter Sub Spesialis / Konsultan Professor', 'Konsultasi Dokter Sub Spesialis dr. Suwito SpPD KGEH', 'Konsultasi Dokter Sub Spesialis dr. Suwito SpPD KGEH hadir di IGD', 'Konsultasi Dokter Sub Spesialis / Konsultan Professor hadir di IGD', 'Visite Dokter Sub Spesialis / Konsultan dr. Suwito SpPD KGEH', 'Visite Dokter Sub Spesialis / Konsultan Professor' (dokter tertentu/profesor); 'Visite On Call Dokter Spesialis (Audio Visual)', 'Visite On Call Dokter Spesialis (Audio)', 'Visite On Call Dokter Spesialis (Chat)', 'Visite On Call Dokter Sub Spesialis (Audio Visual)', 'Visite On Call Dokter Sub Spesialis (Audio)', 'Visite On Call Dokter Sub Spesialis (Chat)' (visite on call jarak jauh (audio/visual/chat)); 'Visite Laktasi' (laktasi)",
 ),
 'Ruang Rawat': dict(
    nama='beda',
    use=[('', 'Kamar Perawatan', 5), ('', 'Kamar Bayi Sehat', 5, {'role': 'Varian bayi'})],
    p7="'Kamar ICU/ ICCU', 'Kamar NICU / PICU', 'Kamar PERINA', 'Kamar HCU' (ruang khusus); 'Kamar Isolasi' (kamar isolasi); 'Kamar ODC (One Day Care)' (one day care); 'Kamar VK' (kamar bersalin)",
 ),
 'Jasa Perawatan': dict(
    nama='sama',
    use=[('DR053', 'Jasa Perawatan', 6)],
    p6="'Jasa Perawatan' di PDF tercantum di tabel 'TARIF JASA VISITE DOKTER / HARI' dengan kode DR053 (tidak ada di tabel 'TARIF PERAWAT')",
    p7="'Jasa Perawat Pendamping Kemoterapi' (pendampingan)",
 ),
 'Pasang IV Line Access': dict(
    nama='beda',
    use=[('NB020', 'Pemasangan Infus', 78), ('DU065', 'Pemasangan Infus Dengan Penyulit', 7, {'role': 'Ragu'}), ('DU089', 'Venaseksi', 8, {'role': 'Ragu'})],
    p3="'Pemasangan Infus Dengan Penyulit' adalah pemasangan infus dengan penyulit oleh dokter umum; 'Venaseksi' adalah akses vena dengan sayatan (cut-down), bukan IV line biasa",
    p7="'Drip Infus' (drip infus (pemberian), bukan pemasangan); 'Pemasangan Infus Intraosseus' (infus intraoseus); 'Saline Infusion Sonohysterography (SIS)' (tindakan kebidanan); 'Infusion Pump 1 s/d 6 jam', 'Infusion Pump > 6 jam - 1 hari' (alat infusion pump)",
 ),
 'Injeksi IM / IV': dict(
    nama='beda',
    use=[('DS490', 'Injeksi Intramuskuler', 10), ('DS491', 'Injeksi Intravena', 10)],
    p3="di buku tidak ada item injeksi intramuskuler/intravena di tabel perawat ('TARIF PERAWAT') maupun dokter umum ('TARIF JASA PEMERIKSAAN DOKTER UMUM'); yang ada hanya di tabel 'TARIF JASA PEMERIKSAAN DOKTER SPESIALIS' (tindakan oleh dokter spesialis)",
    p7="'Jasa Tindakan Injeksi Obat' (jasa tindakan injeksi obat (umum), tidak menyebut IM/IV); 'Injeksi Subkutan', 'Injeksi Intrakutan' (rute lain); 'Injeksi Intramuskular (USG Guidance) - Pain Management' (injeksi dengan panduan USG (pain management)); 'Injeksi Obat IV/IM' (homecare)",
 ),
 'Hematologi Lengkap': dict(
    nama='sama',
    use=[('A1003', 'Hematologi Lengkap', 31)],
    p7="'Hematologi Rutin', 'Hematologi Rutin + Diff count' (parameter lebih sedikit)",
 ),
 'CRP Kuantitatif': dict(
    nama='sama',
    use=[('C2007', 'CRP Kuantitatif', 33), ('B5007', 'hsCRP', 32, {'role': 'Ragu'})],
    p3="'hsCRP' adalah CRP sensitivitas tinggi (fungsi jantung), bukan CRP kuantitatif standar",
    p7='tidak ada CRP kualitatif/CRP tanpa keterangan',
 ),
 'Thorax PA': dict(
    nama='sama',
    use=[('XR114', 'Thorax PA', 40)],
    p7="'Thorax (AP + Lateral)', 'Thorax (AP + Lateral + Oblique)', 'Thorax (PA + Lateral)', 'Thorax (PA + Lateral + Oblique)' (kombinasi proyeksi); 'Thorax AP', 'Thorax Lateral', 'Thorax LLD', 'Thorax RLD', 'Thorax BED', 'Thorax Top Lordotic' (proyeksi lain)",
 ),
 'Infusion Pump / hari': dict(
    nama='beda',
    use=[('SA020', 'Infusion Pump > 6 jam - 1 hari', 45), ('SA035', 'Infusion Pump 1 s/d 6 jam', 45, {'role': 'Ragu'})],
    p3="'Infusion Pump 1 s/d 6 jam' bersatuan 1-6 jam, bukan per hari",
 ),
 'Syringe Pump / hari': dict(
    nama='beda',
    use=[('SA107', 'Syringe Pump > 6 jam - 1 hari', 45), ('SA059', 'Syringe Pump 1 s/d 6 jam', 45, {'role': 'Ragu'})],
    p3="'Syringe Pump 1 s/d 6 jam' bersatuan 1-6 jam, bukan per hari",
 ),
 'O2 / Hari': dict(
    nama='beda',
    use=[('OX002', 'Oksigen > 6 jam - 1 hari', 44), ('OX001', 'Oksigen / jam', 44, {'role': 'Ragu'})],
    p3="'Oksigen / jam' bersatuan per jam, bukan per hari",
 ),
 'Nebulizer': dict(
    nama='beda',
    use=[('DU203', 'Inhalasi/Nebulisasi Dewasa', 8), ('RM058', 'Nebulizer', 28)],
    p3="'Inhalasi/Nebulisasi Dewasa' adalah tindakan nebulisasi; 'Nebulizer' di rehabilitasi medik adalah layanan fisioterapi",
    p7="'1 Modalitas, Nebulizer, Chest Physiotherapy', '2 Modalitas, Nebulizer, Chest Physiotherapy', '3 Modalitas, Nebulizer, Chest Physiotherapy', '4 Modalitas, Nebulizer, Chest Physiotherapy', '5 Modalitas, Nebulizer, Chest Physiotherapy' (paket modalitas fisioterapi); 'Nebulizer + CFT', 'Nebulizer + CFT + IRR' (kombinasi fisioterapi)",
 ),
 'Creatinin': dict(
    nama='beda',
    use=[('B2002', 'Kreatinin + eGFR', 32)],
    p3="satu item 'Kreatinin + eGFR' (kreatinin dengan perhitungan eGFR); tidak ada item kreatinin tanpa eGFR",
    p7="'Creatinin Clearence (CCT)' (clearance); 'Rasio Albumin-Kreatinin Urin', 'Kreatinin - Urine', 'Kreatinin Urine 24 Jam' (urine)",
 ),
 'Ureum': dict(
    nama='sama',
    use=[('B2006', 'Ureum', 32)],
    p7="'Phenylketon Urea (PKU)' (skrining neonatal); 'Urea Clearance Test (UCT)' (clearance); 'UBT (Urea Breath Test)' (tes napas); 'Ureum - Urine' (urine)",
 ),
 'GDS': dict(
    nama='beda',
    use=[('B3005', 'Glukosa Darah (Sewaktu)', 32), ('B3020', 'POCT Glukosa Darah (Sewaktu)', 32, {'role': 'Ragu'})],
    p3="'POCT Glukosa Darah (Sewaktu)' adalah pemeriksaan POCT (alat point-of-care), bukan analisa laboratorium",
    p7="'Glukosa Darah (2 Jam PP)', 'Glukosa Darah (Puasa)' (bukan sewaktu); 'POCT Glukosa Darah (Puasa)', 'POCT Glukosa Darah (2 Jam PP)' (POCT bukan sewaktu)",
 ),
 'Elektrolit (Na, K, Cl)': dict(
    nama='beda',
    use=[('B6008', 'Elektrolit Serum (Na, K, Cl)', 32)],
 ),
}
