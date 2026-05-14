import arcade

from services.event_service import EventBus
from world.systems.combat.entity_stats import EntityStats


class BaseEntity(arcade.Sprite):

    def __init__(self, event_bus: EventBus):
        super().__init__()

        self.event_bus = event_bus

        self.stats = EntityStats()

    def dispose(self):
        pass