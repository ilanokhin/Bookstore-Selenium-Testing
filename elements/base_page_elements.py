from utils.universal_locator import locator


class BasePageElements:
    LOGIN_LINK = ("Войти или зарегистрироваться", locator("#login_link"))
    BASKET_BUTTON = ("Корзина", locator("//div[contains(@class, 'basket-mini')]//a[contains(@href, 'basket')]"))
    USER_ICON = ("Иконка пользователя", locator(".icon-user"))
    LOGOUT_LINK = ("Выход из аккаунта", locator("#logout_link"))
