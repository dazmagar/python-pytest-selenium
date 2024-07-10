import typing as t

from utils.config import get_config


def get_lt_url() -> str:
    lt_username = get_config().remote_options.lt_username
    lt_access_key = get_config().remote_options.lt_access_key
    return f"https://{lt_username}:{lt_access_key}@hub.lambdatest.com/wd/hub"


def get_lt_caps(scenario_name: str) -> t.Dict:
    desired_caps = {
        "platformName": get_config().remote_options.platform,
        "resolution": f'{get_config().remote_options.browser_resolution["width"]}x{get_config().remote_options.browser_resolution["height"]}',
        "pageLoadStrategy": get_config().page_load_strategy,
        # lt run
        "tunnel": True,
        "tunnelName": get_config().remote_options["lt_tunnel"],
        "name": scenario_name,
        "build": get_config().remote_options["lt_build_id"],
        "project": get_config().remote_options.project_name,
        # lt run options
        "video": True,
        "console": "true",
        "visual": False,
        "network": False,
        "w3c": True,
        "selenium_version": get_config().remote_options.selenium_version,
        "plugin": "python-pytest",
        "goog:chromeOptions": {
            "prefs": {
                "download.default_directory": "D:",
                "download.prompt_for_download": False,
                "download.directory_upgrade": False,
                # "safebrowsing.enabled": True
            }
        },
    }
    return desired_caps
