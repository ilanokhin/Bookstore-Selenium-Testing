import pytest
import allure
from faker import Faker
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from tests.test_login_page import TestLoginPage


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--browser", action="store", default="chrome", help="Используемый браузер: chrome*, firefox")
    parser.addoption("--headless", action="store", default="false", help="Запуск в фоновом режиме: true, false*")
    parser.addoption("--images", action="store", default="true", help="Включение/отключение картинок: true*, false")


@pytest.fixture
def driver(request: pytest.FixtureRequest):
    browser = request.config.getoption("--browser")
    browser_name = "Mozilla Firefox" if browser == "firefox" else "Google Chrome"

    options = FirefoxOptions() if browser == "firefox" else ChromeOptions()
    options.add_argument("--no-sandbox")

    if browser != "firefox":
        options.add_argument("--disable-blink-features=AutomationControlled")

    if request.config.getoption("--headless") == "true":
        options.add_argument("--headless")
    if request.config.getoption("--images") == "false":
        options.add_argument("--blink-settings=imagesEnabled=false")

    print(f"\nЗапускается браузер {browser_name}...")
    driver = webdriver.Firefox(options=options) if browser == "firefox" else webdriver.Chrome(options=options)
    driver.set_window_size(1500, 1000)
    print("\nПроводятся тесты...")

    yield driver
    print(f"\nБраузер {browser_name} закрывается...")
    driver.quit()


@pytest.fixture
def fake():
    return Faker()


@pytest.fixture
@allure.title("Регистрация нового пользователя")
def new_user_registration(driver, fake):
    test_suite = TestLoginPage()
    test_suite.test_new_user_registration(driver, fake)
