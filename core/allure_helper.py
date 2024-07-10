import json
import logging
import typing as t
from functools import wraps
from pathlib import Path

from allure_commons._allure import StepContext

import conftest
from utils.config import get_config
from utils.func_args_helper import func_parameters, represent

T = t.TypeVar("T")
logger_prefix = "\n" * 2 + " " * 4  # for beautifying  output we decided to use such a prefix

### OVERRIDE OF allure_step ###


def allure_step(title: str) -> t.Callable:
    if callable(title):
        return CustomStepContext(title.__name__, {})(title)
    return CustomStepContext(title, {})


class CustomStepContext(StepContext):
    logger = logging.getLogger(__name__)

    def __enter__(self) -> None:
        self.logger.info(logger_prefix + "Step Started: " + self.title + "\n")
        super().__enter__()
        conftest.before_allure_step()

    def __exit__(self, exc_type: t.Optional[t.Type[BaseException]], exc_val: t.Optional[BaseException], exc_tb: t.Optional[BaseException]) -> None:
        if exc_type is not None:
            self.logger.exception(logger_prefix + "Step FAILED: " + self.title + "\n")
        conftest.after_allure_step()
        super().__exit__(exc_type, exc_val, exc_tb)
        self.logger.info(logger_prefix + "Step Finished: " + self.title + "\n")

    def __call__(self, func: t.Callable) -> t.Callable:
        @wraps(func)
        def impl(*args: t.Tuple, **kwargs: t.Dict) -> T:
            logger = logging.getLogger(func.__qualname__)  # getting class_name + function_name

            f_args = [represent(x) for x in args]
            f_params = func_parameters(func, *args, **kwargs)
            parametrized_title = self.title.format(*f_args, **f_params)
            with StepContext(parametrized_title, {key: represent(value) for key, value in f_params.items()}):
                conftest.before_allure_step()
                logger.info(logger_prefix + "Step Started: " + parametrized_title + "\n")
                try:
                    step_result = func(*args, **kwargs)
                    logger.info(logger_prefix + "Step Finished: " + parametrized_title + "\n")
                except Exception:
                    logger.exception(logger_prefix + "Step FAILED: " + parametrized_title + "\n")
                    raise
                conftest.after_allure_step()
                return step_result

        return impl


##############################


def write_report_env_details(allure_dir: str) -> None:
    env_path = Path(allure_dir) / "environment.properties"
    with Path(env_path).open(mode="w+") as allure_env:
        allure_env.write(f"Stand={get_config().env}\n")
        allure_env.write(f"BaseUrl={get_config().base_url}\n")
        allure_env.write(f"Browser={get_config().browser.capitalize()}\n")
        if get_config().testrun_type.lower() == "remote":
            allure_env.write(f"Browser.Version={get_config().remote_options.browser_version}\n")
            allure_env.write(f"Platform={get_config().remote_options.platform}\n")


def write_report_executor_details(allure_dir: str) -> None:
    build_num = get_config().get("azure_build_id", None)
    build_name = get_config().get("azure_build_name", None)
    if build_num and build_name:
        exec_path = Path(allure_dir) / "executor.json"
        with Path(exec_path).open(mode="w+") as allure_executor:
            allure_executor.write(
                json.dumps(
                    {
                        "name": "Azure Pipeline",
                        "url": "https://dev.azure.com/organiztion/project/_build",
                        "buildOrder": build_num,
                        "buildName": f"{build_name}#{build_num}",
                        "buildUrl": f"https://dev.azure.com/organiztion/project/_build/results?buildId={build_num}",
                    }
                )
            )
