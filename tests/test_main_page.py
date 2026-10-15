import allure

from elements.basket_page_elements import BasketPageElements
from elements.login_page_elements import LoginPageElements
from elements.main_page_elements import MainPageElements
from pages.basket_page import BasketPage
from pages.login_page import LoginPage
from pages.main_page import MainPage


@allure.sub_suite("Логин с главной страницы")
class TestLoginFromMainPage:
    @allure.title("Гость может перейти на страницу логина")
    def test_guest_can_go_to_login_page(self, driver):
        page, element = MainPage(driver), MainPageElements()
        page.open()
        page.click_on_element(element.LOGIN_LINK)
        page, element = LoginPage(driver), LoginPageElements()
        page.should_be_login_page()

    @allure.title("Гость должен видеть ссылку на логин")
    def test_guest_should_see_login_link(self, driver):
        page, element = MainPage(driver), MainPageElements()
        page.open()
        page.check_element(element.LOGIN_LINK)


@allure.title("Гость, перейдя с главной страницы в корзину, не должен видеть там товары")
def test_guest_should_not_see_products_in_basket_opened_from_main_page(driver):
    page, element = MainPage(driver), MainPageElements()
    page.open()
    page.click_on_element(element.BASKET_BUTTON)
    page, element = BasketPage(driver), BasketPageElements()
    page.check_element(element.BASKET_ITEMS, is_present=False)
    page.check_element(element.EMPTY_BASKET_TEXT)
