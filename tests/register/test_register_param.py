import pytest
import re
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.registration.otp_page import OTPPage
from pages.registration.name_page import NamePage
from pages.registration.password_setup_page import PasswordSetupPage
from pages.registration.gender_page import GenderPage
from pages.registration.profile_setup_page import ProfileSetupPage

@pytest.mark.parametrize("user_data", [
    {
        "email": "hamid123a2008@gmail.com",
        "otp": "572004",
        "name": "Sara",
        "password": "1234",
        "gender": "B",
        "bio": "Hello this is Sara",
        "values": ["Optimism", "Compassion", "Authenticity"],
        "flaws": ["Cowardice", "Grouchiness", "Intolerance"],
        "primary_photo": "avatar-3.png",
        "secondary_photo": "avatar-2.png"
    },
    # Add more test users here
])
def test_new_user_registration_param(page: Page, user_data) -> None:
    # Navigate and accept cookies
    home_page = HomePage(page)
    home_page.accept_cookies()
    home_page.click_get_started()
    
    # Step 1: Enter email
    login_page = LoginPage(page)
    login_page.enter_email(user_data["email"])
    login_page.click_next()
    
    # Step 2: Enter OTP
    otp_page = OTPPage(page)
    otp_page.enter_otp(user_data["otp"])
    otp_page.click_next()
    
    # Step 3: Enter name
    name_page = NamePage(page)
    name_page.enter_name(user_data["name"])
    name_page.click_next()
    
    # Step 4: Set password
    password_page = PasswordSetupPage(page)
    password_page.enter_password(user_data["password"])
    password_page.enter_confirm_password(user_data["password"])
    password_page.click_next()
    
    # Step 5: Select gender
    gender_page = GenderPage(page)
    gender_page.select_gender(user_data["gender"])
    gender_page.click_next()
    
    # Step 6: Setup profile
    profile_page = ProfileSetupPage(page)
    
    # Upload photos
    profile_page.upload_primary_photo(user_data["primary_photo"])
    profile_page.click_save_photos()
    profile_page.upload_secondary_photo(user_data["secondary_photo"])
    profile_page.click_save_photos()
    
    # Enter bio and select values
    profile_page.enter_bio(user_data["bio"])
    profile_page.select_values(user_data["values"])
    profile_page.select_flaws(user_data["flaws"])
    profile_page.save_profile()
    
    # Verify registration success
    page.wait_for_timeout(3000)
    expect(page).to_have_url(re.compile(r".*user/home.*"))
    
    # Logout
    home_page.click_logout()