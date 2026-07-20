import re
from playwright.sync_api import Page
from pages.modals.base_modal import BaseModal

class ReferralModal(BaseModal):
    """Referral modal with referral link functionality"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        # More specific locators for referral modal
        self.referral_link_button = page.get_by_role("button", name=re.compile(r"(?i)referral link"))
        self.copy_link_button = page.get_by_role("button", name=re.compile(r"(?i)copy"))
        self.referral_link_element = page.locator("[class*='referral-link'], [class*='link']").first
        self.referral_list = page.locator("[class*='referral-list']")
        self.empty_message = page.locator("text=/No referrals yet/i")
        self.referral_count = page.locator("[class*='referral-count']")
        # The modal dialog container
        self.modal_container = page.locator(".MuiDialog-root, [role='dialog'], .MuiModal-root").first
    
    def click_referral_link(self):
        """Click on the referral link button to show the link"""
        try:
            # Wait for button to be ready
            self.referral_link_button.wait_for(state="visible", timeout=5000)
            self.referral_link_button.click()
            self.page.wait_for_timeout(500)
            return True
        except Exception as e:
            print(f"Error clicking referral link: {e}")
            return False
    
    def copy_referral_link(self):
        """Click the copy button to copy the referral link"""
        try:
            self.copy_link_button.wait_for(state="visible", timeout=3000)
            self.copy_link_button.click()
            self.page.wait_for_timeout(500)
            return True
        except Exception as e:
            print(f"Error copying referral link: {e}")
            return False
    
    def get_referral_link(self):
        """Get the referral link text"""
        try:
            # Wait for link to be visible
            self.referral_link_element.wait_for(state="visible", timeout=5000)
            link_text = self.referral_link_element.text_content()
            if link_text:
                return link_text.strip()
            return None
        except Exception as e:
            print(f"Error getting referral link: {e}")
            return None
    
    def is_referral_list_empty(self):
        """Check if referral list is empty"""
        try:
            return self.empty_message.is_visible()
        except:
            return False
    
    def get_referral_count(self):
        """Get the number of referrals"""
        try:
            text = self.referral_count.text_content()
            if text:
                import re
                numbers = re.findall(r'\d+', text)
                return int(numbers[0]) if numbers else 0
            return 0
        except:
            return 0
    
    def wait_for_modal_ready(self, timeout=10000):
        """Wait for modal to be fully loaded and ready"""
        try:
            # Wait for the modal container to appear
            self.modal_container.wait_for(state="visible", timeout=timeout)
            self.page.wait_for_timeout(500)  # Extra wait for content to render
            
            # Check if referral link button is present (indicates modal is ready)
            if self.referral_link_button.is_visible(timeout=2000):
                return True
            
            # Or check for the referral link itself
            if self.referral_link_element.is_visible(timeout=2000):
                return True
            
            return False
        except Exception as e:
            print(f"Error waiting for modal ready: {e}")
            return False
        