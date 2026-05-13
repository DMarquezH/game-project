from enum import Enum, auto

from arcade import Texture

from src.entities.base_entity import BaseEntity
from src.services.event_service import EventBus


class EnemyEntity(BaseEntity):

    def __init__(self, event_bus: EventBus, texture: Texture, scale: float):
        super().__init__(event_bus)

        self.texture = texture
        self.scale = scale