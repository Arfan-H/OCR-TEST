"""Spec Primaya Depok (DRAF dibuat make_spec_pri.py, lalu ditinjau manual; format sama dengan spec MIKA)."""
KEY = 'depok'
SHEET = 'Primaya Depok'
PAGE_NOTE = 'hlm. = nomor halaman file PDF (urutan halaman di file), bukan nomor cetak'
SRC = "Effective Date per tabel 'TARIF 1 JANUARI 2026' (hlm. 4); biaya administrasi rawat inap terpisah: AD005 'Administrasi Rawat Inap' (hlm. 5) 7% dari total biaya perawatan"
U = {
 'Konsultasi Dokter Umum IGD': dict(
    nama='beda',
    use=[('DR004', 'Konsultasi Dokter UGD', 6)],
    p7="'Konsultasi Dokter Umum' (konsultasi dokter umum poliklinik, bukan UGD); 'Tele Konsultasi Dokter Umum' (telekonsultasi); 'Observasi di UGD < 6 jam', 'Observasi di UGD > 6 jam' (observasi di UGD, bukan konsultasi)",
 ),
 'Konsultasi Spesialis Rawat Inap': dict(
    nama='beda',
    use=[('DR005', 'Visite Dokter Spesialis', 7), ('DR006', 'Visite Dokter Sub Spesialis / Konsultan', 7, {'role': 'Varian tingkat dokter (urutan kolom sama)'}), ('DR007', 'Visite Dokter Umum', 7, {'role': 'Ragu'})],
    p3="'Visite Dokter Umum' adalah visite dokter umum, bukan spesialis (padanan lemah)",
    p7="'Konsultasi Dokter Spesialis', 'Konsultasi Dokter Sub Spesialis / Konsultan', 'Konsultasi Dokter Spesialis (Hari Libur)', 'Konsultasi Dokter Sub Spesialis / Konsultan (Hari Libur)' (konsultasi rawat jalan, bukan visite rawat inap); 'Visite On Call Dokter Spesialis (Audio Visual)', 'Visite On Call Dokter Spesialis (Audio)', 'Visite On Call Dokter Spesialis (Chat)', 'Visite On Call Dokter Sub Spesialis (Audio Visual)', 'Visite On Call Dokter Sub Spesialis (Audio)', 'Visite On Call Dokter Sub Spesialis (Chat)' (visite on call jarak jauh (audio/visual/chat))",
 ),
 'Ruang Rawat': dict(
    nama='beda',
    rows={'III': [('KM001', 'Kelas III', 4), ('KM023', 'Bayi Sehat Kelas III', 4)], 'II': [('KM002', 'Kelas II', 4), ('KM024', 'Bayi Sehat Kelas II', 4)], 'I & R. KHUSUS': [('KM003', 'Kelas I', 4), ('KM025', 'Bayi Sehat Kelas I', 4)]}, row_labels={1: 'Varian bayi'},
    p3='varian bayi (bayi sehat) dimasukkan sebagai varian umur',
    p7="'Suite', 'President Suite', 'Bayi Sehat Suite', 'Bayi Sehat President Suite' (di atas kelas I); 'ICU', 'ICCU', 'NICU', 'PICU', 'PERINA', 'HCU' (ruang khusus); 'ISOLASI' (kamar isolasi); 'ODC' (one day care); 'VK Kelas III', 'VK Kelas II', 'VK Kelas I', 'VK Suite', 'VK President Suite' (kamar bersalin (VK))",
 ),
 'Jasa Perawatan': dict(
    nama='sama',
    use=[('NB016', 'Jasa Perawatan', 98)],
    p6="tabel perawat tercantum dua kali di buku dengan kode dan tarif sama: 'TARIF JASA PELAYANAN PERAWAT' (hlm. 98, dipakai) dan 'TARIF TINDAKAN PERAWAT' (hlm. 102)",
    p7="'Jasa perawat Infus ICT/ SVF/ aaPRP' (perawat infus ICT/SVF); 'Jasa Perawat Pendamping Kemoterapi' (pendampingan)",
 ),
 'Pasang IV Line Access': dict(
    nama='beda',
    use=[('NB020', 'Pemasangan Infus', 98), ('DU065', 'Pemasangan Infus Dengan Penyulit', 9, {'role': 'Ragu'}), ('DU089', 'Venaseksi', 9, {'role': 'Ragu'})],
    p6="tabel perawat tercantum dua kali di buku dengan kode dan tarif sama: 'TARIF JASA PELAYANAN PERAWAT' (hlm. 98, dipakai) dan 'TARIF TINDAKAN PERAWAT' (hlm. 102)",
    p3="'Pemasangan Infus Dengan Penyulit' adalah pemasangan infus dengan penyulit oleh dokter umum; 'Venaseksi' adalah akses vena dengan sayatan (cut-down), bukan IV line biasa",
    p7="'Drip Infus' (drip infus (pemberian), bukan pemasangan); 'Pemasangan Infus Intraosseus' (infus intraoseus); 'Saline Infusion Sonohysterography (SIS)' (tindakan kebidanan); 'Infusion Pump 1 s/d 6 jam', 'Infusion Pump > 6 jam - 1 hari' (alat infusion pump); 'Jasa perawat Infus ICT/ SVF/ aaPRP', 'Pemasangan Infus untuk Targeting Terapi' (infus terapi/estetik/onkologi)",
 ),
 'Injeksi IM / IV': dict(
    nama='beda',
    use=[('NB103', 'Injeksi Intramuskuler', 98), ('NB104', 'Injeksi Intravena', 98), ('DU103', 'Injeksi Intramuskuler', 10), ('DU104', 'Injeksi Intravena', 10)],
    p6="tabel perawat tercantum dua kali di buku dengan kode dan tarif sama: 'TARIF JASA PELAYANAN PERAWAT' (hlm. 98, dipakai) dan 'TARIF TINDAKAN PERAWAT' (hlm. 102)",
    p7="'Jasa Tindakan Injeksi Obat' (jasa tindakan injeksi obat (umum)); 'Injeksi Subkutan' (injeksi subkutan); 'Injeksi Intramuskular (USG Guidance) - Pain Management' (injeksi dengan panduan USG (pain management))",
 ),
 'Hematologi Lengkap': dict(
    nama='sama',
    use=[('A1003', 'Hematologi Lengkap', 42)],
    p7="'Hematologi Rutin', 'Hematologi Rutin + Diff count' (parameter lebih sedikit)",
 ),
 'CRP Kuantitatif': dict(
    nama='sama',
    use=[('C2007', 'CRP Kuantitatif', 45), ('B5007', 'hsCRP', 44, {'role': 'Ragu'})],
    p3="'hsCRP' adalah CRP sensitivitas tinggi (fungsi jantung), bukan CRP kuantitatif standar",
    p7='tidak ada CRP kualitatif/CRP tanpa keterangan',
 ),
 'Thorax PA': dict(
    nama='sama',
    use=[('XR114', 'Thorax PA', 58), ('XR114E', 'Thorax PA - Jasa Expertise', 58, {'role': 'Komponen jasa expertise (baris terpisah, ditagih bersama)'})],
    p3="di buku cabang ini tarif Thorax PA dipecah dua baris di tabel yang sama: 'Thorax PA' (XR114) dan 'Thorax PA - Jasa Expertise' (XR114E); bila keduanya ditagih, total III 404.000 / II 465.000 / I 502.000 (dijumlah manual, tidak tertulis di PDF)",
    p7="'Thorax AP', 'Thorax Lateral', 'Thorax Top Lordotic', 'Thorax RLD', 'Thorax LLD', 'Thorax BED' (proyeksi lain); 'Thorax AP - Jasa Expertise', 'Thorax Lateral - Jasa Expertise', 'Thorax (AP + Lateral) - Jasa Expertise', 'Thorax (PA + Lateral) - Jasa Expertise', 'Thorax (AP + Lateral + Oblique) - Jasa Expertise', 'Thorax (PA + Lateral + Oblique) - Jasa Expertise', 'Thorax Top Lordotic - Jasa Expertise' dkk. (jasa expertise saja); 'Thorax (AP + Lateral)', 'Thorax (PA + Lateral)', 'Thorax (AP + Lateral + Oblique)', 'Thorax (PA + Lateral + Oblique)' (kombinasi proyeksi)",
 ),
 'Infusion Pump / hari': dict(
    nama='beda',
    use=[('SA020', 'Infusion Pump > 6 jam - 1 hari', 76), ('SA035', 'Infusion Pump 1 s/d 6 jam', 76, {'role': 'Ragu'})],
    p3="'Infusion Pump 1 s/d 6 jam' bersatuan 1-6 jam, bukan per hari",
 ),
 'Syringe Pump / hari': dict(
    nama='beda',
    use=[('SA107', 'Syringe Pump > 6 jam - 1 hari', 77), ('SA059', 'Syringe Pump 1 s/d 6 jam', 77, {'role': 'Ragu'})],
    p3="'Syringe Pump 1 s/d 6 jam' bersatuan 1-6 jam, bukan per hari",
 ),
 'O2 / Hari': dict(
    nama='beda',
    use=[('OX002', 'Oksigen > 6 jam - 1 hari', 75), ('OX001', 'Oksigen / jam', 75, {'role': 'Ragu'})],
    p3="'Oksigen / jam' bersatuan per jam, bukan per hari",
 ),
 'Nebulizer': dict(
    nama='beda',
    use=[('NB203', 'Inhalasi/Nebulisasi Dewasa', 98), ('DU203', 'Inhalasi/Nebulisasi Dewasa', 10), ('RM058', 'Nebulizer', 40)],
    p6="tabel perawat tercantum dua kali di buku dengan kode dan tarif sama: 'TARIF JASA PELAYANAN PERAWAT' (hlm. 98, dipakai) dan 'TARIF TINDAKAN PERAWAT' (hlm. 102)",
    p3="'Inhalasi/Nebulisasi Dewasa' adalah tindakan nebulisasi; 'Nebulizer' di rehabilitasi medik adalah layanan fisioterapi",
    p7="'1 Modalitas, Nebulizer, Chest Physiotherapy', '2 Modalitas, Nebulizer, Chest Physiotherapy', '3 Modalitas, Nebulizer, Chest Physiotherapy', '4 Modalitas, Nebulizer, Chest Physiotherapy', '5 Modalitas, Nebulizer, Chest Physiotherapy' (paket modalitas fisioterapi); 'Nebulizer + CFT', 'Nebulizer + CFT + IRR' (kombinasi fisioterapi)",
 ),
 'Creatinin': dict(
    nama='beda',
    use=[('B2002', 'Kreatinin + eGFR', 43)],
    p3="satu item 'Kreatinin + eGFR' (kreatinin dengan perhitungan eGFR); tidak ada item kreatinin tanpa eGFR",
    p7="'Creatinin Clearence (CCT)' (clearance); 'Rasio Albumin-Kreatinin Urin', 'Kreatinin - Urine', 'Kreatinin Urine 24 Jam' (urine)",
 ),
 'Ureum': dict(
    nama='sama',
    use=[('B2006', 'Ureum', 43)],
    p7="'Phenylketon Urea (PKU)' (skrining neonatal); 'Urea Clearance Test (UCT)' (clearance); 'UBT (Urea Breath Test)' (tes napas); 'Ureum - Urine' (urine)",
 ),
 'GDS': dict(
    nama='beda',
    use=[('B3005', 'Glukosa Darah (Sewaktu)', 43), ('B3020', 'POCT Glukosa Darah (Sewaktu)', 44, {'role': 'Ragu'})],
    p3="'POCT Glukosa Darah (Sewaktu)' adalah pemeriksaan POCT (alat point-of-care), bukan analisa laboratorium",
    p7="'Glukosa Darah (2 Jam PP)', 'Glukosa Darah (Puasa)' (bukan sewaktu); 'POCT Glukosa Darah (Puasa)', 'POCT Glukosa Darah (2 Jam PP)' (POCT bukan sewaktu)",
 ),
 'Elektrolit (Na, K, Cl)': dict(
    nama='beda',
    use=[('B6008', 'Elektrolit Serum (Na, K, Cl)', 44)],
 ),
}
