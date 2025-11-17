# 🏥 BPJS P-Care Automation Tool

## 📋 Deskripsi

Tool otomatisasi untuk entry data pendaftaran pasien BPJS ke sistem P-Care. Script ini menggunakan Selenium untuk mengotomasi proses pengisian form yang berulang-ulang.

## ✨ Fitur Utama

- ✅ **Deteksi Logout Otomatis** - Script berhenti jika session habis
- ✅ **Auto Recovery** - Otomatis recovery dari error
- ✅ **Reset Form Cepat** - Tidak perlu refresh halaman penuh
- ✅ **Laporan Lengkap** - Statistik sukses/gagal di akhir
- ✅ **Error Handling Robust** - Tangani berbagai jenis error
- ✅ **Batch Processing** - Proses ratusan data sekaligus dari CSV

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Jalankan Chrome dengan Remote Debugging
Double-click file `start_chrome.bat` atau jalankan:
```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%USERPROFILE%\selenium_chrome_profile"
```

### 3. Login ke P-Care
Buka https://pcarejkn.bpjs-kesehatan.go.id dan login manual

### 4. Siapkan File CSV
Format: satu nomor BPJS per baris
```
0001234567890
0001234567891
0001234567892
```

### 5. Edit Path CSV di Script
```python
FILE_CSV = r"C:\path\to\your\data.csv"
```

### 6. Jalankan Script
```bash
python bpjs_automation.py
```

## 📚 Dokumentasi

- **[PANDUAN_LENGKAP.md](PANDUAN_LENGKAP.md)** - Panduan lengkap dari A-Z
- **[RINGKASAN_PERBAIKAN.md](RINGKASAN_PERBAIKAN.md)** - Ringkasan perbaikan versi 2.0
- **[README_PERBAIKAN.md](README_PERBAIKAN.md)** - Detail teknis perbaikan

## 🔧 Konfigurasi

### Ubah Poli
```python
select_poli.select_by_visible_text("Konseling")  # Ganti sesuai kebutuhan
```

### Ubah Jenis Kunjungan
```python
# Untuk Kunjungan Sakit, ganti value='false' jadi value='true'
radio_sehat = wait.until(EC.visibility_of_element_located(
    (By.CSS_SELECTOR, "input[type='radio'][name='kunjSakitF'][value='false']") 
))
```

### Ubah Timeout
```python
wait = WebDriverWait(driver, 20)  # Ubah 20 jadi nilai lain
```

## 📊 Output

Script akan menampilkan laporan lengkap:
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

## 🔍 Troubleshooting

### Error: "Gagal terhubung ke Chrome"
**Solusi:** Jalankan ulang `start_chrome.bat`

### Error: "File CSV tidak ditemukan"
**Solusi:** Cek path file di script (baris 15)

### Error: "Session habis atau logout"
**Solusi:** Login manual ke P-Care terlebih dahulu

### Warning: "Tombol Simpan tidak aktif"
**Solusi:** Data BPJS tidak valid atau tidak aktif

Lihat [PANDUAN_LENGKAP.md](PANDUAN_LENGKAP.md) untuk troubleshooting lengkap.

## ⚠️ Perhatian

- Pastikan Chrome jalan dengan port 9222
- Pastikan sudah login ke P-Care sebelum jalankan script
- Jangan tutup atau ganggu Chrome saat script berjalan
- Validasi data CSV sebelum proses
- Gunakan dengan bijak, jangan overload server

## 📦 Requirements

- Python 3.8+
- Google Chrome (versi terbaru)
- Selenium 4.15.0+
- Pandas 2.0.0+

## 🎯 Fitur Baru v2.0

1. ✅ Deteksi logout otomatis
2. ✅ Reset form cepat (tanpa refresh)
3. ✅ Auto recovery dari error
4. ✅ Counter error berturut
5. ✅ Wait for page ready
6. ✅ Laporan lengkap
7. ✅ Event trigger lebih lengkap
8. ✅ Overlay removal lebih sempurna

## 📈 Performa

- **Kecepatan:** 2-3 detik per data
- **Success Rate:** 85-95% (tergantung validitas data)
- **Stability:** Sangat stabil dengan auto recovery

## 📝 Changelog

### v2.0 (17 November 2024)
- ✅ Fix masalah "keblock login ulang"
- ✅ Tambah deteksi logout otomatis
- ✅ Tambah auto recovery
- ✅ Perbaikan event trigger
- ✅ Perbaikan overlay handling
- ✅ Tambah laporan lengkap

### v1.0
- Initial release

## 📄 License

Free to use. Gunakan dengan bijak dan bertanggung jawab.

## 🤝 Contributing

Jika menemukan bug atau punya saran perbaikan, silakan buat issue atau pull request.

## ⭐ Support

Jika tool ini membantu pekerjaan Anda, berikan ⭐ star!

---

**Versi:** 2.0  
**Status:** ✅ Production Ready  
**Terakhir diupdate:** 17 November 2024
