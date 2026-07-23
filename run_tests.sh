#!/bin/bash
set -e

echo "=========================================="
echo "  Flame QA - Run Tests + Allure Report"
echo "=========================================="
echo ""

cd "$(dirname "$0")"

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found."
    echo "Run setup first: ./setup_mac.sh"
    exit 1
fi

source venv/bin/activate

# Clean previous results
echo "[1/4] Cleaning previous results..."
rm -rf reports/allure-results reports/allure-report
mkdir -p reports/allure-results

# Run tests
echo ""
echo "[2/4] Running tests..."
pytest tests/ --alluredir=reports/allure-results || true

# Generate Allure report
echo ""
echo "[3/4] Generating Allure report..."
allure generate reports/allure-results -o reports/allure-report --clean

# Open Allure report in browser
echo ""
echo "[4/4] Opening Allure report..."
allure open reports/allure-report

echo ""
echo "Report saved at: reports/allure-report/index.html"
