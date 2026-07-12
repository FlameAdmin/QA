import allure

from fixtures.login_data import VALID_USER


@allure.epic("Authentication")
@allure.feature("Login")
@allure.story("Valid Login")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "login")
def test_valid_login(login_page):

    with allure.step("Login with valid credentials"):
        login_page.login(
            VALID_USER["email"],
            VALID_USER["password"]
        )

    with allure.step("Verify successful login"):
        login_page.verify_login_success()