from typing import Generic, TypeVar, Callable

T = TypeVar("T")


class RegistryException(Exception):
    pass


class Registry(Generic[T]):

    def __init__(self, name: str):
        self.name = name
        self._entries: dict[str, T] = dict()
        self._frozen = False

    def register(self, key: str, obj: T) -> T:

        if self._frozen:
            raise RegistryException("Registry is frozen!")

        if self.contains(key):
            raise RegistryException(f"Key ({key}) is already registered!")

        self._entries[key] = obj
        return obj

    def get(self, key: str) -> T | None:
        return self._entries.get(key)

    def get_all(self) -> dict[str, T]:
        return self._entries.copy()

    def contains(self, key: str):
        return key in self._entries

    def freeze(self):
        self._frozen = True

    def is_frozen(self) -> bool:
        return self._frozen


class RegistryObject(Generic[T]):

    def __init__(self, key: str, supplier: Callable[[], T]):
        self.key = key
        self._supplier = supplier
        self._instance = None

    def instance(self):

        if self._instance is None:
            self._instance = self._supplier()

        return self._instance


class DeferredRegistry(Generic[T]):

    def __init__(self, registry: Registry[T]):
        self._registry = registry
        self._entries: dict[str, RegistryObject[T]] = dict()

    def register(self, key: str, supplier: Callable[[], T]) -> RegistryObject[T]:

        if key in self._entries:
            raise RegistryException(f"Key ({key}) is already registered!")

        reg_obj = RegistryObject(key, supplier)

        self._entries[key] = reg_obj
        return reg_obj

    def build(self):
        for reg_obj in self._entries.values():
            self._registry.register(reg_obj.key, reg_obj.instance())