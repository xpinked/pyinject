import typing

from ._resolver import DependenciesManager, OverridesMapping, dependencies_manager


class DependencyOverrider:
    def __init__(self, overrides: OverridesMapping, _resolver: DependenciesManager = dependencies_manager) -> None:
        self.overrides = overrides
        self._resolver = _resolver
        self._old_overrides: OverridesMapping = {}

    def __enter__(self):
        self._old_overrides = self._resolver.override_dependencies(self.overrides)
        return self

    def __exit__(self, *args: typing.Any) -> None:
        self._resolver.restore_dependencies(self.overrides, self._old_overrides)
