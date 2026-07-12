from playwright.sync_api import Page

class OTPPage:
    def __init__(self, page: Page):
        self.page = page
        self.otp_input = page.get_by_role("textbox", name="Confirm OTP sent to your")
        self.next_button = page.get_by_role("button", name="Next")
    
    def enter_otp(self, otp: str):
        self.otp_input.fill(otp)
    
    def click_next(self):
        self.next_button.click()