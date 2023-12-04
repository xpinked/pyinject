from typing import Any, Callable

from ._dependency import _Dependency


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


def run_program(starting_point: Callable[..., Any], *args, **kwargs) -> Any:
    return starting_point(*args, **kwargs)
