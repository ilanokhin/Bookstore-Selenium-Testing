from elements.base_page_elements import BasePageElements
from utils.universal_locator import locator


class LoginPageElements(BasePageElements):
    LOGIN_FORM = ("Форма логина", locator("#login_form"))
    REGISTRATION_FORM = ("Форма регистрации", locator("#register_form"))
    REGISTRATION_EMAIL = ("E-mail для регистрации", locator("input[name='registration-email']"))
    REGISTRATION_PASSWORD_1 = ("Пароль для регистрации", locator("input[name='registration-password1']"))
    REGISTRATION_PASSWORD_2 = ("Подтверждение пароля для регистрации", locator("input[name='registration-password2']"))
    REGISTRATION_BUTTON = ("Зарегистрироваться", locator("button[name='registration_submit']"))
