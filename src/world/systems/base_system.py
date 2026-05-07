from src.services.event_service import EventBus


class BaseSystem:

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self._initialized = False

    def init(self):
        self._initialized = True