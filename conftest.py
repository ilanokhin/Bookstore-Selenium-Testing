import pytest
import allure
from faker import Faker
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from tests.test_login_page import TestLoginPage


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--firefox", action="store_true", default=False, help="Использовать браузер Mozilla Firefox")
    parser.addoption("--headless", action="store_true", default=False, help="Запуск в фоновом режиме")
    parser.addoption("--disable-images", action="store_true", default=False, help="Отключить картинки")
    parser.addoption("--screenshot-every-time", action="store_true", default=False, help="Делать частые скриншоты")
    parser.addoption("--wait-for-load", action="store_true", default=False, help="Дожидаться загрузки ресурсов")


@pytest.fixture
def driver(request: pytest.FixtureRequest):
    firefox = request.config.getoption("--firefox")
    headless = request.config.getoption("--headless")
    images = not request.config.getoption("--disable-images")
    screenshots = request.config.getoption("--screenshot-every-time")
    wait = request.config.getoption("--wait-for-load")

    browser_name = "Mozilla Firefox" if firefox else "Google Chrome"
    options = FirefoxOptions() if firefox else ChromeOptions()

    if wait:
        options.page_load_strategy = "normal"
    else:
        options.page_load_strategy = "eager"

    if not firefox:
        options.add_argument("--disable-blink-features=AutomationControlled")

    if headless and not firefox:
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
    elif headless and firefox:
        options.add_argument("--headless")

    if not images:
        options.add_argument("--blink-settings=imagesEnabled=false")

    print(f"\nЗапускается браузер {browser_name}...")
    driver = webdriver.Firefox(options=options) if firefox else webdriver.Chrome(options=options)

    if not headless:
        driver.set_window_size(1500, 1000)

    if screenshots:
        driver.config = {"screenshot_every_time": True}
    else:
        driver.config = {"screenshot_every_time": False}

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
