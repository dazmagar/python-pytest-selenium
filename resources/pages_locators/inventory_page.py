from resources.pages_locators import base_page

sidemenu_wrap = "//div[@class='bm-menu-wrap']"
shopping_cart = "//div[@id='shopping_cart_container']"


def sidemenu_item(sidemenu_name: str) -> str:
    return "//nav/a" + base_page.inner_text(sidemenu_name)


def inventory_item(item_name: str) -> str:
    return "//div[@data-test='inventory-item']" + base_page.descendant_text(item_name)


def inventory_item_img(item_name: str) -> str:
    return inventory_item(item_name) + "//img[@class='inventory_item_img']"


def inventory_item_name(item_name: str) -> str:
    return inventory_item(item_name) + "//div[@data-test='inventory-item-name']"


def inventory_item_desc(item_name: str) -> str:
    return inventory_item(item_name) + "//div[@data-test='inventory-item-desc']"


def inventory_item_price(item_name: str) -> str:
    return inventory_item(item_name) + "//div[@data-test='inventory-item-price']"


def inventory_item_add_button(item_name: str) -> str:
    return inventory_item(item_name) + base_page.button_with_text("Add to cart")


def inventory_item_remove_button(item_name: str) -> str:
    return inventory_item(item_name) + base_page.button_with_text("Remove")
