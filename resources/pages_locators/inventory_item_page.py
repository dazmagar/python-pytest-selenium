from resources.pages_locators import base_page

inventory_container = "//div[@data-test='inventory-container']"
item_img = inventory_container + "//img[@class='inventory_details_img']"
item_name = inventory_container + "//div[@data-test='inventory-item-name']"
item_desc = inventory_container + "//div[@data-test='inventory-item-desc']"
item_price = inventory_container + "//div[@data-test='inventory-item-price']"
