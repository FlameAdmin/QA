# pages/modals/base_modal.py
import re
from playwright.sync_api import Page

class BaseModal:
    """Base class for all modals with common methods"""
    
    def __init__(self, page: Page):
        self.page = page
        # MUI Close button with SVG icon
        self.close_button = page.locator("button.MuiIconButton-root").filter(has=page.locator("svg"))
        self.ok_button = page.get_by_role("button", name="OK")
    
    def close_modal(self):
        """Close the modal using the close button"""
        try:
            # Try MUI IconButton
            if self.close_button.is_visible(timeout=3000):
                self.close_button.click()
                self.page.wait_for_timeout(1000)
                return
        except:
            pass
        
        try:
            # Try any button with no text (common for close buttons)
            close_btn = self.page.get_by_role("button").filter(has_text=re.compile(r"^$")).first
            if close_btn.is_visible(timeout=2000):
                close_btn.click()
                self.page.wait_for_timeout(1000)
                return
        except:
            pass
        
        try:
            # Try clicking on backdrop
            backdrop = self.page.locator(".MuiBackdrop-root")
            if backdrop.is_visible(timeout=2000):
                backdrop.click()
                self.page.wait_for_timeout(1000)
                return
        except:
            pass
        
        # Press Escape as last resort
        try:
            self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(1000)
        except:
            pass
    
    def click_ok(self):
        """Click OK button on modal"""
        try:
            self.ok_button.click(timeout=3000)
            self.page.wait_for_timeout(1000)
        except:
            pass
    
    def is_modal_visible(self):
        """Check if modal is visible"""
        try:
            return self.close_button.is_visible(timeout=2000)
        except:
            return False
    
    def wait_for_modal_to_disappear(self, timeout=5000):
        """Wait for modal to disappear"""
        try:
            self.page.wait_for_selector(".MuiDialog-root", state="detached", timeout=timeout)
            return True
        except:
            return False



# import re
# from playwright.sync_api import Page

# class BaseModal:
#     """Base class for all modals with common methods"""
    
#     def __init__(self, page: Page):
#         self.page = page
#         self.close_button = page.get_by_role("button").filter(has_text=re.compile(r"^$"))
#         self.ok_button = page.get_by_role("button", name="OK")
    
#     def close_modal(self):
#         """Close the modal using the close button"""
#         try:
#             self.close_button.click(timeout=3000)
#         except:
#             pass  # Modal might close automatically
    
#     def click_ok(self):
#         """Click OK button on modal"""
#         self.ok_button.click()
    
#     def is_modal_visible(self):
#         """Check if modal is visible"""
#         try:
#             return self.close_button.is_visible()
#         except:
#             return False