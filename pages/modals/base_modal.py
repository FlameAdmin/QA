import re
from playwright.sync_api import Page

class BaseModal:
    """Base class for all modals with common methods"""
    
    def __init__(self, page: Page):
        self.page = page
        # More flexible modal detection
        self.modal_dialog = page.locator(".MuiDialog-root, [role='dialog'], .modal, .MuiModal-root").first
        self.close_button = page.locator("button.MuiIconButton-root").filter(has=page.locator("svg")).first
        self.ok_button = page.get_by_role("button", name="OK")
        self.modal_title = page.locator(".MuiDialogTitle-root, [class*='title']").first
    
    def is_modal_visible(self):
        """Check if modal is visible with multiple fallback strategies"""
        try:
            # Strategy 1: Check MUI Dialog
            if self.modal_dialog.is_visible(timeout=2000):
                return True
        except:
            pass
        
        try:
            # Strategy 2: Check for any visible dialog role
            dialog = self.page.get_by_role("dialog")
            if dialog.is_visible(timeout=1000):
                return True
        except:
            pass
        
        try:
            # Strategy 3: Check for modal backdrop
            backdrop = self.page.locator(".MuiBackdrop-root, .modal-backdrop")
            if backdrop.is_visible(timeout=1000):
                return True
        except:
            pass
        
        try:
            # Strategy 4: Check for referral-specific elements
            referral_link = self.page.locator("[class*='referral-link']")
            if referral_link.is_visible(timeout=1000):
                return True
        except:
            pass
        
        return False
    
    def wait_for_modal(self, timeout=10000):
        """Wait for modal to appear"""
        try:
            # Try different strategies
            self.page.wait_for_selector(".MuiDialog-root", state="visible", timeout=timeout)
            return True
        except:
            pass
        
        try:
            self.page.wait_for_selector("[role='dialog']", state="visible", timeout=timeout)
            return True
        except:
            pass
        
        try:
            self.page.wait_for_selector("[class*='referral-link']", state="visible", timeout=timeout)
            return True
        except:
            return False
    
    def close_modal(self):
        """Close the modal using the close button"""
        try:
            # Try MUI IconButton
            if self.close_button.is_visible(timeout=3000):
                self.close_button.click()
                self.page.wait_for_timeout(500)
                return True
        except:
            pass
        
        try:
            # Try any button with no text (common for close buttons)
            close_btn = self.page.get_by_role("button").filter(has_text=re.compile(r"^$")).first
            if close_btn.is_visible(timeout=2000):
                close_btn.click()
                self.page.wait_for_timeout(500)
                return True
        except:
            pass
        
        try:
            # Try clicking on backdrop
            backdrop = self.page.locator(".MuiBackdrop-root, .modal-backdrop")
            if backdrop.is_visible(timeout=2000):
                backdrop.click()
                self.page.wait_for_timeout(500)
                return True
        except:
            pass
        
        # Press Escape as last resort
        try:
            self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(500)
            return True
        except:
            return False
    
    def click_ok(self):
        """Click OK button on modal"""
        try:
            self.ok_button.click(timeout=3000)
            self.page.wait_for_timeout(500)
            return True
        except:
            return False
    
    def wait_for_modal_to_disappear(self, timeout=5000):
        """Wait for modal to disappear"""
        try:
            self.page.wait_for_selector(".MuiDialog-root", state="detached", timeout=timeout)
            return True
        except:
            try:
                self.page.wait_for_selector("[role='dialog']", state="detached", timeout=timeout)
                return True
            except:
                return False
