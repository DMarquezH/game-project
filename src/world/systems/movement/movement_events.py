from pyglet.math import Vec2

from src.entities.base_entity import BaseEntity
from src.services.event_service import BaseEvent


class EntityMoveEvent(BaseEvent):

    def __init__(self, entity: BaseEntity, move_dir: Vec2):
        super().__init__()

        self.entity = entity
        self.move_dir = move_dir