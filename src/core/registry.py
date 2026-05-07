from typing import Generic, TypeVar, Callable, Dict, Type, Any

T = TypeVar("T")


class RegistryException(Exception):
    """
    Excepción lanzada por errores relacionados con acciones de registro.
    """
    pass


class Freezable:

    def __init__(self):
        self._frozen = False

    def is_frozen(self) -> bool:
        return self._frozen

    def freeze(self):
        self._frozen = True


class TypeRegistry(Generic[T], Freezable):

    def __init__(self):
        super().__init__()
        self._entries: Dict[Type[T], T] = {}

    def register(self, instance: T):
        self._entries[type(instance)] = instance

    def get(self, obj_type: Type[T]) -> T:
        return self._entries.get(obj_type)

    def get_all(self) -> Dict[Type, T]:
        return self._entries.copy()

    def contains(self, obj_type: Type[T]) -> bool:
        return obj_type in self._entries


class Registry(Generic[T], Freezable):
    """
    Representa una colección de objetos genéricos T, identificados por una clave.
    """

    def __init__(self):
        super().__init__()
        self._entries: dict[str, T] = dict()

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
    """
    Representa un registro diferido de objetos genéricos T.

    Su función principal es preparar un registro (Registry[T]), posponiendo el registro de los objetos al
    momento de la ejecucion de DeferredRegistry.build(). De esta manera, es posible organizar los registros
    de objetos de uso global de forma ordenada, estableciendo prioridades, si procede.

    Utiliza carga perezosa mediante suppliers para la preparación de los registros de los objetos.
    """

    def __init__(self, registry: Registry[T]):
        self._registry = registry
        self._entries: dict[str, RegistryObject[T]] = dict()

    def register(self, key: str, supplier: Callable[[], T]) -> RegistryObject[T]:
        """
        Deja en preparación el registro de un objeto.

        :param key: clave identificativa del objeto.
        :param supplier: Supplier del objeto a registrar.
        """

        if key in self._entries:
            raise RegistryException(f"Key ({key}) is already registered!")

        reg_obj = RegistryObject(key, supplier)

        self._entries[key] = reg_obj
        return reg_obj

    def build(self):
        """
        Ejecuta el registro en el Registry[T] de todos los objetos definidos.
        """

        for reg_obj in self._entries.values():
            self._registry.register(reg_obj.key, reg_obj.instance())