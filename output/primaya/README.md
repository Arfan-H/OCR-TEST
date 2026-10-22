# Normalisasi tarif Primaya (aturan Prompt v6)

File hasil: `Normalisasi_Tarif_Bekasi_Timur_Acute_bronchitis_unspecified_Primaya.xlsx`

- Isi workbook: sheet `Normalisasi` (sama persis dengan file acuan `..._Nama_Provider_RS.xlsx`, dicek sel per sel) + 15 sheet
  Primaya. Tidak ada sheet rumah sakit lain.
- Format tiap sheet sama dengan hasil MIKA: kolom A–E dari sheet Normalisasi, lalu triplet `nama_layanan_n / kelas_kamar_n / tarif_n`,
  `flag_mencurigakan`, `alasan_mencurigakan` (poin 1–8).
- File dan skrip MIKA (`output/Normalisasi_..._Mitra_Keluarga.xlsx`, `output/scripts/mika/`, `output/logs/`) tidak diubah.

## Pasangan PDF dan Excel (1 PDF + 1 Excel dari cabang yang sama, tanpa silang cabang)

Kolom `rumah_sakit` di tiap Excel dicek sama dengan nama cabang PDF; salinan kerja dicek identik (md5) dengan file sumber.

| Sheet | PDF (`Buku Tarif Not Found PDF/PRIMAYA done phase 2/input/done/`) | Excel (`supa excel clean/Primaya/`) |
|---|---|---|
| Primaya Bekasi Timur | Buku Tarif - Primaya Hospital Bekasi Timur.pdf | primaya_tariffv12 - Bekasi Timur_normalized_classNormal.xlsx |
| Primaya Evasari | Buku Tarif - Primaya Evasari Hospital.pdf | primaya_tariffv11 - Evasari_normalized_classNormal.xlsx |
| Primaya Bhaktiwara | Buku Tarif - Primaya Hospital Bhaktiwara.pdf | primaya_tariffv13 - Bhaktiwara_normalized_classNormal.xlsx |
| Primaya Karawang | Buku Tarif - Primaya Hospital Karawang.pdf | primaya_tariffv14 - Karawang_normalized_classNormal.xlsx |
| Primaya Depok | TARIF 2026 - Primaya Hospital Depok.pdf | primaya_tariffv17 - Depok_normalized_classNormal.xlsx |
| Primaya Betang Pambelum | Buku Tarif - Primaya Hospital Betang Pambelum.pdf | primaya_tariffv18 - Betang Pambelum_normalized_classNormal.xlsx |
| Primaya Hertasning | Buku Tarif - Primaya Hospital Hertasning.pdf | primaya_tariffv20 - Hertasning_normalized_classNormal.xlsx |
| Primaya Kelapa Gading | Primaya Hospital Kelapa gading.pdf | primaya_tariffv21 - Kelapa Gading_normalized_classNormal.xlsx |
| Primaya Makassar | Buku Tarif - Primaya Hospital Makassar.pdf | primaya_tariffv22 - Makassar_normalized_classNormal.xlsx |
| Primaya Sukabumi | Buku Tarif - Primaya Hospital Sukabumi.pdf | primaya_tariffv24 - Sukabumi_normalized_classNormal.xlsx |
| Primaya Tangerang | Buku Tarif - Primaya Hospital Tangerang.pdf | primaya_tariffv25 - Tangerang_normalized_classNormal.xlsx |
| Primaya Semarang | Buku Tarif - Primaya Hospital Semarang.pdf | primaya_tariffv26_1-Semarang_normalized_classNormal.xlsx |
| Primaya PGI Cikini | Buku Tarif - Primaya Hospital PGI Cikini.pdf | primaya_tariffv27 - PGI Cikini_normalized_classNormal.xlsx |
| UKRIDA Primaya | Buku Tarif - UKRIDA Primaya Hospital.pdf | primaya_tariffv27 - UKRIDA_normalized_classNormal.xlsx |
| Primaya Pasar Kemis | Buku Tarif - Primaya Hospital Pasar Kemis PHPK2026_NoPass.pdf | primaya_tariffv29 - PASAR KEMIS_normalized_classNormal.xlsx |

Pasar Kemis: dipakai versi `_NoPass` (isi sama, tanpa kata sandi).
Tidak dikerjakan: Bekasi Barat, Bekasi Utara, Rajawali (folder `input/gambar`: PDF berbasis gambar dan tidak ada Excel-nya di `supa excel clean/Primaya`).

## Cara kerja dan pengecekan

1. `extract_pri.py` (alat 1, pdfplumber + pembaca posisi kata `linegrid.py` untuk tabel tanpa garis): semua halaman PDF → JSON
   (kode layanan dipisah dari nama `KODE - Nama`, judul tabel, kelompok, tarif per label kolom). Judul/kelompok tabel yang berlanjut
   ke halaman berikut dibawa dari halaman tempat judul tercetak.
