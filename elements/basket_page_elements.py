from elements.base_page_elements import BasePageElements
from utils.universal_locator import locator


class BasketPageElements(BasePageElements):
    BASKET_ITEMS = ("Товары в корзине", locator(".basket-items"))
    EMPTY_BASKET_TEXT = ("Ваша корзина пуста", locator("#content_inner>p"))
