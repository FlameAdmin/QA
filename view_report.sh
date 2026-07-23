#!/bin/bash

cd "$(dirname "$0")"

if [ -d "reports/allure-report" ]; then
    echo "Opening Allure report..."
    allure open reports/allure-report
else
    echo "ERROR: Report not found. Run tests first: ./run_tests.sh"
    exit 1
fi
