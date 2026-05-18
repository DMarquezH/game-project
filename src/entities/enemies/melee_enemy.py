import arcade

from services.event_service import EventBus
from entities.player_entity import Player
from entities.enemies.base_enemy import BaseEnemy
from settings.game_resources import GameResources
from world.systems.combat.entity_stats import StatDefinition


class MeleeEnemy(BaseEnemy):

    ATTACK_DISTANCE = 40.0

    def __init__(self, event_bus: EventBus, player: Player, barrier_list=None):
        super().__init__(event_bus, player, barrier_list)
        self._attack_timer = 0.0

    def _setup_stats(self) -> None:
        self.stats.set(StatDefinition.MOVEMENT_SPEED, 2.0)
        self.stats.set(StatDefinition.MAX_HEALTH, 50.0)
        self.stats.set(StatDefinition.HEALTH, 50.0)
        self.stats.set(StatDefinition.ATTACK_DAMAGE, 10.0)
        self.stats.set(StatDefinition.ATTACK_SPEED, 0.5)
        self.stats.set(StatDefinition.ATTACK_KNOCKBACK, 5.0)

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
        pass