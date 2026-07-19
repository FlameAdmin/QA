import re
import pytest
import allure
import os
from datetime import datetime
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.login_page import LoginPage

# ============== HOOKS FOR SCREENSHOTS ON FAILURE ==============
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    
    # Take screenshot on failure during test execution
    if rep.when == "call" and rep.failed:
        # Get the page fixture if it exists
        page = item.funcargs.get("page")
        if page:
            try:
                # Create directories if they don't exist
                os.makedirs("reports/screenshots", exist_ok=True)
                os.makedirs("reports/traces", exist_ok=True)
                
                test_name = item.name
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # 1. Take Screenshot
                screenshot_path = f"reports/screenshots/{test_name}_{timestamp}.png"
                page.screenshot(path=screenshot_path, full_page=True)
                
                # Attach to Allure
                with open(screenshot_path, "rb") as f:
                    allure.attach(
                        f.read(),
                        name=f"Screenshot - {test_name}",
                        attachment_type=allure.attachment_type.PNG
                    )
                
                # 2. Save HTML for debugging
                html_content = page.content()
                allure.attach(
                    html_content,
                    name=f"HTML - {test_name}",
                    attachment_type=allure.attachment_type.HTML
                )
                
                # 3. Save Playwright Trace (if tracing is started)
                try:
                    trace_path = f"reports/traces/{test_name}_{timestamp}.zip"
                    page.tracing.stop(path=trace_path)
                    with open(trace_path, "rb") as f:
                        allure.attach(
                            f.read(),
                            name=f"Trace - {test_name}",
                            attachment_type=allure.attachment_type.ZIP
                        )
                except:
                    pass  # Tracing might not be started
                    
            except Exception as e:
                print(f"Failed to capture failure artifacts: {e}")

# ============== PAGE FIXTURE ==============
@pytest.fixture(scope="function")
def page(page: Page, request):
    """Custom page fixture"""
    test_name = request.node.name
    yield page
    

from fixtures.login_data import VALID_USER

@pytest.fixture
def login_page(page):
    home = HomePage(page)
    home.open_login()

    return LoginPage(page)

@pytest.fixture
def logged_in_page(page):

    home = HomePage(page)
    home.open_login()

    login = LoginPage(page)

    login.login(
        VALID_USER["email"],
        VALID_USER["password"]
    )

    login.verify_login_success()

    return page

# ============== ALLURE ENVIRONMENT INFO ==============
@pytest.fixture(scope="session", autouse=True)
def allure_environment_info():
    """Add environment information to Allure report"""
    os.makedirs("reports/allure-results", exist_ok=True)
    
    env_file = "reports/allure-results/environment.properties"
    with open(env_file, "w") as f:
        f.write("Browser=Chromium\n")
        f.write("Browser.Version=Latest\n")
        f.write("Environment=Testing\n")
        f.write("Platform=Windows 11\n")
        f.write("Python.Version=3.12.1\n")
        f.write("Test.Framework=Pytest\n")
        f.write("Playwright.Version=1.61.0\n")
        f.write("Allure.Version=2.44.0\n")

# ============== IMPORT TEST DATA FIXTURES ==============
# from fixtures.test_data import existing_user, new_user
