from dataclasses import dataclass, field
from typing import Any, Callable

from ._dependency import _Dependency
from ._helpers import SingletonMetaClass


@dataclass(slots=True)
class DependencyResolver(metaclass=SingletonMetaClass):
    """
    A dependency resolver that can be used to resolve dependencies from a callable,
    caching them if needed
    """

    _cached_dependencies_values: dict[Callable[..., Any], Any] = field(default_factory=dict)

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

        if _dependency.callable in self._cached_dependencies_values and _dependency.cache:
            return self._cached_dependencies_values[_dependency.callable]

        value = _dependency.callable()
        self._cached_dependencies_values[_dependency.callable] = value

        return value


if "resolver" not in globals():
    resolver = DependencyResolver()
