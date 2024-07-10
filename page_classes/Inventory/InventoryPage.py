import typing as t
from pathlib import Path

from selenium.common.exceptions import *
from selenium.webdriver.remote.webdriver import WebDriver

import definitions
from core.allure_helper import allure_step
from page_classes.BasePage import BasePage
from resources.pages_locators import base_page, inventory_item_page, inventory_page


class InventoryPage(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        super(BasePage, self).__init__(driver)

    @allure_step("I select sidemenu item {sidemenu_name}")
    def select_sidemenu(self, sidemenu_name: str) -> None:
        if "true" in self._get_attribute("aria-hidden", inventory_page.sidemenu_wrap):
            self.click(base_page.button_with_id("react-burger-menu-btn"))
        self.click(inventory_page.sidemenu_item(sidemenu_name))

    @allure_step("I add item '{item_name}' to the shopping cart.")
    def add_item_to_shopping_cart(self, item_name: str) -> None:
        self.validate_element_appear(inventory_page.inventory_item(item_name), need_assert=True)
        if self.wait_element_disappear(inventory_page.inventory_item_remove_button(item_name), wait=definitions.short_timeout):
            self.click(inventory_page.inventory_item_add_button(item_name))
            self.validate_element_appear(inventory_page.inventory_item_remove_button(item_name), need_assert=True)

    @allure_step("I remove item '{item_name}' from shopping cart.")
    def remove_item_from_shopping_cart(self, item_name: str) -> None:
        self.validate_element_appear(inventory_page.inventory_item(item_name), need_assert=True)
        if self.wait_element_disappear(inventory_page.inventory_item_add_button(item_name), wait=definitions.short_timeout):
            self.click(inventory_page.inventory_item_remove_button(item_name))
            self.validate_element_appear(inventory_page.inventory_item_add_button(item_name), need_assert=True)

    @allure_step("I check shopping cart counter == '{cart_items_count}'.")
    def check_shopping_cart_counter(self, cart_items_count: str) -> None:
        self.scroll_to_element(inventory_page.shopping_cart)
        cart_container_text = self.get_text(inventory_page.shopping_cart)
        curr_items_count = cart_container_text if cart_container_text else "0"
        assert cart_items_count == curr_items_count, f"Wrong number of items in shopping cart. Expected: '{cart_items_count}'. But was: {curr_items_count}."

    @allure_step("I get item '{item_name}' details.")
    def get_item_details(self, item_name: str) -> t.Dict[str, str]:
        self.validate_element_appear(inventory_page.inventory_item(item_name), need_assert=True)
        item_info = {
            "img": Path(self._get_attribute("src", inventory_page.inventory_item_img(item_name))).name,
            "name": self.get_text(inventory_page.inventory_item_name(item_name)).strip(),
            "desc": self.get_text(inventory_page.inventory_item_desc(item_name)).strip(),
            "price": self.get_text(inventory_page.inventory_item_price(item_name)),
        }
        return item_info

    @allure_step("I opened item '{item_name}' detailed description.")
    def open_item_page(self, item_name: str) -> None:
        self.validate_element_appear(inventory_page.inventory_item(item_name), need_assert=True)
        self.click(inventory_page.inventory_item_name(item_name))
        self.validate_element_appear(inventory_item_page.inventory_container, base_page.button_with_id("back-to-products"), need_assert=True)
