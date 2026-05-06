from dataclasses import dataclass
from typing import Type, Callable, Dict, TypeVar, List, ParamSpec, Generic, Set

from core.service_container import Service

T = TypeVar("T", bound="BaseEvent")
P = ParamSpec("P")


class BaseEvent:

    def __init__(self):
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    def is_cancelled(self) -> bool:
        return self._cancelled


@dataclass
class EventListener:
    priority: int
    callback: Callable[[BaseEvent], None]


class EventBus(Service):

    def __init__(self):
        super().__init__("event-bus")
        self._listeners: Dict[Type[BaseEvent], List[EventListener]] = {}

    def subscribe(self, event_type: Type[T], callback: Callable[[T], None], priority: int = 0):

        listeners = self._listeners.setdefault(event_type, [])

        listeners.append(EventListener(priority, callback))
        listeners.sort(key=lambda lst: lst.priority, reverse=True)

    def unsubscribe(self, event_type: Type[T], callback: Callable[[T], None]):

        if event_type not in self._listeners: return

        self._listeners[event_type] = [
            lst for lst in self._listeners[event_type]
            if lst.callback != callback
        ]

    def dispatch(self, event: T):

        listeners = self._listeners.get(type(event), []).copy()

        for listener in listeners:
            listener.callback(event)


class Signal(Generic[P]):
    """
    Representa un evento local que envia argumentos definidos en P a los recibidores, cuando este es activado.
    """

    def __init__(self):
        self._receivers: Set[Callable[P, None]] = set()

    def connect(self, callback: Callable[P, None]):
        """
        Registra una función recibidora en el evento.
        :param callback: Función que recibe argumentos P y devuelve None.
        """
        self._receivers.add(callback)

    def disconnect(self, callback: Callable[P, None]):
        """
        Elimina una función recibidora registrada en el evento. AVISO: Si la función que se registró fue definida
        como lambda, no podrá ser eliminada.

        :param callback: Función que recibe argumentos P y devuelve None, ya registrada en el evento.
        """
        self._receivers.discard(callback)

    def emit(self, *args: P.args):
        """
        Envía argumentos P a todas las funciones recibidoras registradas.
        """
        for listener in self._receivers.copy():
            listener(*args)