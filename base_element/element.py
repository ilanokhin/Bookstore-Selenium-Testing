import re
import time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from typing import Any, Callable
from enums.wait_until import WaitUntil
from config import *


class Element:
    def __init__(self, driver: WebDriver, locator: tuple[str, str], timeout: float = TIMEOUT,
                 waiting: WaitUntil = WaitUntil.PRESENT):
        self.driver = driver
        self.locator = locator
        self.timeout = timeout
        self.waiting = waiting
        self._wait = WebDriverWait(self.driver, timeout)

    def __repr__(self) -> str:
        return f"\nЭлемент(локатор: '{self.locator[1]}', таймаут ожидания: {self.timeout} секунд)"

    def get_element(self) -> WebElement | None:
        start_time = time.time()

        while time.time() - start_time < self.timeout:
            try:
                element = self.driver.find_element(*self.locator)
            except NoSuchElementException:
                element = None

            if not element:
                time.sleep(0.1)
                continue

            if self.waiting == WaitUntil.PRESENT:
                return element
            elif self.waiting == WaitUntil.VISIBLE:
                if element.is_displayed():
                    return element
            elif self.waiting == WaitUntil.CLICKABLE:
                if element.is_displayed() and element.is_enabled():
                    return element

            time.sleep(0.1)

        return None

    def get_elements(self) -> list[WebElement]:
        start_time = time.time()

        while time.time() - start_time < self.timeout:
            elements = self.driver.find_elements(*self.locator)

            if not elements:
                time.sleep(0.1)
                continue

            if self.waiting == WaitUntil.PRESENT:
                return elements
            elif self.waiting == WaitUntil.VISIBLE:
                if all(element.is_displayed() for element in elements):
                    return elements
            elif self.waiting == WaitUntil.CLICKABLE:
                if all(element.is_displayed() and element.is_enabled() for element in elements):
                    return elements

            time.sleep(0.1)

        return []

    def _stale_handler(self, function: Callable) -> Any:
        start_time = time.time()

        while time.time() - start_time < self.timeout:
            try:
                return function()
            except (StaleElementReferenceException, WebDriverException):
                time.sleep(0.1)

        return None

    def is_present(self) -> bool:
        res = self._stale_handler(lambda: bool(self.get_element()))
        return res or False

    def is_clickable(self) -> bool:
        res = self._stale_handler(lambda: self.is_present() and self.get_element().is_enabled())
        return res or False

    def is_not_clickable(self) -> bool:
        res = self._stale_handler(lambda: self.is_present() and not self.get_element().is_enabled())
        return res or False

    def is_not_present(self) -> bool:
        res = self._stale_handler(lambda: bool(self.get_element()))
        return not bool(res)

    def type_text(self, text: str) -> None:
        self._stale_handler(lambda: self.get_element().send_keys(text))

    def click(self) -> None:
        self._stale_handler(lambda: self.get_element().click())

    def press(self, *keys_to_press: str | Keys) -> None:
        self._stale_handler(lambda: self.get_element().send_keys(*keys_to_press))

    def get_all_attributes(self) -> list[dict]:
        if self.locator[1].startswith("/"):
            script = f"""
                    const attributes_list = [];
                    const xpath_data = document.evaluate(`{self.locator[1]}`, document, null,
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
                    const elements = document.querySelectorAll(`{self.locator[1]}`);

                    if (elements.length === 0) return null;

                    for (element of elements) {{
                        const attributes = new Object();
                        attributes["text"] = element.innerText;

                        for (let attribute of element.attributes) attributes[attribute.name] = attribute.value;

                        attributes_list.push(attributes);
                    }}

                    return attributes_list;
                    """

        return self.driver.execute_script(script)

    def get_attribute(self, attribute: str = "text") -> str:
        start_time = time.time()

        while time.time() - start_time < self.timeout:
            try:
                if attribute == "text":
                    attribute_value = self.get_element().text
                else:
                    attribute_value = self.get_element().get_attribute(attribute)
                    attribute_value = attribute_value if attribute_value else ""
                    attribute_value = re.sub("<.*?>", "", attribute_value)

                return attribute_value

            except (StaleElementReferenceException, WebDriverException):
                time.sleep(0.1)

        return ""

    def get_attribute_via_js(self, attribute: str = "text") -> str:
        attributes_list = self.get_all_attributes()

        if attributes_list and attribute == "text":
            attribute_value = attributes_list[0].get("text", "")
        elif attribute != "text":
            attribute_value = attributes_list[0].get(attribute, "")
            attribute_value = re.sub("<.*?>", "", attribute_value)
        else:
            attribute_value = ""

        return attribute_value

    def get_attribute_list(self, attribute: str = "text") -> list:
        start_time = time.time()

        while time.time() - start_time < self.timeout:
            try:
                attribute_list = []
                elements = self.get_elements()

                for element in elements:
                    if attribute == "text":
                        attribute_value = element.text
                    else:
                        attribute_value = element.get_attribute(attribute)
                        attribute_value = attribute_value if attribute_value else ""
                        attribute_value = re.sub("<.*?>", "", attribute_value)

                    attribute_list.append(attribute_value)

                return attribute_list

            except (StaleElementReferenceException, WebDriverException):
                time.sleep(0.1)

        return []

    def get_attribute_list_via_js(self, attribute: str = "text") -> list:
        attributes_list = self.get_all_attributes()

        if attributes_list and attribute == "text":
            attribute_values = [element.get("text", "") for element in attributes_list]
        elif attribute != "text":
            attribute_values = []

            for element in attributes_list:
                attribute_value = element.get(attribute, "")
                attribute_value = re.sub("<.*?>", "", attribute_value)
                attribute_values.append(attribute_value)
        else:
            attribute_values = []

        return attribute_values

    def is_attribute_changed(self, attribute: str, old_value: str) -> bool:
        try:
            self._wait.until_not(ec.text_to_be_present_in_element_attribute(self.locator, attribute, old_value))
        except TimeoutException:
            return False

        return True

    def scroll_to(self) -> None:
        self._stale_handler(lambda: self.driver.execute_script("arguments[0].scrollIntoView();", self.get_element()))
