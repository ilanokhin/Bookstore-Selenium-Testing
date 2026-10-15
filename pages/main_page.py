from selenium.webdriver.chrome.webdriver import WebDriver

from pages.base_page import BasePage


class MainPage(BasePage):
    def __init__(self, driver: WebDriver, url_path: str = "/"):
        super().__init__(driver)
        self.url = self.url + url_path

    def open(self, url: str = "", page_name: str = "главную страницу") -> None:
        super().open(url, page_name)
