    # import re
    # from playwright.sync_api import Page

    # class ProfileSetupPage:
    #     def __init__(self, page: Page):
    #         self.page = page
    #         self.upload_area = page.locator("div").filter(has_text=re.compile(r"^Click to upload$")).nth(2)
    #         self.additional_images_input = page.locator("#additionalImages")
    #         self.save_button = page.locator("#simple-tabpanel-0").get_by_role("button", name="Save")
    #         self.label = page.locator("label").first
    #         self.image1_input = page.locator("#image1")
    #         self.bio_textarea = page.get_by_role("textbox", name="Write your information here")
    #         self.combobox = page.get_by_role("combobox").nth(1)
    #         self.select_element = page.locator("select")
    #         self.save_profile_button = page.get_by_role("button", name="Save")
        
    #     def upload_primary_photo(self, photo_path: str):
    #         self.upload_area.click()
    #         self.additional_images_input.set_input_files(photo_path)
    #         self.page.locator("body").press("Enter")
        
    #     def upload_secondary_photo(self, photo_path: str):
    #         self.label.click()
    #         self.image1_input.set_input_files(photo_path)
        
    #     def click_save_photos(self):
    #         self.save_button.click()
        
    #     def enter_bio(self, bio: str):
    #         self.bio_textarea.fill(bio)
        
    #     def select_values(self, values: list):
    #         """Select multiple values from the combobox"""
    #         for value in values:
    #             self.combobox.select_option(value)
        
    #     def select_flaws(self, flaws: list):
    #         """Select multiple flaws from the select element"""
    #         for flaw in flaws:
    #             self.select_element.select_option(flaw)
        
    #     def save_profile(self):
    #         self.save_profile_button.click()




# profile_setup_page with allure
import re
from playwright.sync_api import Page

class ProfileSetupPage:
    def __init__(self, page: Page):
        self.page = page
        self.upload_area = page.locator("div").filter(has_text=re.compile(r"^Click to upload$")).nth(2)
        self.additional_images_input = page.locator("#additionalImages")
        self.save_button = page.locator("#simple-tabpanel-0").get_by_role("button", name="Save")
        self.label = page.locator("label").first
        self.image1_input = page.locator("#image1")
        self.bio_textarea = page.get_by_role("textbox", name="Write your information here")
        self.combobox = page.get_by_role("combobox").nth(1)
        self.select_element = page.locator("select")
        self.save_profile_button = page.get_by_role("button", name="Save")
    
    def upload_primary_photo(self, photo_path: str):
        self.upload_area.click()
        self.additional_images_input.set_input_files(photo_path)
        self.page.locator("body").press("Enter")
    
    def upload_secondary_photo(self, photo_path: str):
        self.label.click()
        self.image1_input.set_input_files(photo_path)
    
    def click_save_photos(self):
        self.save_button.click()
    
    def enter_bio(self, bio: str):
        self.bio_textarea.fill(bio)
    
    def select_values(self, values: list):
        """Select multiple values from the combobox"""
        for value in values:
            self.combobox.select_option(value)
    
    def select_flaws(self, flaws: list):
        """Select multiple flaws from the select element"""
        for flaw in flaws:
            self.select_element.select_option(flaw)
    
    def save_profile(self):
        self.save_profile_button.click()