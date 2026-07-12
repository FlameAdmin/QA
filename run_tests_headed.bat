@echo off
echo ==========================================
echo   Running Playwright Tests (Headed Mode)
echo ==========================================
echo.

cd /d "%~dp0"

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Run tests with Allure in headed mode
echo.
echo [1/4] Running tests in headed mode...
pytest tests/ --headed --browser chromium --slowmo=200 --alluredir=reports/allure-results

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
pause