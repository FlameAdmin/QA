from playwright.sync_api import Page

class DashboardPage:
    """Dashboard page after successful login"""
    
    def __init__(self, page: Page):
        self.page = page
        self.referral_button = page.get_by_role("button", name="Referral")
        self.redeem_button = page.get_by_role("button", name="Redeem")
        self.profile_button = page.get_by_role("button", name="Profile")
        self.notification_button = page.locator("[class*='notification']")
        self.user_menu = page.locator("[class*='user-menu']")
        self.logout_button_ru = page.get_by_role("button", name="Выход")
        self.logout_button_en = page.get_by_role("button", name="Logout")
    
    def click_referral(self):
        """Click referral button to open referral modal"""
        self.referral_button.click()
    
    def click_redeem(self):
        """Click redeem button to open redeem modal"""
        self.redeem_button.click()
    
    def click_profile(self):
        """Click profile button"""
        self.profile_button.click()
    
    def click_notifications(self):
        """Click notification button"""
        self.notification_button.click()
    
    def click_logout(self):
        """Click logout button (tries Russian first, then English)"""
        try:
            self.logout_button_ru.click(timeout=3000)
        except:
            self.logout_button_en.click(timeout=3000)
    
    def is_on_dashboard(self):
        """Verify user is on dashboard"""
        return "user/home" in self.page.url