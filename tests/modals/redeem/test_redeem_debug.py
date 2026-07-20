import allure
from playwright.sync_api import Page
from pages.dashboard_page import DashboardPage
from pages.modals.redeem_modal import RedeemModal

@allure.tag("debug")
def test_debug_redeem_modal(logged_in_page: Page):
    """Debug test to inspect redeem modal"""
    page = logged_in_page
    
    # Open redeem modal
    dashboard = DashboardPage(page)
    dashboard.click_redeem()
    page.wait_for_timeout(2000)
    
    # Get HTML for debugging
    html_content = page.content()
    with open("reports/debug_redeem_modal.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    # Debug information
    print("\n=== Redeem Modal Debug Info ===")
    print(f"URL: {page.url}")
    
    # Check for elements
    elements_to_check = {
        "MUI Dialog": ".MuiDialog-root",
        "Dialog Role": "[role='dialog']",
        "Points Display": "[class*='points'], [class*='balance']",
        "Amount Input": "input[placeholder*='amount'], input[placeholder*='points']",
        "Confirm Button": "button:has-text('Confirm')",
        "OK Button": "button:has-text('OK')",
    }
    
    for name, selector in elements_to_check.items():
        count = page.locator(selector).count()
        print(f"{name}: {count} elements")
        
        if count > 0:
            # Check if visible
            try:
                is_visible = page.locator(selector).first.is_visible()
                print(f"  - First visible: {is_visible}")
            except:
                pass
    
    # Check all buttons
    buttons = page.get_by_role("button").all()
    print(f"\nAll buttons on page ({len(buttons)}):")
    for i, btn in enumerate(buttons[:10]):  # Show first 10
        try:
            text = btn.text_content()[:50] if btn.text_content() else "No text"
            is_visible = btn.is_visible()
            print(f"  {i+1}. '{text}' - visible: {is_visible}")
        except:
            pass
    
    # Take screenshot
    page.screenshot(path="reports/screenshots/debug_redeem_modal.png")
    
    # Try to get points
    redeem_modal = RedeemModal(page)
    points = redeem_modal.get_available_points()
    print(f"\nAvailable points: {points}")
    
    print("\n=== Debug Complete ===")