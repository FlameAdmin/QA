import allure

from pages.login_page import LoginPage
from fixtures.login_data import INVALID_USERS


@allure.epic("Authentication")
@allure.feature("Login")
@allure.story("Wrong Password")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("login")
def test_wrong_password(login_page):
    wrong_password_case = next(
        (user for user in INVALID_USERS if user["case"] == "Wrong password"), 
        None
    )
    
    if not wrong_password_case:
        raise ValueError("Wrong password test case not found in INVALID_USERS")
    
    with allure.step("Login using wrong password"):
        login_page.login(
            wrong_password_case["email"],
            wrong_password_case["password"]
        )

    with allure.step("Verify login failed with error message"):
        # This will now properly fail if error message is not shown
        login_page.verify_login_failed()
        
    with allure.step("Verify specific error message"):
        login_page.verify_error_message(wrong_password_case["error"])