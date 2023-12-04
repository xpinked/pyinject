import inspect
from dataclasses import dataclass, field
from functools import wraps
from typing import Annotated, Any, Callable, get_args, get_origin


class SingletonMetaClass(type):
    _instances = {}
    __allow_reinitialization__: bool = False

    def __call__(cls, *args, **kwargs) -> Any:
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance

        else:
            instance = cls._instances[cls]
            if hasattr(cls, "__allow_reinitialization") and cls.__allow_reinitialization__:
                instance.__init__(*args, **kwargs)

        return instance


@dataclass(slots=True)
class _Dependency:
    """A dependency object, holds a callable that returns a dependency and a cache flag"""

    callable: Callable[..., Any] | None = None
    cache: bool = True

    @classmethod
    def validate(cls, /, _value: Any) -> None:
        """
        Validates that the given value is a _Dependency object

        Args:
            _value (Any): A value to validate

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


resolver = DependencyResolver()


def Depends(callable: Callable[..., Any] | None = None, cache: bool = True) -> _Dependency:
    """
    Given a callable, returns a Dependency object that can be used to annotate

    Args:
        callable (Callable[..., Any]): A callable that returns a dependency
        cache (bool, optional): Whether or not to cache the dependency. Defaults to True.

    Returns:
        _Dependency: A dependency object that can be used to annotate
    """
    return _Dependency(callable, cache)


def AutoWired(func):
    """
    A decorator that resolves dependencies from a callable and injects them to arguments Annotations
    Args:
        func (_type_): function to decorate

    Returns:
        _type_: decorated function with resolved dependencies
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        bound_args = sig.bind_partial(*args, **kwargs)
        bound_args.apply_defaults()

        for param_name, param in sig.parameters.items():
            if param_name in bound_args.arguments:
                continue

            if get_origin(param.annotation) is Annotated:
                _type, _dependency = get_args(param.annotation)
                _Dependency.validate(_dependency)

                if _dependency.callable is None:
                    _dependency.callable = _type

                kwargs[param_name] = resolver.get_dependency_value(_dependency)

        return func(*args, **kwargs)

    return wrapper


def run_program(starting_point: Callable[..., Any], *args, **kwargs) -> Any:
    return starting_point(*args, **kwargs)
