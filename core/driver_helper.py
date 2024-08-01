import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.ie.service import Service as IEService
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.remote.webdriver import WebDriver

import definitions
from core.lambdatest_caps import get_lt_caps, get_lt_url
from utils.config import get_config


class DriverHelper:
    _driver = None

    @classmethod
    def init_local_driver(cls) -> WebDriver:
        config_browser = get_config().browser.lower()
        is_headless = get_config().is_headless
        if config_browser == "chrome":
            # configure options
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            chrome_options.add_experimental_option("useAutomationExtension", False)
            chrome_options.add_experimental_option(
                "prefs",
                {
                    "credentials_enable_service": False,
                    "profile.password_manager_enabled": False,
                    "profile.default_content_settings.popups": 0,
                    "download.default_directory": str(definitions.driver_download_path),
                    "directory_upgrade": True,
                },
            )
            chrome_options.add_argument("--ignore-certificate-errors")
            chrome_options.add_argument("--ignore-ssl-errors")
            # chrome_options.add_argument("--incognito") # clear chrome cache didn't work with '--incognito'
            if is_headless:
                chrome_options.add_argument("--headless=new")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--disable-dev-shm-usage")
            # and get driver
            cls._driver = webdriver.Chrome(service=ChromeService(), options=chrome_options)
        elif config_browser == "firefox":
            cls._driver = webdriver.Firefox(service=FirefoxService())
        elif config_browser == "opera":
            cls._driver = webdriver.Opera()
        elif config_browser == "edge":
            cls._driver = webdriver.Edge(service=EdgeService())
        elif config_browser == "ie":
            cls._driver = webdriver.Ie(service=IEService())

        cls._driver.set_window_size(get_config().browser_resolution["width"], get_config().browser_resolution["height"])
        # cls._driver.maximize_window()

        return cls._driver

    @classmethod
    def init_remote_driver(cls, scenario_name: str) -> WebDriver:
        logger = logging.getLogger(__name__)

        config_browser = get_config().browser.lower()
        if config_browser == "chrome":
            # configure options
            opts = webdriver.ChromeOptions()
            opts.set_capability("browserVersion", get_config().remote_options.browser_version)
            opts.set_capability("LT:Options", get_lt_caps(scenario_name))
        try:
            cls._driver = webdriver.Remote(
                command_executor=RemoteConnection(get_lt_url()),
                options=opts,
            )
            return cls._driver
        except Exception:
            logger.error("Failed to start browser: %s", get_config().browser, exc_info=True)
            raise

    @classmethod
    def get_driver(cls, scenario_name: str = None) -> WebDriver:
        if cls._driver:
            return cls._driver
        else:
            testrun_type = get_config().testrun_type.lower()
            if testrun_type == "remote":
                return cls.init_remote_driver(scenario_name)
            elif testrun_type == "local":
                return cls.init_local_driver()

    @classmethod
    def close_driver(cls) -> None:
        if cls._driver:
            cls._driver.quit()  # close()
            cls._driver = None
