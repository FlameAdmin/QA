import re
from playwright.sync_api import Page
from pages.modals.base_modal import BaseModal

class ReferralModal(BaseModal):
    """Referral modal with referral link functionality"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.referral_link_button = page.get_by_role("button", name="Referral link")
        self.referral_list = page.locator("[class*='referral-list']")
        self.copy_link_button = page.get_by_role("button", name="Copy")
        self.ok_button = page.get_by_role("button", name="OK")
    
    def click_referral_link(self):
        """Click on the referral link button to copy"""
        self.referral_link_button.click()
    
    def copy_referral_link(self):
        """Copy the referral link"""
        self.copy_link_button.click()
    
    def get_referral_link(self):
        """Get the referral link text"""
        # Wait for link to appear
        link_element = self.page.locator("[class*='referral-link']")
        return link_element.text_content()
    
    def is_referral_list_empty(self):
        """Check if referral list is empty"""
        try:
            empty_message = self.page.locator("text=No referrals yet")
            return empty_message.is_visible()
        except:
            return False
    
    def click_ok(self):
        """Click OK button on modal"""
        self.ok_button.click()