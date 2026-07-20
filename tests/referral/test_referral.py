import allure
from playwright.sync_api import Page
from pages.dashboard_page import DashboardPage
from pages.modals.referral_modal import ReferralModal

@allure.epic("Dashboard")
@allure.feature("Referral")
@allure.story("Copy Referral Link")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("referral")
def test_referral_flow(logged_in_page: Page) -> None:
    """Test referral link copying functionality"""
    page = logged_in_page
    
    with allure.step("Open referral modal"):
        dashboard = DashboardPage(page)
        dashboard.click_referral()
        page.wait_for_timeout(1000)  # Wait for modal animation
    
    with allure.step("Copy referral link"):
        referral_modal = ReferralModal(page)
        
        # Verify modal is visible
        assert referral_modal.is_modal_visible(), "Referral modal should be visible"
        
        # Click referral link button
        referral_modal.click_referral_link()
        
        # Click OK to close the copy confirmation
        referral_modal.click_ok()
        
        # Close the referral modal
        referral_modal.close_modal()
        referral_modal.wait_for_modal_to_disappear()
    
    with allure.step("Verify dashboard is still accessible"):
        assert dashboard.is_on_dashboard(), "Should remain on dashboard after closing modal"
    
    with allure.step("Logout"):
        dashboard.click_logout()