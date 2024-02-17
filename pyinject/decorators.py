import inspect
from functools import wraps
from typing import Annotated, Any, Callable, ParamSpec, TypeVar, get_args, get_origin

from ._dependency import _Dependency
from .manager import DependenciesManager, default_manager

R = TypeVar("R", bound=Any)
P = ParamSpec("P")


class _AutoWired:
    """A class that resolves dependencies from a callable and injects them to arguments Annotations"""

    def __init__(self, manager: DependenciesManager) -> None:
        self.manager = manager

    def __call__(self, func: Callable[P, R]) -> Callable[P, R]:
        """Decorator that resolves dependencies from a callable and injects them to arguments Annotations.

        Args:
        ----
            func (Callable[P, R]): A callable to be decorated

        Returns:
        -------
            Callable[P, R]: A decorated callable

        """
        sig = inspect.signature(func)

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            bound_args = sig.bind_partial(*args, **kwargs)
            bound_args.apply_defaults()

            kwargs_after_injection = self._inject_dependencies_to_kwargs(bound_args, sig, kwargs)

            return func(*args, **kwargs_after_injection)

        return wrapper

    def _inject_dependencies_to_kwargs(
        self,
        bound_args: inspect.BoundArguments,
        sig: inspect.Signature,
        original_kwargs: dict[str, Any],
    ) -> dict[str, Any]:
        """Injects dependencies to the arguments Annotations.

        Args:
        ----
            bound_args (inspect.BoundArguments): A bound arguments object
            sig (inspect.Signature): A signature object
            kwargs (dict[str, Any]): A dictionary containing the keyword arguments

        Returns:
        -------
            dict[str, Any]: A dictionary containing the keyword arguments after injection

        """
        new_kwargs = original_kwargs.copy()

        for param_name, param in sig.parameters.items():
            if param_name in bound_args.arguments or param.annotation is inspect.Parameter.empty:
                continue

            # Case of Annotated[<type>, Dependency(...)]
            if get_origin(param.annotation) is Annotated:
                _type, _dependency = get_args(param.annotation)
                _Dependency.validate(_dependency)
                _dependency.callable = _dependency.callable or _type
                new_kwargs[param_name] = self.manager.get_dependency_value(_dependency)

            # Case of globally overridden dependency without Annotated[<type>, Dependency(...)]
            elif param.annotation in self.manager.dependency_overrides:
                _dependency = _Dependency(callable=param.annotation, cache=False)
                new_kwargs[param_name] = self.manager.get_dependency_value(_dependency)

        return new_kwargs


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
    return _AutoWired(manager=manager)
