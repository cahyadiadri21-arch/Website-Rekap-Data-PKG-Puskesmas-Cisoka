import time
import logging
import random
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException

# --- PENGATURAN ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Pastikan path ini BENAR sesuai lokasi file Anda
FILE_CSV = r"C:\Users\puskesmas cisoka\Desktop\vs\readcsvtestdata.csv"

# URL halaman data
BPJS_URL = "https://pcarejkn.bpjs-kesehatan.go.id/eclaim/EntriDaftarDokkel"

# ===============================================
#  FUNGSI BANTUAN "MODE PAKSA"
# ===============================================

def force_click(driver, element):
    """Gunakan JavaScript untuk memaksa klik, melewati 'element not interactable'"""
    try:
        driver.execute_script("arguments[0].click();", element)
    except Exception as e:
        logger.error(f"Gagal 'force_click': {e}")
        raise e

def force_remove_overlay(driver):
    """
    Mencari dan menghapus paksa 'modal-backdrop' (overlay abu-abu)
    yang mungkin menghalangi elemen lain.
    """
    try:
        # Hapus semua overlay yang mungkin ada
        backdrops = driver.find_elements(By.CLASS_NAME, "modal-backdrop")
        for backdrop in backdrops:
            driver.execute_script("arguments[0].remove();", backdrop)
            logger.info("... (Info) Overlay 'modal-backdrop' dihilangkan paksa.")
        
        # Hapus class 'modal-open' dari body agar bisa di-klik
        body = driver.find_element(By.TAG_NAME, "body")
        driver.execute_script("arguments[0].classList.remove('modal-open');", body)
        
        # Hapus semua modal yang mungkin masih terbuka
        modals = driver.find_elements(By.CLASS_NAME, "modal")
        for modal in modals:
            driver.execute_script("arguments[0].style.display = 'none';", modal)
            
    except Exception as e:
        logger.warning(f"Tidak bisa menghapus overlay: {e}")

def check_if_logged_out(driver):
    """
    Cek apakah user sudah logout atau kena redirect ke halaman login
    """
    try:
        current_url = driver.current_url
        # Cek apakah ada kata 'login' di URL atau elemen login di halaman
        if 'login' in current_url.lower() or 'signin' in current_url.lower():
            logger.error("❌ TERDETEKSI: Anda sudah logout atau session habis!")
            return True
        
        # Cek apakah ada elemen login form
        login_elements = driver.find_elements(By.ID, "username") or \
                        driver.find_elements(By.ID, "password") or \
                        driver.find_elements(By.NAME, "username")
        
        if login_elements:
            logger.error("❌ TERDETEKSI: Halaman login muncul!")
            return True
            
        return False
    except Exception as e:
        logger.warning(f"Error saat cek status login: {e}")
        return False

def wait_for_page_ready(driver, timeout=10):
    """
    Tunggu sampai halaman benar-benar siap (document.readyState = complete)
    """
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        logger.info("✅ Halaman sudah siap (document ready).")
        return True
    except TimeoutException:
        logger.warning("⚠️ Timeout menunggu halaman siap.")
        return False

