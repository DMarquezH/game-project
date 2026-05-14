from enum import Enum, auto
from typing import Dict

import arcade

from entities.base_entity import BaseEntity
from services.event_service import EventBus
from world.systems.base_system import BaseSystem
from world.systems.combat.entity_stats import StatDefinition
from world.systems.movement.movement_events import EntityMoveEvent


class MovementMode(Enum):
    FLOOR = auto()
    AIR = auto()


class MovementSystem(BaseSystem):

    DEFAULT_FLOOR_FRICTION = 0.8
    DEFAULT_AIR_FRICTION = 0.2

    def __init__(self, event_bus: EventBus):
        super().__init__(event_bus)

        self.floor_friction = self.DEFAULT_FLOOR_FRICTION
        self.air_friction = self.DEFAULT_AIR_FRICTION

        self.entities: Dict[BaseEntity, MovementMode] = {}

    def init(self):

        if self._initialized: return

        self.event_bus.subscribe(EntityMoveEvent, self._move_entity)

        self._initialized = True

    def add_entity(self, entity: BaseEntity, move_mode: MovementMode):
        if not self._validate_entity(entity): return
        self.entities[entity] = move_mode

    def remove_entity(self, entity: BaseEntity):
        self.entities.pop(entity, None)

    def update(self):

        for entity, move_mode in self.entities.items():

            if entity.change_x != 0 or entity.change_y != 0:
                self._apply_friction(entity, move_mode)

    def _move_entity(self, event: EntityMoveEvent):

        entity = event.entity

        move_dir = event.move_dir
        movement = entity.stats.get(StatDefinition.MOVEMENT_SPEED)

        entity.change_x = round(movement * move_dir.x, 2)
        entity.change_y = round(movement * move_dir.y, 2)

    def _apply_friction(self, entity: arcade.Sprite, move_mode: MovementMode):

        x, y = entity.change_x, entity.change_y

        if move_mode == MovementMode.FLOOR:
            entity.change_x = round(x * self.floor_friction, 2)
            entity.change_y = round(y * self.floor_friction, 2)

        elif move_mode == MovementMode.AIR:
            entity.change_x = round(x * self.air_friction, 2)
            entity.change_y = round(y * self.air_friction, 2)

    def _validate_entity(self, entity: BaseEntity) -> bool:
        return entity.stats.get(StatDefinition.MOVEMENT_SPEED) is not None

    def dispose(self):
        self.event_bus.unsubscribe(EntityMoveEvent, self._move_entity)