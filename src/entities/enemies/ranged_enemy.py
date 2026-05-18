import arcade

from services.event_service import EventBus
from entities.player_entity import Player
from entities.enemies.base_enemy import BaseEnemy
from settings.game_resources import GameResources
from world.systems.combat.entity_stats import StatDefinition


class RangedEnemy(BaseEnemy):

    def __init__(self, event_bus: EventBus, player: Player, barrier_list=None):
        super().__init__(event_bus, player, barrier_list)
        self._shoot_timer = 0.0


    def _setup_stats(self) -> None:
        self.stats.set(StatDefinition.MOVEMENT_SPEED, 1.5)
        self.stats.set(StatDefinition.MAX_HEALTH,     30.0)
        self.stats.set(StatDefinition.HEALTH,         30.0)
        self.stats.set(StatDefinition.ATTACK_DAMAGE,  8.0)
        self.stats.set(StatDefinition.ATTACK_SPEED,   0.2)
        self.stats.set(StatDefinition.ATTACK_RANGE,   200.0)
        self.stats.set(StatDefinition.SHOT_SPEED,     5.0)
        self.stats.set(StatDefinition.SHOT_SPREAD,    0.0)
        
    def _setup_texture(self) -> None:
        self.texture = arcade.load_texture(GameResources.get("textures") / "entity" / "enemy_32.png")
        
    def update_behavior(self, delta_time: float) -> None:
        attack_range = self.stats.get(StatDefinition.ATTACK_RANGE)

        if self._get_distance_to_player() > attack_range:
            self._follow_path()
        else:
            self._stop()
            self._try_shoot(delta_time)

    def _try_shoot(self, delta_time: float) -> None:
        self._shoot_timer += delta_time
        attack_speed = self.stats.get(StatDefinition.ATTACK_SPEED)

        if self._shoot_timer >= 1.0 / attack_speed:
            self._shoot_timer = 0.0
            self._shoot()

    def _shoot(self) -> None:
        direction = self._get_direction_to_player()
        pass