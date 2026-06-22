@echo off
title Sentiment Analyzer - Loading...
color 0A
cls
echo.
echo  ================================================
echo    Sentiment Analyzer v2.0 - With Face Detection
echo  ================================================
echo.
echo  Mengecek Python...
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo  [ERROR] Python tidak ditemukan!
    echo  Download Python 3.11 di: https://python.org
    echo.
    pause
    exit
)

echo  Mengecek library...
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo  Menginstall library (hanya sekali)...
    pip install -r requirements.txt
    if errorlevel 1 (
        color 0C
        echo  [ERROR] Gagal install library!
        pause
        exit
    )
)

echo  Membuka browser...
timeout /t 2 /nobreak >nul
start http://localhost:8000

echo.
echo  ================================================
echo   Server berjalan! Browser akan terbuka otomatis
echo   Tutup jendela ini untuk menghentikan server
echo  ================================================
echo.
python api.py
pause
