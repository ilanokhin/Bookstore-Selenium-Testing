import allure
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoAlertPresentException
from typing import Any, Callable
from base_element.element import Element
from config import *


class BasePage:
    def __init__(self, driver: WebDriver, url: str = BASE_URL):
        self.driver = driver
        self.url = url
        self.config = self.driver.__dict__.get("config", {})
        self.screenshot_every_time = self.config.get("screenshot_every_time", False)

    def open(self, url: str = "", page_name: str = "") -> None:
        if url:
            link = url
            allure_step = f"Перейти по адресу {link}"
        elif page_name:
            link = self.url
            allure_step = f"Перейти на {page_name} ---> {link}"
        else:
            link = self.url
            allure_step = f"Перейти по адресу {link}"

        with allure.step(allure_step):
            self.driver.get(link)

    def screenshot(self, screenshot_path: str = "") -> bytes:
        if screenshot_path:
            self.driver.save_screenshot(screenshot_path)

        return self.driver.get_screenshot_as_png()

    def use_javascript(self, script: str, *args) -> Any:
        self.driver.execute_script(script, *args)

    def allure_screenshot(self, condition: bool = True, name: str = "Скриншот") -> None:
        if condition:
            allure.attach(self.screenshot(), attachment_type=allure.attachment_type.PNG, name=name)

    @staticmethod
    def allure_txt(data: str, name: str) -> None:
        allure.attach(data, attachment_type=allure.attachment_type.TEXT, name=name)

    def check_element(self, element_data: tuple, is_present: bool = True, is_clickable: bool | None = True,
                      timeout: float = TIMEOUT, forbid_screenshot: bool = False) -> Element:
        element = Element(self.driver, element_data[1], timeout)
        allure_step = "Проверить "
        assert_error = f"Элемент '{element_data[0]}' "

        if not is_present:
            allure_step += "отсутствие"
            result = element.is_not_present()
            assert_error += "присутствует"
        elif is_present and is_clickable is False:
            allure_step += "некликабельность"
            result = element.is_not_clickable()
            assert_error += "кликабельный"
        elif is_present and is_clickable is None:
            allure_step += "наличие"
            result = element.is_present()
            assert_error += "отсутствует"
        else:
            allure_step += "наличие"
            result = element.is_clickable()
            assert_error += "некликабельный или отсутствует"

        allure_step += f" элемента '{element_data[0]}'"

        with allure.step(allure_step):
            self.allure_screenshot(self.screenshot_every_time and not forbid_screenshot)

            try:
                assert result, assert_error
            except AssertionError as error:
                self.allure_screenshot(not self.screenshot_every_time and not forbid_screenshot)
                raise AssertionError(error)

        return element

    def type_in_element(self, element_data: tuple, text: str, forbid_screenshot: bool = False) -> None:
        element = self.check_element(element_data, forbid_screenshot=forbid_screenshot)
        with allure.step(f"Ввести текст '{text}' в элемент '{element_data[0]}'"):
            element.type_text(text)

    def click_on_element(self, element_data: tuple, forbid_screenshot: bool = False) -> None:
        element = self.check_element(element_data, forbid_screenshot=forbid_screenshot)
        with allure.step(f"Кликнуть по элементу '{element_data[0]}'"):
            element.click()

    def press_keys(self, element_data: tuple, keys_name: str, *keys: Keys | str,
                   forbid_screenshot: bool = False) -> None:
        element = self.check_element(element_data, forbid_screenshot=forbid_screenshot)
        with allure.step(f"Нажать {keys_name} на элементе '{element_data[0]}'"):
            element.press(*keys)

    def get_elements_attribute_list(self, element_data: tuple, attribute: str = "text", start_index: int = 0,
                                    end_index: int | None = None, forbid_screenshot: bool = False) -> list:
        element = self.check_element(element_data, forbid_screenshot=forbid_screenshot)

        attribute_list = element.get_attribute_list(attribute)
        finish_index = len(attribute_list) if end_index is None else end_index
        attribute_list = [value for i, value in enumerate(attribute_list) if start_index <= i < finish_index]

        return attribute_list

    def get_element_attribute(self, element_data: tuple, attribute: str = "text", autocheck: bool = True,
                              forbid_screenshot: bool = False) -> str:
        if autocheck:
            element = self.check_element(element_data, forbid_screenshot=forbid_screenshot)
        else:
            element = Element(self.driver, element_data[1])

        return element.get_attribute(attribute)

    def get_element_text(self, element_data: tuple, autocheck: bool = True, forbid_screenshot: bool = False) -> str:
        return self.get_element_attribute(element_data, autocheck=autocheck, forbid_screenshot=forbid_screenshot)

    def compare_elements(self, element1_data: tuple, element2_data: tuple, attribute_to_compare: str = "text",
                         element2_old_value: str = "", element2_name: str = "",
                         forbid_screenshot: bool = False) -> None:
        element1 = self.get_element_attribute(element1_data, attribute_to_compare)

        if element2_old_value and element2_name:
            element2 = element2_old_value
            second_name = element2_name
        else:
            element2 = self.get_element_attribute(element2_data, attribute_to_compare)
            second_name = element2_data[0]

        with allure.step(f"Проверить соответствие элементов '{element1_data[0]}' и '{second_name}'"):
            self.allure_screenshot(self.screenshot_every_time and not forbid_screenshot)

            try:
                assert element1 == element2, f"Элементы '{element1_data[0]}' и '{second_name}' не соответствуют"
            except AssertionError as error:
                self.allure_screenshot(not self.screenshot_every_time and not forbid_screenshot)
                raise AssertionError(error)

    def should_be_element_changed(self, element_data: tuple, old_attribute_value: str, attribute: str = "text",
                                  forbid_screenshot: bool = False) -> None:
        element = self.check_element(element_data, forbid_screenshot=forbid_screenshot)
        result = element.is_attribute_changed(attribute, old_attribute_value)

        with allure.step(f"Проверить, что элемент '{element_data[0]}' изменился"):
            self.allure_screenshot(self.screenshot_every_time and not forbid_screenshot)

            try:
                assert result, f"Элемент '{element_data[0]}' не изменился"
            except AssertionError as error:
                self.allure_screenshot(not self.screenshot_every_time and not forbid_screenshot)
                raise AssertionError(error)

    def scroll_to_element(self, element_data: tuple, autocheck: bool = False, forbid_screenshot: bool = False) -> None:
        if autocheck:
            element = self.check_element(element_data, forbid_screenshot=forbid_screenshot)
        else:
            element = Element(self.driver, element_data[1])

        element.scroll_to()

    def scroll_by_distance(self, xdistance: int, ydistance: int) -> None:
        self.use_javascript(f"window.scrollBy({xdistance}, {ydistance});")

    def scroll_to_top(self) -> None:
        self.use_javascript("window.scrollTo(0, 0);")

    def scroll_to_bottom(self) -> None:
        self.use_javascript("window.scrollTo(0, document.body.scrollHeight);")

    def get_url(self) -> str:
        return self.driver.current_url

    def check_in_url(self, included_text: str) -> None:
        with allure.step(f"Проверить наличие '{included_text}' в URL страницы"):
            self.allure_txt(self.get_url(), "URL страницы")
            assert included_text in self.get_url(), f"Текущий URL не содержит '{included_text}'"

    def click_on_element_with_alert(self, element_data: tuple, text_to_send: str = "", confirm: bool = True,
                                    function: Callable = None, forbid_screenshot: bool = False) -> str:
        element = self.check_element(element_data, forbid_screenshot=forbid_screenshot)

        with allure.step(f"Кликнуть по элементу '{element_data[0]}'"):
            element.click()

            try:
                alert = self.driver.switch_to.alert
                message = alert.text

                if function:
                    text = function(message)
                else:
                    text = text_to_send

                if confirm and text:
                    alert.send_keys(text)
                    alert.accept()
                elif confirm and not text:
                    alert.accept()
                else:
                    alert.dismiss()

                return message
            except NoAlertPresentException:
                raise AssertionError("Алёрт отсутствует")
