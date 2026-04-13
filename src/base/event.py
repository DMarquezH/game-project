from typing import Callable


class SimpleEvent:

    def __init__(self):
        self._listeners: set[Callable[[], None]] = set()

    def add_listener(self, callback: Callable[[], None]):
        self._listeners.add(callback)

    def remove_listener(self, callback: Callable[[], None]):
        self._listeners.discard(callback)

    def trigger(self):
        self._notify_listeners()

    def _notify_listeners(self):
        for listener in self._listeners:
            listener()