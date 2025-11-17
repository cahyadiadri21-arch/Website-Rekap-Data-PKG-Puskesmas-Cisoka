@echo off
echo ========================================
echo  MEMULAI CHROME DENGAN REMOTE DEBUGGING
echo ========================================
echo.
echo Chrome akan dibuka dengan port 9222
echo JANGAN TUTUP WINDOW INI!
echo.
echo Setelah Chrome terbuka:
echo 1. Login ke P-Care
echo 2. Jalankan script Python
echo.
echo ========================================

"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%USERPROFILE%\selenium_chrome_profile"

pause
