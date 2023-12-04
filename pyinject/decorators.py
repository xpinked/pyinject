import inspect
from functools import wraps
from typing import Annotated, get_args, get_origin

from ._dependency import _Dependency
from ._resolver import resolver


def AutoWired(func):
    """
    A decorator that resolves dependencies from a callable and injects them to arguments Annotations
    Args:
        func (_type_): function to decorate

    Returns:
        _type_: decorated function with resolved dependencies
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        bound_args = sig.bind_partial(*args, **kwargs)
        bound_args.apply_defaults()

        for param_name, param in sig.parameters.items():
            if param_name in bound_args.arguments:
                continue

            if get_origin(param.annotation) is Annotated:
                _type, _dependency = get_args(param.annotation)
                _Dependency.validate(_dependency)

                if _dependency.callable is None:
                    _dependency.callable = _type

                kwargs[param_name] = resolver.get_dependency_value(_dependency)

        return func(*args, **kwargs)

    return wrapper
