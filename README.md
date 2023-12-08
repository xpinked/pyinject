## PyInject

PyInject is a Python library for dependency injection.

It is inspired by the FastAPI dependency framework.

## Installation

Requires Python 3.10 or higher.

You can install with `pip install git+https://github.com/xpinked/pyinject.git`.

## Basic Usage

### Lets define some services

In this example we will define two services, `ServiceA` and `ServiceB`.

will be in a module called `services.py`.

```python
class ServiceA:
    name = "ServiceA"

    def hello(self):
        return f"Hello from {self.name}"

class ServiceB:
    name = "ServiceB"

    def hello(self):
        return f"Hello from {self.name}"

class ServiceC:
    name = "ServiceC"

    def hello(self):
        return f"Hello from {self.name}"

def get_service_c():
    return ServiceC()
```

---

### Lets use these services

Lets say we want to use these services in a function.

```python
from typing import Annotated
from pyinject import AutoWired, Depends, execute

from .services import ServiceA, ServiceB

@AutoWired()
def func(service_a: Annotated[ServiceA, Depends()], service_b: Annotated[ServiceB, Depends()]):
    print(service_a.hello())
    print(service_b.hello())

if __name__ == "__main__":
    execute(func)
```

We have to use the `AutoWired` decorator to tell the dependency injector that this function should be executed with all its dependencies injected.

and we have to use the `Annotated` type hint to tell the dependency injector what type of dependency we want to inject.

The `Depends` class is used to tell the dependency injector that we want to inject a dependency,

and we used the `execute` function to execute the function with all its dependencies injected.

This will print:

```
Hello from ServiceA
Hello from ServiceB
```

if we do not provide a type hint for the dependency, the dependency injector will try to infer the type from the type hint of the variable.

Otherwise, we can provide a provider function to the `Depends` class, which will be used to provide the dependency.

```python
from typing import Annotated
from pyinject import AutoWired, Depends, execute

from .services import ServiceC, get_service_c

@AutoWired()
def func_2(service_c: Annotated[ServiceC, Depends(get_service_c)]):
    print(service_c.hello())

if __name__ == "__main__":
    execute(func2)
```

This will print:

```
Hello from ServiceC
```

## More Advanced Usage

You can checkout more code examples in [Examples](https://github.com/xpinked/pyinject/tree/main/examples)

## License

This project is licensed under the terms of the MIT license.
