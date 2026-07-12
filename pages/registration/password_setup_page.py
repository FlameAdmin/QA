from playwright.sync_api import Page

class PasswordSetupPage:
    def __init__(self, page: Page):
        self.page = page
        self.password_input = page.get_by_role("textbox", name="Password", exact=True)
        self.confirm_password_input = page.get_by_role("textbox", name="Confirm Password")
        self.next_button = page.get_by_role("button", name="Next")
    
    def enter_password(self, password: str):
        self.password_input.fill(password)
    
    def enter_confirm_password(self, password: str):
        self.confirm_password_input.fill(password)
    
    def click_next(self):
        self.next_button.click()