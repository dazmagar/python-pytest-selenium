import typing as t

from selenium.common.exceptions import *
from selenium.webdriver.remote.webdriver import WebDriver

import definitions
from core.allure_helper import allure_step
from core.base_class import BaseClass
from resources.pages_locators import base_page
from utils.config import get_config


class BasePage(BaseClass):
    """
    Base page representation.
    The abstract page class that we created to inherit into other page classes
    """

    def __init__(self, driver: WebDriver) -> None:
        super(BasePage, self).__init__(driver)

    @allure_step("I login to application by user {user_name}")
    def login(self, user_name: str) -> None:
        self.open(get_config().base_url)
        self.validate_element_appear(base_page.input_with_id("user-name"), wait=definitions.long_timeout, need_assert=True)
        self.type_text(base_page.input_with_id("user-name"), user_name)
        self.type_text(base_page.input_with_id("password"), get_config().test_users_credentials[user_name], confidential=True)
        self.click(base_page.input_with_id("login-button"))

    @allure_step("I logout from application")
    def logout(self) -> None:
        from page_classes.Inventory.InventoryPage import InventoryPage

        inventory_page = InventoryPage(self.driver)
        inventory_page.select_sidemenu("Logout")
        self.validate_element_appear(base_page.input_with_id("user-name"), wait=definitions.long_timeout, need_assert=True)

    @allure_step("I check login box error message: '{error_message}'")
    def check_login_box_error_message(self, error_message: str) -> None:
        self.validate_element_appear(base_page.login_box_error_message + base_page.descendant_text(error_message), need_assert=True)
