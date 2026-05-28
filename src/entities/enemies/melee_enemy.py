import arcade
import random

from pyglet.math import Vec2
from services.event_service import EventBus
from entities.player_entity import Player
from entities.enemies.base_enemy import BaseEnemy
from settings.game_resources import GameResources
from world.systems.combat.entity_stats import StatDefinition
from settings.registered_gameplay_events import EntityAttackedMeleeEvent


class MeleeEnemy(BaseEnemy):

    ATTACK_DISTANCE = 50.0 

    def __init__(self, event_bus: EventBus, player: Player, barrier_list=None):
        super().__init__(event_bus, player, barrier_list)
        self._attack_timer = 0.0

    def _setup_stats(self) -> None:
        # Randomizamos levemente las estadisticas base
        health = random.uniform(40.0, 60.0)
        damage = random.uniform(8.0, 15.0)
        speed = random.uniform(1.8, 2.3)
        
        self.stats.set(StatDefinition.MOVEMENT_SPEED, speed)
        self.stats.set(StatDefinition.MAX_HEALTH, health)
        self.stats.set(StatDefinition.HEALTH, health)
        self.stats.set(StatDefinition.ATTACK_DAMAGE, damage)
        self.stats.set(StatDefinition.ATTACK_SPEED, 1.0) # 1 ataque por segundo
        self.stats.set(StatDefinition.ATTACK_KNOCKBACK, 64.0)

    def _setup_texture(self) -> None:
        self.texture = arcade.load_texture(GameResources.get("textures") / "entity" / "enemy_32.png")

    def update_behavior(self, delta_time: float) -> None:
        if self._get_distance_to_player() <= self.ATTACK_DISTANCE:
            self._stop()
            self._try_attack(delta_time)
        else:
            self._follow_path()

    def _try_attack(self, delta_time: float) -> None:
        self._attack_timer += delta_time
        attack_speed = self.stats.get(StatDefinition.ATTACK_SPEED)

        if self._attack_timer >= 1.0 / attack_speed:
            self._attack_timer = 0.0
            self._attack()

    def _attack(self) -> None:
        p_pos = Vec2(self._player.position[0], self._player.position[1])
        m_pos = Vec2(self.position[0], self.position[1])
        direction = (p_pos - m_pos).normalize()
        damage = self.stats.get(StatDefinition.ATTACK_DAMAGE)
        knockback = self.stats.get(StatDefinition.ATTACK_KNOCKBACK)
        
        self.event_bus.dispatch(EntityAttackedMeleeEvent(
            attacker=self,
            attacker_pos=self.position,
            attack_dir=direction,
            attack_range=self.ATTACK_DISTANCE,
            amplitude=90.0,
            damage=damage,
            knockback=knockback
        ))