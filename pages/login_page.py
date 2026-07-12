from playwright.sync_api import Page, expect
import re
class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email_input = page.get_by_role("textbox", name="email")
        self.password_input = page.get_by_role("textbox", name="Password")
        self.next_button = page.get_by_role("button", name="Next")
        self.error_message = page.locator(".MuiAlert-message")
        self.forgot_password_link = page.get_by_text("Forgot Password")
        

    def enter_email(self, email):
        self.email_input.fill(email)

    def clear_email(self):
        self.email_input.clear()

    def enter_password(self, password):
        self.password_input.fill(password)

    def clear_password(self):
        self.password_input.clear()

    def click_next(self):
        self.next_button.click()

    # ----------------------------

    def login(self, email, password):
        self.enter_email(email)
        self.click_next()
        self.enter_password(password)
        self.click_next()

    # ----------------------------

    def verify_login_success(self):
        expect(self.page).to_have_url(
            re.compile(r".*user/home.*")
        )

    def verify_login_failed(self):
        expect(self.page).not_to_have_url(
            re.compile(r".*user/home.*")
        )

    def click_forgot_password(self):
        self.forgot_password_link.click()



# from playwright.sync_api import Page

# class LoginPage:
#     def __init__(self, page: Page):
#         self.page = page
#         self.email_input = page.get_by_role("textbox", name="email")
#         self.password_input = page.get_by_role("textbox", name="Password")
#         self.next_button = page.get_by_role("button", name="Next")
        
#     def enter_email(self, email: str):
#         self.email_input.fill(email)
    
#     def enter_password(self, password: str):
#         self.password_input.fill(password)
    
#     def click_next(self):
#         self.next_button.click()
