@echo off
echo ==========================================
echo   Opening Allure Report
echo ==========================================
echo.

cd /d "%~dp0"

if exist "reports\allure-report\index.html" (
    echo Opening report...
    start allure open reports/allure-report
    echo.
    echo 📊 Report opened in browser!
) else (
    echo ❌ Report not found!
    echo.
    echo Please run tests first:
    echo   - run_tests.bat (headless)
    echo   - run_tests_headed.bat (with browser)
    echo.
    pause
)