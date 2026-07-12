@echo off
echo ==========================================
echo   Cleaning Allure Reports
echo ==========================================
echo.

cd /d "%~dp0"

echo Cleaning allure-results...
rmdir /s /q reports\allure-results 2>nul

echo Cleaning allure-report...
rmdir /s /q reports\allure-report 2>nul

echo Cleaning screenshots...
rmdir /s /q reports\screenshots 2>nul

echo Cleaning traces...
rmdir /s /q reports\traces 2>nul

echo.
echo ✅ All cleaned!
echo.
echo 📁 Reports folder is now empty.
pause