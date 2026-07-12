import re
import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.modals.referral_modal import ReferralModal
from pages.modals.redeem_modal import RedeemModal

@pytest.mark.parametrize("feature", ["referral", "redeem"])
def test_dashboard_features(page: Page, feature):
    # Login
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
    
    dashboard = DashboardPage(page)
    
    if feature == "referral":
        # Test referral
        dashboard.click_referral()
        referral_modal = ReferralModal(page)
        referral_modal.click_referral_link()
        referral_modal.click_ok()
        referral_modal.close_modal()
    
    elif feature == "redeem":
        # Test redeem
        dashboard.click_redeem()
        redeem_modal = RedeemModal(page)
        points = redeem_modal.get_available_points()
        assert points >= 0, "Points should be 0 or more"
        redeem_modal.close_modal()
    
    # Logout
    dashboard.click_logout()