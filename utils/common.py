import logging
import random
import string
import time
from datetime import datetime
from typing import Tuple

import definitions

logger = logging.getLogger(__name__)


def random_string(stringLength: int) -> str:
    letters = string.ascii_letters
    return "".join(random.choice(letters) for i in range(stringLength))


def get_current_date(date_format: str = "%Y-%m-%d") -> str:
    return datetime.now().strftime(date_format)


def remove_empty_logs(max_retries: int = 3, retry_delay: int = 1) -> None:
    if definitions.log_dir.exists():
        for something in list(definitions.log_dir.iterdir()):
            file_full_path = definitions.log_dir / something
            if file_full_path.is_file() and file_full_path.stat().st_size == 0:
                retry_count = 0
                while retry_count < max_retries:
                    try:
                        file_full_path.unlink()
                        break  # Successfully deleted the file, exit the loop.
                    except PermissionError:
                        retry_count += 1
                        time.sleep(retry_delay)
                else:
                    # Max retries reached, unable to delete the file.
                    logger.error("Failed to delete: %s", file_full_path)


# contextmanager to manage timeouted actions
class timeout:
    def __init__(self, timeout: int) -> None:
        self.timeout = timeout

    def __enter__(self) -> None:
        self.__expired_after = time.time() + self.timeout
        return self

    def __exit__(self, *args: Tuple) -> None:
        pass

    @property
    def expired(self) -> bool:
        return time.time() > self.__expired_after
