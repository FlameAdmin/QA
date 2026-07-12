@echo off
echo ==========================================
echo   Running Playwright Tests (Headless)
echo ==========================================
echo.

cd /d "%~dp0"

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Run tests with Allure
echo.
echo [1/4] Running tests...
pytest tests/ --alluredir=reports/allure-results

REM Check if tests passed
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Some tests failed!
    pause
    exit /b %ERRORLEVEL%
)

REM Generate Allure report
echo.
echo [2/4] Generating Allure report...
allure generate reports/allure-results -o reports/allure-report --clean

REM Open Allure report
echo.
echo [3/4] Opening Allure report...
start allure open reports/allure-report

echo.
echo [4/4] Done!
echo.
echo 📊 Report saved at: reports/allure-report/index.html
echo 📁 Results saved at: reports/allure-results/
echo.
pause