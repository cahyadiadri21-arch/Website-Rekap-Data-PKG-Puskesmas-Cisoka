# 📘 PANDUAN LENGKAP - BPJS AUTOMATION

## 🎯 Daftar Isi
1. [Persiapan Awal](#persiapan-awal)
2. [Instalasi](#instalasi)
3. [Konfigurasi](#konfigurasi)
4. [Cara Penggunaan](#cara-penggunaan)
5. [Troubleshooting](#troubleshooting)
6. [FAQ](#faq)

---

## 📦 Persiapan Awal

### Yang Anda Butuhkan:
- ✅ Windows 10/11
- ✅ Google Chrome (versi terbaru)
- ✅ Python 3.8 atau lebih baru
- ✅ Akses internet
- ✅ Akun P-Care BPJS yang valid

### Cek Versi Python
Buka Command Prompt (CMD) dan ketik:
```bash
python --version
```

Jika muncul error "python is not recognized":
1. Download Python dari https://www.python.org/downloads/
2. Install dengan centang "Add Python to PATH"
3. Restart komputer

---

## 🔧 Instalasi

### Langkah 1: Download File
Download semua file berikut ke satu folder (misal: `C:\BPJS_Automation`):
- `bpjs_automation.py`
- `start_chrome.bat`
- `requirements.txt`
- `contoh_data.csv`

### Langkah 2: Install Dependencies
Buka Command Prompt di folder tersebut, lalu jalankan:
```bash
pip install -r requirements.txt
```

Tunggu sampai selesai. Anda akan melihat:
```
Successfully installed selenium-4.15.0 pandas-2.0.0
```

### Langkah 3: Download ChromeDriver (Opsional)
Selenium biasanya sudah otomatis download ChromeDriver. Jika ada error:
1. Cek versi Chrome: Buka Chrome → Titik 3 → Help → About Google Chrome
2. Download ChromeDriver yang sesuai dari https://chromedriver.chromium.org/
3. Ekstrak dan letakkan di folder yang sama dengan script

---

## ⚙️ Konfigurasi

### 1. Siapkan File CSV
Buat file CSV dengan format:
```
0001234567890
0001234567891
0001234567892
```

**Penting:**
- Satu nomor BPJS per baris
- Tidak ada header/judul kolom
- Tidak ada spasi atau karakter aneh
- Simpan dengan encoding UTF-8

### 2. Edit Path File CSV
Buka `bpjs_automation.py` dengan Notepad atau editor lain.

Cari baris ini (sekitar baris 15):
```python
FILE_CSV = r"C:\Users\puskesmas cisoka\Desktop\vs\readcsvtestdata.csv"
```

Ganti dengan path file CSV Anda:
```python
FILE_CSV = r"C:\BPJS_Automation\data_bpjs.csv"
```

**Tips:** Gunakan `r"..."` agar backslash tidak bermasalah.

### 3. (Opsional) Ubah Pengaturan Lain

#### Ubah Timeout
```python
wait = WebDriverWait(driver, 20)  # Ubah 20 jadi 30 jika koneksi lambat
```

#### Ubah Jeda Antar Data
```python
delay = random.uniform(1.5, 2.5)  # Ubah jadi (2.0, 3.0) jika mau lebih lambat
```

#### Ubah Poli
Cari baris ini (sekitar baris 350):
```python
select_poli.select_by_visible_text("Konseling")
```

Ganti "Konseling" dengan poli lain, misal:
```python
select_poli.select_by_visible_text("Umum")
```

---

## 🚀 Cara Penggunaan

### Langkah 1: Jalankan Chrome dengan Remote Debugging

**Cara 1: Pakai File .bat (Mudah)**
1. Double-click file `start_chrome.bat`
2. Chrome akan terbuka otomatis
3. **JANGAN TUTUP** window Command Prompt yang muncul

**Cara 2: Manual**
1. Tutup semua window Chrome yang sedang buka
2. Buka Command Prompt
3. Jalankan:
```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%USERPROFILE%\selenium_chrome_profile"
```

### Langkah 2: Login ke P-Care
1. Di Chrome yang baru terbuka, buka: https://pcarejkn.bpjs-kesehatan.go.id
2. Login dengan username dan password Anda
3. **PENTING:** Pastikan berhasil login dan bisa akses dashboard
4. Biarkan Chrome tetap terbuka

### Langkah 3: Jalankan Script
1. Buka Command Prompt BARU (jangan yang untuk Chrome)
2. Masuk ke folder script:
```bash
cd C:\BPJS_Automation
```
3. Jalankan script:
```bash
python bpjs_automation.py
```

### Langkah 4: Monitor Proses
Anda akan melihat log seperti ini:
```
2024-11-17 10:30:15 - INFO - ✅ Terhubung ke Chrome aktif.
2024-11-17 10:30:16 - INFO - ✅ Halaman sudah siap (document ready).
2024-11-17 10:30:17 - INFO - ✅ Tanggal (Langkah 3) diatur ke: 2024-11-17
2024-11-17 10:30:18 - INFO - ✅ Berhasil memuat 5 data dari file CSV
2024-11-17 10:30:20 - INFO - 📋 Memproses data 1/5: 0001234567890
2024-11-17 10:30:25 - INFO - ✅ SUKSES: Data berhasil disimpan
```

**Jangan:**
- ❌ Tutup Chrome
- ❌ Klik-klik di Chrome saat script jalan
- ❌ Minimize Chrome (boleh, tapi lebih baik terlihat)
- ❌ Matikan komputer

**Boleh:**
- ✅ Buka aplikasi lain
- ✅ Lihat log di Command Prompt
- ✅ Minum kopi sambil nunggu 😊

### Langkah 5: Selesai
Setelah semua data diproses, Anda akan melihat laporan:
```
============================================================
🎉 OTOMATISASI SELESAI!
============================================================
📊 Total Data: 100
✅ Sukses: 95
❌ Gagal: 5
📈 Success Rate: 95.0%
============================================================
```

---

## 🔍 Troubleshooting

### ❌ Error: "Gagal terhubung ke Chrome"

**Penyebab:** Chrome tidak jalan dengan port 9222

**Solusi:**
1. Tutup SEMUA window Chrome
2. Jalankan ulang `start_chrome.bat`
3. Tunggu Chrome terbuka
4. Jalankan ulang script

### ❌ Error: "File CSV tidak ditemukan"

**Penyebab:** Path file salah

**Solusi:**
1. Cek path file CSV di script
2. Pastikan file benar-benar ada di lokasi tersebut
3. Gunakan path lengkap (absolute path)
4. Gunakan `r"..."` untuk path Windows

Contoh benar:
```python
FILE_CSV = r"C:\BPJS_Automation\data.csv"
```

Contoh salah:
```python
FILE_CSV = "C:\BPJS_Automation\data.csv"  # Tanpa r
FILE_CSV = r"data.csv"  # Path relatif, bisa error
```

### ❌ Error: "Session habis atau logout"

**Penyebab:** Belum login atau session timeout

**Solusi:**
1. Buka Chrome yang jalan dengan port 9222
2. Login manual ke P-Care
3. Pastikan bisa akses dashboard
4. Jalankan ulang script

### ⚠️ Warning: "Tombol Simpan tidak aktif"

**Penyebab:** Data BPJS tidak valid atau tidak aktif

**Solusi:**
1. Cek nomor BPJS di CSV
2. Coba cek manual di P-Care apakah nomor valid
3. Hapus nomor yang tidak valid dari CSV
4. Jalankan ulang script

### ⚠️ Warning: "Data peserta tidak ditemukan"

**Penyebab:** Nomor BPJS salah atau tidak terdaftar

**Solusi:**
1. Verifikasi nomor BPJS
2. Cek apakah ada typo (salah ketik)
3. Pastikan nomor 13 digit
4. Cek apakah peserta masih aktif

### 🐌 Script Jalan Lambat

**Penyebab:** Koneksi internet lambat atau server P-Care lambat

**Solusi:**
1. Cek koneksi internet
2. Tunggu saat jam tidak sibuk
3. Ubah timeout jadi lebih besar:
```python
wait = WebDriverWait(driver, 30)  # Dari 20 jadi 30
```

### 💥 Script Crash/Berhenti Tiba-tiba

**Penyebab:** Error tidak terduga

**Solusi:**
1. Lihat log error terakhir
2. Screenshot error
3. Coba jalankan ulang
4. Jika masih error, coba dengan 1-2 data dulu untuk testing

---

## ❓ FAQ (Frequently Asked Questions)

### Q: Apakah script ini aman?
**A:** Ya, script ini:
- Tidak menyimpan password
- Tidak mengirim data ke server lain
- Hanya mengotomasi klik dan isi form
- Menggunakan session Chrome yang sudah login

### Q: Berapa lama proses untuk 100 data?
**A:** Sekitar 5-10 menit, tergantung:
- Kecepatan internet
- Kecepatan server P-Care
- Validitas data

### Q: Bisa dijalankan di Mac/Linux?
**A:** Bisa, tapi perlu modifikasi:
- Path file pakai `/` bukan `\`
- File .bat tidak bisa, pakai command manual
- Path Chrome berbeda

### Q: Apakah bisa untuk poli lain?
**A:** Bisa! Edit baris ini:
```python
select_poli.select_by_visible_text("Konseling")
```
Ganti "Konseling" dengan nama poli yang Anda mau.

### Q: Apakah bisa untuk "Kunjungan Sakit"?
**A:** Bisa! Edit baris ini:
```python
radio_sehat = wait.until(EC.visibility_of_element_located(
    (By.CSS_SELECTOR, "input[type='radio'][name='kunjSakitF'][value='false']") 
))
```
Ganti `value='false'` jadi `value='true'`

### Q: Bagaimana jika ada data yang gagal?
**A:** Script akan:
- Log nomor yang gagal
- Lanjut ke data berikutnya
- Tidak menghentikan proses
- Tampilkan laporan di akhir

Anda bisa cek log untuk tahu nomor mana yang gagal.

### Q: Apakah bisa dijadwalkan otomatis?
**A:** Bisa dengan Task Scheduler Windows:
1. Buka Task Scheduler
2. Create Basic Task
3. Set trigger (waktu)
4. Set action: Start a program
5. Program: `python`
6. Arguments: `C:\BPJS_Automation\bpjs_automation.py`

**Catatan:** Chrome harus sudah jalan dan login.

### Q: Apakah melanggar aturan BPJS?
**A:** Script ini hanya mengotomasi proses manual yang biasa Anda lakukan. Namun:
- Gunakan dengan bijak
- Jangan spam/overload server
- Pastikan data yang diinput valid
- Tanggung jawab ada pada pengguna

### Q: Bisa untuk entri data lain (bukan pendaftaran)?
**A:** Bisa, tapi perlu modifikasi script sesuai form yang mau diisi. Konsepnya sama:
1. Identifikasi elemen (ID, class, xpath)
2. Isi field dengan JavaScript
3. Klik tombol submit
4. Tangani popup

---

## 📞 Kontak & Support

Jika masih ada masalah:
1. Baca ulang panduan ini dengan teliti
2. Cek log error dengan detail
3. Coba dengan data minimal (1-2 nomor) dulu
4. Screenshot error untuk dokumentasi

---

## 🎓 Tips & Trik

### Tip 1: Testing Dulu
Sebelum proses ratusan data, coba dulu dengan 5-10 data untuk memastikan semua berjalan lancar.

### Tip 2: Backup Data
Selalu backup file CSV sebelum proses, jaga-jaga jika ada yang salah.

### Tip 3: Monitoring
Pantau log secara berkala untuk deteksi masalah lebih awal.

### Tip 4: Waktu Optimal
Jalankan saat jam tidak sibuk (pagi atau malam) untuk performa lebih baik.

### Tip 5: Koneksi Stabil
Pastikan koneksi internet stabil selama proses.

### Tip 6: Jangan Ganggu Browser
Biarkan Chrome fokus pada script, jangan buka tab lain atau klik-klik.

### Tip 7: Log File
Anda bisa redirect log ke file:
```bash
python bpjs_automation.py > log.txt 2>&1
```

### Tip 8: Validasi Data
Validasi nomor BPJS sebelum dimasukkan ke CSV untuk mengurangi error.

---

## 📊 Checklist Sebelum Mulai

Sebelum jalankan script, pastikan:

- [ ] Python sudah terinstall
- [ ] Dependencies sudah terinstall (`pip install -r requirements.txt`)
- [ ] File CSV sudah siap dan valid
- [ ] Path file CSV di script sudah benar
- [ ] Chrome sudah jalan dengan port 9222
- [ ] Sudah login ke P-Care
- [ ] Koneksi internet stabil
- [ ] Punya waktu untuk monitoring (jangan tinggal pergi)

Jika semua sudah ✅, Anda siap untuk mulai!

---

**Selamat menggunakan! Semoga membantu pekerjaan Anda! 🎉**

---

*Versi: 2.0*  
*Terakhir diupdate: 17 November 2024*
