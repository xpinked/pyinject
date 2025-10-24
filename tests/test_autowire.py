from typing import Annotated

from pyinject import inject, Depends


def foo():
    return 1


def bar():
    return 2


@inject()
def func(foo: Annotated[int, Depends(foo)], bar: Annotated[int, Depends(bar)]):
    return foo + bar


def test_autowired__functions() -> None:
    assert func() == 3  # type: ignore
