import logging
import platform
import re
import time
import typing as t
from contextlib import suppress

from selenium.common.exceptions import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from core.decorators import log_exception
from definitions import long_timeout, short_timeout
from utils.common import timeout


class BaseClass:
    """
    Base class representation.
    Contains all actions related to UI interaction.
    All pages will be inherited from this class.
    """

    def __init__(self, driver: t.no_type_check) -> None:
        """
        :param browser: selenium.webdriver.*
        """
        self.driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)

    @staticmethod
    def sleep(s: t.Union[float, int]) -> None:
        time.sleep(s)

    @log_exception("Failed open URL: {}")
    def open(self, url: str, confidential: bool = False) -> None:
        """
        Open given URL in browser
        :param url: str - URL to open
        :param confidential: bool - whether log url part with possible credentials https://<login>:<pass>@url  ->  https://***url
        """
        self.driver.get(url)
        self.logger.info("Opened URL: %s", re.sub(r"://(.+@)", "://***", url) if confidential else url)

    @log_exception("Failed to get element by xpath: {}. Timeout: {wait}s")
    def _get_element(self, element: t.Union[str, WebElement], ec: ec = ec.presence_of_element_located, wait: int = short_timeout) -> WebElement:
        """Function for getting WebElement from given xpath.

        Args:
            element (Union[str, WebElement]): web element xpath or can be selenium.webdriver.remote.webelement.WebElement
            ec (ec, optional): selenium expected condition. Defaults to ec.presence_of_element_located.
            wait (int, optional): element max wait time. Defaults to short_timeout.

        Returns:
            WebElement: single webelement
        """
        if isinstance(element, str):
            self.logger.debug("Trying to find element by locator: %s", element)

            wait = WebDriverWait(self.driver, wait)
            element = wait.until(
                ec((By.XPATH, element)),
                message=f"Failed to get element by xpath: {element}",
            )

            self.logger.info("Got element with locator: %s", element)

        return element

    @log_exception("Failed to get elements by xpath: {}. Timeout: {wait}s")
    def get_elements(self, xpath: str, wait: int = short_timeout) -> t.List[WebElement]:
        """Function for getting multiple elements by xpath.

        Args:
            locator (str): web element xpath.
            wait (int): wait time for object. Defaults to short_timeout.

        Returns:
            List[WebElement]: list of selenium WebElements
        """
        self.logger.debug("Trying to find elements by locator: %s", xpath)
        return WebDriverWait(self.driver, wait).until(
            ec.presence_of_all_elements_located((By.XPATH, xpath)),
            message=f"Failed to get elements by xpath: {xpath}",
        )

    def _get_attribute(self, attribute: str, element: t.Union[str, WebElement], ec: ec = ec.presence_of_element_located, wait: int = short_timeout) -> str:
        return self._get_element(element=element, ec=ec, wait=wait).get_attribute(attribute)

    @log_exception("Failed to count elements by xpath: {}. Timeout: {wait}s")
    def get_elements_count(self, xpath: str, wait: int = short_timeout) -> int:
        try:
            return len(self.get_elements(xpath, wait))
        except TimeoutException:
            return 0

    @log_exception("Failed to execute script: {script}")
    def execute_script(self, element: t.Union[str, WebElement], script: str) -> str:
        """
        Execute JavaScript on the web element
        :param element: selenium.webdriver.remote.webelement.WebElement
        :param script: str - JS script body
        :return: result of script execution
        """
        return self.driver.execute_script(f"return arguments[0].{script}", self._get_element(element))

    def scroll_to_element(self, element: t.Union[str, WebElement]) -> None:
        """
        Function for scroll to element.
        :param element: str - web element xpath or can be selenium.webdriver.remote.webelement.WebElement
        """
        self.execute_script(self._get_element(element), "scrollIntoView(true);")

    @log_exception("Failed to click web element with xpath: {}")
    def click(self, xpath: str, wait: int = short_timeout, scroll: bool = True) -> None:
        """
        Click web element with given xpath
        :param xpath: str - web element xpath
        :param wait: int - wait time for object
        """
        self.logger.debug("Clicking web element with xpath: %s", xpath)
        if scroll:
            self.scroll_to_element(xpath)
        self._get_element(xpath, ec.element_to_be_clickable, wait=wait).click()
        self.logger.info("Clicked web element with xpath: %s", xpath)

    @log_exception("Failed presence check of web element with xpath: {}. Timeout: {wait}s")
    def is_present(self, xpath: str, expected: bool = True, wait: int = short_timeout) -> bool:
        """
        Presence check of web element on the UI.
        :param xpath: str - web element xpath
        :param wait: int - wait time for object
        :param expected: boolean - expected to find it
        :return: boolean - element presence
        """
        found = False
        expected_condition = ec.presence_of_element_located
        if not expected:
            expected_condition = ec.staleness_of

        self.logger.info("Checking presence of web element with xpath: %s. Expected: %s", xpath, expected)
        found = self._get_element(xpath, expected_condition, wait=wait) is not None
        self.logger.info("Presence check of web element with xpath: {xpath}. Result: {found}")
        return found

    @log_exception("Failed visible check of web element with xpath: {}. Timeout: {wait}s")
    def is_visible(self, xpath: str, wait: int = short_timeout) -> bool:
        """
        Visibility check of web element on the UI.
        :param xpath: str - web element xpath
        :param wait: int - wait time for object
        :return: boolean - element visibility
        """
        self.logger.debug("Checking visibility of web element with xpath: %s", xpath)
        result = False
        with suppress(Exception):
            result = self._get_element(xpath, ec=ec.visibility_of_element_located, wait=wait).is_displayed()
        self.logger.info("Visible check of web element with xpath: %s. Result: %s", xpath, result)
        return result

    @log_exception("Failed to mouse over web element with xpath: {}")
    def mouse_over(self, xpath: str, wait: int = short_timeout) -> None:
        """
        Simulate mouse cursor over given web element.
        :param xpath: str - web element xpath
        :param wait: int - wait time for object
        """
        actions = ActionChains(self.driver)
        actions.move_to_element(self._get_element(xpath, wait=wait)).perform()
        self.logger.info("Mouse over web element with xpath: %s", xpath)

    @log_exception("Failed to mouse over web element with xpath: {}")
    def mouse_over_with_offset(
        self,
        xpath: str,
        xoffset: t.Union[int, str],
        yoffset: t.Union[int, str],
        wait: int = short_timeout,
    ) -> None:
        """
        Simulate mouse cursor over given web element.
        :param xpath: str - web element xpath
        :param wait: int - wait time for object
        """
        actions = ActionChains(self.driver)
        actions.move_to_element_with_offset(self._get_element(xpath, wait=wait), xoffset, yoffset).perform()
        self.logger.info("Mouse over web element with xpath: %s", xpath)

    @log_exception("Failed to move mouse to coordinates: {}, {}")
    def mouse_move_to_coordinates(self, x: t.Union[int, str], y: t.Union[int, str]) -> None:
        """
        Simulate mouse cursor move.
        :param x, y: int
        """
        ActionChains(self.driver).move_by_offset(x, y).perform()
        self.logger.info("Mouse move for: %s, %s", x, y)

    @log_exception("Failed to drag mouse")
    def mouse_drag(
        self,
        x1: t.Union[int, str],
        y1: t.Union[int, str],
        x2: t.Union[int, str],
        y2: t.Union[int, str],
    ) -> None:
        """
        Simulate drag mouse from x1 y1 to x2 y2.
        :param xpath: str - web element xpath
        """
        actions = ActionChains(self.driver)
        actions.move_by_offset(x1, y1).click_and_hold()
        actions.move_by_offset(x2 - x1, y2 - y1).release().perform()
        self.logger.info(f"Mouse drag for: %s, %s", x2 - x1, y2 - y1)

    @log_exception("Failed open new tab: {}. Timeout: {wait}s")
    def open_new_tab(self, wait: int = short_timeout) -> None:
        """
        Open new tab in browser
        """
        win_handles_before = self.driver.window_handles
        self.driver.execute_script("window.open('');")
        win_handles_after = self.driver.window_handles
        WebDriverWait(self.driver, wait).until(ec.number_of_windows_to_be(len(win_handles_before) + 1))
        new_window = [x for x in win_handles_after if x not in win_handles_before][0]
        self.driver.switch_to_window(new_window)

    @log_exception("Failed to switch tab: {}. Timeout: {wait}s")
    def switch_to_tab_with_num(self, tab_num: int, wait: int = long_timeout) -> None:
        """
        Switches driver to new tab only. Works by number of tab, counts from 0.
        """
        with timeout(wait) as t:
            while not dict(enumerate(self.driver.window_handles)).get(tab_num, False):
                self.sleep(1)
                if t.expired:
                    raise AssertionError(f"Browser tab with num {tab_num} was not appeared. Timeout: {wait}s")
            self.driver.switch_to_window(self.driver.window_handles[tab_num])

    @log_exception("Cannot get text located: {}. Timeout: {wait}s")
    def get_text(self, xpath: t.Union[str, WebElement], wait: int = short_timeout) -> str:
        """
        Get text of the web element
        :param xpath: str - web element xpath
        :param wait: int - wait time for object
        """
        self.logger.info("Trying to get text from field with xpath: %s", xpath)
        result = self._get_element(xpath, ec.visibility_of_element_located, wait=wait).text
        self.logger.info('Got text "%s" from field with xpath: %s', result, xpath)
        return result

    def clear_input_field(self, element: t.Union[str, WebElement], wait: str = short_timeout) -> None:
        input_field = self._get_element(element, ec.visibility_of_element_located, wait=wait)
        if platform.system() == "Darwin":  # mac os
            input_field.clear()
        else:  # others
            input_field.send_keys(Keys.CONTROL, "a")  # without DELETE btn, to prevent auto complete
            input_field.send_keys(Keys.CONTROL, "a", Keys.DELETE)

    @log_exception("Failed to type text into web element with xpath: {}. Timeout: {wait}s")
    def type_text(
        self,
        xpath: str,
        text: str,
        wait: str = short_timeout,
        scroll: bool = False,
        confidential: bool = False,
    ) -> None:
        """
        Type text into input field with given xpath
        :param xpath: str - web element xpath
        :param text: str - text to type
        :param wait: int - wait time for object
        """
        self.logger.info('Typing "%s" into field with xpath: %s', "***" if confidential else text[:50], xpath)
        if scroll:
            self.execute_script(self._get_element(xpath, wait=wait), "scrollIntoView(true);")
        input_field = self._get_element(xpath, ec.visibility_of_element_located, wait=wait)
        self.clear_input_field(input_field)
        if len(text) <= 100:
            input_field.send_keys(text)
        elif len(text) > 100:
            max_chunk_size = 100
            chunks = [text[i : i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]
            for chunk in chunks:
                input_field.send_keys(chunk)
                self.sleep(0.1)
        self.logger.info('Typed "%s" into field with xpath: %s', "***" if confidential else text[:50] + "...", xpath)

    def send_keys_shadow(self, keys: Keys, sleep: t.Optional[float] = 1) -> None:
        """
        Emulate sending keys from keyboard. Enter is default
        :param keys: selenium.webdriver.common.keys or str text
        """
        ActionChains(self.driver).send_keys(keys).perform()
        self.sleep(sleep)

    def send_keys_to_element(self, xpath: str, keys: Keys = Keys.ENTER, wait: int = short_timeout) -> None:
        """
        Emulate sending keys from keyboard to the given web element. Enter is default
        :param xpath: str - web element xpath
        :param keys: selenium.webdriver.common.keys or str text
        :param wait: int - wait time for object
        """
        self._get_element(xpath, wait=wait).send_keys(keys)
        self.sleep(1)

    def submit_search(self, xpath: str, text: str, wait: int = short_timeout, delay_timeout: t.Optional[int] = 1) -> None:
        """
        Type text into input field with given xpath and send ENTER key
        :param xpath: str - web element xpath
        :param text: str - text to type
        :param wait: int - wait time for object
        """
        self.type_text(xpath, text, wait=wait)
        self.sleep(delay_timeout)
        self.send_keys_to_element(xpath, wait=wait)

    # CUSTOM WAITS

    def check_obj_exists(self, xpath: str) -> bool:
        """
        Return True if object exists
        """
        with suppress(Exception):
            self.driver.find_element(By.XPATH, xpath)
            return True
        return False

    def wait_element_appear(
        self,
        xpath: str,
        wait: t.Optional[int] = long_timeout,
        polling_time: t.Optional[int] = 1,
    ) -> bool:
        with timeout(wait) as t:
            while not self.check_obj_exists(xpath=xpath):
                self.sleep(polling_time)
                if t.expired:
                    return False
            return True

    def wait_element_disappear(
        self,
        xpath: str,
        wait: t.Optional[int] = long_timeout,
        polling_time: t.Optional[int] = 1,
    ) -> bool:
        with timeout(wait) as t:
            while self.check_obj_exists(xpath=xpath):
                self.sleep(polling_time)
                if t.expired:
                    return False
            return True

    def wait_element_visible(
        self,
        xpath: str,
        wait: t.Optional[int] = long_timeout,
        polling_time: t.Optional[int] = 1,
    ) -> bool:
        with timeout(wait) as t:
            while not self.is_visible(xpath=xpath, wait=2):
                self.sleep(polling_time)
                if t.expired:
                    return False
            return True

    def wait_element_invisible(
        self,
        xpath: str,
        wait: t.Optional[int] = long_timeout,
        polling_time: t.Optional[int] = 1,
    ) -> bool:
        with timeout(wait) as t:
            while self.is_visible(xpath=xpath, wait=2):
                self.sleep(polling_time)
                if t.expired:
                    return False
            return True

    @log_exception("Failed check web element state with xpath: {}. Timeout: {wait}s")
    def validate_element_appear(
        self,
        *xpaths: str,
        need_assert: bool = False,
        assert_message: t.Optional[str] = None,
        wait: int = long_timeout,
    ) -> None:
        """
        :param xpath: str - web element xpath
        :param wait: int - maximum wait time
        """
        for xpath in xpaths:
            self.logger.debug("Checking web element with xpath: %s", xpath)

            if not self.wait_element_appear(xpath, wait):
                message = assert_message or f"Element with xpath '{xpath}' don't appear. Timeout: {wait}s"
                raise AssertionError(message) if need_assert else TimeoutException(message)

            self.logger.info("Checked web element with xpath: %s", xpath)

    @log_exception("Failed check web element state with xpath: {}. Timeout: {wait}s")
    def validate_element_disappear(
        self,
        *xpaths: str,
        need_assert: bool = False,
        assert_message: t.Optional[str] = None,
        wait: int = long_timeout,
    ) -> None:
        """
        :param xpath: str - web element xpath
        :param wait: int - maximum wait time
        """
        for xpath in xpaths:
            self.logger.debug("Checking web element with xpath: %s", xpath)

            if not self.wait_element_disappear(xpath, wait):
                message = assert_message or f"Element with xpath '{xpath}' don't disappear. Timeout: {wait}s"
                raise AssertionError(message) if need_assert else TimeoutException(message)

            self.logger.info("Checked web element with xpath: %s", xpath)

    @log_exception("Failed check web element state with xpath: {}. Timeout: {wait}s")
    def validate_element_visible(
        self,
        *xpaths: str,
        need_assert: bool = False,
        assert_message: t.Optional[str] = None,
        wait: int = long_timeout,
    ) -> None:
        """
        :param xpath: str - web element xpath
        :param wait: int - maximum wait time
        """
        for xpath in xpaths:
            self.logger.debug("Checking web element with xpath: %s", xpath)

            if not self.wait_element_visible(xpath, wait):
                message = assert_message or f"Element with xpath '{xpath}' is not visible. Timeout: {wait}s"
                raise AssertionError(message) if need_assert else TimeoutException(message)

            self.logger.info("Checked web element with xpath: %s", xpath)

    @log_exception("Failed check web element state with xpath: {}. Timeout: {wait}s")
    def validate_element_invisible(
        self,
        *xpaths: str,
        need_assert: bool = False,
        assert_message: t.Optional[str] = None,
        wait: int = long_timeout,
    ) -> None:
        """
        :param xpath: str - web element xpath
        :param wait: int - maximum wait time
        """
        for xpath in xpaths:
            self.logger.debug("Checking web element with xpath: %s", xpath)

            if not self.wait_element_invisible(xpath, wait):
                message = assert_message or f"Element with xpath '{xpath}' is still visible. Timeout: {wait}s"
                raise AssertionError(message) if need_assert else TimeoutException(message)

            self.logger.info("Checked web element with xpath: %s", xpath)
