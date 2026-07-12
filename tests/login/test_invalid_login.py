import allure

from pages.login_page import LoginPage


@allure.epic("Authentication")
@allure.feature("Login")
@allure.story("Wrong Password")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("login")
def test_wrong_password(login_page):

    with allure.step("Login using wrong password"):
        login_page.login(
            "kagameacu@gmail.com",
            "wrong123"
        )

    with allure.step("Verify login failed"):
        login_page.verify_login_failed()