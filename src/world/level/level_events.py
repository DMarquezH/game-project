from services.event_service import BaseEvent
from world.level.base_level import BaseLevel


class LevelChangeRequestEvent(BaseEvent):
    def __init__(self, next_level: BaseLevel):
        super().__init__()
        self.next_level = next_level


class LevelChangedEvent(BaseEvent):
    def __init__(self, level: BaseLevel):
        super().__init__()
        self.level = level
