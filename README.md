## PyInject

PyInject is a Python library for dependency injection.

It is inspired by the FastAPI dependency framework.

## Usage

```python
from pyinject import AutoWired, Depends

class ServiceA:
    name = "ServiceA"

    def hello(self):
        return f"Hello from {self.name}"

class ServiceB:
    name = "ServiceB"

    def hello(self):
        return f"Hello from {self.name}"

@AutoWired
def main(service_a: Annotated[ServiceA, Depends()], service_b: Annotated[ServiceB, Depends()]):
    print(service_a.hello())
    print(service_b.hello())

```

## Installation

You can install all of these with `pip install git+https://github.com/xpinked/pyinject.git`.

## License

This project is licensed under the terms of the GPL-3.0 license license.
