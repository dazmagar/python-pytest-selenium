import logging
import os
import typing as t
from datetime import datetime
from pathlib import Path

import allure
import pytest

import definitions
from core.allure_helper import write_report_env_details, write_report_executor_details
from core.driver_helper import DriverHelper
from page_classes import BasePage
from page_classes.Inventory import InventoryItemPage, InventoryPage
from utils.common import remove_empty_logs
from utils.config import Config, get_config
from utils.screenshots import take_screenshot


def pytest_addoption(parser: pytest.Parser) -> None:
    # App Section
    parser.addoption("--base_url", action="store", type=str, default=None, help="Application base url (may also contain '<ENV>' substring which will be replaced with 'env' config option or --env cl argument)")
    parser.addoption("--env", action="store", type=str, default=None, help="'<ENV>' part of base_url param which will be replaced with value provided")
    # * @skipped: browser_resolution. add if you need it.
    # Browser Settings Section
    parser.addoption("--browser", action="store", type=str.lower, default=None, choices=["chrome", "firefox", "edge", "opera", "ie"], help="Browser name to be used during the tests")
    parser.addoption("--is_headless", action="store", type=bool, default=False, help="Should browser executed in headless mode")
    parser.addoption("--testrun_type", action="store", type=str.lower, default=None, choices=["local", "remote"], help="Testrun type - may be local or remote (usually LambdaTest)")
    # Remote only section
    parser.addoption("--remote_options.platform", action="store", type=str, default=None, help="Remote Selenium Grid (LambdaTest) vm platform (Windows 10, etc.)")
    parser.addoption("--remote_options.browser_version", action="store", type=int, default=None, help="Remote Selenium Grid (LambdaTest) browser version")
    parser.addoption("--remote_options.lt_username", action="store", type=str, default=None, help="Username for LambdaTest Tunnel")
    parser.addoption("--remote_options.lt_access_key", action="store", type=str, default=None, help="Access Key for LambdaTest Tunnel")
    parser.addoption("--remote_options.lt_tunnel", action="store", type=str, default=None, help="LambdaTest Tunnel name")
    parser.addoption("--remote_options.lt_build_id", action="store", type=str, default=None, help="LambdaTest BuildID")
    # Options from Azure
    parser.addoption("--azure_build_name", action="store", type=str, default=None, help="Azure DevOps Name")
    parser.addoption("--azure_build_id", action="store", type=int, default=None, help="Azure DevOps BuildID")


def pytest_configure(config: pytest.Config) -> None:
    # Config updates
    Config.update_config_with_cl_args(config)
    # logs work
    definitions.log_dir.mkdir(parents=True, exist_ok=True)  # create if don't have allure dir
    if get_config().reporting.save_logs_to_file:
        config.option.log_file = definitions.log_dir / f"logs_{str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f'))}.log"
    # Allure stuff
    allure_dir = get_config().get("alluredir", None)  # this option could be received through cli args
    if allure_dir:
        Path(allure_dir).mkdir(parents=True, exist_ok=True)
        write_report_env_details(allure_dir)  # and add some details
        if get_config().reporting.add_executor_details:  # it is more complicated stuff, so I decided to put it to the config
            write_report_executor_details(allure_dir)
    # some cleanup because of strange vscode autorun of pytest_configure in background
    if get_config().testrun_type.lower() == "local":
        remove_empty_logs()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_collection_modifyitems(items: t.List[pytest.Item]) -> t.Iterator[None]:
    for item in items:
        # handle id and create id-tag
        for mark in item.iter_markers(name="allure_label"):
            # if item has allure id duplicate it to tags.
            if mark.kwargs["label_type"] == "as_id":
                item.allure_id = mark.args[0]
                item.add_marker(allure.tag(mark.args[0]))
                break
        # handle all tags
        for mark in item.iter_markers(name="allure_label"):
            if mark.kwargs["label_type"] in ["tag", "suite"]:
                # if item has allure tag or suite duplicate it to pytest tags.
                item.add_marker(mark.args[0])
        # simplify access to allure title and modifying it
        # allure creates attrib with this name if case is marked by @allure.title(...)
        if hasattr(item.function, "__allure_display_name__") and get_config().get("reporting").get("add_ids_to_titles") and hasattr(item, "allure_id") and f"[{item.allure_id}]" not in item.function.__allure_display_name__:
            item.function.__allure_display_name__ = f"[{item.allure_id}] " + item.function.__allure_display_name__
            item.allure_title = item.function.__allure_display_name__
    yield


@pytest.fixture(autouse=True)
def driver(request: pytest.FixtureRequest) -> t.Iterator[DriverHelper]:
    logger = logging.getLogger(__name__)

    current_item = request._pyfuncitem
    test_title: str
    if hasattr(current_item, "allure_title"):
        test_title = current_item.allure_title
    else:
        test_title = os.environ["PYTEST_CURRENT_TEST"].split(":")[-1].split(" ")[0]

    logger.info("Started test: %s", test_title)
    driver = DriverHelper.get_driver(test_title)
    yield driver
    DriverHelper.close_driver()


@pytest.fixture(autouse=True)
def pages_init(request: pytest.FixtureRequest, driver: DriverHelper) -> None:
    """pages initialization for tests.
    'requests.cls.' will be equal to 'self.' in the tests methods.
    """
    request.cls.base_page = BasePage.BasePage(driver)
    request.cls.inventory = InventoryPage.InventoryPage(driver)
    request.cls.inventory.item = InventoryItemPage.InventoryItemPage(driver)


def before_allure_step() -> None:
    pass


def after_allure_step() -> None:
    if get_config().get("reporting").get("screen_each_step"):
        allure.attach(DriverHelper.get_driver().get_screenshot_as_png(), "step screenshot", allure.attachment_type.PNG)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> t.Generator[None, pytest.CallInfo, None]:
    logger = logging.getLogger(__name__)

    outcome = yield
    result = outcome.get_result()
    # if result.when == 'setup':
    if result.when == "call":  # ? after test finished
        driver = DriverHelper.get_driver()
        if result.failed:
            screen = take_screenshot(driver, f"{item.nodeid}_FAILED")
            if screen is not None:
                allure.attach.file(screen, "_Fail Screenshot_", allure.attachment_type.PNG)
            logger.info("Test failed: %s", item.name)
        else:
            logger.info("Test successful: %s", item.name)
        if get_config().testrun_type.lower() == "remote":
            # set status to lambdatest test-session
            if result.failed:
                driver.execute_script("lambda-status=failed")
            else:
                driver.execute_script("lambda-status=passed")
    # if result.when == 'teardown':


# def pytest_unconfigure():
#   pass
