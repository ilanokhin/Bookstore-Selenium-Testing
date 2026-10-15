import allure
from selenium.webdriver.chrome.webdriver import WebDriver

from elements.login_page_elements import LoginPageElements
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, driver: WebDriver, url_path: str = "/accounts/login/"):
        super().__init__(driver)
        self.url = self.url + url_path

    def open(self, url: str = "", page_name: str = "страницу логина") -> None:
        super().open(url, page_name)

    @allure.step("Должна открыться страница логина")
    def should_be_login_page(self) -> None:
        self.check_in_url("/accounts/login")
        self.check_element(LoginPageElements.LOGIN_FORM)
        self.check_element(LoginPageElements.REGISTRATION_FORM)
