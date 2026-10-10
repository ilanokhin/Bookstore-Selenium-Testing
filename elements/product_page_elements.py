from elements.base_page_elements import BasePageElements
from utils.universal_locator import locator


class ProductPageElements(BasePageElements):
    ADD_TO_BASKET_BUTTON = ("Добавить в корзину", locator(".btn-add-to-basket"))
    PRODUCT_NAME = ("Имя товара", locator("div.product_main h1"))
    PRODUCT_PRICE = ("Цена товара", locator("div.product_main p.price_color"))
    PRODUCT_ADDED_MESSAGE = ("Сообщение, что товар добавлен", locator(".alert:nth-child(1) strong"))
    BASKET_TOTAL_COST_MESSAGE = ("Сообщение об общей стоимости корзины", locator(".alert:nth-child(3) strong"))
    REVIEWS = ("Отзывы клиентов", locator("#reviews"))
