from selenium.webdriver.chrome.webdriver import WebDriver

from pages.base_page import BasePage


class BasketPage(BasePage):
    def __init__(self, driver: WebDriver, url_path: str = "/basket/"):
        super().__init__(driver)
        self.url = self.url + url_path

    def open(self, url: str = "", page_name: str = "cтраницу корзины") -> None:
        super().open(url, page_name)
