import arcade
from pyglet.math import Vec2

from services.event_service import EventBus
from world.systems.combat.entity_stats import EntityStats


class BaseEntity(arcade.Sprite):

    def __init__(self, event_bus: EventBus):
        super().__init__()

        self.event_bus = event_bus

        self.stats = EntityStats()
        
        self.invulnerable_timer = 0.0
        from entities.combat.hurtbox import Hurtbox
        self.hurtbox = Hurtbox(self)
        
    def update_invulnerability(self, delta_time: float):
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= delta_time

    def kill(self):
        if hasattr(self, "hurtbox") and self.hurtbox:
            self.hurtbox.kill()
        super().kill()

    def dispose(self):
        pass