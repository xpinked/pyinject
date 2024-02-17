from threading import Lock
from typing import Any, Callable

from ._dependency import _Dependency

OverridesMapping = dict[Callable[..., Any], Callable[..., Any]]


class DependenciesManager:
    """A class that manages dependencies and their caching."""

    __slots__ = ["cached_dependencies_values", "_caching_lock", "_overrides_lock", "dependency_overrides"]

    def __init__(self) -> None:
        self.cached_dependencies_values: dict[Callable[..., Any], Any] = {}
        self._caching_lock = Lock()
        self._overrides_lock = Lock()
        self.dependency_overrides: OverridesMapping = {}

    def get_dependency_value(self, _dependency: _Dependency) -> Any:
        """
        Given a _Dependency object, returns the dependency value, caching it if needed

        Args:
        ----
            _dependency (_Dependency): A _Dependency object

        Returns:
        -------
            Any: The dependency value

        """
        if _dependency.callable is None:
            raise ValueError("Dependency cannot be None, please provide a callable")

        with self._overrides_lock:
            if _dependency.callable in self.dependency_overrides:
                return self.dependency_overrides[_dependency.callable]()

        with self._caching_lock:
            if _dependency.callable in self.cached_dependencies_values and _dependency.cache:
                return self.cached_dependencies_values[_dependency.callable]

        value = _dependency.callable()

        if _dependency.cache:
            with self._caching_lock:
                self.cached_dependencies_values[_dependency.callable] = value

        return value

    def override_dependencies(self, overrides: OverridesMapping) -> OverridesMapping:
        """
        Overrides the dependencies with the provided overrides.

        Args:
        ----
            overrides (OverridesMapping): A dictionary containing the dependencies to be overridden.

        Returns:
        -------
            OverridesMapping: A dictionary containing the previous overrides that were replaced.

        """
        with self._overrides_lock:
            old_overrides: OverridesMapping = {}

            for dep, new_dep in overrides.items():
                if dep in self.dependency_overrides:
                    old_overrides[dep] = self.dependency_overrides[dep]
                self.dependency_overrides[dep] = new_dep

            return old_overrides

    def restore_dependencies(self, overrides: OverridesMapping, old_overrides: OverridesMapping) -> None:
        """
        Restores the overridden dependencies to their original values based on the provided overrides and old_overrides mappings.

        Args:
        ----
            overrides (OverridesMapping): A dictionary containing the current overrides for the dependencies.
            old_overrides (OverridesMapping): A dictionary containing the previous overrides for the dependencies.

        Returns:
        -------
            None

        """
        with self._overrides_lock:
            for dep in overrides:
                if dep in old_overrides:
                    self.dependency_overrides[dep] = old_overrides.pop(dep)
                else:
                    del self.dependency_overrides[dep]


if "default_manager" not in globals():
    default_manager = DependenciesManager()
