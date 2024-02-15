import typing

from .decorators import AutoWired, P, R
from .manager import DependenciesManager, OverridesMapping, default_manager


class DependencyOverrider:
    """A context manager that overrides the dependencies with the provided overrides."""

    def __init__(self, overrides: OverridesMapping, *, manager: DependenciesManager = default_manager) -> None:
        self.overrides = overrides
        self.manager = manager
        self._old_overrides: OverridesMapping = {}

    def __enter__(self):  # noqa: ANN204
        """Overrides the dependencies with the provided overrides."""
        self._old_overrides = self.manager.override_dependencies(self.overrides)
        return self

    def __exit__(self, *args: object) -> None:
        """Restores the overridden dependencies to their original values."""
        self.manager.restore_dependencies(self.overrides, self._old_overrides)

    def execute(self, func: typing.Callable[P, R], *args, **kwargs) -> R:
        """Executes a function with the given arguments and keyword arguments.

        Resolving the dependencies from the manager provided in the constructor.
        """
        return AutoWired(manager=self.manager)(func)(*args, **kwargs)  # type: ignore reportCallIssue
