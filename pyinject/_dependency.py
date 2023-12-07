from dataclasses import dataclass
from typing import Any, Callable


@dataclass(slots=True)
class _Dependency:
    """A dependency object, holds a callable that returns a dependency and a cache flag"""

    callable: Callable[..., Any] | None = None
    cache: bool = True

    @classmethod
    def validate(cls, /, _value: object) -> None:
        """
        Validates that the given value is a _Dependency object

        Args:
            _value (object): A value to validate

        Raises:
            ValueError: If the given value is not a _Dependency object
        """
        if not isinstance(_value, _Dependency):
            raise ValueError(
                "Dependency must be a _Dependency object,\n"
                "please use the Depends() function to define a dependency.\n"
                "Examples:\n"
                "1. Annotated[MyDependency, Depends()] \n"
                "2. Annotated[MyDependency, Depends(get_my_dependency)]"
            )
