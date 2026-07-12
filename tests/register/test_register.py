import re
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.registration.otp_page import OTPPage
from pages.registration.name_page import NamePage
from pages.registration.password_setup_page import PasswordSetupPage
from pages.registration.gender_page import GenderPage
from pages.registration.profile_setup_page import ProfileSetupPage

def test_new_user_registration(page: Page) -> None:
    # Navigate and accept cookies
    home_page = HomePage(page)
    home_page.accept_cookies()
    home_page.click_get_started()
    
    # Step 1: Enter email (system will detect new user and send OTP)
    login_page = LoginPage(page)
    login_page.enter_email("hamid123a2008@gmail.com")
    login_page.click_next()
    
    # Step 2: Enter OTP
    otp_page = OTPPage(page)
    otp_page.enter_otp("572004")
    otp_page.click_next()
    
    # Step 3: Enter name
    name_page = NamePage(page)
    name_page.enter_name("Sara")
    name_page.click_next()
    
    # Step 4: Set password
    password_page = PasswordSetupPage(page)
    password_page.enter_password("1234")
    password_page.enter_confirm_password("1234")
    password_page.click_next()
    
    # Step 5: Select gender
    gender_page = GenderPage(page)
    gender_page.select_gender("B")  # Both
    gender_page.click_next()
    
    # Step 6: Setup profile
    profile_page = ProfileSetupPage(page)
    
    # Upload primary photo
    profile_page.upload_primary_photo("avatar-3.png")
    profile_page.click_save_photos()
    
    # Upload secondary photo
    profile_page.upload_secondary_photo("avatar-2.png")
    profile_page.click_save_photos()
    
    # Enter bio
    profile_page.enter_bio("Hello this is Sara")
    
    # Select values (positive traits)
    profile_page.select_values(["Optimism", "Compassion", "Authenticity"])
    
    # Select flaws (negative traits)
    profile_page.select_flaws(["Cowardice", "Grouchiness", "Intolerance"])
    
    # Save profile
    profile_page.save_profile()
    
    # Verify registration success
    page.wait_for_timeout(3000)
    expect(page).to_have_url(re.compile(r".*user/home.*"))
    
    # Logout
    home_page.click_logout()