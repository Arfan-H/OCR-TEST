# Normalisasi tarif Mitra Keluarga (aturan Prompt v6)

File hasil: `Normalisasi_Tarif_Bekasi_Timur_Acute_bronchitis_unspecified_Mitra_Keluarga.xlsx`

- Sheet `Normalisasi`, `Mitra Keluarga Pondok Tjandra`, `Mitra Keluarga Kelapa Gading`, `Mitra Keluarga Jatiasih` tidak diubah (dicek otomatis sel per sel).
- Ditambah 13 sheet baru, satu per rumah sakit, dengan format yang sama: kolom A–E dari sheet Normalisasi, lalu triplet
  `nama_layanan_n / kelas_kamar_n / tarif_n`, `flag_mencurigakan`, `alasan_mencurigakan` (poin 1–8).

## Pasangan PDF dan Excel yang dipakai

| Sheet | PDF (`Buku Tarif Not Found PDF/MIKA done phase 3(to db)/input/done/`) | Excel (`supa excel clean/MIKA/`) |
|---|---|---|
| Mitra Keluarga Depok | Buku Tarif Mitra Keluarga Depok Tahun 2026.pdf | mika_tariffv10_1_Depok_normalized_classNormal.xlsx |
| Mitra Keluarga Kalideres | Buku Tarif Mitra Keluarga Kalideres Tahun 2026.pdf | mika_tariffv11_Kalideres_normalized_classNormal.xlsx |
| Mitra Keluarga Tegal | BUKU TARIF MITRA KELUARGA TEGAL TAHUN 2026.pdf | mika_tariffv12_Tegal_normalized_classNormal.xlsx |
| Mitra Keluarga Kenjeran | Buku Tarif Mitra Keluarga Kenjeran Tahun 2026.pdf | mika_tariffv13_Kenjeran_normalized_classNormal.xlsx |
| Mitra Keluarga Waru | BUKU TARIF MITRA KELUARGA WARU TAHUN 2026.pdf | mika_tariffv14_Waru_normalized_classNormal.xlsx |
| Mitra Keluarga Gading Serpong | Buku Tarif Mitra Keluarga Gading Serpong_ Tahun 2026.pdf | mika_tariffv15_2_Gading Serpong_normalized_classNormal.xlsx |
| Mitra Keluarga Slawi | Buku Tarif Mitra Keluarga Slawi 2026.pdf | mika_tariffv2_Slawi_normalized_classNormal.xlsx |
| Mitra Keluarga Kemayoran | Mika - Kemayoran 2026 (V1).pdf | mika_tariffv4_Kemayoran_normalized_classNormal.xlsx |
| Mitra Keluarga Sidoarjo | 3400 - Sidoarjo 2026 (V1).pdf | mika_tariffv5_Sidoarjo_normalized_classNormal.xlsx |
| Mitra Keluarga Cibubur | Buku Tarif Mitra Keluarga Cibubur Tahun 2026.pdf | mika_tariffv6_1_Cibubur_normalized_classNormal.xlsx |
| Mitra Keluarga Cikarang | Buku Tarif Mitra Keluarga Cikarang Tahun 2026.pdf | mika_tariffv7_1-Cikarang_normalized_classNormal.xlsx |
| Mitra Keluarga Surabaya | Buku Tarif Mitra Keluarga Surabaya Tahun_2026.pdf | mika_tariffv8_1-Surabaya_normalized_classNormal.xlsx |
| Mitra Keluarga Bekasi Barat | Buku Tarif Mitra Keluarga Bekasi Tahun 2026 (Bekasi Barat).pdf | mika_tariffv9_1- Bekasi Barat_normalized_classNormal.xlsx |

Pondok Tjandra, Kelapa Gading dan Jatiasih sudah ada sebelumnya (tidak diubah).
Tidak dikerjakan: Bina Husada, Pamulang, Bintaro (folder `input/gambar`: PDF berbasis gambar dan tidak ada Excel-nya di `supa excel clean/MIKA`).

## Cara kerja dan pengecekan

1. `extract_mika.py` (alat 1, pdfplumber): semua halaman PDF → JSON baris tarif (kode, nama, judul tabel, kelompok, tarif per kolom).
2. `spec_<rs>.py`: pilihan item per uraian + catatan manual (poin 3 Ragu, 4 Janggal, 6, 7 Tidak diambil). Tarif, label kolom,
   perbandingan Excel (poin 5) dan penamaan (poin 8) dihitung `gen_mika.py` dari data, bukan diketik.
3. `build_mika.py`: menulis sheet (gaya sama dengan sheet sebelumnya).
4. `checker_mika.py` (alat 2, PyMuPDF, independen dari alat 1): mencocokkan setiap nama + kode + halaman yang dikutip,
   tarif per label kolom, label kelas, kutipan `'...'` ada di PDF, kutipan `"..."` ada di Excel, pasangan (label, tarif) di Excel,
   flag, format poin, gaya, serta memastikan sheet lain tidak berubah. Hasil: **0 error di ke-13 sheet**.
5. `mutate_mika.py`: 64 kesalahan buatan per sheet (nama, tarif, label, kutipan, halaman, flag, gaya, sheet lain) — semua harus ditolak checker.
6. `crop_mika.py`: potongan gambar header + baris PDF untuk setiap item yang dikutip; semua sheet dicek visual satu per satu.

Catatan khusus yang tercatat di kolom alasan, antara lain:
- Kemayoran: PDF ber-watermark "CONTROLLED COPY"; checker membaca tabel dari garis yang digambar.
- Cibubur: nama di PDF diawali tanda daftar "- " (tidak dimasukkan ke nama, dicatat di poin 8).
- Cikarang & Bekasi Barat: tarif per kelas ada di sub-baris kolom `JENIS KAMAR` / `KELAS` di bawah kode dan nama yang digabung;
  nama diberi akhiran isi kolom itu (mis. `Jasa Perawatan - III`, `Spesialis - I/ISOLASI`).
- Bekasi Barat: `Jasa Perawatan` tidak ada di Excel; Excel menaruh sebagian tarif SubSpesialis/Konsultan di bawah nama Spesialis.
- Judul/kelompok tabel yang terpotong atau salah terbaca oleh ekstraksi di halaman lanjutan dikoreksi lewat override di spec
  (`grp`/`ttl`) setelah dicek visual.

## Menjalankan ulang

Salin `scripts/mika/*` ke `<folder kerja>/scripts/`, lalu siapkan `<folder kerja>/pdf/<key>.pdf`, `<folder kerja>/work/ex/<key>.xlsx`
dan `<folder kerja>/work/base.xlsx` (workbook sebelum 13 sheet baru ditambahkan). Key: depok, kalideres, tegal, kenjeran, waru, gs,
slawi, kemayoran, sidoarjo, cibubur, cikarang, surabaya, bekasibarat.

```
bash scripts/run_extract.sh                                   # pdf -> work/json/<key>.json
cd scripts && python3 build_mika.py ../work/base.xlsx ../work/out.xlsx ../work spec_depok spec_kalideres ...   # nama spec tanpa .py
bash scripts/run_check.sh "depok:Mitra Keluarga Depok" ...      # hasil di work/chk_<key>.txt
bash scripts/run_mut.sh   "depok:Mitra Keluarga Depok" ...      # hasil di work/mut_<key>.txt
```
Skrip lama dari sesi sebelumnya (tidak dipakai lagi) ada di `scripts/mika/lama/`.
Log checker dan uji mutasi terakhir ada di `logs/`.
