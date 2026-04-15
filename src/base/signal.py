from typing import TypeVar, Generic, Callable

T = TypeVar("T")


class Signal(Generic[T]):

    def __init__(self):
        self._listeners: set[Callable[[T], None]] = set()

    def connect(self, callback: Callable[[T], None]):
        self._listeners.add(callback)

    def disconnect(self, callback: Callable[[T], None]):
        self._listeners.discard(callback)

    def emit(self, obj: T):
        for listener in self._listeners:
            listener(obj)


class SimpleSignal:

    def __init__(self):
        self._listeners: set[Callable[[], None]] = set()

    def connect(self, callback: Callable[[], None]):
        self._listeners.add(callback)

    def disconnect(self, callback: Callable[[], None]):
        self._listeners.discard(callback)

    def emit(self):
        for listener in self._listeners:
            listener()