2. `spec_<cabang>.py`: pilihan item per uraian (berdasar kode layanan Primaya yang seragam antar cabang, draf dari
   `make_spec_pri.py`, lalu ditinjau manual) + catatan poin 3 Ragu, 4 Janggal, 6, 7 Tidak diambil. Tarif, label kolom, perbandingan
   Excel (poin 5) dan penamaan (poin 8) dihitung `gen_pri.py` dari data, bukan diketik.
3. `build_pri.py`: menulis sheet.
4. `checker_pri.py` (alat 2, PyMuPDF, independen dari alat 1): mencocokkan nama + kode + halaman yang dikutip, tarif per label kolom,
   label kelas, judul tabel/kelompok tercetak di halaman yang disebut, kutipan `'...'` ada di PDF, kutipan `"..."` ada di Excel,
   pasangan (label, tarif) di Excel, flag, format poin, gaya, dan sheet Normalisasi tidak berubah. Hasil: **0 error di ke-15 sheet**
   (`logs/chk_*.txt`).
5. `mutate_pri.py`: kesalahan buatan per sheet (nama, tarif, label, kutipan, halaman, judul tabel, kode, flag, gaya) — semua harus
   ditolak checker (`logs/mut_*.txt`).
6. `crop_pri.py`: potongan gambar header + baris PDF untuk setiap item yang dikutip (dan halaman judul tabel berlanjut); semua sheet
   dicek visual satu per satu.

## Catatan khusus (tercatat di kolom alasan)

- Kolom kelas I di banyak cabang digabung dengan ruang khusus (mis. `I,ICU,ICCU,HCU,NICU,PERINA,ISOLASI`, `KELAS I / KAMAR KHUSUS`)
  → dipakai sebagai kolom kelas I sesuai aturan; Hertasning & Makassar: Excel memberi label "I" untuk kolom `KELAS I / KAMAR KHUSUS`.
- Kamar: sebagian cabang punya item per kelas (`KM001 - Kelas III` dst., satu kolom tarif; tiap baris memakai item kelasnya sendiri),
  sebagian punya `Kamar Perawatan` dengan kolom kelas.
- Evasari & UKRIDA: Excel memberi label "RJ" untuk tarif kamar rawat inap (poin 4 Janggal).
- Bhaktiwara: Excel tidak punya tarif kelas III/II/I untuk Hematologi Lengkap dan infusion/syringe pump (poin 5 selisih).
- Tangerang: Excel menaruh Jasa Perawatan, Pemasangan Infus dan injeksi perawat di kategori "TARIF HOMECARE" (poin 5).
- Kelapa Gading: tidak ada injeksi IM/IV di tabel perawat/dokter umum → dipakai versi dokter spesialis (DS490/DS491, poin 3);
  `Jasa Perawatan` ada di tabel visite dengan kode DR053.
- UKRIDA: buku tidak memuat tarif pemakaian alat → Infusion/Syringe Pump "Tidak ditemukan"; oksigen hanya bertarif RJ (poin 4).
- Depok: Thorax PA dipecah dua baris (`Thorax PA` + `Thorax PA - Jasa Expertise`), keduanya dimasukkan; tabel perawat tercantum dua kali.
- PGI Cikini: ada tabel `TARIF RADIOLOGI`, `TARIF RADIOLOGI RS`, `TARIF RADIOLOGI DOKTER` → dipakai tarif total.
- Nama yang di PDF tertulis aneh dipakai apa adanya dan dicatat: Karawang `Oksigen > 6 jam - 1 haFi`, Evasari `Pemasangan Infus Dengan`
  (terpotong di PDF), PGI Cikini `Pemasangan Infus Dengan Penyulit` (terpotong tampilan sel, teks lengkap ada di PDF).

## Menjalankan ulang

Siapkan `<folder kerja>/pdf/<key>.pdf`, `<folder kerja>/work/ex/<key>.xlsx` (pasangan di tabel atas) dan `<folder kerja>/work/base.xlsx`
(file acuan dengan sheet Normalisasi saja), salin `scripts/*` ke `<folder kerja>/scripts/`. Key: bekasitimur, evasari, bhaktiwara,
karawang, depok, betang, hertasning, kelapagading, makassar, sukabumi, tangerang, semarang, pgicikini, ukrida, pasarkemis.

```
bash scripts/run_extract_pri.sh                         # pdf -> work/json/<key>.json
cd scripts && python3 build_pri.py ../work/base.xlsx ../work/out.xlsx ../work spec_bekasitimur spec_evasari ...  # nama spec tanpa .py
bash scripts/check_all.sh                               # hasil di work/chk_<key>.txt
bash scripts/run_mut_pri.sh "bekasitimur:Primaya Bekasi Timur" ...   # hasil di work/mut_<key>.txt
```
