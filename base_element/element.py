import re
import time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from enums.wait_until import WaitUntil
from config import *


class Element:
    def __init__(self, driver: WebDriver, locator: tuple[str, str], timeout: float = TIMEOUT,
                 wait: WaitUntil = WaitUntil.PRESENT):
        self.driver = driver
        self.locator = locator
        self._wait = WebDriverWait(self.driver, timeout)
        self._elements = Element.find_elements(driver, locator, timeout, wait)
        self.attributes = Element.get_all_atributes(driver, locator[1])
        self._size = len(self._elements)

    @staticmethod
    def find_elements(driver: WebDriver, locator: tuple[str, str], timeout: float, wait: WaitUntil) -> list:
        start_time = time.time()

        while time.time() - start_time < timeout:
            elements = driver.find_elements(*locator)

            if not elements:
                time.sleep(0.1)
                continue

            if wait == WaitUntil.PRESENT:
                return elements

            elif wait == WaitUntil.VISIBLE:
                visible = [element for element in elements if element.is_displayed()]

                if visible:
                    return visible

            elif wait == WaitUntil.CLICKABLE:
                clickable = [element for element in elements if element.is_displayed() and element.is_enabled()]

                if clickable:
                    return clickable

            time.sleep(0.1)

        return []

    @staticmethod
    def get_all_atributes(driver: WebDriver, css_or_xpath_locator: str) -> list[dict]:
        attributes_list = []

        if css_or_xpath_locator.startswith("/"):
            script = f"""
                const attributes_list = [];
                const xpath_data = document.evaluate(`{css_or_xpath_locator}`, document, null,
                    XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);

                if (xpath_data.snapshotLength === 0) return null;

                for (let i = 0; i < xpath_data.snapshotLength; i++) {{
                    const attributes = new Object();
                    let element = xpath_data.snapshotItem(i);
                    attributes["text"] = element.innerText;

                    for (let attribute of element.attributes) attributes[attribute.name] = attribute.value;

                    attributes_list.push(attributes);
                }}

                return attributes_list;
            """
        else:
            script = f"""
                const attributes_list = [];
                const elements = document.querySelectorAll(`{css_or_xpath_locator}`);

                if (elements.length === 0) return null;

                for (element of elements) {{
                    const attributes = new Object();
                    attributes["text"] = element.innerText;

                    for (let attribute of element.attributes) attributes[attribute.name] = attribute.value;

                    attributes_list.push(attributes);
                }}

                return attributes_list;
                """

        attributes_list = driver.execute_script(script)

        return attributes_list

    def __repr__(self) -> str:
        return f"\nЭлемент(локатор: '{self.locator[1]}', количество: {self._size})"

    def __len__(self) -> int:
        return self._size

    def get_selenium_element(self, element_index: int = 0) -> WebElement:
        return self._elements[element_index]

    def is_present(self) -> bool:
        return bool(self._elements)

    def is_clickable(self) -> bool:
        return self.is_present() and self._elements[0].is_enabled()

    def is_not_clickable(self) -> bool:
        return self.is_present() and not self._elements[0].is_enabled()

    def is_not_present(self) -> bool:
        return not self._elements

    def type_text(self, text: str) -> None:
        self._elements[0].send_keys(text)

    def click(self) -> None:
        self._elements[0].click()

    def press(self, *keys_to_press: str | Keys) -> None:
        self._elements[0].send_keys(*keys_to_press)

    def get_attribute(self, attribute: str = "text", element_index: int = 0) -> str:
        if attribute == "text":
            attribute_value = self.attributes[element_index].get("text", "")
        else:
            attribute_value = self.attributes[element_index].get(attribute, "")
            attribute_value = re.sub("<.*?>", "", attribute_value)

        return attribute_value

    def get_attribute_list(self, attribute: str = "text") -> list:
        attribute_values = []

        for i in range(0, len(self.attributes)):
            attribute_values.append(self.get_attribute(attribute, i))

        return attribute_values

    def is_attribute_changed(self, attribute: str, old_value: str) -> bool:
        try:
            self._wait.until_not(ec.text_to_be_present_in_element_attribute(self.locator, attribute, old_value))
        except TimeoutException:
            return False

        return True

    def scroll_to(self) -> None:
        self.driver.execute_script("arguments[0].scrollIntoView();", self._elements[0])
