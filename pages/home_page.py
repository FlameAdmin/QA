
class HomePage:
    URL = "https://theflame.life/"

    def __init__(self, page):
        self.page = page
        self.allow_cookies_button = page.get_by_role("button", name="Allow All")
        self.get_started_button = page.get_by_role("banner").get_by_role("button", name="Get Started")
        self.logout_button_ru = page.get_by_role("button", name="Выход")
        self.logout_button_en = page.get_by_role("button", name="Logout")
    

    def open(self):
        self.page.goto(self.URL, timeout=90000, wait_until="domcontentloaded")

    # def accept_cookies(self):
    #     self.allow_cookies_button.click()
    def accept_cookies(self):
        try:    
            # Wait for the cookie banner to be visible
            self.page.wait_for_selector("button:has-text('Allow All')", state="visible", timeout=10000)
            self.allow_cookies_button.click()
        except:
            # If no cookie banner, just continue
            pass
    
    def click_get_started(self):
        self.get_started_button.click()

    def open_login(self):
        self.open()
        self.accept_cookies()
        self.click_get_started()
            
    def click_logout(self):
        """Click the logout button (tries Russian first, then English)"""
        try:
            self.logout_button_ru.click(timeout=3000)
        except:
            self.logout_button_en.click(timeout=3000)




# from playwright.sync_api import Page

# class HomePage:
#     def __init__(self, page: Page) -> None:
#         self.page = page
#         self.page.goto("https://theflame.life/", timeout=90000)
#         self.allow_cookies_button = page.get_by_role("button", name="Allow All")
#         self.get_started_button = page.get_by_role("banner").get_by_role("button", name="Get Started")
#         self.logout_button_ru = page.get_by_role("button", name="Выход")
#         self.logout_button_en = page.get_by_role("button", name="Logout")
    
#     def accept_cookies(self):
#         self.allow_cookies_button.click()
    
#     def click_get_started(self):
#         self.get_started_button.click()

            
#     def click_logout(self):
#         """Click the logout button (tries Russian first, then English)"""
#         try:
#             self.logout_button_ru.click(timeout=3000)
#         except:
#             self.logout_button_en.click(timeout=3000)
