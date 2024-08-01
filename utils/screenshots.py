import logging
from datetime import datetime

from selenium.webdriver.remote.webdriver import WebDriver

import definitions

logger = logging.getLogger(__name__)


def take_screenshot(driver: WebDriver, node_id: str) -> str:
    """Make a screenshot with a name of the test, date and time
    return: screenshot filename.
    """
    node_id = node_id.replace("/", "_").replace(":", "_")
    file_name = f'{node_id}_{datetime.today().strftime("%Y-%m-%d_%H_%M")}.png'
    folder = definitions.log_dir / node_id
    file_path = folder / file_name
    try:
        folder.mkdir(parents=True, exist_ok=True)
        driver.save_screenshot(str(file_path))
        return file_path
    except Exception as e:
        logger.error("Exception while screen-shot creation: %s", str(e), exc_info=True)
        return None
