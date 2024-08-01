import typing as t
from pathlib import Path

from selenium.common.exceptions import *
from selenium.webdriver.remote.webdriver import WebDriver

from core.allure_helper import allure_step
from page_classes.BasePage import BasePage
from resources.pages_locators import inventory_item_page


class InventoryItemPage(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        super(BasePage, self).__init__(driver)

    @allure_step("I get item details.")
    def get_item_details(self) -> t.Dict[str, str]:
        item_info = {
            "img": Path(self._get_attribute("src", inventory_item_page.item_img)).name,
            "name": self.get_text(inventory_item_page.item_name).strip(),
            "desc": self.get_text(inventory_item_page.item_desc).strip(),
            "price": self.get_text(inventory_item_page.item_price),
        }
        return item_info
