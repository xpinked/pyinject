from typing import Any, Callable, TypeVar

from ._dependency import _Dependency
from .manager import DependenciesManager

R = TypeVar("R", bound=Any)


def Depends(_callable: Callable[..., Any] | None = None, cache: bool = True) -> _Dependency:  # noqa: N802, FBT002
    """
    Given a callable, returns a Dependency object that can be used to annotate

    Args:
    ----
        callable (Callable[..., Any]): A callable that returns a dependency
        cache (bool, optional): Whether or not to cache the dependency. Defaults to True.

    Returns:
    -------
        _Dependency: A dependency object that can be used to annotate

    """
    return _Dependency(_callable, cache)


def get_default_manager() -> DependenciesManager:
    """
    Returns the default DependenciesManager instance.

    Returns
    -------
        DependenciesManager: The default DependenciesManager instance.

    """
    from .manager import default_manager

    return default_manager


def create_manager() -> DependenciesManager:
    """
    Returns a new DependenciesManager instance.

    Returns
    -------
        DependenciesManager: A new DependenciesManager instance.

    """
    return DependenciesManager()


def execute(starting_point: Callable[..., R], *args: Any, **kwargs: Any) -> R:
    """Executes a function with the given arguments and keyword arguments

    Args:
    ----
        starting_point (Callable[..., R]): The function to execute
        *args (Any): The positional arguments
        **kwargs (Any): The keyword arguments

    Returns:
    -------
        R: The result of the function

    """
    return starting_point(*args, **kwargs)
