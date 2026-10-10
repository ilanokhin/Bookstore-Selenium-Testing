import allure
import pytest
from pages.product_page import ProductPage
from pages.basket_page import BasketPage
from pages.login_page import LoginPage
from elements.product_page_elements import ProductPageElements
from elements.basket_page_elements import BasketPageElements
from elements.login_page_elements import LoginPageElements


@allure.sub_suite("Пользователь добавляет товар в корзину")
class TestUserAddToBasketFromProductPage:
    @allure.title("Пользователь не видит сообщение о добавлении товара при переходе на его страницу")
    def test_user_cant_see_product_added_message(self, driver, new_user_registration):
        page, element = ProductPage(driver), ProductPageElements()
        page.open()
        page.should_be_product_page()
        page.check_element(element.PRODUCT_ADDED_MESSAGE, is_present=False)

    @allure.title("Пользователь может добавить товар в корзину")
    def test_user_can_add_product_to_basket(self, driver, new_user_registration):
        page, element = ProductPage(driver), ProductPageElements()
        page.open("https://selenium1py.pythonanywhere.com/ru/catalogue/coders-at-work_207/?promo=offer1")
        page.should_be_product_page()
        page.click_on_element_with_alert(element.ADD_TO_BASKET_BUTTON, function=page.solve_quiz)
        page.product_added_message_should_contain_product_name()
        page.basket_cost_message_should_contain_product_price()

@pytest.mark.parametrize("offer_number", (1, pytest.param(2, marks=pytest.mark.xfail), 3))
@allure.title("Гость может добавить товар в корзину")
def test_guest_can_add_product_to_basket(driver, offer_number):
    page, element = ProductPage(driver), ProductPageElements()
    page.open(f"https://selenium1py.pythonanywhere.com/ru/catalogue/coders-at-work_207/?promo=offer{offer_number}")
    page.should_be_product_page()
    page.click_on_element_with_alert(element.ADD_TO_BASKET_BUTTON, function=page.solve_quiz)
    page.product_added_message_should_contain_product_name()
    page.basket_cost_message_should_contain_product_price()


@allure.title("Гость должен видеть ссылку на логин на странице товара")
def test_guest_should_see_login_link_on_product_page(driver):
    page, element = ProductPage(driver), ProductPageElements()
    page.open()
    page.check_element(element.LOGIN_LINK)


@allure.title("Гость не видит сообщение о добавлении товара при переходе на его страницу")
def test_guest_cant_see_product_added_message(driver):
    page, element = ProductPage(driver), ProductPageElements()
    page.open()
    page.scroll_to_element(element.REVIEWS)
    page.should_be_product_page()
    page.check_element(element.PRODUCT_ADDED_MESSAGE, is_present=False)


@allure.title("Гость не видит товары в корзине, при переходе со страницы товара")
def test_guest_cant_see_product_in_basket_opened_from_product_page(driver):
    page, element = ProductPage(driver), ProductPageElements()
    page.open()
    page.click_on_element(element.BASKET_BUTTON)
    page, element = BasketPage(driver), BasketPageElements()
    page.check_element(element.BASKET_ITEMS, is_present=False)
    page.check_element(element.EMPTY_BASKET_TEXT)


@allure.title("Гость может перейти на страницу логина со страницы товара")
def test_guest_can_go_to_login_page_from_product_page(driver):
    page, element = ProductPage(driver), ProductPageElements()
    page.open()
    page.click_on_element(element.LOGIN_LINK)
    page, element = LoginPage(driver), LoginPageElements()
    page.should_be_login_page()
