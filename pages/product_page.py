import allure
import math
from selenium.webdriver.chrome.webdriver import WebDriver
from pages.base_page import BasePage
from elements.product_page_elements import ProductPageElements


class ProductPage(BasePage):
    def __init__(self, driver: WebDriver, url_path: str = "/catalogue/expert-c-programming_179/"):
        super().__init__(driver)
        self.url = self.url + url_path

    def open(self, url: str = "", page_name: str = "cтраницу товара") -> None:
        super().open(url, page_name)

    @allure.step("Должна открыться страница товара")
    def should_be_product_page(self) -> None:
        self.check_element(ProductPageElements.ADD_TO_BASKET_BUTTON)
        self.check_element(ProductPageElements.PRODUCT_NAME)
        self.check_element(ProductPageElements.PRODUCT_PRICE)

    @allure.step("Решить задачу в алёрте")
    def solve_quiz(self, alert_message: str):
        x = alert_message.split(" ")[2]
        return str(math.log(abs((12 * math.sin(float(x))))))

    def product_added_message_should_contain_product_name(self):
        product_name = self.get_element_text(ProductPageElements.PRODUCT_NAME)
        product_added_message = self.get_element_text(ProductPageElements.PRODUCT_ADDED_MESSAGE)

        with allure.step("Имя товара должно быть в сообщении о его добавлении"):
            try:
                assert product_name in product_added_message, "Имя товара отсутствует в сообщении о его добавлении"
            except AssertionError as error:
                self.allure_screenshot()
                raise AssertionError(error)

    def basket_cost_message_should_contain_product_price(self):
        product_price = self.get_element_text(ProductPageElements.PRODUCT_PRICE)
        basket_cost_message = self.get_element_text(ProductPageElements.BASKET_TOTAL_COST_MESSAGE)

        with allure.step("Сообщение о стоимости корзины должно содержать цену товара"):
            assert product_price in basket_cost_message, "Сообщение о стоимости корзины не содержит цену товара"
