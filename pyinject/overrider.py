import typing

from .manager import DependenciesManager, OverridesMapping, default_manager
from .decorators import AutoWired, R, P


class DependencyOverrider:
    def __init__(self, overrides: OverridesMapping, *, manager: DependenciesManager = default_manager) -> None:
        self.overrides = overrides
        self.manager = manager
        self._old_overrides: OverridesMapping = {}

    def __enter__(self):
        self._old_overrides = self.manager.override_dependencies(self.overrides)
        return self

    def __exit__(self, *args: typing.Any) -> None:
        self.manager.restore_dependencies(self.overrides, self._old_overrides)

    def execute(self, func: typing.Callable[P, R], *args, **kwargs) -> R:
        return AutoWired(manager=self.manager)(func)(*args, **kwargs)
