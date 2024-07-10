import allure
import pytest


@pytest.mark.smoke
@allure.parent_suite("Tests")
@allure.suite("Defaults")
@allure.feature("Common")
class TestCommon:

    @allure.id("01")
    @allure.title("Login with standard_user")
    def test_01(self):
        self.base_page.login("standard_user")
        self.base_page.sleep(3)
        self.base_page.logout()

    @allure.id("02")
    @allure.title("Login with locked_out_user")
    def test_02(self):
        self.base_page.login("locked_out_user")
        self.base_page.check_login_box_error_message("Epic sadface: Sorry, this user has been locked out.")
        self.base_page.sleep(3)

    @allure.id("03")
    @allure.title("Login with incorrect credentials")
    def test_03(self):
        self.base_page.login("incorrect_login")
        self.base_page.check_login_box_error_message("Epic sadface: Username and password do not match any user in this service")
        self.base_page.sleep(3)

    @allure.id("04")
    @allure.title("Check item could be added to the shopping cart")
    def test_04(self):
        self.base_page.login("standard_user")
        self.inventory.add_item_to_shopping_cart("Sauce Labs Backpack")
        self.inventory.check_shopping_cart_counter("1")
        self.inventory.add_item_to_shopping_cart("Sauce Labs Bike Light")
        self.inventory.check_shopping_cart_counter("2")
        self.inventory.remove_item_from_shopping_cart("Sauce Labs Backpack")
        self.inventory.check_shopping_cart_counter("1")
        self.inventory.remove_item_from_shopping_cart("Sauce Labs Bike Light")
        self.inventory.check_shopping_cart_counter("0")

    @allure.id("05")
    @allure.title("Check item details are different on the inventory page and on the item page for problem_user")
    def test_05(self):
        self.base_page.login("problem_user")
        item_inventory_info = self.inventory.get_item_details("Sauce Labs Backpack")
        self.inventory.open_item_page("Sauce Labs Backpack")
        item_info = self.inventory.item.get_item_details()
        assert item_inventory_info != item_info, "Item details are equal, but should be different."
