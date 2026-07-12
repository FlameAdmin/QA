import re
import allure
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.modals.redeem_modal import RedeemModal

@allure.epic("Dashboard")
@allure.feature("Redeem")
@allure.story("Points Redemption")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("redeem")
def test_redeem_flow(page: Page) -> None:
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
    
    with allure.step("Open redeem modal"):
        dashboard = DashboardPage(page)
        dashboard.click_redeem()
        page.wait_for_timeout(2000)
    
    with allure.step("Check available points"):
        redeem_modal = RedeemModal(page)
        available_points = redeem_modal.get_available_points()
        allure.attach(
            str(available_points), 
            name="Available Points", 
            attachment_type=allure.attachment_type.TEXT
        )
        print(f"Available points: {available_points}")
    
    with allure.step("Attempt to redeem points"):
        if available_points >= 10:
            redeem_modal.enter_amount(available_points)
            redeem_modal.click_confirm()
            page.wait_for_timeout(3000)
            
            if redeem_modal.is_success_displayed():
                allure.attach(
                    "✅ Redeem successful!", 
                    name="Status", 
                    attachment_type=allure.attachment_type.TEXT
                )
                print("✅ Redeem successful!")
                redeem_modal.click_ok()
            else:
                allure.attach(
                    "❌ Redeem failed", 
                    name="Status", 
                    attachment_type=allure.attachment_type.TEXT
                )
                print("❌ Redeem failed")
        else:
            allure.attach(
                f"Not enough points (have {available_points}, need 10)",
                name="Status",
                attachment_type=allure.attachment_type.TEXT
            )
            print(f"Not enough points (have {available_points}, need 10)")
    
    with allure.step("Close modal and logout"):
        redeem_modal.close_modal()
        page.wait_for_timeout(2000)
        dashboard.click_logout()