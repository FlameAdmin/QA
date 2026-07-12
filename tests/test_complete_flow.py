import re
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.modals.referral_modal import ReferralModal
from pages.modals.redeem_modal import RedeemModal

def test_complete_dashboard_flow(page: Page) -> None:
    # Login
    home_page = HomePage(page)
    home_page.accept_cookies()
    home_page.click_get_started()
    
    login_page = LoginPage(page)
    login_page.enter_email("kagameacu@gmail.com")
    login_page.click_next()
    login_page.enter_password("1234")
    login_page.click_next()
    
    page.wait_for_timeout(3000)
    expect(page).to_have_url(re.compile(r".*user/home.*"))
    
    dashboard = DashboardPage(page)
    
    # 1. Test Referral Flow
    dashboard.click_referral()
    referral_modal = ReferralModal(page)
    referral_modal.click_referral_link()
    referral_modal.click_ok()
    referral_modal.close_modal()
    
    # 2. Test Redeem Flow
    dashboard.click_redeem()
    redeem_modal = RedeemModal(page)
    points = redeem_modal.get_available_points()
    print(f"Available points: {points}")
    
    if points >= 500:
        redeem_modal.enter_amount(500)
        redeem_modal.click_confirm()
        if redeem_modal.is_success_displayed():
            redeem_modal.click_ok()
    
    redeem_modal.close_modal()
    
    # 3. Logout
    dashboard.click_logout()
    page.wait_for_timeout(2000)