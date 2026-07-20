import allure
from playwright.sync_api import Page
from pages.dashboard_page import DashboardPage
from pages.modals.redeem_modal import RedeemModal

@allure.epic("Dashboard")
@allure.feature("Redeem")
@allure.story("Points Redemption")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("redeem")
def test_redeem_flow(logged_in_page: Page) -> None:
    """Test points redemption flow"""
    page = logged_in_page
    
    with allure.step("Open redeem modal"):
        dashboard = DashboardPage(page)
        dashboard.click_redeem()
        page.wait_for_timeout(2000)  # Wait for modal animation
    
    with allure.step("Initialize redeem modal"):
        redeem_modal = RedeemModal(page)
        
        # Verify modal is visible
        assert redeem_modal.is_modal_visible(), "Redeem modal should be visible"
        
        # Wait for modal to be ready
        assert redeem_modal.wait_for_modal_ready(), "Redeem modal should be fully loaded"
    
    with allure.step("Check available points"):
        available_points = redeem_modal.get_available_points()
        allure.attach(
            str(available_points), 
            name="Available Points", 
            attachment_type=allure.attachment_type.TEXT
        )
        print(f"Available points: {available_points}")
    
    with allure.step("Attempt to redeem points"):
        if available_points >= 10:
            # Enter amount to redeem (use half of available points for testing)
            redeem_amount = min(available_points, 100)  # Cap at 100 for safety
            if redeem_amount > 0:
                redeem_modal.enter_amount(redeem_amount)
                page.wait_for_timeout(500)
                
                # Click confirm
                redeem_modal.click_confirm()
                page.wait_for_timeout(3000)
                
                # Check for success or error
                if redeem_modal.is_success_displayed():
                    allure.attach(
                        f"Successfully redeemed {redeem_amount} points!", 
                        name="Status", 
                        attachment_type=allure.attachment_type.TEXT
                    )
                    print(f"Successfully redeemed {redeem_amount} points!")
                    redeem_modal.click_ok()
                else:
                    # Check for error message
                    error_text = redeem_modal.get_error_text()
                    allure.attach(
                        f"❌ Redeem failed: {error_text}", 
                        name="Status", 
                        attachment_type=allure.attachment_type.TEXT
                    )
                    print(f"❌ Redeem failed: {error_text}")
                    
                    # Handle error modal
                    if redeem_modal.is_error_displayed():
                        redeem_modal.click_ok()
            else:
                allure.attach(
                    "No points to redeem (0 points available)",
                    name="Status",
                    attachment_type=allure.attachment_type.TEXT
                )
                print("No points to redeem (0 points available)")
        else:
            allure.attach(
                f"Not enough points (have {available_points}, need 10)",
                name="Status",
                attachment_type=allure.attachment_type.TEXT
            )
            print(f"Not enough points (have {available_points}, need 10)")
    
    with allure.step("Close modal"):
        # Try to close the modal
        redeem_modal.close_modal()
        page.wait_for_timeout(1000)
        
        # Verify modal is closed
        assert redeem_modal.wait_for_modal_to_disappear(), "Redeem modal should close"
    
    with allure.step("Verify dashboard is still accessible"):
        assert dashboard.is_on_dashboard(), "Should remain on dashboard after closing modal"
    
    with allure.step("Logout"):
        dashboard.click_logout()
