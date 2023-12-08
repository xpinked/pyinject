from typing import Any, Callable, TypeVar

from ._dependency import _Dependency
from .manager import DependenciesManager

R = TypeVar("R", bound=Any)


def Depends(callable: Callable[..., Any] | None = None, cache: bool = True) -> _Dependency:
    """
    Given a callable, returns a Dependency object that can be used to annotate

    Args:
        callable (Callable[..., Any]): A callable that returns a dependency
        cache (bool, optional): Whether or not to cache the dependency. Defaults to True.

    Returns:
        _Dependency: A dependency object that can be used to annotate
    """
    return _Dependency(callable, cache)


def get_default_manager() -> DependenciesManager:
    from .manager import default_manager

    return default_manager


def create_manager() -> DependenciesManager:
    return DependenciesManager()


def execute(starting_point: Callable[..., R], *args: Any, **kwargs: Any) -> R:
    return starting_point(*args, **kwargs)
