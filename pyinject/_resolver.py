from dataclasses import dataclass, field
from threading import Lock
from typing import Any, Callable

from ._dependency import _Dependency
from ._meta import SingletonMetaClass

OverridesMapping = dict[Callable[..., Any], Callable[..., Any]]


@dataclass(slots=True)
class DependenciesManager(metaclass=SingletonMetaClass):
    """
    A dependency resolver that can be used to resolve dependencies from a callable,
    caching them if needed
    """

    cached_dependencies_values: dict[Callable[..., Any], Any] = field(default_factory=dict)
    dependency_overrides: OverridesMapping = field(default_factory=dict)

    _caching_lock = Lock()
    _overrides_lock = Lock()

    def get_dependency_value(self, _dependency: _Dependency) -> Any:
        """
        Given a _Dependency object, returns the dependency value, caching it if needed

        Args:
            _dependency (_Dependency): A _Dependency object

        Returns:
            Any: The dependency value
        """

        if _dependency.callable is None:
            raise ValueError("Dependency cannot be None, please provide a callable")

        if _dependency.callable in self.dependency_overrides:
            return self.dependency_overrides[_dependency.callable]()

        if _dependency.callable in self.cached_dependencies_values and _dependency.cache:
            return self.cached_dependencies_values[_dependency.callable]

        value = _dependency.callable()

        if _dependency.cache:
            with self._caching_lock:
                self.cached_dependencies_values[_dependency.callable] = value

        return value

    def override_dependencies(self, overrides: OverridesMapping) -> OverridesMapping:
        self._overrides_lock.acquire()

        old_overrides: OverridesMapping = {}

        for dep, new_dep in overrides.items():
            if dep in self.dependency_overrides:
                old_overrides[dep] = self.dependency_overrides[dep]
            self.dependency_overrides[dep] = new_dep

        return old_overrides

    def restore_dependencies(self, overrides: OverridesMapping, old_overrides: OverridesMapping):
        for dep in overrides.keys():
            if dep in old_overrides:
                self.dependency_overrides[dep] = old_overrides.pop(dep)
            else:
                del self.dependency_overrides[dep]

        self._overrides_lock.release()


if "resolver" not in globals():
    dependencies_manager = DependenciesManager()
