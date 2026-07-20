import re
from playwright.sync_api import Page
from pages.modals.base_modal import BaseModal

class RedeemModal(BaseModal):
    """Redeem modal for points redemption"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        
        # Points display - try multiple selectors
        self.points_display = page.locator("[class*='points'], [class*='balance'], [class*='Points']").first
        
        # Amount input - try multiple placeholders
        self.amount_input = page.locator("input[placeholder*='amount'], input[placeholder*='points'], input[type='number']").first
        
        # Buttons
        self.confirm_button = page.get_by_role("button", name=re.compile(r"(?i)confirm"))
        self.ok_button = page.get_by_role("button", name=re.compile(r"(?i)ok"))
        
        # Age verification (if needed)
        self.verify_age_button = page.get_by_role("button", name=re.compile(r"(?i)verify age"))
        
        # Messages
        self.error_message = page.locator("[class*='error'], [class*='Error'], .MuiAlert-colorError").first
        self.success_message = page.locator("text=/successfully redeemed|redemption successful/i").first
        
        # Modal container
        self.modal_container = page.locator(".MuiDialog-root, [role='dialog'], .MuiModal-root").first
        
        # Close button - using MUI IconButton with SVG
        self.close_button = page.locator("button.MuiIconButton-root").filter(has=page.locator("svg")).first
    
    def get_available_points(self):
        """Get the available points balance"""
        try:
            # Wait for points to be visible
            self.points_display.wait_for(state="visible", timeout=5000)
            points_text = self.points_display.text_content()
            print(f"Points text: {points_text}")
            
            if not points_text:
                return 0
            
            # Try various patterns to extract points
            patterns = [
                r'(\d+)\s*Points?',  # "10 Points" or "10 Point"
                r'(\d+)\s*=\s*\$',   # "10 = $0.00"
                r'Balance:\s*(\d+)',  # "Balance: 10"
                r'(\d+)\s*points?',   # "10 points"
                r'(\d+)',             # Just any number
            ]
            
            for pattern in patterns:
                match = re.search(pattern, points_text, re.IGNORECASE)
                if match:
                    return int(match.group(1))
            
            return 0
        except Exception as e:
            print(f"Error getting points: {e}")
            return 0
    
    def enter_amount(self, amount: int):
        """Enter the amount to redeem"""
        try:
            # Clear and fill
            self.amount_input.wait_for(state="visible", timeout=5000)
            self.amount_input.clear()
            self.amount_input.fill(str(amount))
            self.page.wait_for_timeout(500)
            return True
        except Exception as e:
            print(f"Error entering amount: {e}")
            # Try alternative: click and type
            try:
                self.amount_input.click()
                self.amount_input.press("Control+A")
                self.amount_input.type(str(amount))
                return True
            except:
                return False
    
    def click_confirm(self):
        """Click confirm button to redeem"""
        try:
            self.confirm_button.wait_for(state="visible", timeout=3000)
            self.confirm_button.click()
            self.page.wait_for_timeout(500)
            return True
        except Exception as e:
            print(f"Error clicking confirm: {e}")
            return False
    
    def click_ok(self):
        """Click OK button on success/error modal"""
        try:
            self.ok_button.wait_for(state="visible", timeout=3000)
            self.ok_button.click()
            self.page.wait_for_timeout(500)
            return True
        except Exception as e:
            print(f"Error clicking OK: {e}")
            return False
    
    def click_verify_age(self):
        """Click Verify Age Now button"""
        try:
            self.verify_age_button.wait_for(state="visible", timeout=3000)
            self.verify_age_button.click()
            self.page.wait_for_timeout(500)
            return True
        except:
            return False
    
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
            self.error_message.wait_for(state="visible", timeout=3000)
            return self.error_message.text_content()
        except:
            return None
    
    def wait_for_modal_ready(self, timeout=10000):
        """Wait for modal to be fully loaded and ready"""
        try:
            # Wait for the modal container to appear
            self.modal_container.wait_for(state="visible", timeout=timeout)
            self.page.wait_for_timeout(500)  # Extra wait for content to render
            
            # Check if points display is present (indicates modal is ready)
            if self.points_display.is_visible(timeout=2000):
                return True
            
            # Or check for the amount input
            if self.amount_input.is_visible(timeout=2000):
                return True
            
            return False
        except Exception as e:
            print(f"Error waiting for modal ready: {e}")
            return False 