# pages/modals/redeem_modal.py
import re
from playwright.sync_api import Page
from pages.modals.base_modal import BaseModal

class RedeemModal(BaseModal):
    """Redeem modal for points redemption"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        # Points display
        self.points_display = page.locator("[class*='points']")
        
        # Amount input
        self.amount_input = page.get_by_placeholder("Enter amount")
        
        # Buttons
        self.confirm_button = page.get_by_role("button", name="Confirm")
        self.ok_button = page.get_by_role("button", name="OK")
        
        # Age verification
        self.verify_age_button = page.get_by_role("button", name="Verify Age Now")
        
        # Messages
        self.error_message = page.locator("[class*='error']")
        self.success_message = page.locator("text=Successfully redeemed")
        
        # Close button - using MUI IconButton with SVG
        self.close_button = page.locator("button.MuiIconButton-root").filter(has=page.locator("svg"))
        # Alternative close button locators:
        self.close_button_alt1 = page.get_by_role("button").filter(has_text=re.compile(r"^$")).filter(has=page.locator("svg"))
        self.close_button_alt2 = page.locator("button.MuiButtonBase-root.MuiIconButton-root")
        
        # Modal container
        self.modal_container = page.locator("[role='dialog']")
        self.modal_paper = page.locator(".MuiPaper-root.MuiDialog-paper")
    
    def get_available_points(self):
        """Get the available points balance"""
        try:
            # Look for points display
            points_text = self.points_display.text_content(timeout=5000)
            print(f"Points text: {points_text}")
            
            # Try to extract number from various formats
            # Format: "10 Points" or "0.00 = $0.00"
            match = re.search(r'(\d+)\s*Points', points_text)
            if match:
                return int(match.group(1))
            
            # Alternative: look for the numeric value
            match = re.search(r'(\d+)\s*=\s*\$', points_text)
            if match:
                return int(match.group(1))
            
            return 0
        except Exception as e:
            print(f"Error getting points: {e}")
            return 0
    
    def enter_amount(self, amount: int):
        """Enter the amount to redeem"""
        try:
            self.amount_input.fill(str(amount))
        except:
            # Try alternative locator
            self.page.get_by_placeholder("Enter points you want to redeem").fill(str(amount))
    
    def click_confirm(self):
        """Click confirm button to redeem"""
        self.confirm_button.click()
    
    def click_ok(self):
        """Click OK button on success/error modal"""
        try:
            self.ok_button.click(timeout=3000)
        except:
            pass
    
    def click_verify_age(self):
        """Click Verify Age Now button"""
        self.verify_age_button.click()
    
    def is_success_displayed(self):
        """Check if success message is displayed"""
        try:
            return self.success_message.is_visible(timeout=3000)
        except:
            return False
    
    def is_error_displayed(self):
        """Check if error message is displayed"""
        try:
            return self.error_message.is_visible(timeout=3000)
        except:
            return False
    
    def get_error_text(self):
        """Get error message text"""
        try:
            return self.error_message.text_content(timeout=3000)
        except:
            return None
    
    def close_modal(self):
        """Close the modal using the close button"""
        try:
            # Try the MUI IconButton with SVG
            if self.close_button.is_visible(timeout=3000):
                self.close_button.click()
                self.page.wait_for_timeout(1000)
                return
        except:
            pass
        
        try:
            # Try alternative close button
            if self.close_button_alt1.is_visible(timeout=2000):
                self.close_button_alt1.click()
                self.page.wait_for_timeout(1000)
                return
        except:
            pass
        
        try:
            # Try clicking the close button by role
            close_btn = self.page.get_by_role("button").filter(has_text=re.compile(r"^$")).first
            if close_btn.is_visible(timeout=2000):
                close_btn.click()
                self.page.wait_for_timeout(1000)
                return
        except:
            pass
        
        try:
            # Try clicking on the backdrop (outside the modal)
            backdrop = self.page.locator(".MuiBackdrop-root")
            if backdrop.is_visible(timeout=2000):
                backdrop.click()
                self.page.wait_for_timeout(1000)
                return
        except:
            pass
        
        # If all else fails, press Escape key
        try:
            self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(1000)
        except:
            pass
    
    def wait_for_modal_to_close(self, timeout=5000):
        """Wait for modal to close completely"""
        try:
            self.page.wait_for_selector(".MuiDialog-root", state="detached", timeout=timeout)
            return True
        except:
            return False