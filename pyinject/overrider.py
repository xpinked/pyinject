import typing

from ._manager import DependenciesManager, OverridesMapping, dependencies_manager


class DependencyOverrider:
    def __init__(self, overrides: OverridesMapping, _dependencies_manager: DependenciesManager = dependencies_manager) -> None:
        self.overrides = overrides
        self._dependencies_manager = _dependencies_manager
        self._old_overrides: OverridesMapping = {}

    def __enter__(self):
        self._old_overrides = self._dependencies_manager.override_dependencies(self.overrides)
        return self

    def __exit__(self, *args: typing.Any) -> None:
        self._dependencies_manager.restore_dependencies(self.overrides, self._old_overrides)
