#!/bin/bash
set -e

echo "=========================================="
echo "  Flame QA - First-Time Mac Setup"
echo "=========================================="
echo ""

cd "$(dirname "$0")"

# 1. Check Homebrew
if ! command -v brew &>/dev/null; then
    echo "ERROR: Homebrew is not installed."
    echo "Install it first: https://brew.sh"
    exit 1
fi

# 2. Install Allure CLI
if ! command -v allure &>/dev/null; then
    echo "[1/4] Installing Allure via Homebrew..."
    brew install allure
else
    echo "[1/4] Allure already installed: $(allure --version)"
fi

# 3. Create Python virtual environment
echo ""
echo "[2/4] Creating Python virtual environment..."
python3 -m venv venv
echo "      Done."

# 4. Install Python dependencies
echo ""
echo "[3/4] Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "      Done."

# 5. Install Playwright browsers
echo ""
echo "[4/4] Installing Playwright browsers..."
playwright install chromium
echo "      Done."

echo ""
echo "=========================================="
echo "  Setup complete!"
echo "=========================================="
echo ""
echo "Now run tests with:"
echo "  ./run_tests.sh"
echo ""
