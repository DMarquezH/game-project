from dataclasses import dataclass
from typing import Type, Callable, Dict, TypeVar, List, Tuple

T = TypeVar("T", bound="Event")


class Event:

    def __init__(self):
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    def is_cancelled(self) -> bool:
        return self._cancelled


@dataclass
class EventListener:
    priority: int
    callback: Callable[[Event], None]


class EventBus:

    def __init__(self):
        self._listeners: Dict[Type[Event], List[EventListener]] = {}

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