from typing import Annotated

from pyinject import AutoWired, Depends
from pyinject.overrider import DependencyOverrider


def foo():
    return 1


def bar():
    return 2


def foo_override():
    return 2


@AutoWired
def func(foo: Annotated[int, Depends(foo)], bar: Annotated[int, Depends(bar)]):
    return foo + bar


def test_autowired__functions() -> None:
    with DependencyOverrider({foo: foo_override}):
        assert func() == 4  # type: ignore
