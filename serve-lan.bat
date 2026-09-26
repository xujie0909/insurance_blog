@echo off
chcp 65001 >nul
setlocal EnableExtensions
rem ============================================================
rem  One-click LAN preview for the Hugo blog
rem  Double-click this file to start Hugo server. Then open the
rem  blog from your phone (same Wi-Fi/LAN) using the URL below.
rem  Links will point to this PC's LAN IP, not localhost.
rem ============================================================

cd /d "%~dp0"

rem --- make sure hugo is available ---
where hugo >nul 2>nul
if errorlevel 1 (
    echo [ERROR] "hugo" was not found in PATH.
    echo Please install Hugo first: https://gohugo.io/installation/
    echo.
    pause
    exit /b 1
)

rem --- detect the LAN IPv4 address of the connected adapter ---
set "LAN_IP="
powershell -NoProfile -Command "(Get-NetIPConfiguration | Where-Object { $_.IPv4DefaultGateway -ne $null -and $_.NetAdapter.Status -eq 'Up' } | Select-Object -First 1).IPv4Address.IPAddress" > "%TEMP%\hugo_lan_ip.txt" 2>nul
if exist "%TEMP%\hugo_lan_ip.txt" (
    set /p LAN_IP=<"%TEMP%\hugo_lan_ip.txt"
    del "%TEMP%\hugo_lan_ip.txt" >nul 2>nul
)

if "%LAN_IP%"=="" (
    echo [ERROR] Could not detect a LAN IPv4 address.
    echo Make sure your network adapter is connected.
    echo.
    pause
    exit /b 1
)

set "PORT=1313"
set "BASEURL=http://%LAN_IP%:%PORT%/"

echo.
echo ================================================
echo   Hugo server - LAN preview
echo   PC:     http://localhost:%PORT%/
echo   Phone:  %BASEURL%
echo   ^(phone must be on the same LAN/Wi-Fi^)
echo   Press Ctrl+C to stop.
echo ================================================
echo.

hugo server -D --bind 0.0.0.0 --port %PORT% --baseURL "%BASEURL%"

echo.
echo Server stopped.
pause
