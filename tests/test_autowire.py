from typing import Annotated

from pyinject import AutoWired, Depends


def test_autowired__functions() -> None:
    def foo():
        return 1

    def bar():
        return 2

    @AutoWired
    def func(foor: Annotated[int, Depends(foo)], bar: Annotated[int, Depends(bar)]):
        return foor + bar

    assert func() == 3  # type: ignore