# ===============================================
#  FUNGSI UTAMA SETUP HALAMAN (DIPERBAIKI)
# ===============================================
def setup_page(driver, wait):
    """
    Menjalankan langkah 1, 2, dan 3 untuk setup halaman.
    (Menutup notifikasi, menutup bootbox, dan mengisi tanggal)
    """
    try:
        # Tunggu halaman benar-benar siap
        wait_for_page_ready(driver)
        
        # Cek apakah sudah logout
        if check_if_logged_out(driver):
            logger.error("❌ FATAL: Session habis atau logout. Silakan login manual terlebih dahulu!")
            raise Exception("Session habis - perlu login ulang")
        
        # --- LANGKAH 1: Menutup Notifikasi "WARNING!" (PAKSA) ---
        try:
            close_alert_notify = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[data-notify='dismiss']")
            ))
            force_click(driver, close_alert_notify)
            logger.info("✅ Notifikasi 'WARNING' (Langkah 1) ditutup PAKSA.")
            time.sleep(0.5)
        except TimeoutException:
            logger.warning("⚠️ Tidak ada notifikasi 'WARNING' (Langkah 1), melanjutkan.")

        # --- LANGKAH 2: Klik Tombol OK Bootbox (PAKSA) ---
        try:
            accept_button = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.bootbox-accept")
            ))
            force_click(driver, accept_button)
            logger.info("✅ Bootbox 'OK' (Langkah 2) diklik PAKSA.")
            time.sleep(0.5)
        except TimeoutException:
            logger.warning("⚠️ Tidak ada popup bootbox (Langkah 2), melanjutkan.")
        
        # --- PENTING: HILANGKAN SISA OVERLAY ---
        force_remove_overlay(driver)
        time.sleep(0.5)

        # --- LANGKAH 3: Mengisi Tanggal (PERBAIKAN PALING PENTING) ---
        logger.info("Mencoba mengatur tanggal (Langkah 3)...")
        tanggal_hari_ini = datetime.now().strftime('%Y-%m-%d')
        
        # Tunggu field tanggal muncul dan bisa diinteraksi
        date_input = wait.until(EC.presence_of_element_located((By.ID, "txttanggal")))
        
        # Scroll ke elemen agar terlihat
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", date_input)
        time.sleep(0.3)
        
        # Clear dulu jika ada value sebelumnya
        driver.execute_script("arguments[0].value = '';", date_input)
        
        # Set nilainya
        driver.execute_script(f"arguments[0].value = '{tanggal_hari_ini}';", date_input)
        
        # Trigger event secara berurutan
        driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", date_input)
        driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", date_input)
        driver.execute_script("arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));", date_input)

        logger.info(f"✅ Tanggal (Langkah 3) diatur ke: {tanggal_hari_ini} (event triggered)")
        
        # Beri jeda lebih lama agar JS P-Care selesai memproses
        time.sleep(2)
        
        # Verifikasi bahwa form sudah unlock
        try:
            search_field = driver.find_element(By.ID, "txtnokartu")
            is_disabled = driver.execute_script("return arguments[0].disabled;", search_field)
            if is_disabled:
                logger.warning("⚠️ Field 'No. Kartu' masih disabled. Mencoba trigger ulang...")
                driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", date_input)
                time.sleep(1)
        except Exception as e:
            logger.warning(f"Tidak bisa verifikasi status field: {e}")
        
    except Exception as e:
        logger.error(f"❌ GAGAL saat setup halaman: {e}")
        raise e

# ===============================================
#  FUNGSI RESET FORM (BARU)
# ===============================================
def reset_form(driver, wait):
    """
    Reset form tanpa refresh halaman penuh (lebih cepat dan aman)
    """
    try:
        logger.info("🔄 Mereset form...")
        
        # Cek apakah ada tombol reset/batal
        try:
            reset_button = driver.find_element(By.ID, "btnBatal")
            force_click(driver, reset_button)
            logger.info("✅ Form direset dengan tombol 'Batal'.")
            time.sleep(1)
            force_remove_overlay(driver)
            return True
        except NoSuchElementException:
            pass
        
        # Jika tidak ada tombol reset, clear manual
        try:
            search_field = driver.find_element(By.ID, "txtnokartu")
            driver.execute_script("arguments[0].value = '';", search_field)
            driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", search_field)
            logger.info("✅ Field 'No. Kartu' di-clear manual.")
        except Exception as e:
            logger.warning(f"Tidak bisa clear field: {e}")
        
        force_remove_overlay(driver)
        return True
        
    except Exception as e:
        logger.error(f"❌ Gagal reset form: {e}")
        return False

# =============================
#  HUBUNGKAN KE CHROME AKTIF
# =============================
chrome_options = Options()
chrome_options.debugger_address = "127.0.0.1:9222"

try:
    driver = webdriver.Chrome(options=chrome_options)
    logger.info("✅ Terhubung ke Chrome aktif.")
    wait = WebDriverWait(driver, 20)
except Exception as e:
    logger.error(f"❌ Gagal terhubung ke Chrome. {e}")
    logger.error("PASTIKAN Anda sudah menjalankan Chrome dengan port 9222 (gunakan file .bat).")
    exit(1)

