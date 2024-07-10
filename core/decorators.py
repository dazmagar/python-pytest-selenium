import logging
import typing as t
from functools import wraps

from utils.func_args_helper import func_parameters, represent

T = t.TypeVar("T")


def log_exception(message: str) -> t.Callable:
    """
    Decorator for function execution in try/except with first logging what tried to do and then raising an exception
    could log method arguments with positional {} and kw {arg} style
    """

    def decorator(func: t.Callable) -> t.Callable:
        @wraps(func)
        def wrapper(self: object, *args: t.Tuple, **kwargs: t.Dict) -> T:
            try:
                return func(self, *args, **kwargs)
            except Exception:
                log = self.logger if hasattr(self, "logger") else logging.getLogger(self.__class__.__name__)

                f_args = [represent(x) for x in args]
                f_params = func_parameters(func, *args, **kwargs)

                log.error(message.format(*f_args, **f_params))
                raise

        return wrapper

    return decorator
