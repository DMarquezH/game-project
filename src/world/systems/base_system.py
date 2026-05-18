from abc import ABC, abstractmethod

from services.event_service import EventBus


class BaseSystem(ABC):

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self._initialized = False

    def init(self, **kwargs):
        self._initialized = True

    def update(self):
        pass
    
    def on_update(self, delta_time: float):
        pass

    @abstractmethod
    def dispose(self):
        pass