# ========================================================
#  PROGRAM UTAMA
# ========================================================
try:
    # Cek status login dulu
    if check_if_logged_out(driver):
        logger.error("❌ FATAL: Anda belum login! Silakan login manual terlebih dahulu.")
        exit(1)
    
    current_url = driver.current_url
    if not current_url.startswith(BPJS_URL):
        driver.get(BPJS_URL)
        logger.info(f"Navigasi ke {BPJS_URL}")
        time.sleep(2)
    else:
        logger.info(f"Sudah berada di halaman yang benar: {current_url}")

    # --- PERSIAPAN HALAMAN AWAL (Langkah 1, 2, 3) ---
    setup_page(driver, wait)
    
    # --- MEMBACA FILE CSV ---
    try:
        data_df = pd.read_csv(FILE_CSV, header=None, dtype=str)
        bpjs_numbers = data_df[0].tolist() 
        logger.info(f"✅ Berhasil memuat {len(bpjs_numbers)} data dari {FILE_CSV}")
    except FileNotFoundError:
        logger.error(f"❌ GAGAL: File {FILE_CSV} tidak ditemukan.")
        exit(1)
    except Exception as e:
        logger.error(f"❌ GAGAL memuat atau memproses CSV: {e}")
        exit(1)

    # Counter untuk tracking
    sukses_count = 0
    gagal_count = 0
    error_berturut = 0
    MAX_ERROR_BERTURUT = 3

    # ===================================================
    #  LOOP ENTRI DATA (DIPERBAIKI)
    # ===================================================
    for i, bpjs_num in enumerate(bpjs_numbers):
        bpjs_num = str(bpjs_num).strip()
        logger.info(f"\n{'='*60}")
        logger.info(f"📋 Memproses data {i+1}/{len(bpjs_numbers)}: {bpjs_num}")
        logger.info(f"{'='*60}")

        try:
            # Cek status login sebelum proses
            if check_if_logged_out(driver):
                logger.error("❌ FATAL: Session habis! Hentikan proses.")
                break
            
            # --- LANGKAH 4: Isi No. Kartu BPJS (PAKSA) ---
            search_field = wait.until(EC.visibility_of_element_located((By.ID, "txtnokartu")))
            
            # Scroll ke field
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_field)
            time.sleep(0.3)
            
            # Clear dan isi
            driver.execute_script("arguments[0].value = '';", search_field)
            driver.execute_script(f"arguments[0].value = '{bpjs_num}';", search_field)
            driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", search_field)
            driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", search_field)
            logger.info("✅ Mengisi No. Kartu (Langkah 4) via JS.")
            time.sleep(0.5)

            # --- LANGKAH 5: Klik Tombol Cari (PAKSA) ---
            cari_button = wait.until(EC.element_to_be_clickable((By.ID, "btnCariPeserta")))
            force_click(driver, cari_button)
            logger.info("✅ Klik 'Cari' (Langkah 5) via JS.")
            
            # Tunggu response dari server (loading)
            time.sleep(2)

            # --- LANGKAH 6: Pilih "Kunjungan Sehat" (PAKSA) ---
            try:
                radio_sehat = wait.until(EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "input[type='radio'][name='kunjSakitF'][value='false']") 
                ))
                force_click(driver, radio_sehat)
                logger.info("✅ Memilih 'Kunjungan Sehat' (Langkah 6) via JS.")
                time.sleep(0.5)
            except TimeoutException:
                logger.error(f"❌ GAGAL: Data peserta {bpjs_num} tidak ditemukan atau tidak valid.")
                gagal_count += 1
                error_berturut += 1
                reset_form(driver, wait)
                time.sleep(1)
                continue

            # --- LANGKAH 7: Pilih Poli "Konseling" ---
            try:
                select_poli = Select(wait.until(EC.element_to_be_clickable((By.ID, "poli"))))
                select_poli.select_by_visible_text("Konseling")
                logger.info("✅ Memilih Poli 'Konseling' (Langkah 7)")
                time.sleep(random.uniform(0.5, 1.0))
            except Exception as e:
                logger.error(f"❌ GAGAL memilih poli: {e}")
                gagal_count += 1
                error_berturut += 1
                reset_form(driver, wait)
                continue

            # ====================================================================
            # --- LANGKAH 8: KLIK SIMPAN (DENGAN PENGECEKAN LEBIH KETAT) ---
            # ====================================================================
            logger.info("⏳ Menunggu tombol 'Simpan' aktif (Langkah 8)...")
            
            try:
                # Tunggu tombol simpan muncul dan aktif
                simpan_button = wait.until(EC.element_to_be_clickable(
                    (By.ID, "btnSimpanPendaftaran")
                ))
                
                # Double check: pastikan tombol tidak disabled
                is_disabled = driver.execute_script("return arguments[0].disabled;", simpan_button)
                if is_disabled:
                    logger.warning("⚠️ Tombol 'Simpan' masih disabled. Menunggu 2 detik lagi...")
                    time.sleep(2)
                    is_disabled = driver.execute_script("return arguments[0].disabled;", simpan_button)
                    if is_disabled:
                        raise TimeoutException("Tombol Simpan tidak aktif setelah menunggu")
                
                # Scroll ke tombol
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", simpan_button)
                time.sleep(0.3)
                
                # Klik paksa
                force_click(driver, simpan_button)
                logger.info("✅ Tombol 'Simpan' (Langkah 8) diklik.")
                time.sleep(1)

            except TimeoutException:
                logger.warning(f"⚠️ GAGAL: Tombol 'Simpan' tidak aktif untuk {bpjs_num}.")
                logger.warning("Kemungkinan: Data tidak valid, kuota habis, atau peserta tidak aktif.")
                gagal_count += 1
                error_berturut += 1
                reset_form(driver, wait)
                time.sleep(1)
                continue

            # --- MENANGANI POPUP SUKSES/GAGAL (DIPERBAIKI) ---
            try:
                popup = wait.until(EC.visibility_of_element_located(
                    (By.XPATH, "//div[contains(@class,'bootbox-alert') or contains(@class,'bootbox')]")
                ))
                popup_text = popup.find_element(By.CLASS_NAME, "bootbox-body").text.strip()
                
                if "Berhasil" in popup_text or "sukses" in popup_text.lower():
                    logger.info(f"✅ SUKSES: {popup_text} (untuk {bpjs_num})")
                    sukses_count += 1
                    error_berturut = 0  # Reset counter error
                else:
                    logger.warning(f"⚠️ GAGAL (Info P-Care): {popup_text} (untuk {bpjs_num})")
                    gagal_count += 1

                # Klik OK
                ok_button = popup.find_element(By.XPATH, ".//button[contains(text(),'OK') or contains(@class,'bootbox-accept')]")
                force_click(driver, ok_button)
                
                # Tunggu popup hilang
                wait.until(EC.invisibility_of_element(popup))
                time.sleep(0.5)
                
                # Hapus overlay sisa
                force_remove_overlay(driver)
                
            except TimeoutException:
                logger.warning("⚠️ Tidak ada popup konfirmasi muncul.")
                gagal_count += 1

        except TimeoutException:
            logger.error(f"❌ GAGAL (Timeout): {bpjs_num}. Data tidak ditemukan atau halaman macet.")
            gagal_count += 1
            error_berturut += 1
            
            # Jika error berturut-turut terlalu banyak, refresh halaman
            if error_berturut >= MAX_ERROR_BERTURUT:
                logger.warning(f"⚠️ Terlalu banyak error berturut ({error_berturut}x). Refresh halaman...")
                driver.get(BPJS_URL)
                time.sleep(2)
                force_remove_overlay(driver)
                setup_page(driver, wait)
                error_berturut = 0
            else:
                reset_form(driver, wait)
            
            time.sleep(1)
            continue
            
        except Exception as e:
            logger.error(f"❌ GAGAL (Error): {bpjs_num}. Terjadi error: {e}")
            gagal_count += 1
            error_berturut += 1
            
            if error_berturut >= MAX_ERROR_BERTURUT:
                logger.warning(f"⚠️ Terlalu banyak error berturut ({error_berturut}x). Refresh halaman...")
                driver.get(BPJS_URL)
                time.sleep(2)
                force_remove_overlay(driver)
                setup_page(driver, wait)
                error_berturut = 0
            else:
                reset_form(driver, wait)
            
            time.sleep(1)
            continue

        # Jeda antar entri
        delay = random.uniform(1.5, 2.5)
        logger.info(f"⏱️  Jeda {delay:.1f} detik sebelum data berikutnya...")
        time.sleep(delay)

    # ===================================================
    #  LAPORAN AKHIR
    # ===================================================
    logger.info("\n" + "="*60)
    logger.info("🎉 OTOMATISASI SELESAI!")
    logger.info("="*60)
    logger.info(f"📊 Total Data: {len(bpjs_numbers)}")
    logger.info(f"✅ Sukses: {sukses_count}")
    logger.info(f"❌ Gagal: {gagal_count}")
    logger.info(f"📈 Success Rate: {(sukses_count/len(bpjs_numbers)*100):.1f}%")
    logger.info("="*60)

except Exception as e:
    logger.error(f"❌ Terjadi error fatal: {e}")
    import traceback
    logger.error(traceback.format_exc())
finally:
    logger.info("\n✅ Skrip selesai. Browser tetap terbuka.")
