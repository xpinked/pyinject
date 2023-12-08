from typing import Annotated

import pytest

from pyinject import AutoWired, Depends, create_manager
from pyinject import execute as _
from pyinject.manager import DependenciesManager
from pyinject.overrider import DependencyOverrider


def foo():
    return 1


def bar():
    return 2


def foo_override():
    return 2


@pytest.fixture
def manager() -> DependenciesManager:
    return create_manager()


@AutoWired()
def func(foo: Annotated[int, Depends(foo)], bar: Annotated[int, Depends(bar)]) -> int:
    return foo + bar


test_manager = create_manager()


@AutoWired(manager=test_manager)
def func2(foo: Annotated[int, Depends(foo)], bar: Annotated[int, Depends(bar)]) -> int:
    return foo + bar


def test_autowired__default_manager() -> None:
    """Executing AutoWired function with default manager"""
    assert _(func) == 3


def test_autowired__non_default_manager() -> None:
    """Executing AutoWired function with non default manager"""
    assert _(func2) == 3


def test_autowired__default_manager_override() -> None:
    """Overriding default manager"""
    with DependencyOverrider({foo: foo_override}):
        assert _(func) == 4


def test_autowired__non_default_manager_override() -> None:
    """Overriding dependencies of test_manager and executing function who depends on it"""
    with DependencyOverrider({foo: foo_override}, manager=test_manager):
        assert _(func2) == 4


def test_autowired__overriding_manager(manager: DependenciesManager) -> None:
    """Executing function in isolation with overridden manager"""
    with DependencyOverrider({}, manager=manager) as overrider:
        assert overrider.execute(func2) == 3


def test_autowired__overriding_manager_overriding_dependency(manager: DependenciesManager) -> None:
    """Executing function in isolation with overridden manager"""
    with DependencyOverrider({foo: foo_override}, manager=manager) as overrider:
        assert overrider.execute(func2) == 4
