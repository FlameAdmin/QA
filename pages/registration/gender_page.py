from playwright.sync_api import Page

class GenderPage:
    def __init__(self, page: Page):
        self.page = page
        self.male_radio = page.get_by_role("radio", name="M")
        self.female_radio = page.get_by_role("radio", name="F")
        self.both_radio = page.get_by_role("radio", name="B")
        self.next_button = page.get_by_role("button", name="Next")
    
    def select_gender(self, gender: str):
        """Select gender: 'M', 'F', or 'B'"""
        if gender.upper() == "M":
            self.male_radio.check()
        elif gender.upper() == "F":
            self.female_radio.check()
        elif gender.upper() == "B":
            self.both_radio.check()
    
    def click_next(self):
        self.next_button.click()