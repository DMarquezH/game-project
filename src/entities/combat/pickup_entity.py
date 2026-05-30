import random

import arcade
from pyglet.math import Vec2
from settings.game_resources import GameResources
from entities.player_entity import Player

class BasePickupEntity(arcade.Sprite):
    def __init__(self, texture, position: tuple[float, float], initial_velocity: Vec2):
        super().__init__(texture)
        self.position = position
        self.velocity_vec = initial_velocity
        self.friction = 0.9  # Desaceleración
        self.magnet_range = 100.0
        self.magnet_speed = 8.0

    def on_update(self, delta_time: float, player: Player = None, obstacles: arcade.SpriteList = None):
        dt_scale = delta_time * 60
        
        if obstacles:
            self.center_x += self.velocity_vec.x * dt_scale
            if arcade.check_for_collision_with_list(self, obstacles):
                self.center_x -= self.velocity_vec.x * dt_scale
                self.velocity_vec = Vec2(self.velocity_vec.x * -0.8, self.velocity_vec.y)
            self.center_y += self.velocity_vec.y * dt_scale
            if arcade.check_for_collision_with_list(self, obstacles):
                self.center_y -= self.velocity_vec.y * dt_scale
                self.velocity_vec = Vec2(self.velocity_vec.x, self.velocity_vec.y * -0.8)
        else:
            self.center_x += self.velocity_vec.x * dt_scale
            self.center_y += self.velocity_vec.y * dt_scale
        
        self.velocity_vec *= (self.friction ** dt_scale)
        
        # Magnetismo hacia el jugador si está cerca
        if player:
            dist = Vec2(player.center_x - self.center_x, player.center_y - self.center_y)
            if dist.length() < self.magnet_range:
                magnet_dir = dist.normalize()
                self.velocity_vec += magnet_dir * self.magnet_speed * dt_scale
                self.friction = 0.98

    def apply_effect(self, player: Player, event_bus):
        pass

class CoinPickupEntity(BasePickupEntity):
    def __init__(self, position: tuple[float, float], initial_velocity: Vec2):
        texture = arcade.load_texture(GameResources.get("textures") / "ui" / "hud" / "coin_32.png")
        super().__init__(texture, position, initial_velocity)
        self.scale = 0.5

    def apply_effect(self, player: Player, event_bus):
        from settings.registered_gameplay_events import CoinCollectedEvent
        event_bus.dispatch(CoinCollectedEvent(int(random.randint(10, 25))))

class HeartPickupEntity(BasePickupEntity):
    def __init__(self, position: tuple[float, float], initial_velocity: Vec2):
        texture = arcade.load_texture(GameResources.get("textures") / "ui" / "hud" / "heart_32.png")
        super().__init__(texture, position, initial_velocity)
        self.scale = 0.5

    def apply_effect(self, player: Player, event_bus):
        from world.systems.combat.entity_stats import StatDefinition
        max_health = player.stats.get(StatDefinition.MAX_HEALTH) or 100.0
        
        import random
        heal_amount = max_health * random.uniform(0.05, 0.15)
        player.stats.increase(StatDefinition.HEALTH, heal_amount)
        
        current = player.stats.get(StatDefinition.HEALTH)
        if current > max_health:
            player.stats.set(StatDefinition.HEALTH, max_health)
