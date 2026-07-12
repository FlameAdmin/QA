import re
import allure
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.modals.referral_modal import ReferralModal

@allure.epic("Dashboard")
@allure.feature("Referral")
@allure.story("Copy Referral Link")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("referral")
def test_referral_flow(page: Page) -> None:
    with allure.step("Login to application"):
        home_page = HomePage(page)
        home_page.open_login()
        # home_page.accept_cookies()
        # home_page.click_get_started()
        
        login_page = LoginPage(page)
        login_page.enter_email("kagameacu@gmail.com")
        login_page.click_next()
        login_page.enter_password("1234")
        login_page.click_next()
        
        page.wait_for_timeout(3000)
        expect(page).to_have_url(re.compile(r".*user/home.*"))
    
    with allure.step("Open referral modal"):
        dashboard = DashboardPage(page)
        dashboard.click_referral()
    
    with allure.step("Copy referral link"):
        referral_modal = ReferralModal(page)
        referral_modal.click_referral_link()
        referral_modal.click_ok()
        referral_modal.close_modal()
    
    with allure.step("Logout"):
        dashboard.click_logout()