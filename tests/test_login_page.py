import allure
from pages.login_page import LoginPage
from elements.login_page_elements import LoginPageElements


@allure.sub_suite("Тест страницы логина")
class TestLoginPage:
    @allure.title("Регистрация нового пользователя")
    def test_new_user_registration(self, driver, fake):
        page, element = LoginPage(driver), LoginPageElements()
        page.open()
        page.type_in_element(element.REGISTRATION_EMAIL, fake.email())
        page.type_in_element(element.REGISTRATION_PASSWORD_1, "parol12345")
        page.type_in_element(element.REGISTRATION_PASSWORD_2, "parol12345")
        page.click_on_element(element.REGISTRATION_BUTTON)
        page.check_element(element.USER_ICON)
