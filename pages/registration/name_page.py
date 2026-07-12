from playwright.sync_api import Page

class NamePage:
    def __init__(self, page: Page):
        self.page = page
        self.name_input = page.get_by_role("textbox", name="Enter your name")
        self.next_button = page.get_by_role("button", name="Next")
    
    def enter_name(self, name: str):
        self.name_input.fill(name)
    
    def click_next(self):
        self.next_button.click()