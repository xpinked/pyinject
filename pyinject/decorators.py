import inspect
from functools import wraps
from typing import Annotated, Any, Callable, ParamSpec, TypeVar, get_args, get_origin

from ._dependency import _Dependency
from .manager import DependenciesManager, default_manager

R = TypeVar("R", bound=Any)
P = ParamSpec("P")


def AutoWired(*, manager: DependenciesManager = default_manager) -> Callable[[Callable[P, R]], Callable[P, R]]:  # noqa: N802
    """
    A decorator that resolves dependencies from a callable and injects them to arguments Annotations

    Args:
    ----
        manager (DependenciesManager, optional): A manager that holds the dependencies. Defaults to default_manager.

    Returns:
    -------
        Callable[[Callable[P, R]], Callable[P, R]]: A decorator that resolves dependencies

    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
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

                    kwargs[param_name] = manager.get_dependency_value(_dependency)
                    continue

                if param.annotation is not None and param.annotation in manager.dependency_overrides:
                    kwargs[param_name] = manager.get_dependency_value(_Dependency(callable=param.annotation))

            return func(*args, **kwargs)

        return wrapper

    return decorator
