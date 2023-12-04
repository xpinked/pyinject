from typing import Any


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
